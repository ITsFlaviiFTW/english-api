from django.core.management.base import BaseCommand
from english.models import Category, Lesson

L3 = {
  "category_slug": "around-the-house",
  "unit_number": 1,
  "lesson_number": 3,
  "title": "This / That / These / Those",
  "level": "A1",

  "sections": [
    {
      "type":"overview",
      "id":"ov",
      "body_md":"<p>Deosebești <em>this/that/these/those</em> și consolidezi <em>Is there…?/Are there…?</em> cu răspunsuri scurte și forme prescurtate <em>There’s / There’re</em>.</p>",
      "narration_ro":"Învățăm this/that/these/those (aproape/departe; singular/plural) și repetăm întrebările Is there…?/Are there…?"
    },
    {
      "type":"teach",
      "id":"teach-1",
      "narration_ro":"Cuvinte utile pentru poziție și indicare.",
      "items":[
        {"front":"this","back":"acesta/aceasta (aproape, sg.)","ipa":"/ðɪs/"},
        {"front":"that","back":"acela/aceea (departe, sg.)","ipa":"/ðæt/"},
        {"front":"these","back":"aceștia/acestea (aproape, pl.)","ipa":"/ðiz/"},
        {"front":"those","back":"aceia/acelea (departe, pl.)","ipa":"/ðoʊz/"},
        {"front":"here","back":"aici","ipa":"/hɪr/"},
        {"front":"there","back":"acolo","ipa":"/ðer/"},
        {"front":"near","back":"aproape","ipa":"/nɪr/"},
        {"front":"far","back":"departe","ipa":"/fɑr/"},
        {"front":"left","back":"stânga","ipa":"/lɛft/"},
        {"front":"right","back":"dreapta","ipa":"/raɪt/"},
        {"front":"corner","back":"colț","ipa":"/ˈkɔrnər/"},
        {"front":"center","back":"centru","ipa":"/ˈsɛntər/"}
      ]
    },
    {
      "type":"grammar",
      "id":"g1",
      "narration_ro":"Demonstra­tive + întrebări cu there is/are.",
      "points":[
        "this/that = singular (aproape/departe); these/those = plural (aproape/departe).",
        "There’s = There is; There’re = There are (prescurtări uzuale).",
        "Întrebări: Is there a…? / Are there any…? Răspuns scurt: Yes, there is/are. No, there isn’t/aren’t."
      ]
    },
    {
      "type":"patterns",
      "id":"p1",
      "narration_ro":"Spune și repetă modelele.",
      "examples":[
        {"en":"This plant is near the window.","ro":"Planta aceasta este lângă fereastră."},
        {"en":"Those pictures are on the right wall.","ro":"Acele tablouri sunt pe peretele din dreapta."},
        {"en":"Is there a mirror here? — Yes, there is.","ro":"Este o oglindă aici? — Da, este."},
        {"en":"Are there any chairs in the corner? — No, there aren’t.","ro":"Sunt scaune în colț? — Nu, nu sunt."}
      ]
    },
    {
      "type":"build",
      "id":"b1",
      "narration_ro":"Construiește propoziția corectă.",
      "tasks":[
        {"tokens":["This","picture","is","on","the","left","."],"answer":"This picture is on the left."},
        {"tokens":["Those","plants","are","near","the","door","."],"answer":"Those plants are near the door."},
        {"tokens":["Is","there","a","mirror","here","?"],"answer":"Is there a mirror here?"}
      ]
    },
    {
      "type":"listen",
      "id":"l1",
      "narration_ro":"Alege varianta corectă.",
      "tasks":[
        {"options":["These chair is new.","These chairs are new."],"correct_index":1,"prompt_ro":"Alege pluralul corect."},
        {"options":["That pictures are nice.","Those pictures are nice."],"correct_index":1,"prompt_ro":"Alege varianta corectă."}
      ]
    },
    {
      "type":"dictation",
      "id":"d1",
      "narration_ro":"Tastează propoziția auzită.",
      "tasks":[
        {"answer":"There’s a plant near the window."},
        {"answer":"Are there any chairs in the corner?"}
      ]
    },
    {"type":"review","id":"rev","narration_ro":"Super! Treci la test."}
  ],

  "targets":[
    {"en":"this","ro":"acesta/aceasta","pos":"det/pron","ipa":"/ðɪs/","chunks":["this room","this chair"],"example_en":"This chair is comfortable.","example_ro":"Acest scaun este confortabil."},
    {"en":"that","ro":"acela/aceea","pos":"det/pron","ipa":"/ðæt/","chunks":["that room","that lamp"],"example_en":"That lamp is very bright.","example_ro":"Acea lampă este foarte puternică."},
    {"en":"these","ro":"aceștia/acestea","pos":"det/pron","ipa":"/ðiz/","chunks":["these chairs","these pictures"],"example_en":"These chairs are new.","example_ro":"Aceste scaune sunt noi."},
    {"en":"those","ro":"aceia/acelea","pos":"det/pron","ipa":"/ðoʊz/","chunks":["those plants","those shelves"],"example_en":"Those plants are near the door.","example_ro":"Acele plante sunt lângă ușă."},
    {"en":"here","ro":"aici","pos":"adv","ipa":"/hɪr/","chunks":["over here","come here"],"example_en":"The mirror is here.","example_ro":"Oglinda este aici."},
    {"en":"there","ro":"acolo","pos":"adv","ipa":"/ðer/","chunks":["over there","there is/are"],"example_en":"The TV is over there.","example_ro":"Televizorul este acolo."},
    {"en":"near","ro":"aproape/lângă","pos":"prep","ipa":"/nɪr/","chunks":["near the door","near the window"],"example_en":"The couch is near the window.","example_ro":"Canapeaua este lângă fereastră."},
    {"en":"far","ro":"departe","pos":"adv/adj","ipa":"/fɑr/","chunks":["far from","far away"],"example_en":"The bedroom is far from the kitchen.","example_ro":"Dormitorul este departe de bucătărie."},
    {"en":"left","ro":"stânga","pos":"n/adj/adv","ipa":"/lɛft/","chunks":["on the left","left wall"],"example_en":"The picture is on the left.","example_ro":"Tabloul este în stânga."},
    {"en":"right","ro":"dreapta","pos":"n/adj/adv","ipa":"/raɪt/","chunks":["on the right","right wall"],"example_en":"The mirror is on the right.","example_ro":"Oglinda este în dreapta."},
    {"en":"corner","ro":"colț","pos":"noun","ipa":"/ˈkɔrnər/","chunks":["in the corner","corner table"],"example_en":"There is a chair in the corner.","example_ro":"Este un scaun în colț."},
    {"en":"center","ro":"centru","pos":"noun","ipa":"/ˈsɛntər/","chunks":["in the center","center of the room"],"example_en":"The table is in the center.","example_ro":"Masa este în centru."}
  ],

  "examples":[
    {"en":"This plant is near the window.","ro":"Planta aceasta este lângă fereastră."},
    {"en":"Those pictures are on the right wall.","ro":"Acele tablouri sunt pe peretele din dreapta."},
    {"en":"Is there a mirror here?","ro":"Este o oglindă aici?"},
    {"en":"There’s a rug in the center of the room.","ro":"Este un covoraș în centrul camerei."}
  ],

  "dialogues":[
    {
      "title":"Showing the living room",
      "turns":[
        {"en":"This is the living room.","ro":"Aceasta este sufrageria."},
        {"en":"Nice! Are those plants real?","ro":"Frumos! Acele plante sunt reale?"},
        {"en":"Yes, they are. The mirror is over there.","ro":"Da. Oglinda este acolo."},
        {"en":"Great. Is there a rug?","ro":"Super. Este un covoraș?"},
        {"en":"Yes, there’s a rug in the center.","ro":"Da, este un covoraș în centru."}
      ]
    }
  ],

  "micro_grammar":{
    "topic":"This/That/These/Those + There’s/There’re",
    "points":[
      "this/that = singular; these/those = plural (aproape vs departe).",
      "There’s = There is; There’re = There are (prescurtat).",
      "Întrebări: Is there a…? / Are there any…? Răspunsuri: Yes, there is/are. No, there isn’t/aren’t."
    ],
    "mini_examples":[
      {"en":"Is there a plant here? — Yes, there is.","ro":"Este o plantă aici? — Da, este."},
      {"en":"Are there any chairs? — No, there aren’t.","ro":"Sunt scaune? — Nu, nu sunt."}
    ],
    "common_errors":[
      {"bad":"These picture is nice.","good":"This picture is nice."},
      {"bad":"Those chair are new.","good":"Those chairs are new."}
    ]
  },

  "quiz":{
    "items":[
      {"type":"choose","prompt_en":"Pick the correct word: ___ chair (near me).","options":["That","These","This"],"correct":"This"},
      {"type":"choose","prompt_en":"Pick the correct word: ___ plants (far).","options":["Those","This","These"],"correct":"Those"},
      {"type":"fill_blank","prompt_en":"___ a mirror here.","options":["There’s","There are","There’re"],"correct":"There’s"},
      {"type":"fill_blank","prompt_en":"___ any chairs in the corner?","options":["Is there","Are there","There are"],"correct":"Are there"},
      {"type":"translate_ro_en","prompt_ro":"Acele tablouri sunt în dreapta.","answer_en":"Those pictures are on the right.","accept":["Those pictures are on the right wall."]},
      {"type":"translate_en_ro","prompt_en":"There’s a rug in the center.","answer_ro":"Este un covoraș în centru."},
      {"type":"word_order","prompt_en":"Reorder: there / is / a / plant / here / ?","answer_en":"Is there a plant here?","tokens":["Is","there","a","plant","here","?"]},
      {"type":"dialogue_reply","prompt_en":"Are there any chairs?","options":["Yes, there are.","There’s a chair.","This chair."],"correct":"Yes, there are."},
      {"type":"fill_blank","prompt_en":"___ pictures are beautiful (near me).","options":["Those","These","This"],"correct":"These"},
      {"type":"translate_ro_en","prompt_ro":"Acest tablou este în stânga.","answer_en":"This picture is on the left.","accept":[]}
    ]
  },

  "spaced_review_tags":[
    {"en":"these","review_after_days":2},
    {"en":"those","review_after_days":3},
    {"en":"there’s","review_after_days":4}
  ]
}

class Command(BaseCommand):
    help = "Seed Around the House → Unit 1 → Lesson 3"

    def handle(self, *args, **kwargs):
        cat, _ = Category.objects.get_or_create(
            slug="around-the-house",
            defaults=dict(title="Around the House", description="Rooms & objects at home", emoji="🏠"),
        )
        word_count = len(L3.get("targets") or [])
        lesson, created = Lesson.objects.get_or_create(
            category=cat,
            title=L3.get("title","This / That / These / Those"),
            defaults=dict(difficulty=L3.get("level","A1"), word_count=word_count, content=L3),
        )
        if not created:
            lesson.content = L3
            lesson.word_count = word_count
            lesson.difficulty = L3.get("level","A1")
            lesson.save()
        self.stdout.write(self.style.SUCCESS(f"Seeded: {lesson.title} in {cat.title}"))
