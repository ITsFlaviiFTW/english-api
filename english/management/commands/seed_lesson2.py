from django.core.management.base import BaseCommand
from english.models import Category, Lesson

L2 = {
  "category_slug": "around-the-house",
  "unit_number": 1,
  "lesson_number": 2,
  "title": "Articles: a / an / the",
  "level": "A1",

  "sections": [
    {
      "type": "overview",
      "id": "ov",
      "body_md": "<p>Exersezi <em>a/an/the</em> cu obiecte din casă. <em>a / an</em> pentru ceva nespecificat (o/ un), <em>the</em> pentru ceva cunoscut/clar.</p>",
      "narration_ro": "Învățăm a/an/the: a/an pentru ceva general, the pentru ceva anume sau deja cunoscut."
    },
    {
      "type": "teach",
      "id": "teach-1",
      "narration_ro": "Cuvinte noi pentru obiecte din casă.",
      "items": [
        {"front":"window","back":"fereastră","ipa":"/ˈwɪn.doʊ/"},
        {"front":"door","back":"ușă","ipa":"/dɔr/"},
        {"front":"wall","back":"perete","ipa":"/wɔl/"},
        {"front":"floor","back":"pardoseală","ipa":"/flɔr/"},
        {"front":"ceiling","back":"tavan","ipa":"/ˈsiːlɪŋ/"},
        {"front":"rug","back":"covoraș","ipa":"/rʌg/"},
        {"front":"carpet","back":"mochetă / covor","ipa":"/ˈkɑrpət/"},
        {"front":"mirror","back":"oglindă","ipa":"/ˈmɪrər/"},
        {"front":"picture","back":"tablou / poză","ipa":"/ˈpɪk.tʃər/"},
        {"front":"plant","back":"plantă","ipa":"/plænt/"},
        {"front":"TV","back":"televizor","ipa":"/ˌtiːˈviː/"},
        {"front":"remote (control)","back":"telecomandă","ipa":"/rɪˈmoʊt/"}
      ]
    },
    {
      "type": "grammar",
      "id": "g1",
      "narration_ro": "a/an pentru singular nespecificat; the pentru ceva anume.",
      "points": [
        "a + sunet de consoană: a door, a rug, a plant.",
        "an + sunet de vocală: an apple, an umbrella. (după sunet, nu literă!)",
        "the = «acel/acea» specific(ă) sau cunoscut(ă): the door (ușa despre care știm).",
        "Zero articol pentru plural general/obiecte nenumărabile: Doors are open. (uși, în general)."
      ]
    },
    {
      "type": "patterns",
      "id": "p1",
      "narration_ro": "Modele cu articole.",
      "examples": [
        {"en":"There is a picture on the wall.","ro":"Este un tablou pe perete."},
        {"en":"Open the door, please.","ro":"Deschide ușa, te rog."},
        {"en":"She bought a plant for the living room.","ro":"Ea a cumpărat o plantă pentru sufragerie."},
        {"en":"The TV is on the wall.","ro":"Televizorul este pe perete."}
      ]
    },
    {
      "type": "build",
      "id": "b1",
      "narration_ro": "Construiește propoziția corectă cu articolul potrivit.",
      "tasks": [
        {"tokens":["There","is","a","mirror","on","the","wall","."],"answer":"There is a mirror on the wall."},
        {"tokens":["Open","the","window",",","please","."],"answer":"Open the window, please."},
        {"tokens":["She","has","a","rug","on","the","floor","."],"answer":"She has a rug on the floor."}
      ]
    },
    {
      "type": "listen",
      "id": "l1",
      "narration_ro": "Alege propoziția cu articol corect.",
      "tasks": [
        {"options":["There is an TV on the wall.","There is a TV on the wall."],"correct_index":1,"prompt_ro":"Alege varianta corectă."},
        {"options":["He bought an plant.","He bought a plant."],"correct_index":1,"prompt_ro":"Alege varianta corectă."}
      ]
    },
    {
      "type": "dictation",
      "id": "d1",
      "narration_ro": "Tastează propoziția auzită.",
      "tasks": [
        {"answer":"There is a picture on the wall."},
        {"answer":"Open the door, please."}
      ]
    },
    {"type":"review","id":"rev","narration_ro":"Gata! Urmează testul scurt."}
  ],

  "targets": [
    {"en":"window","ro":"fereastră","pos":"noun","ipa":"/ˈwɪn.doʊ/","chunks":["open the window","close the window"],"example_en":"Open the window, please.","example_ro":"Deschide fereastra, te rog."},
    {"en":"door","ro":"ușă","pos":"noun","ipa":"/dɔr/","chunks":["open the door","close the door"],"example_en":"Close the door.","example_ro":"Închide ușa."},
    {"en":"wall","ro":"perete","pos":"noun","ipa":"/wɔl/","chunks":["on the wall","wall picture"],"example_en":"The picture is on the wall.","example_ro":"Tabloul este pe perete."},
    {"en":"floor","ro":"pardoseală","pos":"noun","ipa":"/flɔr/","chunks":["on the floor","clean the floor"],"example_en":"There is a rug on the floor.","example_ro":"Este un covoraș pe podea."},
    {"en":"ceiling","ro":"tavan","pos":"noun","ipa":"/ˈsiːlɪŋ/","chunks":["on the ceiling","high ceiling"],"example_en":"The light is on the ceiling.","example_ro":"Lampa este pe tavan."},
    {"en":"rug","ro":"covoraș","pos":"noun","ipa":"/rʌg/","chunks":["a small rug","on the rug"],"example_en":"She bought a rug.","example_ro":"Ea a cumpărat un covoraș."},
    {"en":"carpet","ro":"mochetă / covor","pos":"noun","ipa":"/ˈkɑrpət/","chunks":["carpet floor","new carpet"],"example_en":"The carpet is new.","example_ro":"Mocheta este nouă."},
    {"en":"mirror","ro":"oglindă","pos":"noun","ipa":"/ˈmɪrər/","chunks":["a big mirror","in the mirror"],"example_en":"There is a mirror in the hallway.","example_ro":"Este o oglindă pe hol."},
    {"en":"picture","ro":"tablou / poză","pos":"noun","ipa":"/ˈpɪk.tʃər/","chunks":["a family picture","hang a picture"],"example_en":"Hang the picture on the wall.","example_ro":"Atârnă tabloul pe perete."},
    {"en":"plant","ro":"plantă","pos":"noun","ipa":"/plænt/","chunks":["a green plant","water the plant"],"example_en":"She waters the plant.","example_ro":"Ea udă planta."},
    {"en":"TV","ro":"televizor","pos":"noun","ipa":"/ˌtiːˈviː/","chunks":["watch TV","turn on the TV"],"example_en":"Turn on the TV.","example_ro":"Pornește televizorul."},
    {"en":"remote","ro":"telecomandă","pos":"noun","ipa":"/rɪˈmoʊt/","chunks":["remote control","use the remote"],"example_en":"Where is the remote?","example_ro":"Unde este telecomanda?"}
  ],

  "examples": [
    {"en":"There is a mirror on the wall.","ro":"Este o oglindă pe perete."},
    {"en":"Close the door, please.","ro":"Închide ușa, te rog."},
    {"en":"The TV is on the wall.","ro":"Televizorul este pe perete."},
    {"en":"She bought a plant for the living room.","ro":"Ea a cumpărat o plantă pentru sufragerie."}
  ],

  "dialogues": [
    {
      "title":"Finding the remote",
      "turns":[
        {"en":"Where is the remote?","ro":"Unde este telecomanda?"},
        {"en":"It’s on the rug.","ro":"Este pe covoraș."},
        {"en":"No, I don’t see it.","ro":"Nu, nu o văd."},
        {"en":"Check the table near the door.","ro":"Verifică masa de lângă ușă."},
        {"en":"Got it!","ro":"Gata, am găsit-o!"}
      ]
    }
  ],

  "micro_grammar": {
    "topic":"a / an / the",
    "points":[
      "a + consoană (sunet): a door, a rug.",
      "an + vocală (sunet): an umbrella, an hour (sunet de vocală).",
      "the pentru lucru specific sau menționat: Open the door.",
      "Zero articol la plural general: Doors are heavy. / Uncount: I like coffee."
    ],
    "mini_examples":[
      {"en":"There is a picture.","ro":"Este un tablou."},
      {"en":"Open the window, please.","ro":"Deschide fereastra, te rog."}
    ],
    "common_errors":[
      {"bad":"There is an TV.","good":"There is a TV."},
      {"bad":"He bought an plant.","good":"He bought a plant."}
    ]
  },

  "quiz": {
    "items": [
      {"type":"choose","prompt_en":"Pick the correct article: ___ TV is on the wall.","options":["A","An","The"],"correct":"The"},
      {"type":"fill_blank","prompt_en":"There is ___ plant in the living room.","options":["a","an","the"],"correct":"a"},
      {"type":"fill_blank","prompt_en":"Open ___ door, please.","options":["a","an","the"],"correct":"the"},
      {"type":"translate_ro_en","prompt_ro":"Este un tablou pe perete.","answer_en":"There is a picture on the wall.","accept":[]},
      {"type":"translate_en_ro","prompt_en":"Turn on the TV.","answer_ro":"Pornește televizorul."},
      {"type":"choose","prompt_en":"Choose the natural sentence.","options":["There is an TV.","There is a TV.","There are a TV."],"correct":"There is a TV."},
      {"type":"word_order","prompt_en":"Reorder: the / open / please / window / ,","answer_en":"Open the window, please.","tokens":["Open","the","window",",","please","."]},
      {"type":"fill_blank","prompt_en":"She bought ___ rug.","options":["a","an","the"],"correct":"a"},
      {"type":"translate_ro_en","prompt_ro":"Ușa este deschisă.","answer_en":"The door is open.","accept":[]},
      {"type":"fill_blank","prompt_en":"There are ___ pictures on the wall.","options":["a","the","—"],"correct":"—","explain":"Zero articol pentru plural general."}
    ]
  },

  "spaced_review_tags":[
    {"en":"door","review_after_days":2},
    {"en":"window","review_after_days":3},
    {"en":"plant","review_after_days":4}
  ]
}

class Command(BaseCommand):
    help = "Seed Around the House → Unit 1 → Lesson 2"

    def handle(self, *args, **kwargs):
        cat, _ = Category.objects.get_or_create(
            slug="around-the-house",
            defaults=dict(title="Around the House", description="Rooms & objects at home", emoji="🏠"),
        )
        word_count = len(L2.get("targets") or [])
        lesson, created = Lesson.objects.get_or_create(
            category=cat,
            title=L2.get("title", "Articles: a / an / the"),
            defaults=dict(difficulty=L2.get("level","A1"), word_count=word_count, content=L2),
        )
        if not created:
            lesson.content = L2
            lesson.word_count = word_count
            lesson.difficulty = L2.get("level","A1")
            lesson.save()
        self.stdout.write(self.style.SUCCESS(f"Seeded: {lesson.title} in {cat.title}"))
