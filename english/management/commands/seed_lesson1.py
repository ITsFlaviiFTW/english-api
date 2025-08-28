from django.core.management.base import BaseCommand
from english.models import Category, Lesson

# JSON data for Lesson 1
L1 = {
  "category_slug": "around-the-house",
  "unit_number": 1,
  "lesson_number": 1,
  "title": "Rooms & Objects",
  "level": "A1",
  "targets": [
    {
      "en": "room",
      "ro": "cameră",
      "pos": "noun",
      "ipa": "/ruːm/",
      "chunks": ["in my room", "a small room"],
      "example_en": "My room is warm.",
      "example_ro": "Camera mea e călduroasă.",
      "pron_tip": "Long /uː/, not 'rum'."
    },
    {
      "en": "living room",
      "ro": "sufragerie",
      "pos": "noun",
      "ipa": "/ˈlɪv.ɪŋ ˌruːm/",
      "chunks": ["in the living room", "living room sofa"],
      "example_en": "We relax in the living room.",
      "example_ro": "Ne relaxăm în sufragerie.",
      "pron_tip": "Stress LIV-ing."
    },
    {
      "en": "kitchen",
      "ro": "bucătărie",
      "pos": "noun",
      "ipa": "/ˈkɪtʃ.ən/",
      "chunks": ["in the kitchen", "kitchen table"],
      "example_en": "I’m in the kitchen.",
      "example_ro": "Sunt în bucătărie.",
      "pron_tip": "/tʃ/ like 'ci' in 'cină'."
    },
    {
      "en": "bathroom",
      "ro": "baie",
      "pos": "noun",
      "ipa": "/ˈbæθ.ruːm/",
      "chunks": ["in the bathroom", "bathroom sink"],
      "example_en": "The bathroom is clean.",
      "example_ro": "Baia este curată.",
      "pron_tip": "Thin 'th' /θ/, not 't'."
    },
    {
      "en": "bedroom",
      "ro": "dormitor",
      "pos": "noun",
      "ipa": "/ˈbed.ruːm/",
      "chunks": ["in the bedroom", "bedroom window"],
      "example_en": "The bedroom is quiet.",
      "example_ro": "Dormitorul e liniștit.",
      "pron_tip": "Say 'bed' + 'room' clearly."
    },
    {
      "en": "sofa",
      "ro": "canapea",
      "pos": "noun",
      "ipa": "/ˈsoʊ.fə/",
      "chunks": ["on the sofa", "sofa cushions"],
      "example_en": "Sit on the sofa.",
      "example_ro": "Stai pe canapea.",
      "pron_tip": "Use 'on' the sofa (pe)."
    },
    {
      "en": "table",
      "ro": "masă",
      "pos": "noun",
      "ipa": "/ˈteɪ.bəl/",
      "chunks": ["on the table", "kitchen table"],
      "example_en": "The keys are on the table.",
      "example_ro": "Cheile sunt pe masă.",
      "pron_tip": "'on' = pe (surface)."
    },
    {
      "en": "chair",
      "ro": "scaun",
      "pos": "noun",
      "ipa": "/tʃer/",
      "chunks": ["a chair", "four chairs"],
      "example_en": "There are four chairs.",
      "example_ro": "Sunt patru scaune.",
      "pron_tip": "ch=/tʃ/, not 'ș'."
    },
    {
      "en": "bed",
      "ro": "pat",
      "pos": "noun",
      "ipa": "/bed/",
      "chunks": ["go to bed", "under the bed"],
      "example_en": "The cat is under the bed.",
      "example_ro": "Pisica e sub pat.",
      "pron_tip": "Use 'under', not 'down the bed'."
    },
    {
      "en": "wardrobe",
      "ro": "dulap",
      "pos": "noun",
      "ipa": "/ˈwɔːr.droʊb/",
      "chunks": ["in the wardrobe", "a big wardrobe"],
      "example_en": "Coats are in the wardrobe.",
      "example_ro": "Paltoanele sunt în dulap.",
      "pron_tip": "Say 'war-drobe'."
    },
    {
      "en": "shelf",
      "ro": "raft",
      "pos": "noun",
      "ipa": "/ʃelf/",
      "chunks": ["on the shelf", "book shelf"],
      "example_en": "Put the book on the shelf.",
      "example_ro": "Pune cartea pe raft.",
      "pron_tip": "sh=/ʃ/ (like 'ș')."
    },
    {
      "en": "lamp",
      "ro": "lampă",
      "pos": "noun",
      "ipa": "/læmp/",
      "chunks": ["a desk lamp", "turn on the lamp"],
      "example_en": "Turn on the lamp.",
      "example_ro": "Pornește lampa.",
      "pron_tip": "Short /æ/ as in 'cat'."
    }
  ],
  "examples": [
    {
      "en": "There is a lamp on the table.",
      "ro": "Este o lampă pe masă.",
      "notes": ["chunk: on the table"]
    },
    {
      "en": "There are two chairs in the kitchen.",
      "ro": "Sunt două scaune în bucătărie.",
      "notes": ["chunk: in the kitchen"]
    },
    {
      "en": "The keys are on the shelf.",
      "ro": "Cheile sunt pe raft.",
      "notes": ["chunk: on the shelf"]
    },
    {
      "en": "The cat is under the bed.",
      "ro": "Pisica e sub pat.",
      "notes": ["chunk: under the bed"]
    },
    {
      "en": "We watch TV in the living room.",
      "ro": "Ne uităm la TV în sufragerie.",
      "notes": ["chunk: in the living room"]
    },
    {
      "en": "I’m at home now.",
      "ro": "Sunt acasă acum.",
      "notes": ["chunk: at home"]
    }
  ],
  "dialogues": [
    {
      "title": "Looking for the keys",
      "turns": [
        {"en": "Where are my keys?", "ro": "Unde sunt cheile mele?"},
        {"en": "They’re on the table, in the kitchen.", "ro": "Sunt pe masă, în bucătărie."},
        {"en": "No, I don’t see them.", "ro": "Nu, nu le văd."},
        {"en": "Check the shelf near the door.", "ro": "Verifică raftul de lângă ușă."},
        {"en": "Got them! Thanks.", "ro": "Le-am găsit! Mulțumesc."}
      ]
    },
    {
      "title": "Showing the room",
      "turns": [
        {"en": "This is the bedroom.", "ro": "Acesta e dormitorul."},
        {"en": "Nice! There’s a big wardrobe.", "ro": "Frumos! Este un dulap mare."},
        {"en": "Yes, and the bed is very comfortable.", "ro": "Da, și patul e foarte confortabil."},
        {"en": "Where’s the lamp?", "ro": "Unde e lampa?"},
        {"en": "On the bedside table.", "ro": "Pe noptieră."}
      ]
    }
  ],
  "micro_grammar": {
    "topic": "There is / There are + prepositions of place",
    "points": [
      "Use 'There is' for singular; 'There are' for plural.",
      "RO often uses 'este/sunt' without an expletive; EN needs 'there'.",
      "'in' = inside; 'on' = on a surface; 'under' = beneath; 'at' = point/place.",
      "Negatives/questions: 'There isn’t…' / 'Is there…?'",
      "Common RO error: missing 'there'."
    ],
    "mini_examples": [
      {"en": "There is a chair in the room.", "ro": "Este un scaun în cameră."},
      {"en": "There are books on the shelf.", "ro": "Sunt cărți pe raft."}
    ],
    "common_errors": [
      {"bad": "Is a lamp on the table.", "good": "There is a lamp on the table."},
      {"bad": "I’m in home.", "good": "I’m at home."}
    ]
  },
  "quiz": {
    "items": [
      {
        "type": "translate_ro_en",
        "prompt_ro": "Sunt două scaune în bucătărie.",
        "answer_en": "There are two chairs in the kitchen.",
        "accept": ["There are 2 chairs in the kitchen."]
      },
      {
        "type": "translate_en_ro",
        "prompt_en": "There is a lamp on the table.",
        "answer_ro": "Este o lampă pe masă."
      },
      {
        "type": "fill_blank",
        "prompt_en": "___ is a sofa in the living room.",
        "options": ["There", "It", "This"],
        "correct": "There",
        "explain": "English uses 'there' as an expletive subject."
      },
      {
        "type": "fill_blank",
        "prompt_en": "The cat is ___ the bed.",
        "options": ["under", "on", "at"],
        "correct": "under",
        "explain": "'under' = sub."
      },
      {
        "type": "choose",
        "prompt_en": "Choose the correct preposition: The keys are ___ the shelf.",
        "options": ["in", "on", "at"],
        "correct": "on"
      },
      {
        "type": "translate_ro_en",
        "prompt_ro": "Patul este în dormitor.",
        "answer_en": "The bed is in the bedroom.",
        "accept": []
      },
      {
        "type": "translate_en_ro",
        "prompt_en": "We relax in the living room.",
        "answer_ro": "Ne relaxăm în sufragerie."
      },
      {
        "type": "fill_blank",
        "prompt_en": "There ___ a big wardrobe.",
        "options": ["is", "are"],
        "correct": "is"
      },
      {
        "type": "fill_blank",
        "prompt_en": "There ___ four chairs.",
        "options": ["is", "are"],
        "correct": "are"
      },
      {
        "type": "word_order",
        "prompt_en": "Reorder to make a question: there / a lamp / is / on the table / ?",
        "answer_en": "Is there a lamp on the table?",
        "tokens": ["Is", "there", "a", "lamp", "on", "the", "table", "?"]
      },
      {
        "type": "translate_ro_en",
        "prompt_ro": "Cheile sunt pe masă.",
        "answer_en": "The keys are on the table.",
        "accept": []
      },
      {
        "type": "translate_en_ro",
        "prompt_en": "Turn on the lamp.",
        "answer_ro": "Pornește lampa."
      },
      {
        "type": "choose",
        "prompt_en": "Pick the natural sentence.",
        "options": [
          "Is a sofa in the living room.",
          "There is a sofa in the living room.",
          "There are a sofa in the living room."
        ],
        "correct": "There is a sofa in the living room."
      },
      {
        "type": "fill_blank",
        "prompt_en": "I’m ___ home now.",
        "options": ["at", "in", "on"],
        "correct": "at",
        "explain": "Use 'at home', not 'in home'."
      },
      {
        "type": "translate_ro_en",
        "prompt_ro": "Pune cartea pe raft.",
        "answer_en": "Put the book on the shelf.",
        "accept": []
      },
      {
        "type": "dialogue_reply",
        "prompt_en": "Where are my keys?",
        "options": [
          "They’re on the table, in the kitchen.",
          "There is a lamp on the table.",
          "It’s a bedroom."
        ],
        "correct": "They’re on the table, in the kitchen."
      },
      {
        "type": "fill_blank",
        "prompt_en": "The coats are ___ the wardrobe.",
        "options": ["in", "on", "under"],
        "correct": "in"
      },
      {
        "type": "translate_en_ro",
        "prompt_en": "There are books on the shelf.",
        "answer_ro": "Sunt cărți pe raft."
      },
      {
        "type": "translate_ro_en",
        "prompt_ro": "Stăm pe canapea.",
        "answer_en": "We sit on the sofa.",
        "accept": ["We’re sitting on the sofa."]
      },
      {
        "type": "choose",
        "prompt_en": "Best option: The bedroom is very ___.",
        "options": ["quiet", "under", "on"],
        "correct": "quiet"
      }
    ]
  },
  "spaced_review_tags": [
    {"en": "table", "review_after_days": 2},
    {"en": "chair", "review_after_days": 3},
    {"en": "lamp", "review_after_days": 4}
  ]
}


class Command(BaseCommand):
    help = "Seed Around the House → Unit 1 → Lesson 1"

    def handle(self, *args, **kwargs):
        cat, _ = Category.objects.get_or_create(
            slug="around-the-house",
            defaults=dict(
                title="Around the House",
                description="Rooms & objects at home",
                emoji="🏠",
            ),
        )
        word_count = len(L1.get("targets") or [])
        lesson, created = Lesson.objects.get_or_create(
            category=cat,
            title=L1.get("title", "Rooms & Objects"),
            defaults=dict(
                difficulty=L1.get("level", "A1"),
                word_count=word_count,
                content=L1,
            ),
        )
        if not created:
            lesson.content = L1
            lesson.word_count = word_count
            lesson.difficulty = L1.get("level", "A1")
            lesson.save()
        self.stdout.write(self.style.SUCCESS(f"Seeded: {lesson.title} in {cat.title}"))
