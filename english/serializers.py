# english/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "display_name", "avatar_url"]

    def get_display_name(self, obj):
        return getattr(obj, "first_name", "") or obj.username

    def get_avatar_url(self, obj):
        return ""

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_username(self, v):
        if User.objects.filter(username=v).exists():
            raise serializers.ValidationError("Username already exists")
        return v

    def validate(self, attrs):
        # Build a transient user for similarity checks (not saved)
        candidate = User(username=attrs.get("username", ""), email=attrs.get("email", ""))
        try:
            validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as e:
            # Attach messages to the password field
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )



# --- Catalog serializers -----------------------------------------------------
from rest_framework import serializers
from .models import Category, Lesson

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title", "description", "emoji", "completion_percentage"]

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "difficulty", "category", "word_count"]

class LessonDetailSerializer(serializers.ModelSerializer):
    body_md = serializers.SerializerMethodField()
    flashcards = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["id", "title", "difficulty", "category", "word_count", "body_md", "flashcards", "questions"]

    def get_body_md(self, obj: Lesson) -> str:
        c = obj.content or {}
        parts = []
        # examples -> simple markdown bullets
        ex = c.get("examples") or []
        if ex:
            lines = [f"- {e.get('en','')} — *{e.get('ro','')}*" for e in ex[:6]]
            parts.append("### Examples\n" + "\n".join(lines))
        # micro_grammar -> brief section
        mg = c.get("micro_grammar") or {}
        if mg:
            topic = mg.get("topic") or "Grammar"
            points = mg.get("points") or []
            pt_lines = "\n".join([f"- {p}" for p in points])
            parts.append(f"### Grammar: {topic}\n{pt_lines}")
        return "\n\n".join(parts)

    def get_flashcards(self, obj: Lesson):
        targets = (obj.content or {}).get("targets") or []
        cards = []
        for i, t in enumerate(targets, start=1):
            cards.append({
                "id": i,
                "front_text": t.get("en", ""),
                "back_text": t.get("ro", ""),
                "audio_url": None,
            })
        return cards

    def get_questions(self, obj: Lesson):
        items = ((obj.content or {}).get("quiz") or {}).get("items") or []
        out, qid = [], 1
        for it in items:
            t = it.get("type")
            if t == "choose":
                out.append({
                    "id": qid,
                    "prompt": it.get("prompt_en",""),
                    "qtype": "mcq",
                    "payload": {"options": it.get("options") or []},
                })
            elif t == "fill_blank":
                out.append({
                    "id": qid,
                    "prompt": it.get("prompt_en",""),
                    "qtype": "fill",
                    "payload": {"blanks": 1},
                })
            elif t in ("translate_ro_en", "translate_en_ro", "word_order"):
                prompt = it.get("prompt_en") or it.get("prompt_ro") or ""
                out.append({"id": qid, "prompt": prompt, "qtype": "fill", "payload": {"blanks": 1}})
            elif t == "dialogue_reply":
                out.append({
                    "id": qid,
                    "prompt": it.get("prompt_en",""),
                    "qtype": "mcq",
                    "payload": {"options": it.get("options") or []},
                })
            elif t == "tf":
                out.append({"id": qid, "prompt": it.get("prompt_en",""), "qtype": "tf", "payload": {}})
            else:
                continue
            qid += 1
        return out