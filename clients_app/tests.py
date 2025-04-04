from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import ClientProfile as Client

class ClientModelTests(TestCase):
    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        pass