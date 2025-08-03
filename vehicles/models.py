"""
Vehicle model for the car rental system
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from users.models import User


class Vehicle(models.Model):
    """
    Vehicle model representing cars in the rental fleet
    """
    
    # Vehicle types
    VEHICLE_TYPE_CHOICES = [
        ('sedan', _('Sedan')),
        ('suv', _('SUV')),
        ('hatchback', _('Hatchback')),
        ('convertible', _('Convertible')),
        ('truck', _('Truck')),
        ('van', _('Van')),
        ('luxury', _('Luxury')),
        ('economy', _('Economy')),
    ]
    
    # Fuel types
    FUEL_TYPE_CHOICES = [
        ('petrol', _('Petrol')),
        ('diesel', _('Diesel')),
        ('electric', _('Electric')),
        ('hybrid', _('Hybrid')),
        ('cng', _('CNG')),
    ]
    
    # Transmission types
    TRANSMISSION_CHOICES = [
        ('manual', _('Manual')),
        ('automatic', _('Automatic')),
    ]
    
    # Vehicle status
    STATUS_CHOICES = [
        ('available', _('Available')),
        ('rented', _('Rented')),
        ('maintenance', _('Under Maintenance')),
        ('out_of_service', _('Out of Service')),
    ]
    
    # Basic vehicle information
    make = models.CharField(
        max_length=100,
        help_text=_("Vehicle manufacturer (e.g., Toyota, Honda)")
    )
    
    model = models.CharField(
        max_length=100,
        help_text=_("Vehicle model (e.g., Camry, Civic)")
    )
    
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900, message=_("Year must be 1900 or later")),
            MaxValueValidator(2030, message=_("Year cannot be in the future"))
        ],
        help_text=_("Manufacturing year")
    )
    
    license_plate = models.CharField(
        max_length=20,
        unique=True,
        help_text=_("Vehicle license plate number")
    )
    
    # Vehicle specifications
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
        default='sedan',
        help_text=_("Type of vehicle")
    )
    
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
        default='petrol',
        help_text=_("Type of fuel used")
    )
    
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        default='automatic',
        help_text=_("Transmission type")
    )
    
    engine_size = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        help_text=_("Engine size in liters")
    )
    
    mileage = models.PositiveIntegerField(
        default=0,
        help_text=_("Current mileage in kilometers")
    )
    
    # Rental information
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Daily rental rate")
    )
    
    weekly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Weekly rental rate (optional)")
    )
    
    monthly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Monthly rental rate (optional)")
    )
    
    # Vehicle status and ownership
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        help_text=_("Current status of the vehicle")
    )
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles',
        help_text=_("User who owns/manages this vehicle")
    )
    
    # Additional information
    color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("Vehicle color")
    )
    
    seats = models.PositiveSmallIntegerField(
        default=5,
        help_text=_("Number of seats")
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional description of the vehicle")
    )
    
    # Images
    image = models.ImageField(
        upload_to='vehicles/',
        blank=True,
        null=True,
        help_text=_("Vehicle image")
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")
        db_table = 'vehicles'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.license_plate})"
    
    @property
    def full_name(self):
        """Return the full vehicle name"""
        return f"{self.year} {self.make} {self.model}"
    
    @property
    def is_available(self):
        """Check if vehicle is available for rental"""
        return self.status == 'available'
    
    def get_daily_rate_display(self):
        """Return formatted daily rate"""
        return f"${self.daily_rate}/day"
    
    def get_weekly_rate_display(self):
        """Return formatted weekly rate"""
        if self.weekly_rate:
            return f"${self.weekly_rate}/week"
        return "Not available"
    
    def get_monthly_rate_display(self):
        """Return formatted monthly rate"""
        if self.monthly_rate:
            return f"${self.monthly_rate}/month"
        return "Not available"
