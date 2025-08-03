"""
Payment models for Stripe deposit integration
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.utils import timezone
from bookings.models import Booking
from users.models import User


class Payment(models.Model):
    """
    Payment model for handling deposits and payments
    """
    
    # Payment types
    PAYMENT_TYPE_CHOICES = [
        ('deposit', _('Deposit')),
        ('full_payment', _('Full Payment')),
        ('refund', _('Refund')),
    ]
    
    # Payment status
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ]
    
    # Payment methods
    PAYMENT_METHOD_CHOICES = [
        ('stripe', _('Stripe')),
        ('cash', _('Cash')),
        ('bank_transfer', _('Bank Transfer')),
    ]
    
    # Basic payment information
    payment_id = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Unique payment identifier")
    )
    
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text=_("Booking associated with this payment")
    )
    
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text=_("Customer who made the payment")
    )
    
    # Payment details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_("Payment amount")
    )
    
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text=_("Payment currency")
    )
    
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default='deposit',
        help_text=_("Type of payment")
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='stripe',
        help_text=_("Payment method used")
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text=_("Payment status")
    )
    
    # Stripe specific fields
    stripe_payment_intent_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Stripe Payment Intent ID")
    )
    
    stripe_charge_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Stripe Charge ID")
    )
    
    # Additional information
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Payment description")
    )
    
    failure_reason = models.TextField(
        blank=True,
        null=True,
        help_text=_("Reason for payment failure")
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("When payment was processed")
    )
    
    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.payment_id} - {self.booking.booking_number}"
    
    def save(self, *args, **kwargs):
        """Override save to generate payment ID"""
        if not self.payment_id:
            self.payment_id = self.generate_payment_id()
        super().save(*args, **kwargs)
    
    def generate_payment_id(self):
        """Generate unique payment ID"""
        import random
        import string
        
        # Generate a random 12-character string
        chars = string.ascii_uppercase + string.digits
        payment_id = ''.join(random.choice(chars) for _ in range(12))
        
        # Check if it already exists
        while Payment.objects.filter(payment_id=payment_id).exists():
            payment_id = ''.join(random.choice(chars) for _ in range(12))
        
        return payment_id
    
    @property
    def is_completed(self):
        """Check if payment is completed"""
        return self.status == 'completed'
    
    @property
    def is_pending(self):
        """Check if payment is pending"""
        return self.status == 'pending'
    
    @property
    def is_failed(self):
        """Check if payment failed"""
        return self.status == 'failed'
    
    def process_payment(self):
        """Mock payment processing"""
        if self.status == 'pending':
            # Simulate payment processing
            import random
            import time
            
            # Simulate processing time
            time.sleep(0.1)
            
            # 95% success rate for mock payments
            if random.random() < 0.95:
                self.status = 'completed'
                self.processed_at = timezone.now()
                self.stripe_payment_intent_id = f"pi_{self.payment_id.lower()}"
                self.stripe_charge_id = f"ch_{self.payment_id.lower()}"
            else:
                self.status = 'failed'
                self.failure_reason = "Mock payment failed for testing purposes"
            
            self.save()
            return self.status == 'completed'
        return False
    
    def refund_payment(self, amount=None):
        """Mock payment refund"""
        if self.status == 'completed':
            refund_amount = amount or self.amount
            
            # Create refund record
            refund = Payment.objects.create(
                booking=self.booking,
                customer=self.customer,
                amount=refund_amount,
                currency=self.currency,
                payment_type='refund',
                payment_method=self.payment_method,
                status='completed',
                description=f"Refund for payment {self.payment_id}",
                processed_at=timezone.now()
            )
            
            return refund
        return None
