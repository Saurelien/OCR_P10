from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'age', 'can_be_contacted', 'can_data_be_shared')

    def validate_age(self, value):
        """
        Validation de l'âge.
        """
        if value < 15:
            raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans.")
        return value

    def validate(self, attrs):
        """
        Modification des champs en fonction de l'âge.
        Afin d'être conforme a la demande du projet et la protection des personne ayant 15-17 ans
        """
        age = attrs.get('age')
        if 15 <= age <= 17:
            attrs['can_be_contacted'] = False
            attrs['can_data_be_shared'] = False
        return attrs

    def save(self):
        """
        Création de l'utilisateur en utilisant create_user pour gérer le mot de passe.
        """
        self.instance = User.objects.create_user(
            self.validated_data.pop('username'),
            password=self.validated_data.pop('password'),
            **self.validated_data
        )
        return self.instance

