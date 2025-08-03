"""
Vehicle views for CRUD operations
"""
from rest_framework import status, generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from vehicles.models import Vehicle
from vehicles.serializers import (
    VehicleSerializer,
    VehicleCreateSerializer,
    VehicleUpdateSerializer,
    VehicleListSerializer,
    VehicleDetailSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a vehicle to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class VehicleListView(generics.ListCreateAPIView):
    """
    Vehicle list and create endpoint
    GET /vehicles/ - List user's vehicles
    POST /vehicles/ - Create new vehicle
    """
    serializer_class = VehicleListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle_type', 'fuel_type', 'transmission', 'status']
    search_fields = ['make', 'model', 'license_plate', 'color']
    ordering_fields = ['created_at', 'daily_rate', 'year', 'mileage']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return vehicles owned by the current user"""
        return Vehicle.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for create operation"""
        if self.request.method == 'POST':
            return VehicleCreateSerializer
        return VehicleListSerializer
    
    def create(self, request, *args, **kwargs):
        """Create new vehicle"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()
        
        # Return detailed vehicle info
        detail_serializer = VehicleDetailSerializer(vehicle)
        
        return Response({
            'success': True,
            'message': 'Vehicle created successfully',
            'data': detail_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        """List user's vehicles"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vehicle detail, update, and delete endpoint
    GET /vehicles/{id}/ - Get vehicle details
    PUT /vehicles/{id}/ - Update vehicle
    DELETE /vehicles/{id}/ - Delete vehicle
    """
    serializer_class = VehicleDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Return vehicles owned by the current user"""
        return Vehicle.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for update operation"""
        if self.request.method in ['PUT', 'PATCH']:
            return VehicleUpdateSerializer
        return VehicleDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Get vehicle details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Update vehicle"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()
        
        # Return updated vehicle details
        detail_serializer = VehicleDetailSerializer(vehicle)
        
        return Response({
            'success': True,
            'message': 'Vehicle updated successfully',
            'data': detail_serializer.data
        })
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update vehicle"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete vehicle"""
        instance = self.get_object()
        
        # Check if vehicle has active bookings
        if instance.bookings.filter(status__in=['pending', 'confirmed', 'active']).exists():
            return Response({
                'success': False,
                'message': 'Cannot delete vehicle with active bookings'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.delete()
        
        return Response({
            'success': True,
            'message': 'Vehicle deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class VehicleSearchView(generics.ListAPIView):
    """
    Vehicle search endpoint
    GET /vehicles/search/ - Search available vehicles
    """
    serializer_class = VehicleListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle_type', 'fuel_type', 'transmission']
    search_fields = ['make', 'model', 'license_plate', 'color', 'year']
    ordering_fields = ['daily_rate', 'year', 'mileage']
    ordering = ['daily_rate']
    
    def get_queryset(self):
        """Return available vehicles"""
        return Vehicle.objects.filter(status='available')
    
    def list(self, request, *args, **kwargs):
        """List available vehicles"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
