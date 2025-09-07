from django.core.management.base import BaseCommand
from english.models import Category, Lesson

# Lesson 1 JSON (American usage) + content v2 "sections" at TOP LEVEL.
L1 = {
  "category_slug": "around-the-house",
  "unit_number": 1,
  "lesson_number": 1,
  "title": "Rooms & Objects",
  "level": "A1",

  # ───────────────── content v2 (drives the new paged UI) ─────────────────
  "sections": [
    {
      "type": "overview",
      "id": "ov",
      # Keep simple HTML; UI renders via dangerouslySetInnerHTML
      "body_md": "<p>În lecția aceasta înveți cuvinte despre camere și obiecte din casă, apoi regula scurtă <em>There is / There are</em> și propoziții simple.</p>",
      "narration_ro": "Astăzi înveți cuvinte despre camere și obiecte din casă, apoi exersezi propoziții cu There is / There are."
    },
    {
      "type": "teach",
      "id": "teach-1",
      "narration_ro": "Îți arăt cuvântul în engleză. Atinge pentru a vedea traducerea în română și ascultă pronunția.",
      "items": [
        {"front": "room",        "back": "cameră",     "ipa": "/ruːm/"},
        {"front": "living room", "back": "sufragerie", "ipa": "/ˈlɪvɪŋ ˌruːm/"},
        {"front": "kitchen",     "back": "bucătărie",  "ipa": "/ˈkɪtʃən/"},
        {"front": "bathroom",    "back": "baie",       "ipa": "/ˈbæθruːm/"},
        {"front": "bedroom",     "back": "dormitor",   "ipa": "/ˈbedruːm/"},
        {"front": "couch",       "back": "canapea",    "ipa": "/kaʊtʃ/"},
        {"front": "table",       "back": "masă",       "ipa": "/ˈteɪbəl/"},
        {"front": "chair",       "back": "scaun",      "ipa": "/tʃer/"},
        {"front": "bed",         "back": "pat",        "ipa": "/bed/"},
        {"front": "closet",      "back": "dulap",      "ipa": "/ˈklɑːzɪt/"},
        {"front": "shelf",       "back": "raft",       "ipa": "/ʃelf/"},
        {"front": "lamp",        "back": "lampă",      "ipa": "/læmp/"}
      ]
    },
    {
      "type": "grammar",
      "id": "g1",
      "narration_ro": "Folosim There is pentru singular și There are pentru plural. Prepozițiile in, on, under și at arată locul.",
      "points": [
        "There is + singular; There are + plural.",
        "'in' = înăuntru; 'on' = pe o suprafață; 'under' = sub; 'at' = la (un punct/loc).",
        "Întrebări: Is there…? / Are there…? Negativ: There isn’t… / There aren’t…",
        "EN cere adesea ‘there’ (expletiv). RO spune doar ‘este/sunt’: Este o lampă pe masă. → There is a lamp on the table."
      ]
    },
    {
      "type": "patterns",
      "id": "p1",
      "narration_ro": "Ascultă și repetă propozițiile model.",
      "examples": [
        {"en": "There is a lamp on the table.", "ro": "Este o lampă pe masă."},
        {"en": "There are two chairs in the kitchen.", "ro": "Sunt două scaune în bucătărie."},
        {"en": "The cat is under the bed.", "ro": "Pisica e sub pat."},
        {"en": "We sit on the couch in the living room.", "ro": "Stăm pe canapea în sufragerie."}
      ]
    },
    {
      "type": "build",
      "id": "b1",
      "narration_ro": "Construiește propoziția din bucăți.",
      "tasks": [
        {"tokens": ["There","is","a","lamp","on","the","table","."], "answer": "There is a lamp on the table."},
        {"tokens": ["There","are","two","chairs","in","the","kitchen","."], "answer": "There are two chairs in the kitchen."},
        {"tokens": ["The","cat","is","under","the","bed","."], "answer": "The cat is under the bed."}
      ]
    },
    {
      "type": "listen",
      "id": "l1",
      "narration_ro": "Ascultă și alege varianta corectă.",
      "tasks": [
        {
          "options": ["There is a couch in the living room.", "There are a couch in the living room."],
          "correct_index": 0,
          "prompt_ro": "Alege propoziția corectă."
        },
        {
          "options": ["The keys are on the shelf.", "The keys are in the shelf."],
          "correct_index": 0,
          "prompt_ro": "Alege prepoziția corectă."
        }
      ]
    },
    {
      "type": "dictation",
      "id": "d1",
      "narration_ro": "Ascultă și tastează propoziția.",
      "tasks": [
        # Keep only words/structures covered or extremely transparent:
        {"answer": "There is a lamp on the table."},
        {"answer": "There are two chairs in the kitchen."}
      ]
    },
    { "type": "review", "id": "rev", "narration_ro": "Ai terminat lecția. Poți trece la testul scurt." }
  ],

  # ────────── legacy fields (kept for analytics/quiz/back-compat) ──────────
  "targets": [
    {"en":"room","ro":"cameră","pos":"noun","ipa":"/ruːm/","chunks":["in my room","a small room"],"example_en":"My room is warm.","example_ro":"Camera mea e caldă.","pron_tip":"Long /uː/, not 'rum'."},
    {"en":"living room","ro":"sufragerie","pos":"noun","ipa":"/ˈlɪvɪŋ ˌruːm/","chunks":["in the living room","living room couch"],"example_en":"We relax in the living room.","example_ro":"Ne relaxăm în sufragerie.","pron_tip":"Stress LIV-ing."},
    {"en":"kitchen","ro":"bucătărie","pos":"noun","ipa":"/ˈkɪtʃən/","chunks":["in the kitchen","kitchen table"],"example_en":"I’m in the kitchen.","example_ro":"Sunt în bucătărie.","pron_tip":"/tʃ/ ca în «cină»."},
    {"en":"bathroom","ro":"baie","pos":"noun","ipa":"/ˈbæθruːm/","chunks":["in the bathroom","bathroom sink"],"example_en":"The bathroom is clean.","example_ro":"Baia este curată.","pron_tip":"Subțire «th» /θ/, nu «t»."},
    {"en":"bedroom","ro":"dormitor","pos":"noun","ipa":"/ˈbedruːm/","chunks":["in the bedroom","bedroom window"],"example_en":"The bedroom is quiet.","example_ro":"Dormitorul e liniștit.","pron_tip":"Spune clar «bed» + «room»."},
    {"en":"couch","ro":"canapea","pos":"noun","ipa":"/kaʊtʃ/","chunks":["on the couch","couch cushions"],"example_en":"Sit on the couch.","example_ro":"Stai pe canapea.","pron_tip":"Folosește «on» (pe) cu suprafețe."},
    {"en":"table","ro":"masă","pos":"noun","ipa":"/ˈteɪbəl/","chunks":["on the table","kitchen table"],"example_en":"The keys are on the table.","example_ro":"Cheile sunt pe masă.","pron_tip":"«on» = pe (suprafață)."},
    {"en":"chair","ro":"scaun","pos":"noun","ipa":"/tʃer/","chunks":["a chair","four chairs"],"example_en":"There are four chairs.","example_ro":"Sunt patru scaune.","pron_tip":"ch = /tʃ/."},
    {"en":"bed","ro":"pat","pos":"noun","ipa":"/bed/","chunks":["go to bed","under the bed"],"example_en":"The cat is under the bed.","example_ro":"Pisica e sub pat.","pron_tip":"Folosește «under» pentru «sub»."},
    {"en":"closet","ro":"dulap","pos":"noun","ipa":"/ˈklɑːzɪt/","chunks":["in the closet","a big closet"],"example_en":"Coats are in the closet.","example_ro":"Paltoanele sunt în dulap.","pron_tip":"American: «closet» (nu «wardrobe»)."},
    {"en":"shelf","ro":"raft","pos":"noun","ipa":"/ʃelf/","chunks":["on the shelf","top shelf"],"example_en":"Put the book on the shelf.","example_ro":"Pune cartea pe raft.","pron_tip":"sh = /ʃ/ (ca «ș»)."},
    {"en":"lamp","ro":"lampă","pos":"noun","ipa":"/læmp/","chunks":["a desk lamp","turn on the lamp"],"example_en":"Turn on the lamp.","example_ro":"Pornește lampa.","pron_tip":"/æ/ scurt, ca în «cat»."}
  ],

  "examples": [
    {"en":"There is a lamp on the table.","ro":"Este o lampă pe masă.","notes":["chunk: on the table"]},
    {"en":"There are two chairs in the kitchen.","ro":"Sunt două scaune în bucătărie.","notes":["chunk: in the kitchen"]},
    {"en":"The keys are on the shelf.","ro":"Cheile sunt pe raft.","notes":["chunk: on the shelf"]},
    {"en":"The cat is under the bed.","ro":"Pisica e sub pat.","notes":["chunk: under the bed"]},
    {"en":"We watch TV in the living room.","ro":"Ne uităm la TV în sufragerie.","notes":["chunk: in the living room"]},
    {"en":"Coats are in the closet.","ro":"Paltoanele sunt în dulap.","notes":["chunk: in the closet"]},
    {"en":"I’m at home now.","ro":"Sunt acasă acum.","notes":["chunk: at home"]}
  ],

  "dialogues": [
    {
      "title":"Looking for the keys",
      "turns":[
        {"en":"Where are my keys?","ro":"Unde sunt cheile mele?"},
        {"en":"They’re on the table, in the kitchen.","ro":"Sunt pe masă, în bucătărie."},
        {"en":"No, I don’t see them.","ro":"Nu, nu le văd."},
        {"en":"Check the shelf near the door.","ro":"Verifică raftul de lângă ușă."},
        {"en":"Got them! Thanks.","ro":"Le-am găsit! Mulțumesc."}
      ]
    },
    {
      "title":"Showing the room",
      "turns":[
        {"en":"This is the bedroom.","ro":"Acesta e dormitorul."},
        {"en":"Nice! There’s a big closet.","ro":"Frumos! Este un dulap mare."},
        {"en":"Yes, and the bed is very comfortable.","ro":"Da, și patul e foarte confortabil."},
        {"en":"Where’s the lamp?","ro":"Unde e lampa?"},
        {"en":"On the nightstand.","ro":"Pe noptieră."}
      ]
    }
  ],

  "micro_grammar": {
    "topic":"There is / There are + prepositions of place",
    "points":[
      "Use 'There is' for singular; 'There are' for plural.",
      "RO spune adesea doar «este/sunt»; EN cere «there».",
      "'in' = inside; 'on' = on a surface; 'under' = beneath; 'at' = point/place.",
      "Negatives/questions: 'There isn’t…' / 'Is there…?' / 'Are there…?'"
    ],
    "mini_examples":[
      {"en":"There is a chair in the room.","ro":"Este un scaun în cameră."},
      {"en":"There are books on the shelf.","ro":"Sunt cărți pe raft."}
    ],
    "common_errors":[
      {"bad":"Is a lamp on the table.","good":"There is a lamp on the table."},
      {"bad":"I’m in home.","good":"I’m at home."}
    ]
  },

  "quiz": {
    "items": [
      {"type":"translate_ro_en","prompt_ro":"Sunt două scaune în bucătărie.","answer_en":"There are two chairs in the kitchen.","accept":["There are 2 chairs in the kitchen."]},
      {"type":"translate_en_ro","prompt_en":"There is a lamp on the table.","answer_ro":"Este o lampă pe masă."},
      {"type":"fill_blank","prompt_en":"___ is a couch in the living room.","options":["There","It","This"],"correct":"There","explain":"English uses 'there' as an expletive subject."},
      {"type":"fill_blank","prompt_en":"The cat is ___ the bed.","options":["under","on","at"],"correct":"under","explain":"'under' = sub."},
      {"type":"choose","prompt_en":"Choose the correct preposition: The keys are ___ the shelf.","options":["in","on","at"],"correct":"on"},
      {"type":"translate_ro_en","prompt_ro":"Patul este în dormitor.","answer_en":"The bed is in the bedroom.","accept":[]},
      {"type":"translate_en_ro","prompt_en":"We relax in the living room.","answer_ro":"Ne relaxăm în sufragerie."},
      {"type":"fill_blank","prompt_en":"There ___ a big closet.","options":["is","are"],"correct":"is"},
      {"type":"fill_blank","prompt_en":"There ___ four chairs.","options":["is","are"],"correct":"are"},
      {"type":"word_order","prompt_en":"Reorder to make a question: there / a lamp / is / on the table / ?","answer_en":"Is there a lamp on the table?","tokens":["Is","there","a","lamp","on","the","table","?"]},
      {"type":"translate_ro_en","prompt_ro":"Cheile sunt pe masă.","answer_en":"The keys are on the table.","accept":[]},
      {"type":"translate_en_ro","prompt_en":"Turn on the lamp.","answer_ro":"Pornește lampa."},
      {"type":"choose","prompt_en":"Pick the natural sentence.","options":["Is a couch in the living room.","There is a couch in the living room.","There are a couch in the living room."],"correct":"There is a couch in the living room."},
      {"type":"fill_blank","prompt_en":"I’m ___ home now.","options":["at","in","on"],"correct":"at","explain":"Use 'at home', not 'in home'."},
      {"type":"translate_ro_en","prompt_ro":"Pune cartea pe raft.","answer_en":"Put the book on the shelf.","accept":[]},
      {"type":"dialogue_reply","prompt_en":"Where are my keys?","options":["They’re on the table, in the kitchen.","There is a lamp on the table.","It’s a bedroom."],"correct":"They’re on the table, in the kitchen."},
      {"type":"fill_blank","prompt_en":"The coats are ___ the closet.","options":["in","on","under"],"correct":"in"},
      # Removed the bookshelf/bibliotecă pitfall to avoid wrong preposition mapping in RO
      {"type":"translate_ro_en","prompt_ro":"Stăm pe canapea.","answer_en":"We sit on the couch.","accept":["We're sitting on the couch."]},
      {"type":"choose","prompt_en":"Best option: The bedroom is very ___.","options":["quiet","under","on"],"correct":"quiet"},
      {"type":"translate_ro_en","prompt_ro":"Chiuveta este în baie.","answer_en":"The sink is in the bathroom.","accept":[]},
      {"type":"translate_ro_en","prompt_ro":"Coșul de gunoi este în bucătărie.","answer_en":"The trash can is in the kitchen.","accept":["The garbage can is in the kitchen."]},
      {"type":"fill_blank","prompt_en":"Turn ___ the lamp.","options":["on","in","at"],"correct":"on"},
      {"type":"word_order","prompt_en":"Reorder: on / the / couch / we / sit / .","answer_en":"We sit on the couch.","tokens":["We","sit","on","the","couch","."]},
      {"type":"translate_en_ro","prompt_en":"Open the closet.","answer_ro":"Deschide dulapul."}
    ]
  },

  "spaced_review_tags": [
    {"en": "table", "review_after_days": 2},
    {"en": "chair", "review_after_days": 3},
    {"en": "lamp", "review_after_days": 4},
    {"en": "couch", "review_after_days": 5},
    {"en": "closet", "review_after_days": 6}
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
