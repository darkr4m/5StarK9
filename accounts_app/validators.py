from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_name(name):
    """
    Validates that the name contains only Unicode letters, spaces, hyphens,
    and apostrophes. It also ensures the name is not empty after stripping whitespace
    and does not contain numbers or other disallowed symbols.
    """
    if not name: # Handles empty string or None cases early
        raise ValidationError(_("Name cannot be empty."))
    
    name_stripped = name.strip()
    if not name_stripped:
        raise ValidationError(_("Name cannot consist of only whitespace characters."))
    
    regex = r'^[^0-9_!¡?÷?¿/\\+=@#$%^&*(){}|~<>;:[\]]+$'

    good_name = re.match(regex, name_stripped)
    if good_name:
        return name
    else:
        raise ValidationError(_("Invalid name format. Only letters, spaces, hyphens, apostrophes allowed"))