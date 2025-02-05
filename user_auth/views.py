from user_auth.serializers import UserProfileSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()


class UserRegistrationView(APIView):
    @staticmethod
    def post(request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_to_delete = request.user

        try:
            user_to_delete.delete()
            return Response({'message': 'Votre compte a été supprimé avec succès.'},
                            status=204)
        except Exception as e:
            return Response({'error': 'Une erreur s\'est produite lors de la suppression du compte.'},
                            status=500)
