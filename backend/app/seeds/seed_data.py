import json

COURSE_DATA = {
    "code": "es-en",
    "title": "Spanish",
    "target_lang": "Spanish",
    "units": [
        {
            "order_index": 1,
            "title": "Unit 1: Rookie Basics",
            "description": "Greet people, introduce yourself, and order basic food and drinks.",
            "hex_color": "#58cc02",
            "skills": [
                {
                    "order_index": 1,
                    "title": "Greetings",
                    "icon_name": "message-circle",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Hello & Goodbye",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Hello'",
                                    "prompt_translation": "Greeting",
                                    "canonical_answer": "Hola",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_1_1", "text": "Hola"},
                                            {"id": "mc_1_2", "text": "Adiós"},
                                            {"id": "mc_1_3", "text": "Por favor"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate the sentence: 'Good morning, friend'",
                                    "prompt_translation": "Good morning, friend",
                                    "canonical_answer": "Buenos días amigo",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_1_1", "text": "Buenos"},
                                            {"id": "wb_1_2", "text": "días"},
                                            {"id": "wb_1_3", "text": "amigo"},
                                            {"id": "wb_1_4", "text": "noche"},
                                            {"id": "wb_1_5", "text": "leche"},
                                            {"id": "wb_1_6", "text": "agua"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_1_1", "left": "Hola", "right": "Hello"},
                                            {"id": "mp_1_2", "left": "Adiós", "right": "Goodbye"},
                                            {"id": "mp_1_3", "left": "Por favor", "right": "Please"},
                                            {"id": "mp_1_4", "left": "Gracias", "right": "Thank you"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "___ días, ¿cómo estás?",
                                    "prompt_translation": "Good morning, how are you?",
                                    "canonical_answer": "Buenos",
                                    "payload_json": json.dumps({
                                        "template": "___ días, ¿cómo estás?",
                                        "options": [
                                            {"id": "fb_1_1", "text": "Buenos"},
                                            {"id": "fb_1_2", "text": "Buenas"},
                                            {"id": "fb_1_3", "text": "Buen"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Hello, goodbye' in Spanish",
                                    "prompt_translation": "Hello, goodbye",
                                    "canonical_answer": "Hola, adiós",
                                    "payload_json": json.dumps({
                                        "accepted_answers": ["Hola, adiós", "Hola, adios", "hola adios", "hola, adios"]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Night & Day",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Good night'",
                                    "prompt_translation": "Good night",
                                    "canonical_answer": "Buenas noches",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_2_1", "text": "Buenas noches"},
                                            {"id": "mc_2_2", "text": "Buenos días"},
                                            {"id": "mc_2_3", "text": "Hasta luego"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'See you later, thanks'",
                                    "prompt_translation": "See you later, thanks",
                                    "canonical_answer": "Hasta luego gracias",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_2_1", "text": "Hasta"},
                                            {"id": "wb_2_2", "text": "luego"},
                                            {"id": "wb_2_3", "text": "gracias"},
                                            {"id": "wb_2_4", "text": "sí"},
                                            {"id": "wb_2_5", "text": "pan"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_2_1", "left": "Sí", "right": "Yes"},
                                            {"id": "mp_2_2", "left": "No", "right": "No"},
                                            {"id": "mp_2_3", "left": "Noche", "right": "Night"},
                                            {"id": "mp_2_4", "left": "Día", "right": "Day"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Muchas ___, amigo mío.",
                                    "prompt_translation": "Thank you very much, my friend.",
                                    "canonical_answer": "gracias",
                                    "payload_json": json.dumps({
                                        "template": "Muchas ___, amigo mío.",
                                        "options": [
                                            {"id": "fb_2_1", "text": "gracias"},
                                            {"id": "fb_2_2", "text": "de nada"},
                                            {"id": "fb_2_3", "text": "por favor"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Thank you very much' in Spanish",
                                    "prompt_translation": "Thank you very much",
                                    "canonical_answer": "Muchas gracias",
                                    "payload_json": json.dumps({
                                        "accepted_answers": ["Muchas gracias", "muchas gracias"]
                                    })
                                }
                            ]
                        }
                    ]
                },
                {
                    "order_index": 2,
                    "title": "Food & Drinks",
                    "icon_name": "coffee",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Water & Bread",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "What is 'water' in Spanish?",
                                    "prompt_translation": "water",
                                    "canonical_answer": "Agua",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_3_1", "text": "Agua"},
                                            {"id": "mc_3_2", "text": "Leche"},
                                            {"id": "mc_3_3", "text": "Pan"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The boy drinks water'",
                                    "prompt_translation": "The boy drinks water",
                                    "canonical_answer": "El niño bebe agua",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_3_1", "text": "El"},
                                            {"id": "wb_3_2", "text": "niño"},
                                            {"id": "wb_3_3", "text": "bebe"},
                                            {"id": "wb_3_4", "text": "agua"},
                                            {"id": "wb_3_5", "text": "come"},
                                            {"id": "wb_3_6", "text": "manzana"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_3_1", "left": "Agua", "right": "Water"},
                                            {"id": "mp_3_2", "left": "Pan", "right": "Bread"},
                                            {"id": "mp_3_3", "left": "Leche", "right": "Milk"},
                                            {"id": "mp_3_4", "left": "Manzana", "right": "Apple"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Yo ___ una manzana roja.",
                                    "prompt_translation": "I eat a red apple.",
                                    "canonical_answer": "como",
                                    "payload_json": json.dumps({
                                        "template": "Yo ___ una manzana roja.",
                                        "options": [
                                            {"id": "fb_3_1", "text": "como"},
                                            {"id": "fb_3_2", "text": "come"},
                                            {"id": "fb_3_3", "text": "comen"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'I drink milk' in Spanish",
                                    "prompt_translation": "I drink milk",
                                    "canonical_answer": "Yo bebo leche",
                                    "payload_json": json.dumps({
                                        "accepted_answers": ["Yo bebo leche", "Bebo leche", "yo bebo leche", "bebo leche"]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Daily Meals",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "What is 'bread' in Spanish?",
                                    "prompt_translation": "bread",
                                    "canonical_answer": "Pan",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_4_1", "text": "Pan"},
                                            {"id": "mc_4_2", "text": "Manzana"},
                                            {"id": "mc_4_3", "text": "Pescado"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The woman eats bread'",
                                    "prompt_translation": "The woman eats bread",
                                    "canonical_answer": "La mujer come pan",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_4_1", "text": "La"},
                                            {"id": "wb_4_2", "text": "mujer"},
                                            {"id": "wb_4_3", "text": "come"},
                                            {"id": "wb_4_4", "text": "pan"},
                                            {"id": "wb_4_5", "text": "bebe"},
                                            {"id": "wb_4_6", "text": "el"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_4_1", "left": "Comer", "right": "To eat"},
                                            {"id": "mp_4_2", "left": "Beber", "right": "To drink"},
                                            {"id": "mp_4_3", "left": "Mujer", "right": "Woman"},
                                            {"id": "mp_4_4", "left": "Hombre", "right": "Man"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Ella ___ agua fresca.",
                                    "prompt_translation": "She drinks fresh water.",
                                    "canonical_answer": "bebe",
                                    "payload_json": json.dumps({
                                        "template": "Ella ___ agua fresca.",
                                        "options": [
                                            {"id": "fb_4_1", "text": "bebe"},
                                            {"id": "fb_4_2", "text": "bebo"},
                                            {"id": "fb_4_3", "text": "beben"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'The boy eats an apple' in Spanish",
                                    "prompt_translation": "The boy eats an apple",
                                    "canonical_answer": "El niño come una manzana",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "El niño come una manzana",
                                            "El nino come una manzana",
                                            "el nino come una manzana"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "order_index": 2,
            "title": "Unit 2: Daily Life",
            "description": "Express common phrases, family relationships, and travel needs.",
            "hex_color": "#1cb0f6",
            "skills": [
                {
                    "order_index": 1,
                    "title": "Basic Phrases",
                    "icon_name": "compass",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Common Expressions",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "How do you say 'Excuse me' in Spanish?",
                                    "prompt_translation": "Excuse me",
                                    "canonical_answer": "Perdón",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_5_1", "text": "Perdón"},
                                            {"id": "mc_5_2", "text": "Hola"},
                                            {"id": "mc_5_3", "text": "Adiós"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I am sorry, my friend'",
                                    "prompt_translation": "I am sorry, my friend",
                                    "canonical_answer": "Lo siento mi amigo",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_5_1", "text": "Lo"},
                                            {"id": "wb_5_2", "text": "siento"},
                                            {"id": "wb_5_3", "text": "mi"},
                                            {"id": "wb_5_4", "text": "amigo"},
                                            {"id": "wb_5_5", "text": "gracias"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_5_1", "left": "Perdón", "right": "Excuse me"},
                                            {"id": "mp_5_2", "left": "Lo siento", "right": "I am sorry"},
                                            {"id": "mp_5_3", "left": "De nada", "right": "You are welcome"},
                                            {"id": "mp_5_4", "left": "Mucho gusto", "right": "Nice to meet you"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "___ gusto en conocerte.",
                                    "prompt_translation": "Nice to meet you.",
                                    "canonical_answer": "Mucho",
                                    "payload_json": json.dumps({
                                        "template": "___ gusto en conocerte.",
                                        "options": [
                                            {"id": "fb_5_1", "text": "Mucho"},
                                            {"id": "fb_5_2", "text": "Muy"},
                                            {"id": "fb_5_3", "text": "Bien"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'You are welcome' in Spanish",
                                    "prompt_translation": "You are welcome",
                                    "canonical_answer": "De nada",
                                    "payload_json": json.dumps({
                                        "accepted_answers": ["De nada", "de nada"]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Daily Greetings",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "How do you say 'See you tomorrow'?",
                                    "prompt_translation": "See you tomorrow",
                                    "canonical_answer": "Hasta mañana",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_6_1", "text": "Hasta mañana"},
                                            {"id": "mc_6_2", "text": "Hasta luego"},
                                            {"id": "mc_6_3", "text": "Buenos días"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'How are you today?'",
                                    "prompt_translation": "How are you today?",
                                    "canonical_answer": "Cómo estás hoy",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_6_1", "text": "Cómo"},
                                            {"id": "wb_6_2", "text": "estás"},
                                            {"id": "wb_6_3", "text": "hoy"},
                                            {"id": "wb_6_4", "text": "bien"},
                                            {"id": "wb_6_5", "text": "tú"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_6_1", "left": "Hoy", "right": "Today"},
                                            {"id": "mp_6_2", "left": "Mañana", "right": "Tomorrow"},
                                            {"id": "mp_6_3", "left": "Ayer", "right": "Yesterday"},
                                            {"id": "mp_6_4", "left": "Ahora", "right": "Now"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Estoy muy ___ hoy.",
                                    "prompt_translation": "I am very well today.",
                                    "canonical_answer": "bien",
                                    "payload_json": json.dumps({
                                        "template": "Estoy muy ___ hoy.",
                                        "options": [
                                            {"id": "fb_6_1", "text": "bien"},
                                            {"id": "fb_6_2", "text": "bueno"},
                                            {"id": "fb_6_3", "text": "mal"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'See you soon' in Spanish",
                                    "prompt_translation": "See you soon",
                                    "canonical_answer": "Hasta pronto",
                                    "payload_json": json.dumps({
                                        "accepted_answers": ["Hasta pronto", "hasta pronto"]
                                    })
                                }
                            ]
                        }
                    ]
                },
                {
                    "order_index": 2,
                    "title": "Travel",
                    "icon_name": "map-pin",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Airport & Taxi",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "What is 'airport' in Spanish?",
                                    "prompt_translation": "airport",
                                    "canonical_answer": "Aeropuerto",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_7_1", "text": "Aeropuerto"},
                                            {"id": "mc_7_2", "text": "Estación"},
                                            {"id": "mc_7_3", "text": "Hotel"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'A taxi to the hotel'",
                                    "prompt_translation": "A taxi to the hotel",
                                    "canonical_answer": "Un taxi al hotel",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_7_1", "text": "Un"},
                                            {"id": "wb_7_2", "text": "taxi"},
                                            {"id": "wb_7_3", "text": "al"},
                                            {"id": "wb_7_4", "text": "hotel"},
                                            {"id": "wb_7_5", "text": "en"},
                                            {"id": "wb_7_6", "text": "el"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_7_1", "left": "Taxi", "right": "Taxi"},
                                            {"id": "mp_7_2", "left": "Hotel", "right": "Hotel"},
                                            {"id": "mp_7_3", "left": "Boleto", "right": "Ticket"},
                                            {"id": "mp_7_4", "left": "Maleta", "right": "Suitcase"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "¿Dónde está mi ___?",
                                    "prompt_translation": "Where is my suitcase?",
                                    "canonical_answer": "maleta",
                                    "payload_json": json.dumps({
                                        "template": "¿Dónde está mi ___?",
                                        "options": [
                                            {"id": "fb_7_1", "text": "maleta"},
                                            {"id": "fb_7_2", "text": "hotel"},
                                            {"id": "fb_7_3", "text": "taxi"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Where is the hotel?' in Spanish",
                                    "prompt_translation": "Where is the hotel?",
                                    "canonical_answer": "¿Dónde está el hotel?",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "¿Dónde está el hotel?",
                                            "Donde esta el hotel",
                                            "donde esta el hotel",
                                            "¿Donde esta el hotel?"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Train & Station",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "What is 'train' in Spanish?",
                                    "prompt_translation": "train",
                                    "canonical_answer": "Tren",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_8_1", "text": "Tren"},
                                            {"id": "mc_8_2", "text": "Autobús"},
                                            {"id": "mc_8_3", "text": "Avión"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I need a ticket please'",
                                    "prompt_translation": "I need a ticket please",
                                    "canonical_answer": "Necesito un boleto por favor",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_8_1", "text": "Necesito"},
                                            {"id": "wb_8_2", "text": "un"},
                                            {"id": "wb_8_3", "text": "boleto"},
                                            {"id": "wb_8_4", "text": "por"},
                                            {"id": "wb_8_5", "text": "favor"},
                                            {"id": "wb_8_6", "text": "tren"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 3,
                                    "exercise_type": "match_pairs",
                                    "prompt": "Tap the matching pairs",
                                    "prompt_translation": None,
                                    "canonical_answer": "matched",
                                    "payload_json": json.dumps({
                                        "pairs": [
                                            {"id": "mp_8_1", "left": "Tren", "right": "Train"},
                                            {"id": "mp_8_2", "left": "Estación", "right": "Station"},
                                            {"id": "mp_8_3", "left": "Autobús", "right": "Bus"},
                                            {"id": "mp_8_4", "left": "Ciudad", "right": "City"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "El tren va a la ___.",
                                    "prompt_translation": "The train goes to the city.",
                                    "canonical_answer": "ciudad",
                                    "payload_json": json.dumps({
                                        "template": "El tren va a la ___.",
                                        "options": [
                                            {"id": "fb_8_1", "text": "ciudad"},
                                            {"id": "fb_8_2", "text": "tren"},
                                            {"id": "fb_8_3", "text": "boleto"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'A ticket to Madrid' in Spanish",
                                    "prompt_translation": "A ticket to Madrid",
                                    "canonical_answer": "Un boleto a Madrid",
                                    "payload_json": json.dumps({
                                        "accepted_answers": ["Un boleto a Madrid", "un boleto a madrid"]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

ACHIEVEMENTS_DATA = [
    {
        "code": "first_lesson",
        "title": "First Steps",
        "description": "Complete your very first lesson!",
        "icon_name": "zap"
    },
    {
        "code": "streak_3",
        "title": "Wildfire",
        "description": "Reach an impressive 3-day streak!",
        "icon_name": "flame"
    },
    {
        "code": "xp_100",
        "title": "Centurion",
        "description": "Earn 100 total XP in your language journey!",
        "icon_name": "award"
    },
    {
        "code": "perfect_lesson",
        "title": "Flawless Victory",
        "description": "Finish a full lesson without losing a single heart!",
        "icon_name": "target"
    }
]

LEADERBOARD_USERS_DATA = [
    {"username": "sofia_polyglot", "display_name": "Sofia R.", "avatar_url": "/mascots/avatar_1.svg", "weekly_xp": 620},
    {"username": "marcus_k", "display_name": "Marcus K.", "avatar_url": "/mascots/avatar_2.svg", "weekly_xp": 410},
    {"username": "elena_de", "display_name": "Elena D.", "avatar_url": "/mascots/avatar_3.svg", "weekly_xp": 380},
    {"username": "carlos_m", "display_name": "Carlos M.", "avatar_url": "/mascots/avatar_4.svg", "weekly_xp": 310},
    {"username": "priya_s", "display_name": "Priya S.", "avatar_url": "/mascots/avatar_5.svg", "weekly_xp": 270},
    {"username": "liam_w", "display_name": "Liam W.", "avatar_url": "/mascots/avatar_6.svg", "weekly_xp": 230},
    {"username": "chloe_t", "display_name": "Chloe T.", "avatar_url": "/mascots/avatar_7.svg", "weekly_xp": 190},
    {"username": "yuki_t", "display_name": "Yuki T.", "avatar_url": "/mascots/avatar_8.svg", "weekly_xp": 150},
    {"username": "mateo_b", "display_name": "Mateo B.", "avatar_url": "/mascots/avatar_9.svg", "weekly_xp": 110}
]

DEFAULT_LEARNER_DATA = {
    "username": "duo_learner",
    "display_name": "Alex Developer",
    "avatar_url": "/mascots/learner_avatar.svg",
    "stats": {
        "xp": 340,
        "hearts": 5,
        "max_hearts": 5,
        "gems": 450,
        "streak": 4,
    }
}
