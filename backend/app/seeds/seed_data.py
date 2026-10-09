import json

COURSE_DATA = {
    "code": "es-en",
    "title": "Spanish",
    "target_lang": "Spanish",
    "units": [
        # --- SECTION 1: ROOKIE BASICS ---
        {
            "order_index": 1,
            "section_index": 1,
            "section_title": "Rookie Basics",
            "title": "Unit 1: First Words",
            "description": "Greet people, introduce yourself, and learn basic courtesies.",
            "hex_color": "#58cc02",
            "is_checkpoint": False,
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
                                    "prompt": "Buenas ___, hasta mañana.",
                                    "prompt_translation": "Good night, see you tomorrow.",
                                    "canonical_answer": "noches",
                                    "payload_json": json.dumps({
                                        "template": "Buenas ___, hasta mañana.",
                                        "options": [
                                            {"id": "fb_2_1", "text": "noches"},
                                            {"id": "fb_2_2", "text": "días"},
                                            {"id": "fb_2_3", "text": "tardes"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Good night, see you later' in Spanish",
                                    "prompt_translation": "Good night, see you later",
                                    "canonical_answer": "Buenas noches, hasta luego",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Buenas noches, hasta luego",
                                            "Buenas noches hasta luego",
                                            "buenas noches, hasta luego",
                                            "buenas noches hasta luego"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: Names & Introductions",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "How do you say 'My name is' in Spanish?",
                                    "prompt_translation": "My name is",
                                    "canonical_answer": "Me llamo",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_3_1", "text": "Me llamo"},
                                            {"id": "mc_3_2", "text": "Cómo estás"},
                                            {"id": "mc_3_3", "text": "Mucho gusto"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Nice to meet you, my name is Alex'",
                                    "prompt_translation": "Nice to meet you, my name is Alex",
                                    "canonical_answer": "Mucho gusto me llamo Alex",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_3_1", "text": "Mucho"},
                                            {"id": "wb_3_2", "text": "gusto"},
                                            {"id": "wb_3_3", "text": "me"},
                                            {"id": "wb_3_4", "text": "llamo"},
                                            {"id": "wb_3_5", "text": "Alex"},
                                            {"id": "wb_3_6", "text": "adiós"}
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
                                            {"id": "mp_3_1", "left": "Yo", "right": "I"},
                                            {"id": "mp_3_2", "left": "Tú", "right": "You"},
                                            {"id": "mp_3_3", "left": "Nombre", "right": "Name"},
                                            {"id": "mp_3_4", "left": "Amigo", "right": "Friend"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "¿Cómo te ___?",
                                    "prompt_translation": "What is your name?",
                                    "canonical_answer": "llamas",
                                    "payload_json": json.dumps({
                                        "template": "¿Cómo te ___?",
                                        "options": [
                                            {"id": "fb_3_1", "text": "llamas"},
                                            {"id": "fb_3_2", "text": "llamo"},
                                            {"id": "fb_3_3", "text": "llama"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'My name is Maria' in Spanish",
                                    "prompt_translation": "My name is Maria",
                                    "canonical_answer": "Me llamo María",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Me llamo María",
                                            "Me llamo Maria",
                                            "me llamo maria",
                                            "me llamo maría"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: Please & Thank You",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Thank you very much'",
                                    "prompt_translation": "Thank you very much",
                                    "canonical_answer": "Muchas gracias",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_4_1", "text": "Muchas gracias"},
                                            {"id": "mc_4_2", "text": "Por favor"},
                                            {"id": "mc_4_3", "text": "De nada"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Please, a coffee'",
                                    "prompt_translation": "Please, a coffee",
                                    "canonical_answer": "Por favor un café",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_4_1", "text": "Por"},
                                            {"id": "wb_4_2", "text": "favor"},
                                            {"id": "wb_4_3", "text": "un"},
                                            {"id": "wb_4_4", "text": "café"},
                                            {"id": "wb_4_5", "text": "gracias"}
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
                                            {"id": "mp_4_1", "left": "Gracias", "right": "Thank you"},
                                            {"id": "mp_4_2", "left": "Por favor", "right": "Please"},
                                            {"id": "mp_4_3", "left": "De nada", "right": "You are welcome"},
                                            {"id": "mp_4_4", "left": "Perdón", "right": "Excuse me"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Muchas ___ por tu ayuda.",
                                    "prompt_translation": "Thank you very much for your help.",
                                    "canonical_answer": "gracias",
                                    "payload_json": json.dumps({
                                        "template": "Muchas ___ por tu ayuda.",
                                        "options": [
                                            {"id": "fb_4_1", "text": "gracias"},
                                            {"id": "fb_4_2", "text": "favor"},
                                            {"id": "fb_4_3", "text": "nada"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Thank you, friend' in Spanish",
                                    "prompt_translation": "Thank you, friend",
                                    "canonical_answer": "Gracias, amigo",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Gracias, amigo",
                                            "Gracias amigo",
                                            "gracias amigo",
                                            "gracias, amigo"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Counting 1 to 5",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Three'",
                                    "prompt_translation": "Number 3",
                                    "canonical_answer": "Tres",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_5_1", "text": "Tres"},
                                            {"id": "mc_5_2", "text": "Dos"},
                                            {"id": "mc_5_3", "text": "Cuatro"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'One, two, three, four, five'",
                                    "prompt_translation": "Counting 1 to 5",
                                    "canonical_answer": "Uno dos tres cuatro cinco",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_5_1", "text": "Uno"},
                                            {"id": "wb_5_2", "text": "dos"},
                                            {"id": "wb_5_3", "text": "tres"},
                                            {"id": "wb_5_4", "text": "cuatro"},
                                            {"id": "wb_5_5", "text": "cinco"},
                                            {"id": "wb_5_6", "text": "seis"}
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
                                            {"id": "mp_5_1", "left": "Uno", "right": "One"},
                                            {"id": "mp_5_2", "left": "Dos", "right": "Two"},
                                            {"id": "mp_5_3", "left": "Tres", "right": "Three"},
                                            {"id": "mp_5_4", "left": "Cuatro", "right": "Four"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Uno, dos, ___ y cuatro.",
                                    "prompt_translation": "One, two, three and four.",
                                    "canonical_answer": "tres",
                                    "payload_json": json.dumps({
                                        "template": "Uno, dos, ___ y cuatro.",
                                        "options": [
                                            {"id": "fb_5_1", "text": "tres"},
                                            {"id": "fb_5_2", "text": "cinco"},
                                            {"id": "fb_5_3", "text": "siete"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'One, two, three' in Spanish",
                                    "prompt_translation": "One, two, three",
                                    "canonical_answer": "Uno, dos, tres",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Uno, dos, tres",
                                            "Uno dos tres",
                                            "uno, dos, tres",
                                            "uno dos tres"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # --- UNIT 2: EVERYDAY WORDS ---
        {
            "order_index": 2,
            "section_index": 1,
            "section_title": "Rookie Basics",
            "title": "Unit 2: Everyday Words",
            "description": "Explore food, drinks, common objects, and everyday staples.",
            "hex_color": "#1cb0f6",
            "is_checkpoint": False,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Food & Drinks",
                    "icon_name": "coffee",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Café Essentials",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Coffee with milk'",
                                    "prompt_translation": "Coffee with milk",
                                    "canonical_answer": "Café con leche",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_6_1", "text": "Café con leche"},
                                            {"id": "mc_6_2", "text": "Té con limón"},
                                            {"id": "mc_6_3", "text": "Agua fría"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I want a coffee with milk'",
                                    "prompt_translation": "I want a coffee with milk",
                                    "canonical_answer": "Quiero un café con leche",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_6_1", "text": "Quiero"},
                                            {"id": "wb_6_2", "text": "un"},
                                            {"id": "wb_6_3", "text": "café"},
                                            {"id": "wb_6_4", "text": "con"},
                                            {"id": "wb_6_5", "text": "leche"},
                                            {"id": "wb_6_6", "text": "pan"}
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
                                            {"id": "mp_6_1", "left": "Café", "right": "Coffee"},
                                            {"id": "mp_6_2", "left": "Leche", "right": "Milk"},
                                            {"id": "mp_6_3", "left": "Agua", "right": "Water"},
                                            {"id": "mp_6_4", "left": "Té", "right": "Tea"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Un vaso de ___, por favor.",
                                    "prompt_translation": "A glass of water, please.",
                                    "canonical_answer": "agua",
                                    "payload_json": json.dumps({
                                        "template": "Un vaso de ___, por favor.",
                                        "options": [
                                            {"id": "fb_6_1", "text": "agua"},
                                            {"id": "fb_6_2", "text": "café"},
                                            {"id": "fb_6_3", "text": "leche"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'A coffee, please' in Spanish",
                                    "prompt_translation": "A coffee, please",
                                    "canonical_answer": "Un café, por favor",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Un café, por favor",
                                            "Un cafe, por favor",
                                            "Un cafe por favor",
                                            "un cafe por favor"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Breakfast Table",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Bread and cheese'",
                                    "prompt_translation": "Bread and cheese",
                                    "canonical_answer": "Pan y queso",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_7_1", "text": "Pan y queso"},
                                            {"id": "mc_7_2", "text": "Huevo y fruta"},
                                            {"id": "mc_7_3", "text": "Café con pan"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The boy eats bread and cheese'",
                                    "prompt_translation": "The boy eats bread and cheese",
                                    "canonical_answer": "El niño come pan y queso",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_7_1", "text": "El"},
                                            {"id": "wb_7_2", "text": "niño"},
                                            {"id": "wb_7_3", "text": "come"},
                                            {"id": "wb_7_4", "text": "pan"},
                                            {"id": "wb_7_5", "text": "y"},
                                            {"id": "wb_7_6", "text": "queso"}
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
                                            {"id": "mp_7_1", "left": "Pan", "right": "Bread"},
                                            {"id": "mp_7_2", "left": "Queso", "right": "Cheese"},
                                            {"id": "mp_7_3", "left": "Huevo", "right": "Egg"},
                                            {"id": "mp_7_4", "left": "Fruta", "right": "Fruit"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Yo como ___ para el desayuno.",
                                    "prompt_translation": "I eat bread for breakfast.",
                                    "canonical_answer": "pan",
                                    "payload_json": json.dumps({
                                        "template": "Yo como ___ para el desayuno.",
                                        "options": [
                                            {"id": "fb_7_1", "text": "pan"},
                                            {"id": "fb_7_2", "text": "agua"},
                                            {"id": "fb_7_3", "text": "té"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Bread and butter' in Spanish",
                                    "prompt_translation": "Bread and butter",
                                    "canonical_answer": "Pan y mantequilla",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Pan y mantequilla",
                                            "pan y mantequilla"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: Fresh Fruits",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'The red apple'",
                                    "prompt_translation": "The red apple",
                                    "canonical_answer": "La manzana roja",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_8_1", "text": "La manzana roja"},
                                            {"id": "mc_8_2", "text": "La naranja dulce"},
                                            {"id": "mc_8_3", "text": "El limón verde"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I eat an apple and an orange'",
                                    "prompt_translation": "I eat an apple and an orange",
                                    "canonical_answer": "Yo como una manzana y una naranja",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_8_1", "text": "Yo"},
                                            {"id": "wb_8_2", "text": "como"},
                                            {"id": "wb_8_3", "text": "una"},
                                            {"id": "wb_8_4", "text": "manzana"},
                                            {"id": "wb_8_5", "text": "y"},
                                            {"id": "wb_8_6", "text": "naranja"}
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
                                            {"id": "mp_8_1", "left": "Manzana", "right": "Apple"},
                                            {"id": "mp_8_2", "left": "Naranja", "right": "Orange"},
                                            {"id": "mp_8_3", "left": "Plátano", "right": "Banana"},
                                            {"id": "mp_8_4", "left": "Limón", "right": "Lemon"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "La ___ es dulce y deliciosa.",
                                    "prompt_translation": "The apple is sweet and delicious.",
                                    "canonical_answer": "manzana",
                                    "payload_json": json.dumps({
                                        "template": "La ___ es dulce y deliciosa.",
                                        "options": [
                                            {"id": "fb_8_1", "text": "manzana"},
                                            {"id": "fb_8_2", "text": "sal"},
                                            {"id": "fb_8_3", "text": "mesa"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'The orange is sweet' in Spanish",
                                    "prompt_translation": "The orange is sweet",
                                    "canonical_answer": "La naranja es dulce",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "La naranja es dulce",
                                            "la naranja es dulce"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: At Home",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the translation for 'The table and the chair'",
                                    "prompt_translation": "The table and the chair",
                                    "canonical_answer": "La mesa y la silla",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_9_1", "text": "La mesa y la silla"},
                                            {"id": "mc_9_2", "text": "La casa y la puerta"},
                                            {"id": "mc_9_3", "text": "El libro y la pluma"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The house has a large window'",
                                    "prompt_translation": "The house has a large window",
                                    "canonical_answer": "La casa tiene una ventana grande",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_9_1", "text": "La"},
                                            {"id": "wb_9_2", "text": "casa"},
                                            {"id": "wb_9_3", "text": "tiene"},
                                            {"id": "wb_9_4", "text": "una"},
                                            {"id": "wb_9_5", "text": "ventana"},
                                            {"id": "wb_9_6", "text": "grande"}
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
                                            {"id": "mp_9_1", "left": "Casa", "right": "House"},
                                            {"id": "mp_9_2", "left": "Mesa", "right": "Table"},
                                            {"id": "mp_9_3", "left": "Silla", "right": "Chair"},
                                            {"id": "mp_9_4", "left": "Puerta", "right": "Door"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "La llave está en la ___.",
                                    "prompt_translation": "The key is on the table.",
                                    "canonical_answer": "mesa",
                                    "payload_json": json.dumps({
                                        "template": "La llave está en la ___.",
                                        "options": [
                                            {"id": "fb_9_1", "text": "mesa"},
                                            {"id": "fb_9_2", "text": "leche"},
                                            {"id": "fb_9_3", "text": "amigo"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'A house with a door' in Spanish",
                                    "prompt_translation": "A house with a door",
                                    "canonical_answer": "Una casa con una puerta",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Una casa con una puerta",
                                            "una casa con una puerta"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Personal Things",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'The book and the pen'",
                                    "prompt_translation": "The book and the pen",
                                    "canonical_answer": "El libro y el bolígrafo",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_10_1", "text": "El libro y el bolígrafo"},
                                            {"id": "mc_10_2", "text": "La llave y el teléfono"},
                                            {"id": "mc_10_3", "text": "La mesa y la silla"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I have my phone and keys'",
                                    "prompt_translation": "I have my phone and keys",
                                    "canonical_answer": "Tengo mi teléfono y llaves",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_10_1", "text": "Tengo"},
                                            {"id": "wb_10_2", "text": "mi"},
                                            {"id": "wb_10_3", "text": "teléfono"},
                                            {"id": "wb_10_4", "text": "y"},
                                            {"id": "wb_10_5", "text": "llaves"},
                                            {"id": "wb_10_6", "text": "pan"}
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
                                            {"id": "mp_10_1", "left": "Libro", "right": "Book"},
                                            {"id": "mp_10_2", "left": "Teléfono", "right": "Phone"},
                                            {"id": "mp_10_3", "left": "Llave", "right": "Key"},
                                            {"id": "mp_10_4", "left": "Bolígrafo", "right": "Pen"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Mi ___ está en la mesa.",
                                    "prompt_translation": "My book is on the table.",
                                    "canonical_answer": "libro",
                                    "payload_json": json.dumps({
                                        "template": "Mi ___ está en la mesa.",
                                        "options": [
                                            {"id": "fb_10_1", "text": "libro"},
                                            {"id": "fb_10_2", "text": "agua"},
                                            {"id": "fb_10_3", "text": "noche"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'My book is here' in Spanish",
                                    "prompt_translation": "My book is here",
                                    "canonical_answer": "Mi libro está aquí",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Mi libro está aquí",
                                            "Mi libro esta aqui",
                                            "mi libro esta aqui",
                                            "mi libro está aquí"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # --- UNIT 3: SIMPLE SENTENCES ---
        {
            "order_index": 3,
            "section_index": 1,
            "section_title": "Rookie Basics",
            "title": "Unit 3: Simple Sentences",
            "description": "Form sentences with 'to be', express desires, and describe things.",
            "hex_color": "#ff9600",
            "is_checkpoint": False,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Describing Things",
                    "icon_name": "compass",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: I am & You are",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'I am a student'",
                                    "prompt_translation": "I am a student",
                                    "canonical_answer": "Yo soy estudiante",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_11_1", "text": "Yo soy estudiante"},
                                            {"id": "mc_11_2", "text": "Tú eres profesor"},
                                            {"id": "mc_11_3", "text": "Él es doctor"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'You are my good friend'",
                                    "prompt_translation": "You are my good friend",
                                    "canonical_answer": "Tú eres mi buen amigo",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_11_1", "text": "Tú"},
                                            {"id": "wb_11_2", "text": "eres"},
                                            {"id": "wb_11_3", "text": "mi"},
                                            {"id": "wb_11_4", "text": "buen"},
                                            {"id": "wb_11_5", "text": "amigo"},
                                            {"id": "wb_11_6", "text": "él"}
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
                                            {"id": "mp_11_1", "left": "Yo soy", "right": "I am"},
                                            {"id": "mp_11_2", "left": "Tú eres", "right": "You are"},
                                            {"id": "mp_11_3", "left": "Él es", "right": "He is"},
                                            {"id": "mp_11_4", "left": "Ella es", "right": "She is"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Yo ___ una persona feliz.",
                                    "prompt_translation": "I am a happy person.",
                                    "canonical_answer": "soy",
                                    "payload_json": json.dumps({
                                        "template": "Yo ___ una persona feliz.",
                                        "options": [
                                            {"id": "fb_11_1", "text": "soy"},
                                            {"id": "fb_11_2", "text": "eres"},
                                            {"id": "fb_11_3", "text": "es"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'I am a doctor' in Spanish",
                                    "prompt_translation": "I am a doctor",
                                    "canonical_answer": "Yo soy médico",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Yo soy médico",
                                            "Yo soy medico",
                                            "yo soy medico",
                                            "yo soy médico"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Where Things Are",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "How do you say 'Where is the station?'",
                                    "prompt_translation": "Where is the station?",
                                    "canonical_answer": "¿Dónde está la estación?",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_12_1", "text": "¿Dónde está la estación?"},
                                            {"id": "mc_12_2", "text": "¿Qué es la estación?"},
                                            {"id": "mc_12_3", "text": "¿Quién está aquí?"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The book is on the table'",
                                    "prompt_translation": "The book is on the table",
                                    "canonical_answer": "El libro está en la mesa",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_12_1", "text": "El"},
                                            {"id": "wb_12_2", "text": "libro"},
                                            {"id": "wb_12_3", "text": "está"},
                                            {"id": "wb_12_4", "text": "en"},
                                            {"id": "wb_12_5", "text": "la"},
                                            {"id": "wb_12_6", "text": "mesa"}
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
                                            {"id": "mp_12_1", "left": "Aquí", "right": "Here"},
                                            {"id": "mp_12_2", "left": "Allí", "right": "There"},
                                            {"id": "mp_12_3", "left": "Dónde", "right": "Where"},
                                            {"id": "mp_12_4", "left": "En", "right": "In or On"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "¿___ está el baño?",
                                    "prompt_translation": "Where is the bathroom?",
                                    "canonical_answer": "Dónde",
                                    "payload_json": json.dumps({
                                        "template": "¿___ está el baño?",
                                        "options": [
                                            {"id": "fb_12_1", "text": "Dónde"},
                                            {"id": "fb_12_2", "text": "Cómo"},
                                            {"id": "fb_12_3", "text": "Quién"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'It is here' in Spanish",
                                    "prompt_translation": "It is here",
                                    "canonical_answer": "Está aquí",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Está aquí",
                                            "Esta aqui",
                                            "esta aqui",
                                            "está aquí"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: Wanting & Needing",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'I need water'",
                                    "prompt_translation": "I need water",
                                    "canonical_answer": "Necesito agua",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_13_1", "text": "Necesito agua"},
                                            {"id": "mc_13_2", "text": "Tengo café"},
                                            {"id": "mc_13_3", "text": "Quiero pan"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I want to drink cold water'",
                                    "prompt_translation": "I want to drink cold water",
                                    "canonical_answer": "Quiero beber agua fría",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_13_1", "text": "Quiero"},
                                            {"id": "wb_13_2", "text": "beber"},
                                            {"id": "wb_13_3", "text": "agua"},
                                            {"id": "wb_13_4", "text": "fría"},
                                            {"id": "wb_13_5", "text": "leche"}
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
                                            {"id": "mp_13_1", "left": "Quiero", "right": "I want"},
                                            {"id": "mp_13_2", "left": "Necesito", "right": "I need"},
                                            {"id": "mp_13_3", "left": "Tengo", "right": "I have"},
                                            {"id": "mp_13_4", "left": "Puedo", "right": "I can"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Yo ___ ayuda, por favor.",
                                    "prompt_translation": "I need help, please.",
                                    "canonical_answer": "necesito",
                                    "payload_json": json.dumps({
                                        "template": "Yo ___ ayuda, por favor.",
                                        "options": [
                                            {"id": "fb_13_1", "text": "necesito"},
                                            {"id": "fb_13_2", "text": "tengo"},
                                            {"id": "fb_13_3", "text": "soy"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'I want a coffee' in Spanish",
                                    "prompt_translation": "I want a coffee",
                                    "canonical_answer": "Quiero un café",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Quiero un café",
                                            "Quiero un cafe",
                                            "quiero un cafe",
                                            "quiero un café"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: Colors & Senses",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'The blue car'",
                                    "prompt_translation": "The blue car",
                                    "canonical_answer": "El carro azul",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_14_1", "text": "El carro azul"},
                                            {"id": "mc_14_2", "text": "La casa roja"},
                                            {"id": "mc_14_3", "text": "El libro verde"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The red flower is very pretty'",
                                    "prompt_translation": "The red flower is very pretty",
                                    "canonical_answer": "La flor roja es muy bonita",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_14_1", "text": "La"},
                                            {"id": "wb_14_2", "text": "flor"},
                                            {"id": "wb_14_3", "text": "roja"},
                                            {"id": "wb_14_4", "text": "es"},
                                            {"id": "wb_14_5", "text": "muy"},
                                            {"id": "wb_14_6", "text": "bonita"}
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
                                            {"id": "mp_14_1", "left": "Rojo", "right": "Red"},
                                            {"id": "mp_14_2", "left": "Azul", "right": "Blue"},
                                            {"id": "mp_14_3", "left": "Verde", "right": "Green"},
                                            {"id": "mp_14_4", "left": "Amarillo", "right": "Yellow"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "El cielo es ___ y brillante.",
                                    "prompt_translation": "The sky is blue and bright.",
                                    "canonical_answer": "azul",
                                    "payload_json": json.dumps({
                                        "template": "El cielo es ___ y brillante.",
                                        "options": [
                                            {"id": "fb_14_1", "text": "azul"},
                                            {"id": "fb_14_2", "text": "pan"},
                                            {"id": "fb_14_3", "text": "mesa"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'The shirt is white' in Spanish",
                                    "prompt_translation": "The shirt is white",
                                    "canonical_answer": "La camisa es blanca",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "La camisa es blanca",
                                            "la camisa es blanca"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Big & Small",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'A big city'",
                                    "prompt_translation": "A big city",
                                    "canonical_answer": "Una ciudad grande",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_15_1", "text": "Una ciudad grande"},
                                            {"id": "mc_15_2", "text": "Un pueblo pequeño"},
                                            {"id": "mc_15_3", "text": "Una casa nueva"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The small cat drinks milk'",
                                    "prompt_translation": "The small cat drinks milk",
                                    "canonical_answer": "El gato pequeño bebe leche",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_15_1", "text": "El"},
                                            {"id": "wb_15_2", "text": "gato"},
                                            {"id": "wb_15_3", "text": "pequeño"},
                                            {"id": "wb_15_4", "text": "bebe"},
                                            {"id": "wb_15_5", "text": "leche"},
                                            {"id": "wb_15_6", "text": "agua"}
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
                                            {"id": "mp_15_1", "left": "Grande", "right": "Big"},
                                            {"id": "mp_15_2", "left": "Pequeño", "right": "Small"},
                                            {"id": "mp_15_3", "left": "Nuevo", "right": "New"},
                                            {"id": "mp_15_4", "left": "Viejo", "right": "Old"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Es un coche muy ___ y rápido.",
                                    "prompt_translation": "It is a very big and fast car.",
                                    "canonical_answer": "grande",
                                    "payload_json": json.dumps({
                                        "template": "Es un coche muy ___ y rápido.",
                                        "options": [
                                            {"id": "fb_15_1", "text": "grande"},
                                            {"id": "fb_15_2", "text": "ayer"},
                                            {"id": "fb_15_3", "text": "gracias"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'A small house' in Spanish",
                                    "prompt_translation": "A small house",
                                    "canonical_answer": "Una casa pequeña",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Una casa pequeña",
                                            "Una casa pequena",
                                            "una casa pequena",
                                            "una casa pequeña"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # --- UNIT 4: EVERYDAY CONVERSATIONS ---
        {
            "order_index": 4,
            "section_index": 1,
            "section_title": "Rookie Basics",
            "title": "Unit 4: Everyday Conversations",
            "description": "Talk with friends, describe family members, and ask questions.",
            "hex_color": "#ce82ff",
            "is_checkpoint": False,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Family & People",
                    "icon_name": "users",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Family Members",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'My mother and father'",
                                    "prompt_translation": "My mother and father",
                                    "canonical_answer": "Mi madre y mi padre",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_16_1", "text": "Mi madre y mi padre"},
                                            {"id": "mc_16_2", "text": "Mi hermano y mi hermana"},
                                            {"id": "mc_16_3", "text": "Mi amigo y mi amiga"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'My brother has a friendly dog'",
                                    "prompt_translation": "My brother has a friendly dog",
                                    "canonical_answer": "Mi hermano tiene un perro simpático",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_16_1", "text": "Mi"},
                                            {"id": "wb_16_2", "text": "hermano"},
                                            {"id": "wb_16_3", "text": "tiene"},
                                            {"id": "wb_16_4", "text": "un"},
                                            {"id": "wb_16_5", "text": "perro"},
                                            {"id": "wb_16_6", "text": "simpático"}
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
                                            {"id": "mp_16_1", "left": "Madre", "right": "Mother"},
                                            {"id": "mp_16_2", "left": "Padre", "right": "Father"},
                                            {"id": "mp_16_3", "left": "Hermano", "right": "Brother"},
                                            {"id": "mp_16_4", "left": "Hermana", "right": "Sister"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Mi ___ cocina muy rico.",
                                    "prompt_translation": "My mother cooks very well.",
                                    "canonical_answer": "madre",
                                    "payload_json": json.dumps({
                                        "template": "Mi ___ cocina muy rico.",
                                        "options": [
                                            {"id": "fb_16_1", "text": "madre"},
                                            {"id": "fb_16_2", "text": "agua"},
                                            {"id": "fb_16_3", "text": "mesa"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'My family is big' in Spanish",
                                    "prompt_translation": "My family is big",
                                    "canonical_answer": "Mi familia es grande",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Mi familia es grande",
                                            "mi familia es grande"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Friends & Neighbors",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'He is my best friend'",
                                    "prompt_translation": "He is my best friend",
                                    "canonical_answer": "Él es mi mejor amigo",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_17_1", "text": "Él es mi mejor amigo"},
                                            {"id": "mc_17_2", "text": "Ella es mi vecina"},
                                            {"id": "mc_17_3", "text": "Yo tengo amigos"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'We are very good friends'",
                                    "prompt_translation": "We are very good friends",
                                    "canonical_answer": "Nosotros somos muy buenos amigos",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_17_1", "text": "Nosotros"},
                                            {"id": "wb_17_2", "text": "somos"},
                                            {"id": "wb_17_3", "text": "muy"},
                                            {"id": "wb_17_4", "text": "buenos"},
                                            {"id": "wb_17_5", "text": "amigos"},
                                            {"id": "wb_17_6", "text": "casa"}
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
                                            {"id": "mp_17_1", "left": "Amigo", "right": "Friend"},
                                            {"id": "mp_17_2", "left": "Vecino", "right": "Neighbor"},
                                            {"id": "mp_17_3", "left": "Gente", "right": "People"},
                                            {"id": "mp_17_4", "left": "Niño", "right": "Child"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Ella es mi ___ favorita.",
                                    "prompt_translation": "She is my favorite friend.",
                                    "canonical_answer": "amiga",
                                    "payload_json": json.dumps({
                                        "template": "Ella es mi ___ favorita.",
                                        "options": [
                                            {"id": "fb_17_1", "text": "amiga"},
                                            {"id": "fb_17_2", "text": "amigo"},
                                            {"id": "fb_17_3", "text": "libro"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Hello, my friend' in Spanish",
                                    "prompt_translation": "Hello, my friend",
                                    "canonical_answer": "Hola, mi amigo",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Hola, mi amigo",
                                            "Hola mi amigo",
                                            "hola mi amigo",
                                            "hola, mi amigo"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: Questions & Answers",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "How do you ask 'What is your name?' in Spanish?",
                                    "prompt_translation": "What is your name?",
                                    "canonical_answer": "¿Cuál es tu nombre?",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_18_1", "text": "¿Cuál es tu nombre?"},
                                            {"id": "mc_18_2", "text": "¿Dónde vives tú?"},
                                            {"id": "mc_18_3", "text": "¿Quién es tu padre?"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Who is that tall person?'",
                                    "prompt_translation": "Who is that tall person?",
                                    "canonical_answer": "¿Quién es esa persona alta?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_18_1", "text": "¿Quién"},
                                            {"id": "wb_18_2", "text": "es"},
                                            {"id": "wb_18_3", "text": "esa"},
                                            {"id": "wb_18_4", "text": "persona"},
                                            {"id": "wb_18_5", "text": "alta?"},
                                            {"id": "wb_18_6", "text": "dónde"}
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
                                            {"id": "mp_18_1", "left": "¿Qué?", "right": "What?"},
                                            {"id": "mp_18_2", "left": "¿Quién?", "right": "Who?"},
                                            {"id": "mp_18_3", "left": "¿Cuándo?", "right": "When?"},
                                            {"id": "mp_18_4", "left": "¿Por qué?", "right": "Why?"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "¿___ hora es ahora?",
                                    "prompt_translation": "What time is it now?",
                                    "canonical_answer": "Qué",
                                    "payload_json": json.dumps({
                                        "template": "¿___ hora es ahora?",
                                        "options": [
                                            {"id": "fb_18_1", "text": "Qué"},
                                            {"id": "fb_18_2", "text": "Quién"},
                                            {"id": "fb_18_3", "text": "Dónde"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Why not?' in Spanish",
                                    "prompt_translation": "Why not?",
                                    "canonical_answer": "¿Por qué no?",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "¿Por qué no?",
                                            "Por qué no?",
                                            "Por que no?",
                                            "por que no",
                                            "por qué no"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: At the Restaurant",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'The bill, please'",
                                    "prompt_translation": "The bill, please",
                                    "canonical_answer": "La cuenta, por favor",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_19_1", "text": "La cuenta, por favor"},
                                            {"id": "mc_19_2", "text": "El menú del día"},
                                            {"id": "mc_19_3", "text": "La mesa de dos"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'A table for two people, please'",
                                    "prompt_translation": "A table for two people, please",
                                    "canonical_answer": "Una mesa para dos personas por favor",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_19_1", "text": "Una"},
                                            {"id": "wb_19_2", "text": "mesa"},
                                            {"id": "wb_19_3", "text": "para"},
                                            {"id": "wb_19_4", "text": "dos"},
                                            {"id": "wb_19_5", "text": "personas"},
                                            {"id": "wb_19_6", "text": "por favor"}
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
                                            {"id": "mp_19_1", "left": "Mesa", "right": "Table"},
                                            {"id": "mp_19_2", "left": "Menú", "right": "Menu"},
                                            {"id": "mp_19_3", "left": "Cuenta", "right": "Bill"},
                                            {"id": "mp_19_4", "left": "Plato", "right": "Dish"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "¿Nos trae la ___, por favor?",
                                    "prompt_translation": "Could you bring us the bill, please?",
                                    "canonical_answer": "cuenta",
                                    "payload_json": json.dumps({
                                        "template": "¿Nos trae la ___, por favor?",
                                        "options": [
                                            {"id": "fb_19_1", "text": "cuenta"},
                                            {"id": "fb_19_2", "text": "silla"},
                                            {"id": "fb_19_3", "text": "calle"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'A table, please' in Spanish",
                                    "prompt_translation": "A table, please",
                                    "canonical_answer": "Una mesa, por favor",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Una mesa, por favor",
                                            "Una mesa por favor",
                                            "una mesa por favor",
                                            "una mesa, por favor"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Polite Requests",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "How do you say 'Excuse me, may I pass?'",
                                    "prompt_translation": "Excuse me, may I pass?",
                                    "canonical_answer": "Con permiso, ¿puedo pasar?",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_20_1", "text": "Con permiso, ¿puedo pasar?"},
                                            {"id": "mc_20_2", "text": "De nada, hasta luego"},
                                            {"id": "mc_20_3", "text": "Muchas gracias a todos"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Excuse me, do you speak Spanish?'",
                                    "prompt_translation": "Excuse me, do you speak Spanish?",
                                    "canonical_answer": "Disculpe, ¿usted habla español?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_20_1", "text": "Disculpe,"},
                                            {"id": "wb_20_2", "text": "¿usted"},
                                            {"id": "wb_20_3", "text": "habla"},
                                            {"id": "wb_20_4", "text": "español?"},
                                            {"id": "wb_20_5", "text": "inglés"}
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
                                            {"id": "mp_20_1", "left": "Con permiso", "right": "Excuse me (passing)"},
                                            {"id": "mp_20_2", "left": "Disculpe", "right": "Pardon me"},
                                            {"id": "mp_20_3", "left": "Claro", "right": "Of course"},
                                            {"id": "mp_20_4", "left": "Perdón", "right": "Sorry"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Con ___, necesito pasar.",
                                    "prompt_translation": "Excuse me, I need to pass.",
                                    "canonical_answer": "permiso",
                                    "payload_json": json.dumps({
                                        "template": "Con ___, necesito pasar.",
                                        "options": [
                                            {"id": "fb_20_1", "text": "permiso"},
                                            {"id": "fb_20_2", "text": "queso"},
                                            {"id": "fb_20_3", "text": "leche"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Excuse me, sir' in Spanish",
                                    "prompt_translation": "Excuse me, sir",
                                    "canonical_answer": "Disculpe, señor",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Disculpe, señor",
                                            "Disculpe señor",
                                            "Disculpe, senor",
                                            "disculpe senor",
                                            "disculpe, señor"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # --- UNIT 5: PRACTICE & REVIEW ---
        {
            "order_index": 5,
            "section_index": 1,
            "section_title": "Rookie Basics",
            "title": "Unit 5: Practice & Review",
            "description": "Reinforce grammar, polish vocabulary, and prepare for the Section 1 Checkpoint.",
            "hex_color": "#2b70c9",
            "is_checkpoint": False,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Comprehensive Review",
                    "icon_name": "star",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Vocabulary Review",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Good morning and welcome'",
                                    "prompt_translation": "Good morning and welcome",
                                    "canonical_answer": "Buenos días y bienvenido",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_21_1", "text": "Buenos días y bienvenido"},
                                            {"id": "mc_21_2", "text": "Buenas noches amigo"},
                                            {"id": "mc_21_3", "text": "Hasta luego mi familia"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I want a warm cup of coffee'",
                                    "prompt_translation": "I want a warm cup of coffee",
                                    "canonical_answer": "Quiero una taza de café caliente",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_21_1", "text": "Quiero"},
                                            {"id": "wb_21_2", "text": "una"},
                                            {"id": "wb_21_3", "text": "taza"},
                                            {"id": "wb_21_4", "text": "de"},
                                            {"id": "wb_21_5", "text": "café"},
                                            {"id": "wb_21_6", "text": "caliente"}
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
                                            {"id": "mp_21_1", "left": "Buenos días", "right": "Good morning"},
                                            {"id": "mp_21_2", "left": "Buenas noches", "right": "Good night"},
                                            {"id": "mp_21_3", "left": "Gracias", "right": "Thanks"},
                                            {"id": "mp_21_4", "left": "Por favor", "right": "Please"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "___ tardes, ¿cómo está usted?",
                                    "prompt_translation": "Good afternoon, how are you?",
                                    "canonical_answer": "Buenas",
                                    "payload_json": json.dumps({
                                        "template": "___ tardes, ¿cómo está usted?",
                                        "options": [
                                            {"id": "fb_21_1", "text": "Buenas"},
                                            {"id": "fb_21_2", "text": "Buenos"},
                                            {"id": "fb_21_3", "text": "Buen"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Welcome, friend' in Spanish",
                                    "prompt_translation": "Welcome, friend",
                                    "canonical_answer": "Bienvenido, amigo",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Bienvenido, amigo",
                                            "Bienvenido amigo",
                                            "bienvenido amigo",
                                            "bienvenido, amigo"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Grammar Review",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'She is at the café'",
                                    "prompt_translation": "She is at the café",
                                    "canonical_answer": "Ella está en el café",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_22_1", "text": "Ella está en el café"},
                                            {"id": "mc_22_2", "text": "Él es de España"},
                                            {"id": "mc_22_3", "text": "Yo tengo un libro"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'We need to speak today'",
                                    "prompt_translation": "We need to speak today",
                                    "canonical_answer": "Nosotros necesitamos hablar hoy",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_22_1", "text": "Nosotros"},
                                            {"id": "wb_22_2", "text": "necesitamos"},
                                            {"id": "wb_22_3", "text": "hablar"},
                                            {"id": "wb_22_4", "text": "hoy"},
                                            {"id": "wb_22_5", "text": "ayer"}
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
                                            {"id": "mp_22_1", "left": "Yo tengo", "right": "I have"},
                                            {"id": "mp_22_2", "left": "Tú tienes", "right": "You have"},
                                            {"id": "mp_22_3", "left": "Él tiene", "right": "He has"},
                                            {"id": "mp_22_4", "left": "Nosotros tenemos", "right": "We have"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Ellos ___ dos hermanos.",
                                    "prompt_translation": "They have two brothers.",
                                    "canonical_answer": "tienen",
                                    "payload_json": json.dumps({
                                        "template": "Ellos ___ dos hermanos.",
                                        "options": [
                                            {"id": "fb_22_1", "text": "tienen"},
                                            {"id": "fb_22_2", "text": "tengo"},
                                            {"id": "fb_22_3", "text": "tiene"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'I have two books' in Spanish",
                                    "prompt_translation": "I have two books",
                                    "canonical_answer": "Tengo dos libros",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Tengo dos libros",
                                            "Yo tengo dos libros",
                                            "tengo dos libros",
                                            "yo tengo dos libros"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: Dialogue Practice",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the translation for 'See you tomorrow at noon'",
                                    "prompt_translation": "See you tomorrow at noon",
                                    "canonical_answer": "Hasta mañana al mediodía",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_23_1", "text": "Hasta mañana al mediodía"},
                                            {"id": "mc_23_2", "text": "Buenos días a las dos"},
                                            {"id": "mc_23_3", "text": "Buenas noches a todos"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Hello, how are you this morning?'",
                                    "prompt_translation": "Hello, how are you this morning?",
                                    "canonical_answer": "Hola, ¿cómo estás esta mañana?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_23_1", "text": "Hola,"},
                                            {"id": "wb_23_2", "text": "¿cómo"},
                                            {"id": "wb_23_3", "text": "estás"},
                                            {"id": "wb_23_4", "text": "esta"},
                                            {"id": "wb_23_5", "text": "mañana?"},
                                            {"id": "wb_23_6", "text": "noche"}
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
                                            {"id": "mp_23_1", "left": "Hola", "right": "Hello"},
                                            {"id": "mp_23_2", "left": "Adiós", "right": "Bye"},
                                            {"id": "mp_23_3", "left": "Hasta pronto", "right": "See you soon"},
                                            {"id": "mp_23_4", "left": "Mucho gusto", "right": "Nice to meet you"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Muy bien, ¿y ___?",
                                    "prompt_translation": "Very good, and you?",
                                    "canonical_answer": "tú",
                                    "payload_json": json.dumps({
                                        "template": "Muy bien, ¿y ___?",
                                        "options": [
                                            {"id": "fb_23_1", "text": "tú"},
                                            {"id": "fb_23_2", "text": "yo"},
                                            {"id": "fb_23_3", "text": "él"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Very good, thank you' in Spanish",
                                    "prompt_translation": "Very good, thank you",
                                    "canonical_answer": "Muy bien, gracias",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Muy bien, gracias",
                                            "Muy bien gracias",
                                            "muy bien gracias",
                                            "muy bien, gracias"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: Speed Challenge",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select the correct translation for 'Red apple'",
                                    "prompt_translation": "Red apple",
                                    "canonical_answer": "Manzana roja",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_24_1", "text": "Manzana roja"},
                                            {"id": "mc_24_2", "text": "Pan dulce"},
                                            {"id": "mc_24_3", "text": "Agua fresca"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'One, two, three, four'",
                                    "prompt_translation": "One, two, three, four",
                                    "canonical_answer": "Uno dos tres cuatro",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_24_1", "text": "Uno"},
                                            {"id": "wb_24_2", "text": "dos"},
                                            {"id": "wb_24_3", "text": "tres"},
                                            {"id": "wb_24_4", "text": "cuatro"},
                                            {"id": "wb_24_5", "text": "cinco"}
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
                                            {"id": "mp_24_1", "left": "Agua", "right": "Water"},
                                            {"id": "mp_24_2", "left": "Pan", "right": "Bread"},
                                            {"id": "mp_24_3", "left": "Leche", "right": "Milk"},
                                            {"id": "mp_24_4", "left": "Queso", "right": "Cheese"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "El café con ___ está listo.",
                                    "prompt_translation": "The coffee with milk is ready.",
                                    "canonical_answer": "leche",
                                    "payload_json": json.dumps({
                                        "template": "El café con ___ está listo.",
                                        "options": [
                                            {"id": "fb_24_1", "text": "leche"},
                                            {"id": "fb_24_2", "text": "casa"},
                                            {"id": "fb_24_3", "text": "puerta"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Yes, I want water' in Spanish",
                                    "prompt_translation": "Yes, I want water",
                                    "canonical_answer": "Sí, quiero agua",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Sí, quiero agua",
                                            "Si, quiero agua",
                                            "Si quiero agua",
                                            "si quiero agua"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Pre-Checkpoint Trial",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'I am ready for the challenge'",
                                    "prompt_translation": "I am ready for the challenge",
                                    "canonical_answer": "Estoy listo para el desafío",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_25_1", "text": "Estoy listo para el desafío"},
                                            {"id": "mc_25_2", "text": "Tengo sueño hoy"},
                                            {"id": "mc_25_3", "text": "Quiero salir ahora"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Excuse me, where is the station?'",
                                    "prompt_translation": "Excuse me, where is the station?",
                                    "canonical_answer": "Perdón, ¿dónde está la estación?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_25_1", "text": "Perdón,"},
                                            {"id": "wb_25_2", "text": "¿dónde"},
                                            {"id": "wb_25_3", "text": "está"},
                                            {"id": "wb_25_4", "text": "la"},
                                            {"id": "wb_25_5", "text": "estación?"},
                                            {"id": "wb_25_6", "text": "aquí"}
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
                                            {"id": "mp_25_1", "left": "Casa", "right": "House"},
                                            {"id": "mp_25_2", "left": "Mesa", "right": "Table"},
                                            {"id": "mp_25_3", "left": "Familia", "right": "Family"},
                                            {"id": "mp_25_4", "left": "Amigo", "right": "Friend"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Todo está muy ___, gracias.",
                                    "prompt_translation": "Everything is very good, thanks.",
                                    "canonical_answer": "bien",
                                    "payload_json": json.dumps({
                                        "template": "Todo está muy ___, gracias.",
                                        "options": [
                                            {"id": "fb_25_1", "text": "bien"},
                                            {"id": "fb_25_2", "text": "mal"},
                                            {"id": "fb_25_3", "text": "ayer"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'I speak Spanish' in Spanish",
                                    "prompt_translation": "I speak Spanish",
                                    "canonical_answer": "Yo hablo español",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Yo hablo español",
                                            "Hablo español",
                                            "Yo hablo espanol",
                                            "Hablo espanol",
                                            "yo hablo espanol",
                                            "hablo espanol"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # --- UNIT 6: SECTION 1 CHECKPOINT CHALLENGE ---
        {
            "order_index": 6,
            "section_index": 1,
            "section_title": "Rookie Basics",
            "title": "Section 1 Checkpoint Challenge",
            "description": "Prove your mastery of Rookie Basics to unlock Section 2!",
            "hex_color": "#ff4b4b",
            "is_checkpoint": True,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Section 1 Checkpoint Challenge",
                    "icon_name": "trophy",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Section 1 Checkpoint Challenge",
                            "xp_reward": 50,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'Hello, welcome to my home'",
                                    "prompt_translation": "Hello, welcome to my home",
                                    "canonical_answer": "Hola, bienvenido a mi casa",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_26_1", "text": "Hola, bienvenido a mi casa"},
                                            {"id": "mc_26_2", "text": "Buenas noches amigo mío"},
                                            {"id": "mc_26_3", "text": "Hasta luego mi doctor"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'My brother wants a coffee and bread'",
                                    "prompt_translation": "My brother wants a coffee and bread",
                                    "canonical_answer": "Mi hermano quiere un café y pan",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_26_1", "text": "Mi"},
                                            {"id": "wb_26_2", "text": "hermano"},
                                            {"id": "wb_26_3", "text": "quiere"},
                                            {"id": "wb_26_4", "text": "un"},
                                            {"id": "wb_26_5", "text": "café"},
                                            {"id": "wb_26_6", "text": "y"},
                                            {"id": "wb_26_7", "text": "pan"}
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
                                            {"id": "mp_26_1", "left": "Por favor", "right": "Please"},
                                            {"id": "mp_26_2", "left": "Gracias", "right": "Thank you"},
                                            {"id": "mp_26_3", "left": "Amigo", "right": "Friend"},
                                            {"id": "mp_26_4", "left": "Familia", "right": "Family"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Yo soy un estudiante y hablo ___ muy bien.",
                                    "prompt_translation": "I am a student and speak Spanish very well.",
                                    "canonical_answer": "español",
                                    "payload_json": json.dumps({
                                        "template": "Yo soy un estudiante y hablo ___ muy bien.",
                                        "options": [
                                            {"id": "fb_26_1", "text": "español"},
                                            {"id": "fb_26_2", "text": "mesa"},
                                            {"id": "fb_26_3", "text": "ayer"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Hello, I speak Spanish' in Spanish",
                                    "prompt_translation": "Hello, I speak Spanish",
                                    "canonical_answer": "Hola, yo hablo español",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Hola, yo hablo español",
                                            "Hola, hablo español",
                                            "Hola yo hablo español",
                                            "Hola, yo hablo espanol",
                                            "Hola hablo espanol",
                                            "hola yo hablo espanol"
                                        ]
                                    })
                                }
                            ]
                        }
                    ]
                }
            ]
        },

        # --- SECTION 2: DAILY LIFE ---
        {
            "order_index": 7,
            "section_index": 2,
            "section_title": "Daily Life",
            "title": "Unit 1: Food & Dining",
            "description": "Order food, explore local delicacies, and dine out with ease.",
            "hex_color": "#1cb0f6",
            "is_checkpoint": False,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Travel Basics",
                    "icon_name": "compass",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Airport Check-in",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'My passport and boarding pass'",
                                    "prompt_translation": "My passport and boarding pass",
                                    "canonical_answer": "Mi pasaporte y boleto",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_27_1", "text": "Mi pasaporte y boleto"},
                                            {"id": "mc_27_2", "text": "La maleta grande"},
                                            {"id": "mc_27_3", "text": "El avión rápido"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The flight leaves in thirty minutes'",
                                    "prompt_translation": "The flight leaves in thirty minutes",
                                    "canonical_answer": "El vuelo sale en treinta minutos",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_27_1", "text": "El"},
                                            {"id": "wb_27_2", "text": "vuelo"},
                                            {"id": "wb_27_3", "text": "sale"},
                                            {"id": "wb_27_4", "text": "en"},
                                            {"id": "wb_27_5", "text": "treinta"},
                                            {"id": "wb_27_6", "text": "minutos"}
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
                                            {"id": "mp_27_1", "left": "Pasaporte", "right": "Passport"},
                                            {"id": "mp_27_2", "left": "Vuelo", "right": "Flight"},
                                            {"id": "mp_27_3", "left": "Avión", "right": "Airplane"},
                                            {"id": "mp_27_4", "left": "Maleta", "right": "Suitcase"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Aquí está mi ___, oficial.",
                                    "prompt_translation": "Here is my passport, officer.",
                                    "canonical_answer": "pasaporte",
                                    "payload_json": json.dumps({
                                        "template": "Aquí está mi ___, oficial.",
                                        "options": [
                                            {"id": "fb_27_1", "text": "pasaporte"},
                                            {"id": "fb_27_2", "text": "té"},
                                            {"id": "fb_27_3", "text": "pan"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Here is my ticket' in Spanish",
                                    "prompt_translation": "Here is my ticket",
                                    "canonical_answer": "Aquí está mi boleto",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Aquí está mi boleto",
                                            "Aqui esta mi boleto",
                                            "aqui esta mi boleto",
                                            "aquí está mi boleto"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Taking a Taxi",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'To the city center, please'",
                                    "prompt_translation": "To the city center, please",
                                    "canonical_answer": "Al centro, por favor",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_28_1", "text": "Al centro, por favor"},
                                            {"id": "mc_28_2", "text": "A la casa mía"},
                                            {"id": "mc_28_3", "text": "Al parque verde"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Can you take me to the airport?'",
                                    "prompt_translation": "Can you take me to the airport?",
                                    "canonical_answer": "¿Puede llevarme al aeropuerto?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_28_1", "text": "¿Puede"},
                                            {"id": "wb_28_2", "text": "llevarme"},
                                            {"id": "wb_28_3", "text": "al"},
                                            {"id": "wb_28_4", "text": "aeropuerto?"},
                                            {"id": "wb_28_5", "text": "hotel"}
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
                                            {"id": "mp_28_1", "left": "Taxi", "right": "Taxi"},
                                            {"id": "mp_28_2", "left": "Calle", "right": "Street"},
                                            {"id": "mp_28_3", "left": "Parada", "right": "Stop"},
                                            {"id": "mp_28_4", "left": "Estación", "right": "Station"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Un taxi al ___, por favor.",
                                    "prompt_translation": "A taxi to the hotel, please.",
                                    "canonical_answer": "hotel",
                                    "payload_json": json.dumps({
                                        "template": "Un taxi al ___, por favor.",
                                        "options": [
                                            {"id": "fb_28_1", "text": "hotel"},
                                            {"id": "fb_28_2", "text": "agua"},
                                            {"id": "fb_28_3", "text": "leche"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'To the hotel, please' in Spanish",
                                    "prompt_translation": "To the hotel, please",
                                    "canonical_answer": "Al hotel, por favor",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Al hotel, por favor",
                                            "Al hotel por favor",
                                            "al hotel por favor",
                                            "al hotel, por favor"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: At the Hotel",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'I have a room reservation'",
                                    "prompt_translation": "I have a room reservation",
                                    "canonical_answer": "Tengo una reservación de habitación",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_29_1", "text": "Tengo una reservación de habitación"},
                                            {"id": "mc_29_2", "text": "Quiero salir de aquí"},
                                            {"id": "mc_29_3", "text": "Dónde está la puerta"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Where is the room key?'",
                                    "prompt_translation": "Where is the room key?",
                                    "canonical_answer": "¿Dónde está la llave de la habitación?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_29_1", "text": "¿Dónde"},
                                            {"id": "wb_29_2", "text": "está"},
                                            {"id": "wb_29_3", "text": "la"},
                                            {"id": "wb_29_4", "text": "llave"},
                                            {"id": "wb_29_5", "text": "de la"},
                                            {"id": "wb_29_6", "text": "habitación?"}
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
                                            {"id": "mp_29_1", "left": "Habitación", "right": "Room"},
                                            {"id": "mp_29_2", "left": "Llave", "right": "Key"},
                                            {"id": "mp_29_3", "left": "Cama", "right": "Bed"},
                                            {"id": "mp_29_4", "left": "Baño", "right": "Bathroom"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "La ___ número diez está lista.",
                                    "prompt_translation": "Room number ten is ready.",
                                    "canonical_answer": "habitación",
                                    "payload_json": json.dumps({
                                        "template": "La ___ número diez está lista.",
                                        "options": [
                                            {"id": "fb_29_1", "text": "habitación"},
                                            {"id": "fb_29_2", "text": "mesa"},
                                            {"id": "fb_29_3", "text": "calle"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'The key, please' in Spanish",
                                    "prompt_translation": "The key, please",
                                    "canonical_answer": "La llave, por favor",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "La llave, por favor",
                                            "La llave por favor",
                                            "la llave por favor",
                                            "la llave, por favor"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: Asking for Directions",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'Turn left at the corner'",
                                    "prompt_translation": "Turn left at the corner",
                                    "canonical_answer": "Gire a la izquierda en la esquina",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_30_1", "text": "Gire a la izquierda en la esquina"},
                                            {"id": "mc_30_2", "text": "Camine todo recto por el parque"},
                                            {"id": "mc_30_3", "text": "Gire a la derecha en la plaza"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Go straight ahead and turn right'",
                                    "prompt_translation": "Go straight ahead and turn right",
                                    "canonical_answer": "Siga todo recto y gire a la derecha",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_30_1", "text": "Siga"},
                                            {"id": "wb_30_2", "text": "todo"},
                                            {"id": "wb_30_3", "text": "recto"},
                                            {"id": "wb_30_4", "text": "y"},
                                            {"id": "wb_30_5", "text": "gire"},
                                            {"id": "wb_30_6", "text": "a la derecha"}
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
                                            {"id": "mp_30_1", "left": "Izquierda", "right": "Left"},
                                            {"id": "mp_30_2", "left": "Derecha", "right": "Right"},
                                            {"id": "mp_30_3", "left": "Recto", "right": "Straight"},
                                            {"id": "mp_30_4", "left": "Cerca", "right": "Close"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "La plaza está muy ___ de aquí.",
                                    "prompt_translation": "The plaza is very close to here.",
                                    "canonical_answer": "cerca",
                                    "payload_json": json.dumps({
                                        "template": "La plaza está muy ___ de aquí.",
                                        "options": [
                                            {"id": "fb_30_1", "text": "cerca"},
                                            {"id": "fb_30_2", "text": "lejos"},
                                            {"id": "fb_30_3", "text": "pan"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Turn right' in Spanish",
                                    "prompt_translation": "Turn right",
                                    "canonical_answer": "Gire a la derecha",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Gire a la derecha",
                                            "Dobla a la derecha",
                                            "gire a la derecha",
                                            "dobla a la derecha"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Sightseeing",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'The historical museum'",
                                    "prompt_translation": "The historical museum",
                                    "canonical_answer": "El museo histórico",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_31_1", "text": "El museo histórico"},
                                            {"id": "mc_31_2", "text": "La playa hermosa"},
                                            {"id": "mc_31_3", "text": "El parque central"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'The city park is very beautiful'",
                                    "prompt_translation": "The city park is very beautiful",
                                    "canonical_answer": "El parque de la ciudad es muy hermoso",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_31_1", "text": "El"},
                                            {"id": "wb_31_2", "text": "parque"},
                                            {"id": "wb_31_3", "text": "de la"},
                                            {"id": "wb_31_4", "text": "ciudad"},
                                            {"id": "wb_31_5", "text": "es"},
                                            {"id": "wb_31_6", "text": "muy"},
                                            {"id": "wb_31_7", "text": "hermoso"}
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
                                            {"id": "mp_31_1", "left": "Museo", "right": "Museum"},
                                            {"id": "mp_31_2", "left": "Parque", "right": "Park"},
                                            {"id": "mp_31_3", "left": "Playa", "right": "Beach"},
                                            {"id": "mp_31_4", "left": "Catedral", "right": "Cathedral"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Visité el ___ ayer por la tarde.",
                                    "prompt_translation": "I visited the museum yesterday in the afternoon.",
                                    "canonical_answer": "museo",
                                    "payload_json": json.dumps({
                                        "template": "Visité el ___ ayer por la tarde.",
                                        "options": [
                                            {"id": "fb_31_1", "text": "museo"},
                                            {"id": "fb_31_2", "text": "agua"},
                                            {"id": "fb_31_3", "text": "queso"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'A beautiful city' in Spanish",
                                    "prompt_translation": "A beautiful city",
                                    "canonical_answer": "Una ciudad hermosa",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Una ciudad hermosa",
                                            "Una ciudad bonita",
                                            "una ciudad hermosa",
                                            "una ciudad bonita"
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
            "order_index": 8,
            "section_index": 2,
            "section_title": "Daily Life",
            "title": "Unit 2: Daily Routines",
            "description": "Handle daily routines, market shopping, and schedules.",
            "hex_color": "#58cc02",
            "is_checkpoint": False,
            "skills": [
                {
                    "order_index": 1,
                    "title": "Daily Routines",
                    "icon_name": "coffee",
                    "total_crown_levels": 5,
                    "lessons": [
                        {
                            "order_index": 1,
                            "title": "Lesson 1: Morning Routines",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'I wake up early'",
                                    "prompt_translation": "I wake up early",
                                    "canonical_answer": "Me despierto temprano",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_32_1", "text": "Me despierto temprano"},
                                            {"id": "mc_32_2", "text": "Tengo mucho trabajo"},
                                            {"id": "mc_32_3", "text": "Voy al mercado ahora"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I drink coffee every morning'",
                                    "prompt_translation": "I drink coffee every morning",
                                    "canonical_answer": "Bebo café todas las mañanas",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_32_1", "text": "Bebo"},
                                            {"id": "wb_32_2", "text": "café"},
                                            {"id": "wb_32_3", "text": "todas"},
                                            {"id": "wb_32_4", "text": "las"},
                                            {"id": "wb_32_5", "text": "mañanas"}
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
                                            {"id": "mp_32_1", "left": "Mañana", "right": "Morning"},
                                            {"id": "mp_32_2", "left": "Desayuno", "right": "Breakfast"},
                                            {"id": "mp_32_3", "left": "Temprano", "right": "Early"},
                                            {"id": "mp_32_4", "left": "Día", "right": "Day"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Me despierto a las siete de la ___.",
                                    "prompt_translation": "I wake up at seven in the morning.",
                                    "canonical_answer": "mañana",
                                    "payload_json": json.dumps({
                                        "template": "Me despierto a las siete de la ___.",
                                        "options": [
                                            {"id": "fb_32_1", "text": "mañana"},
                                            {"id": "fb_32_2", "text": "noche"},
                                            {"id": "fb_32_3", "text": "tarde"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Good morning, everyone' in Spanish",
                                    "prompt_translation": "Good morning, everyone",
                                    "canonical_answer": "Buenos días a todos",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Buenos días a todos",
                                            "Buenos dias a todos",
                                            "buenos dias a todos",
                                            "buenos días a todos"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 2,
                            "title": "Lesson 2: Shopping at the Market",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'How much does this fruit cost?'",
                                    "prompt_translation": "How much does this fruit cost?",
                                    "canonical_answer": "¿Cuánto cuesta esta fruta?",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_33_1", "text": "¿Cuánto cuesta esta fruta?"},
                                            {"id": "mc_33_2", "text": "¿Dónde compras el pan?"},
                                            {"id": "mc_33_3", "text": "¿Tienes dinero hoy?"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I want to buy fresh apples'",
                                    "prompt_translation": "I want to buy fresh apples",
                                    "canonical_answer": "Quiero comprar manzanas frescas",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_33_1", "text": "Quiero"},
                                            {"id": "wb_33_2", "text": "comprar"},
                                            {"id": "wb_33_3", "text": "manzanas"},
                                            {"id": "wb_33_4", "text": "frescas"},
                                            {"id": "wb_33_5", "text": "leche"}
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
                                            {"id": "mp_33_1", "left": "Comprar", "right": "To buy"},
                                            {"id": "mp_33_2", "left": "Precio", "right": "Price"},
                                            {"id": "mp_33_3", "left": "Mercado", "right": "Market"},
                                            {"id": "mp_33_4", "left": "Dinero", "right": "Money"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "¿Cuánto ___ este pan caliente?",
                                    "prompt_translation": "How much does this warm bread cost?",
                                    "canonical_answer": "cuesta",
                                    "payload_json": json.dumps({
                                        "template": "¿Cuánto ___ este pan caliente?",
                                        "options": [
                                            {"id": "fb_33_1", "text": "cuesta"},
                                            {"id": "fb_33_2", "text": "es"},
                                            {"id": "fb_33_3", "text": "tiene"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'How much does it cost?' in Spanish",
                                    "prompt_translation": "How much does it cost?",
                                    "canonical_answer": "¿Cuánto cuesta?",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "¿Cuánto cuesta?",
                                            "Cuánto cuesta?",
                                            "Cuanto cuesta?",
                                            "cuanto cuesta",
                                            "cuánto cuesta"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 3,
                            "title": "Lesson 3: Talking about Time",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'What time is it now?'",
                                    "prompt_translation": "What time is it now?",
                                    "canonical_answer": "¿Qué hora es ahora?",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_34_1", "text": "¿Qué hora es ahora?"},
                                            {"id": "mc_34_2", "text": "¿Dónde es la fiesta?"},
                                            {"id": "mc_34_3", "text": "¿Cuándo vienes tú?"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'It is three in the afternoon'",
                                    "prompt_translation": "It is three in the afternoon",
                                    "canonical_answer": "Son las tres de la tarde",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_34_1", "text": "Son"},
                                            {"id": "wb_34_2", "text": "las"},
                                            {"id": "wb_34_3", "text": "tres"},
                                            {"id": "wb_34_4", "text": "de la"},
                                            {"id": "wb_34_5", "text": "tarde"}
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
                                            {"id": "mp_34_1", "left": "Hora", "right": "Hour"},
                                            {"id": "mp_34_2", "left": "Minuto", "right": "Minute"},
                                            {"id": "mp_34_3", "left": "Tarde", "right": "Afternoon"},
                                            {"id": "mp_34_4", "left": "Noche", "right": "Night"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Es la una en ___.",
                                    "prompt_translation": "It is exactly one o'clock.",
                                    "canonical_answer": "punto",
                                    "payload_json": json.dumps({
                                        "template": "Es la una en ___.",
                                        "options": [
                                            {"id": "fb_34_1", "text": "punto"},
                                            {"id": "fb_34_2", "text": "casa"},
                                            {"id": "fb_34_3", "text": "mesa"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'It is five o clock' in Spanish",
                                    "prompt_translation": "It is five o clock",
                                    "canonical_answer": "Son las cinco",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Son las cinco",
                                            "son las cinco"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 4,
                            "title": "Lesson 4: Weekend Plans",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'We go to the movies this weekend'",
                                    "prompt_translation": "We go to the movies this weekend",
                                    "canonical_answer": "Vamos al cine este fin de semana",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_35_1", "text": "Vamos al cine este fin de semana"},
                                            {"id": "mc_35_2", "text": "Descansamos en casa el domingo"},
                                            {"id": "mc_35_3", "text": "Salimos de viaje mañana"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'I want to relax on Saturday'",
                                    "prompt_translation": "I want to relax on Saturday",
                                    "canonical_answer": "Quiero descansar el sábado",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_35_1", "text": "Quiero"},
                                            {"id": "wb_35_2", "text": "descansar"},
                                            {"id": "wb_35_3", "text": "el"},
                                            {"id": "wb_35_4", "text": "sábado"},
                                            {"id": "wb_35_5", "text": "domingo"}
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
                                            {"id": "mp_35_1", "left": "Sábado", "right": "Saturday"},
                                            {"id": "mp_35_2", "left": "Domingo", "right": "Sunday"},
                                            {"id": "mp_35_3", "left": "Cine", "right": "Cinema"},
                                            {"id": "mp_35_4", "left": "Fiesta", "right": "Party"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Buen fin de ___ a todos.",
                                    "prompt_translation": "Have a good weekend everyone.",
                                    "canonical_answer": "semana",
                                    "payload_json": json.dumps({
                                        "template": "Buen fin de ___ a todos.",
                                        "options": [
                                            {"id": "fb_35_1", "text": "semana"},
                                            {"id": "fb_35_2", "text": "año"},
                                            {"id": "fb_35_3", "text": "mes"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'Have a good weekend' in Spanish",
                                    "prompt_translation": "Have a good weekend",
                                    "canonical_answer": "Buen fin de semana",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Buen fin de semana",
                                            "buen fin de semana"
                                        ]
                                    })
                                }
                            ]
                        },
                        {
                            "order_index": 5,
                            "title": "Lesson 5: Making Appointments",
                            "xp_reward": 15,
                            "exercises": [
                                {
                                    "order_index": 1,
                                    "exercise_type": "multiple_choice",
                                    "prompt": "Select: 'I have an appointment at four'",
                                    "prompt_translation": "I have an appointment at four",
                                    "canonical_answer": "Tengo una cita a las cuatro",
                                    "payload_json": json.dumps({
                                        "options": [
                                            {"id": "mc_36_1", "text": "Tengo una cita a las cuatro"},
                                            {"id": "mc_36_2", "text": "Voy al trabajo temprano"},
                                            {"id": "mc_36_3", "text": "Hablo con el doctor ahora"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 2,
                                    "exercise_type": "word_bank",
                                    "prompt": "Translate: 'Is the doctor available today?'",
                                    "prompt_translation": "Is the doctor available today?",
                                    "canonical_answer": "¿Está disponible el doctor hoy?",
                                    "payload_json": json.dumps({
                                        "tokens": [
                                            {"id": "wb_36_1", "text": "¿Está"},
                                            {"id": "wb_36_2", "text": "disponible"},
                                            {"id": "wb_36_3", "text": "el"},
                                            {"id": "wb_36_4", "text": "doctor"},
                                            {"id": "wb_36_5", "text": "hoy?"}
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
                                            {"id": "mp_36_1", "left": "Cita", "right": "Appointment"},
                                            {"id": "mp_36_2", "left": "Doctor", "right": "Doctor"},
                                            {"id": "mp_36_3", "left": "Disponible", "right": "Available"},
                                            {"id": "mp_36_4", "left": "Confirmar", "right": "Confirm"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 4,
                                    "exercise_type": "fill_blank",
                                    "prompt": "Deseo confirmar mi ___ médica.",
                                    "prompt_translation": "I wish to confirm my medical appointment.",
                                    "canonical_answer": "cita",
                                    "payload_json": json.dumps({
                                        "template": "Deseo confirmar mi ___ médica.",
                                        "options": [
                                            {"id": "fb_36_1", "text": "cita"},
                                            {"id": "fb_36_2", "text": "casa"},
                                            {"id": "fb_36_3", "text": "mesa"}
                                        ]
                                    })
                                },
                                {
                                    "order_index": 5,
                                    "exercise_type": "type_answer",
                                    "prompt": "Type 'I have an appointment' in Spanish",
                                    "prompt_translation": "I have an appointment",
                                    "canonical_answer": "Tengo una cita",
                                    "payload_json": json.dumps({
                                        "accepted_answers": [
                                            "Tengo una cita",
                                            "tengo una cita"
                                        ]
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
        "title": "First Step",
        "description": "Complete your very first Spanish lesson!",
        "icon_name": "zap"
    },
    {
        "code": "streak_3",
        "title": "On Fire",
        "description": "Reach an impressive 3-day learning streak!",
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
