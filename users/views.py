from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import password_validation
from .serializers import LoginSerializer, UserSerializer, PostSerializer
from .models import Post
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework.authentication import TokenAuthentication  # Token-based Authentication


# User CRUD (Create, Read, Update, Delete)
class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Check if email already exists
        email = serializer.validated_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError({'email': 'Email is already taken.'})
        # Create the user
        serializer.save()

class UserUpdateView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDeleteView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        return self.request.user

# Post creation API

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    authentication_classes = [TokenAuthentication]  # Token authentication

    def perform_create(self, serializer):
        # Automatically associate the post with the authenticated user
        serializer.save(user=self.request.user)
# Login API to generate JWT tokens
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate with the email instead of username
        try:
            user = get_user_model().objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except get_user_model().DoesNotExist:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'refresh': str(refresh),
                'access': str(access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Forgot Password (Send reset email)
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email', None)
    if email is None:
        return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_user_model().objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())  # Convert ID to string before encoding
        
        reset_url = f"http://127.0.0.1:8000/api/reset-password/{uid}/{token}/"  # The reset URL

        return Response({"detail": f"Password reset link: {reset_url}"}, status=status.HTTP_200_OK)

    except get_user_model().DoesNotExist:
        return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

# Reset Password (Accept new password)
@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except Exception as e:
        return Response({"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

    new_password = request.data.get('password', None)
    confirm_password = request.data.get('confirm_password', None)
    if not new_password or not confirm_password:
        return Response({"detail": "Password and confirm password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        password_validation.validate_password(new_password, user)
        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password has been successfully reset."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
