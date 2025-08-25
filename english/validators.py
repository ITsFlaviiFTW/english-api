# english/validators.py
import re
from django.core.exceptions import ValidationError

class UppercaseValidator:
    message = "Password must contain at least one uppercase letter."
    code = "password_no_uppercase"

    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message

class SpecialCharacterValidator:
    message = "Password must contain at least one special character."
    code = "password_no_special"

    # Adjust the class of special characters if you want a specific set:
    # pattern = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]"
    pattern = r"[^A-Za-z0-9]"

    def validate(self, password, user=None):
        if not re.search(self.pattern, password):
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return self.message
