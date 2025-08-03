"""
Vehicle serializers for CRUD operations
"""
from rest_framework import serializers
from vehicles.models import Vehicle
from users.serializers import UserProfileSerializer


class VehicleSerializer(serializers.ModelSerializer):
    """
    Serializer for Vehicle model
    """
    owner = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    daily_rate_display = serializers.ReadOnlyField()
    weekly_rate_display = serializers.ReadOnlyField()
    monthly_rate_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'make', 'model', 'year', 'license_plate', 'vehicle_type',
            'fuel_type', 'transmission', 'engine_size', 'mileage',
            'daily_rate', 'weekly_rate', 'monthly_rate', 'status',
            'owner', 'color', 'seats', 'description', 'image',
            'full_name', 'is_available', 'daily_rate_display',
            'weekly_rate_display', 'monthly_rate_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def validate_license_plate(self, value):
        """Validate license plate uniqueness"""
        if Vehicle.objects.filter(license_plate=value).exists():
            raise serializers.ValidationError(
                "A vehicle with this license plate already exists."
            )
        return value
    
    def validate_daily_rate(self, value):
        """Validate daily rate is positive"""
        if value <= 0:
            raise serializers.ValidationError(
                "Daily rate must be greater than zero."
            )
        return value
    
    def validate_weekly_rate(self, value):
        """Validate weekly rate if provided"""
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Weekly rate must be greater than zero."
            )
        return value
    
    def validate_monthly_rate(self, value):
        """Validate monthly rate if provided"""
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Monthly rate must be greater than zero."
            )
        return value


class VehicleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating vehicles
    """
    class Meta:
        model = Vehicle
        fields = [
            'make', 'model', 'year', 'license_plate', 'vehicle_type',
            'fuel_type', 'transmission', 'engine_size', 'mileage',
            'daily_rate', 'weekly_rate', 'monthly_rate', 'color',
            'seats', 'description', 'image'
        ]
    
    def create(self, validated_data):
        """Create vehicle and assign to current user"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class VehicleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating vehicles
    """
    class Meta:
        model = Vehicle
        fields = [
            'make', 'model', 'year', 'license_plate', 'vehicle_type',
            'fuel_type', 'transmission', 'engine_size', 'mileage',
            'daily_rate', 'weekly_rate', 'monthly_rate', 'status',
            'color', 'seats', 'description', 'image'
        ]
    
    def validate_license_plate(self, value):
        """Validate license plate uniqueness excluding current instance"""
        instance = self.instance
        if Vehicle.objects.filter(license_plate=value).exclude(id=instance.id).exists():
            raise serializers.ValidationError(
                "A vehicle with this license plate already exists."
            )
        return value


class VehicleListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing vehicles (simplified)
    """
    full_name = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    daily_rate_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'full_name', 'license_plate', 'vehicle_type',
            'fuel_type', 'transmission', 'daily_rate', 'daily_rate_display',
            'status', 'is_available', 'color', 'seats', 'image',
            'created_at'
        ]


class VehicleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for vehicle details
    """
    owner = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    daily_rate_display = serializers.ReadOnlyField()
    weekly_rate_display = serializers.ReadOnlyField()
    monthly_rate_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Vehicle
        fields = [
            'id', 'make', 'model', 'year', 'license_plate', 'vehicle_type',
            'fuel_type', 'transmission', 'engine_size', 'mileage',
            'daily_rate', 'weekly_rate', 'monthly_rate', 'status',
            'owner', 'color', 'seats', 'description', 'image',
            'full_name', 'is_available', 'daily_rate_display',
            'weekly_rate_display', 'monthly_rate_display',
            'created_at', 'updated_at'
        ] 