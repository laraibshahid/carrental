"""
Booking model for the car rental system
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from users.models import User
from vehicles.models import Vehicle


class Booking(models.Model):
    """
    Booking model representing car rental reservations
    """
    
    # Booking status choices
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('no_show', _('No Show')),
    ]
    
    # Payment status choices
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('partial', _('Partial')),
        ('paid', _('Paid')),
        ('refunded', _('Refunded')),
        ('failed', _('Failed')),
    ]
    
    # Basic booking information
    booking_number = models.CharField(
        max_length=20,
        unique=True,
        help_text=_("Unique booking reference number")
    )
    
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text=_("Customer who made the booking")
    )
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text=_("Vehicle being rented")
    )
    
    # Rental period
    start_date = models.DateTimeField(
        help_text=_("Start date and time of rental")
    )
    
    end_date = models.DateTimeField(
        help_text=_("End date and time of rental")
    )
    
    # Rental details
    pickup_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Pickup location")
    )
    
    return_location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Return location")
    )
    
    # Pricing
    daily_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Daily rate at time of booking")
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Total rental amount")
    )
    
    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Deposit amount required")
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text=_("Current status of the booking")
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        help_text=_("Payment status")
    )
    
    # Additional information
    notes = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional notes for the booking")
    )
    
    cancellation_reason = models.TextField(
        blank=True,
        null=True,
        help_text=_("Reason for cancellation if applicable")
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Booking")
        verbose_name_plural = _("Bookings")
        db_table = 'bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self.booking_number} - {self.customer.username}"
    
    def clean(self):
        """Custom validation for booking data"""
        super().clean()
        
        # Check if end date is after start date
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({
                    'end_date': _('End date must be after start date.')
                })
            
            # Check if booking is not in the past
            if self.start_date < timezone.now():
                raise ValidationError({
                    'start_date': _('Start date cannot be in the past.')
                })
    
    def save(self, *args, **kwargs):
        """Override save to generate booking number and calculate total"""
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()
        
        if not self.total_amount:
            self.total_amount = self.calculate_total_amount()
        
        super().save(*args, **kwargs)
    
    def generate_booking_number(self):
        """Generate unique booking number"""
        import random
        import string
        
        # Generate a random 8-character string
        chars = string.ascii_uppercase + string.digits
        booking_number = ''.join(random.choice(chars) for _ in range(8))
        
        # Check if it already exists
        while Booking.objects.filter(booking_number=booking_number).exists():
            booking_number = ''.join(random.choice(chars) for _ in range(8))
        
        return booking_number
    
    def calculate_total_amount(self):
        """Calculate total rental amount"""
        if self.start_date and self.end_date and self.daily_rate:
            duration = self.end_date - self.start_date
            days = duration.days + (duration.seconds / 86400)  # Convert seconds to days
            return self.daily_rate * Decimal(str(days))
        return Decimal('0.00')
    
    @property
    def duration_days(self):
        """Calculate rental duration in days"""
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            return duration.days + (duration.seconds / 86400)
        return 0
    
    @property
    def is_active(self):
        """Check if booking is currently active"""
        now = timezone.now()
        return (
            self.status == 'active' and
            self.start_date <= now <= self.end_date
        )
    
    @property
    def is_upcoming(self):
        """Check if booking is upcoming"""
        now = timezone.now()
        return (
            self.status in ['pending', 'confirmed'] and
            self.start_date > now
        )
    
    @property
    def is_completed(self):
        """Check if booking is completed"""
        return self.status == 'completed'
    
    @property
    def is_cancelled(self):
        """Check if booking is cancelled"""
        return self.status == 'cancelled'
    
    def can_cancel(self):
        """Check if booking can be cancelled"""
        now = timezone.now()
        # Can cancel if booking is not active and start date is in the future
        return (
            self.status in ['pending', 'confirmed'] and
            self.start_date > now
        )
    
    def cancel_booking(self, reason=None):
        """Cancel the booking"""
        if self.can_cancel():
            self.status = 'cancelled'
            self.cancellation_reason = reason
            self.save()
            return True
        return False
