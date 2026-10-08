import re
import json
import random
import unicodedata
from typing import Any, Dict, List, Tuple
from app.models.exercise import Exercise

def normalize_text(text: Any) -> str:
    """
    Unicode-safe text normalization:
    - Trims surrounding whitespace
    - Lowercases text
    - Normalizes unicode NFKD to strip combining diacritics
    - Strips punctuation: ¿, ¡, ., ,, !, ?, :, ;, ", ', -, (, )
    - Collapses repeated whitespace into a single space
    """
    if text is None:
        return ""
    text_str = str(text).strip().lower()
    # Remove Spanish and English punctuation marks
    text_str = re.sub(r'[¿¡.,!?:;"\'\-\(\)\[\]]', '', text_str)
    # Strip combining diacritical marks (e.g. accents)
    text_str = "".join(
        c for c in unicodedata.normalize("NFD", text_str)
        if unicodedata.category(c) != "Mn"
    )
    # Collapse multiple whitespace characters
    text_str = re.sub(r'\s+', ' ', text_str)
    return text_str.strip()

def build_safe_exercise_payload(exercise: Exercise) -> Dict[str, Any]:
    """
    Parses payload_json and thoroughly scrubs any canonical answers,
    accepted answer arrays, or grading keys before returning to the browser.
    """
    raw_payload = json.loads(exercise.payload_json)

    # Remove any potential answer leakage fields
    scrubbed = {
        k: v for k, v in raw_payload.items()
        if k not in ("canonical_answer", "accepted_answers", "answer_key", "is_correct")
    }

    # For match_pairs: decouple left and right items into shuffled lists
    # so the client cannot match pairs simply by inspecting array indexes or IDs.
    if exercise.exercise_type == "match_pairs" and "pairs" in raw_payload:
        pairs = raw_payload["pairs"]
        left_items = [{"id": f"L_{idx}", "text": p["left"]} for idx, p in enumerate(pairs)]
        right_items = [{"id": f"R_{idx}", "text": p["right"]} for idx, p in enumerate(pairs)]
        
        # Deterministic or randomized shuffle
        rng = random.Random(exercise.id * 31)
        rng.shuffle(left_items)
        rng.shuffle(right_items)
        
        scrubbed = {
            "left_items": left_items,
            "right_items": right_items
        }

    return scrubbed

def grade_exercise_submission(exercise: Exercise, answer_payload: Any) -> Tuple[bool, str]:
    """
    Authoritatively grades a learner's submission against the exercise's DB canonical answer.
    Returns: (is_correct: bool, canonical_display_solution: str)
    """
    ex_type = exercise.exercise_type
    raw_payload = json.loads(exercise.payload_json)
    canonical = exercise.canonical_answer

    # 1. Multiple Choice
    if ex_type == "multiple_choice":
        options = raw_payload.get("options", [])
        # Answer could be option text or option ID
        user_text = ""
        if isinstance(answer_payload, str):
            # Check if answer matches option ID
            matched_opt = next((o for o in options if o.get("id") == answer_payload), None)
            user_text = matched_opt["text"] if matched_opt else answer_payload
        elif isinstance(answer_payload, dict):
            user_text = answer_payload.get("text", answer_payload.get("id", ""))
        
        is_correct = (normalize_text(user_text) == normalize_text(canonical))
        return is_correct, canonical

    # 2. Word Bank
    elif ex_type == "word_bank":
        # Answer could be list of tokens ["Buenos", "días", "amigo"],
        # list of dicts [{"text": "Buenos"}], or joined string
        assembled = ""
        if isinstance(answer_payload, list):
            words = []
            for item in answer_payload:
                if isinstance(item, dict):
                    words.append(item.get("text", ""))
                else:
                    words.append(str(item))
            assembled = " ".join(words)
        elif isinstance(answer_payload, str):
            assembled = answer_payload

        is_correct = (normalize_text(assembled) == normalize_text(canonical))
        return is_correct, canonical

    # 3. Match Pairs
    elif ex_type == "match_pairs":
        canonical_pairs = raw_payload.get("pairs", [])
        # Build canonical forward and reverse mappings
        req_mapping = {
            normalize_text(p["left"]): normalize_text(p["right"])
            for p in canonical_pairs
        }
        reverse_mapping = {
            normalize_text(p["right"]): normalize_text(p["left"])
            for p in canonical_pairs
        }

        submitted_pairs = []
        if isinstance(answer_payload, list):
            submitted_pairs = answer_payload
        elif isinstance(answer_payload, dict) and "matched_pairs" in answer_payload:
            submitted_pairs = answer_payload["matched_pairs"]

        # Rule 1: Submitted pair count must equal canonical pair count
        if len(submitted_pairs) != len(canonical_pairs):
            return False, "All pairs must be matched"

        seen_lefts = set()
        seen_rights = set()

        for pair in submitted_pairs:
            if not isinstance(pair, dict):
                return False, "Invalid pair format"
            left = normalize_text(pair.get("left", ""))
            right = normalize_text(pair.get("right", ""))

            # Validate exact mapping in either forward or reverse orientation
            if left in req_mapping and req_mapping[left] == right:
                canon_left, canon_right = left, right
            elif left in reverse_mapping and reverse_mapping[left] == right:
                canon_left, canon_right = right, left
            else:
                return False, "One or more pairs are incorrect"

            # Rule 2 & 3: Every submitted left and right item must be unique
            if canon_left in seen_lefts or canon_right in seen_rights:
                return False, "Duplicate items in submitted pairs"

            seen_lefts.add(canon_left)
            seen_rights.add(canon_right)

        # Rule 4 & 6: Exactly all canonical items must be matched
        if len(seen_lefts) != len(canonical_pairs):
            return False, "All unique pairs must be matched"

        return True, "All pairs matched"

    # 4. Fill in the Blank
    elif ex_type == "fill_blank":
        options = raw_payload.get("options", [])
        user_text = ""
        if isinstance(answer_payload, str):
            matched_opt = next((o for o in options if o.get("id") == answer_payload), None)
            user_text = matched_opt["text"] if matched_opt else answer_payload
        elif isinstance(answer_payload, dict):
            user_text = answer_payload.get("text", answer_payload.get("id", ""))

        is_correct = (normalize_text(user_text) == normalize_text(canonical))
        return is_correct, canonical

    # 5. Type the Answer
    elif ex_type == "type_answer":
        user_text = str(answer_payload) if answer_payload is not None else ""
        norm_user = normalize_text(user_text)
        
        # Check against primary canonical answer
        if norm_user == normalize_text(canonical):
            return True, canonical

        # Check against any secondary accepted answers
        accepted = raw_payload.get("accepted_answers", [])
        for alt in accepted:
            if norm_user == normalize_text(alt):
                return True, canonical

        return False, canonical

    # Fallback default
    return (normalize_text(answer_payload) == normalize_text(canonical)), canonical
