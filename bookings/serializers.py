"""
Booking serializers for booking management operations
"""
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from bookings.models import Booking
from vehicles.models import Vehicle
from users.serializers import UserProfileSerializer
from vehicles.serializers import VehicleListSerializer


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model
    """
    customer = UserProfileSerializer(read_only=True)
    vehicle = VehicleListSerializer(read_only=True)
    duration_days = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    is_cancelled = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'customer', 'vehicle', 'start_date',
            'end_date', 'pickup_location', 'return_location', 'daily_rate',
            'total_amount', 'deposit_amount', 'status', 'payment_status',
            'notes', 'cancellation_reason', 'duration_days', 'is_active',
            'is_upcoming', 'is_completed', 'is_cancelled', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'booking_number', 'customer', 'total_amount',
            'created_at', 'updated_at'
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating bookings
    """
    vehicle_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'vehicle_id', 'start_date', 'end_date', 'pickup_location',
            'return_location', 'notes'
        ]
    
    def validate_vehicle_id(self, value):
        """Validate vehicle exists and is available"""
        try:
            vehicle = Vehicle.objects.get(id=value)
            if not vehicle.is_available:
                raise serializers.ValidationError(
                    "This vehicle is not available for booking."
                )
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError(
                "Vehicle not found."
            )
        return value
    
    def validate_start_date(self, value):
        """Validate start date is in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Start date must be in the future."
            )
        return value
    
    def validate_end_date(self, value):
        """Validate end date is after start date"""
        start_date = self.initial_data.get('start_date')
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                if value <= start_date:
                    raise serializers.ValidationError(
                        "End date must be after start date."
                    )
            except (ValueError, TypeError):
                pass
        return value
    
    def validate(self, attrs):
        """Validate booking dates and check for overlaps"""
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        vehicle_id = attrs.get('vehicle_id')
        
        if start_date and end_date and vehicle_id:
            # Check for booking overlaps
            overlapping_bookings = Booking.objects.filter(
                vehicle_id=vehicle_id,
                status__in=['pending', 'confirmed', 'active'],
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    "This vehicle is already booked for the selected dates."
                )
        
        return attrs
    
    def create(self, validated_data):
        """Create booking with calculated values"""
        vehicle_id = validated_data.pop('vehicle_id')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        # Set customer and daily rate
        validated_data['customer'] = self.context['request'].user
        validated_data['vehicle'] = vehicle
        validated_data['daily_rate'] = vehicle.daily_rate
        
        # Calculate deposit (e.g., 20% of total)
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        duration = end_date - start_date
        days = duration.days + (duration.seconds / 86400)
        total_amount = vehicle.daily_rate * Decimal(str(days))
        validated_data['deposit_amount'] = total_amount * Decimal('0.2')
        
        return super().create(validated_data)


class BookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating bookings
    """
    class Meta:
        model = Booking
        fields = [
            'start_date', 'end_date', 'pickup_location', 'return_location',
            'notes', 'status'
        ]
    
    def validate_start_date(self, value):
        """Validate start date is in the future"""
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Start date must be in the future."
            )
        return value
    
    def validate_end_date(self, value):
        """Validate end date is after start date"""
        start_date = self.initial_data.get('start_date')
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                if value <= start_date:
                    raise serializers.ValidationError(
                        "End date must be after start date."
                    )
            except (ValueError, TypeError):
                pass
        return value
    
    def validate_status(self, value):
        """Validate status changes"""
        instance = self.instance
        if instance and instance.status in ['completed', 'cancelled']:
            raise serializers.ValidationError(
                "Cannot modify completed or cancelled bookings."
            )
        return value


class BookingListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing bookings (simplified)
    """
    vehicle = VehicleListSerializer(read_only=True)
    duration_days = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'vehicle', 'start_date', 'end_date',
            'total_amount', 'status', 'payment_status', 'duration_days',
            'is_active', 'created_at'
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for booking details
    """
    customer = UserProfileSerializer(read_only=True)
    vehicle = VehicleListSerializer(read_only=True)
    duration_days = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    is_cancelled = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'customer', 'vehicle', 'start_date',
            'end_date', 'pickup_location', 'return_location', 'daily_rate',
            'total_amount', 'deposit_amount', 'status', 'payment_status',
            'notes', 'cancellation_reason', 'duration_days', 'is_active',
            'is_upcoming', 'is_completed', 'is_cancelled', 'created_at', 'updated_at'
        ]


class BookingCancelSerializer(serializers.Serializer):
    """
    Serializer for cancelling bookings
    """
    cancellation_reason = serializers.CharField(
        max_length=500,
        required=False,
        help_text="Reason for cancellation"
    )
    
    def validate(self, attrs):
        """Validate booking can be cancelled"""
        booking = self.context['booking']
        if not booking.can_cancel():
            raise serializers.ValidationError(
                "This booking cannot be cancelled."
            )
        return attrs 