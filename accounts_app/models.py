from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators as v
from .validators import validate_name
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Uses email as the unique identifier for authentication instead of a username.
    Includes a user type system (Client, Staff, Admin) and a specific flag
    for application-level staff privileges (`is_staff_member`).

    :ivar email: Unique email address for the user. Also serves as the username.
    :vartype email: models.EmailField
    :ivar user_type: Categorizes the user (e.g., Client, Staff, Admin).
    :vartype user_type: models.CharField
    :ivar is_staff_member: Flag indicating application-specific staff privileges,
                           distinct from Django admin access (`is_staff`).
    :vartype is_staff_member: models.BooleanField
    """ 
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
        help_text=_("Required. Unique email address for the user. Serves as the username for logging in.")
    )
    first_name = models.CharField(
        _('first name'),
        max_length=100,
        blank=False,
        null=False,
        validators=[v.MinLengthValidator(2), validate_name],
        help_text="Required. Enter the user's first name (100 characters max)."
    )
    last_name = models.CharField(
        _('last name'),
        max_length=100,
        blank=False,
        null=False,
        validators=[v.MinLengthValidator(2), validate_name],
        help_text="Required. Enter the user's last name (100 characters max)."
    )

    class Types(models.TextChoices):
        """
        Enumeration for the different types of users within the application.

        :cvar CLIENT: Standard client user.
        :cvar STAFF: Staff user with specific application permissions.
        :cvar ADMIN: Administrator user, typically also a superuser.
        """
        CLIENT = 'CLIENT', _('Client')
        STAFF = 'STAFF', _('Staff')
        ADMIN = 'ADMIN', _('Admin')

    user_type = models.CharField(
        _('Type'),
        max_length=10,
        choices=Types.choices,
        default=Types.CLIENT,
        help_text=_("Categorizes the user role within the application (Client, Staff, Admin).")
    )
    
    # IMPORTANT: Django's built-in 'is_staff' controls access to the Django Admin site.
    # Use 'is_staff_member' for application-specific staff logic/permissions.
    # Admins will have is_staff=True, is_superuser=True, is_staff_member=True.
    # Regular staff will have is_staff_member=True, is_staff=False (if they don't need admin access)

    is_staff_member = models.BooleanField(
        _('staff member status'),
        default=False,
        help_text=_("Designates whether the user has staff privileges within the application (distinct from Django Admin access).")
    )

    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        """
        Metadata options for the User model.
        """
        ordering = ['last_name', 'first_name', 'email']
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """
        Return a string representation of the user.

        Defaults to the user's full name if available, otherwise their email.

        :return: String representation of the user.
        :rtype: str
        """
        full_name = self.get_full_name()
        return full_name.strip() or self.email
    
    @property
    def is_client(self):
        """Check if the user is of type CLIENT."""
        return self.user_type == self.Types.CLIENT
    
    @property
    def is_staff_user(self):
        """Check if the user is of type STAFF."""
        return self.user_type == self.Types.STAFF
    
    @property
    def is_admin_user(self):
        """Check if the user is of type ADMIN."""
        return self.user_type == self.Types.ADMIN