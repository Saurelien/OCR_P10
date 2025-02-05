from user_auth.models import User
from rest_framework import serializers
from project_manager.models import Project, Issue, Comment


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'age', 'can_be_contacted', 'can_data_be_shared')


class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    nb_contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('pk', 'title', 'description', 'type', 'author', 'nb_contributors', 'created_time', 'updated_time')

    def get_author(self, obj):
        # réutiliser une classe qui récupère les info d'un contributeur auteur
        return UserLiteSerializer(obj.author).data

    def get_nb_contributors(self, obj):
        return obj.contributors.count()



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('pk', 'title', 'description', 'type', 'created_time', 'updated_time')

    def validate_title(self, value):
        if Project.objects.filter(title=value).exists():
            raise serializers.ValidationError("Le titre du projet existe déjà")
        return value


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = (
            'pk', 'title', 'description', 'assignee', 'status', 'priority', 'tag',
            'created_time', 'updated_time'
        )
        read_only_fields = ('created_time', 'updated_time')

    def validate_assignee(self, value):
        if value is not None:
            project_pk = self.context["view"].kwargs["project_pk"]
            if not value.contributed_projects.filter(pk=project_pk).exists():
                raise serializers.ValidationError('L\'utilisateur assigné doit être un contributeur du projet.')

            return value

        return self.context['request'].user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = UserLiteSerializer(instance.author).data

        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('uid', 'pk', 'description', 'created_time', 'updated_time')

    def validate(self, data):
        user = self.context['request'].user
        issue_pk = self.context['view'].kwargs['issue_pk']

        # Vérification si l'utilisateur est assigné à l'issue
        issue = Issue.objects.get(pk=issue_pk)
        if issue.assignee != user:
            raise serializers.ValidationError("Vous n'êtes pas autorisé à commenter cette issue.")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = UserLiteSerializer(instance.author).data

        return representation

