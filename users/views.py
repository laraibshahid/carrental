"""
User views for authentication and profile management
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import update_session_auth_hash
from users.models import User
from users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint
    POST /register
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create new user and return JWT tokens"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    User login endpoint
    POST /login
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Authenticate user and return JWT tokens"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile endpoint
    GET /profile - Get user profile
    PUT /profile - Update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return current user"""
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        """Get user profile"""
        user = self.get_object()
        serializer = self.get_serializer(user)
        
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        """Update user profile"""
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return updated profile
        profile_serializer = UserProfileSerializer(user)
        
        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'data': profile_serializer.data
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    Change password endpoint
    POST /change-password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, user)
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    User logout endpoint
    POST /logout
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Logout user by blacklisting refresh token"""
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """
    Refresh token endpoint
    POST /refresh-token
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Refresh access token"""
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({
                    'success': False,
                    'message': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            
            return Response({
                'success': True,
                'data': {
                    'access': str(token.access_token),
                    'refresh': str(token),
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)
