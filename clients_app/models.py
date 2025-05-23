from django.db import models
from django.core import validators as v
from ..accounts_app.validators import validate_name
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ClientProfile(models.Model):
    first_name = models.CharField(validators=[validate_name])
    last_name = models.CharField()
    email = models.EmailField()
    phone_number = models.CharField()
    alternate_phone_number = models.CharField()
    preferred_contact_method = models.CharField()
    emergency_contact_name = models.CharField()
    emergency_contact_phone = models.CharField()
    notes = models.TextField()
    client_status = models.CharField()
    referral_source = models.CharField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        ordering = ['last_name', 'first_name']

    def get_full_name(self):
        """Returns the client's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        """String representation for the ClientProfile model."""
        return self.get_full_name()