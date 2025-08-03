"""
Booking views for booking management operations
"""
from rest_framework import status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from bookings.models import Booking
from bookings.serializers import (
    BookingSerializer,
    BookingCreateSerializer,
    BookingUpdateSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
    BookingCancelSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a booking to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the customer
        return obj.customer == request.user


class BookingListView(generics.ListCreateAPIView):
    """
    Booking list and create endpoint
    GET /bookings/ - List user's bookings
    POST /bookings/ - Create new booking
    """
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['booking_number', 'vehicle__make', 'vehicle__model']
    ordering_fields = ['created_at', 'start_date', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return bookings for the current user"""
        return Booking.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for create operation"""
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingListSerializer
    
    def create(self, request, *args, **kwargs):
        """Create new booking"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        # Return detailed booking info
        detail_serializer = BookingDetailSerializer(booking)
        
        return Response({
            'success': True,
            'message': 'Booking created successfully',
            'data': detail_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        """List user's bookings"""
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


class BookingDetailView(generics.RetrieveUpdateAPIView):
    """
    Booking detail and update endpoint
    GET /bookings/{id}/ - Get booking details
    PUT /bookings/{id}/ - Update booking
    """
    serializer_class = BookingDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Return bookings for the current user"""
        return Booking.objects.filter(customer=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for update operation"""
        if self.request.method in ['PUT', 'PATCH']:
            return BookingUpdateSerializer
        return BookingDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Get booking details"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Update booking"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        # Return updated booking details
        detail_serializer = BookingDetailSerializer(booking)
        
        return Response({
            'success': True,
            'message': 'Booking updated successfully',
            'data': detail_serializer.data
        })
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update booking"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class BookingCancelView(APIView):
    """
    Booking cancel endpoint
    POST /bookings/{id}/cancel/ - Cancel booking
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def post(self, request, pk):
        """Cancel booking"""
        try:
            booking = Booking.objects.get(id=pk, customer=request.user)
        except Booking.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Booking not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookingCancelSerializer(
            data=request.data,
            context={'booking': booking}
        )
        serializer.is_valid(raise_exception=True)
        
        # Cancel the booking
        reason = serializer.validated_data.get('cancellation_reason')
        if booking.cancel_booking(reason):
            detail_serializer = BookingDetailSerializer(booking)
            
            return Response({
                'success': True,
                'message': 'Booking cancelled successfully',
                'data': detail_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Cannot cancel this booking'
            }, status=status.HTTP_400_BAD_REQUEST)


class BookingConfirmView(APIView):
    """
    Booking confirm endpoint
    POST /bookings/{id}/confirm/ - Confirm booking
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def post(self, request, pk):
        """Confirm booking"""
        try:
            booking = Booking.objects.get(id=pk, customer=request.user)
        except Booking.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Booking not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if booking.status == 'pending':
            booking.status = 'confirmed'
            booking.save()
            
            detail_serializer = BookingDetailSerializer(booking)
            
            return Response({
                'success': True,
                'message': 'Booking confirmed successfully',
                'data': detail_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Booking cannot be confirmed'
            }, status=status.HTTP_400_BAD_REQUEST)


class BookingSearchView(generics.ListAPIView):
    """
    Booking search endpoint
    GET /bookings/search/ - Search bookings with filters
    """
    serializer_class = BookingListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['booking_number', 'vehicle__make', 'vehicle__model']
    ordering_fields = ['created_at', 'start_date', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return bookings for the current user with date filters"""
        queryset = Booking.objects.filter(customer=self.request.user)
        
        # Add date filters
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        
        if from_date:
            try:
                from_date = timezone.datetime.strptime(from_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                queryset = queryset.filter(start_date__gte=from_date)
            except ValueError:
                pass
        
        if to_date:
            try:
                to_date = timezone.datetime.strptime(to_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                queryset = queryset.filter(end_date__lte=to_date)
            except ValueError:
                pass
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """List filtered bookings"""
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
