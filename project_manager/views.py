from django.http import JsonResponse
from django.views import View
from rest_framework.generics import get_object_or_404
from project_manager.serializers import ProjectSerializer, IssueSerializer, ProjectDetailSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from project_manager.models import Project, Issue, Comment
from rest_framework.exceptions import ValidationError
from project_manager.permissions import IsProjectAuthor, IsIssueCreator, IsCommentAuthor
from libs.views import MultipleSerializerMixin

User = get_user_model()


class ProjectViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
    detail_serializer_class = ProjectDetailSerializer
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def get_queryset(self):
        if self.action in ["join", "unjoin"]:
            return Project.objects.all()
        return self.request.user.contributed_projects.order_by("created_time")

    def perform_create(self, serializer):
        user = self.request.user
        user_age = user.age

        if user_age < 18:
            raise ValidationError({'error': 'Vous devez être majeur pour cette action.'})

        project = serializer.save(author=user)

        # Ajoutez les détails des contributeurs au projet
        project.contributors.set([user])
        project.save()

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        project = self.get_object()
        user = request.user
        # Vérifiez si l'utilisateur est déjà contributeur du projet
        if project.contributors.filter(id=user.id).exists():
            return Response({'detail': f'Vous avez déjà rejoint le projet {project.title}.'
                                       f' ID du projet {project.pk}'}, status=200)
        # Ajouter un contributeur au projet
        project.contributors.add(user)
        return Response({'detail': 'Inscription réussie au projet.'}, status=200)

    @action(detail=True, methods=['post'])
    def unjoin(self, request, pk=None):
        project = self.get_object()
        user = self.request.user

        # Vérifiez si l'utilisateur est déjà contributeur du projet
        if project.contributors.filter(id=user.id).exists():
            # Retirer le contributeur du projet
            project.contributors.remove(user)
            return Response({'message': f'Vous vous êtes retiré du projet {project.title} ID: {project.pk}.'},
                            status=200)
        # Renvoyer un message indiquant qu'il n'est pas contributeur.
        return Response({'message': f'Vous n\'êtes pas actuellement contributeur du projet {project.title}'
                                    f' ID: {project.pk}.'},
                        status=200)


class ProjectJSONView(View):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsIssueCreator]

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributors=user, project__id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, project_id=self.kwargs["project_pk"])


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsCommentAuthor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs["issue_pk"], issue__project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs["issue_pk"])
        serializer.save(author=self.request.user, issue=issue)
