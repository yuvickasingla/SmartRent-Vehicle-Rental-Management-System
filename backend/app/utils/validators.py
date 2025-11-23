import re


class ValidationError(Exception):
    """
    Simple custom exception to signal validation errors.
    """
    pass


def validate_email(email: str) -> None:
    """
    Very basic email validation using a regular expression.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")


def validate_phone(phone: str) -> None:
    """
    Simple validation: phone must be exactly 10 digits.
    """
    if not re.fullmatch(r"\d{10}", phone):
        raise ValidationError("Phone number must be 10 digits")
