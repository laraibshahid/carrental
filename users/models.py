"""
Custom User model for the car rental system
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model for the car rental system
    Extends Django's AbstractUser with additional fields
    """
    
    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    # Additional fields
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text=_("Phone number in international format")
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        help_text=_("User's address")
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text=_("User's date of birth")
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text=_("Whether the user's email is verified")
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = 'users'
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_short_name(self):
        """Return the user's short name"""
        return self.first_name or self.username
