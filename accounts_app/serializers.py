from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    Handles creation, retrieval, and updates of User objects,
    ensuring password security and correct flag management based on user_type.
    """

    password = serializers.CharField(
        write_only=True,  # Ensure password is never sent back to the client
        required=True,  # Required for creation
        style={"input_type": "password"},
        validators=[validate_password],  # Use Django's password validators
        help_text=_("Required for user creation. Must meet complexity requirements."),
    )
    date_joined = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = User
        # Defines the fields to include in the serialized output/input
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",  # Write-only
            "user_type",
            "is_staff_member",
            "is_staff",
            "is_active",
            "date_joined",
        ]
        # Defines fields that should not be editable via the API after creation
        read_only_fields = [
            "id",
            "date_joined",
            "is_active",
            "is_staff",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
