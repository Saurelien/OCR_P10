from rest_framework import permissions


class IsProjectAuthor(permissions.BasePermission):
    """
    Permission pour verifier si l'utilisateur est l'autheur du projet avec
    une méthode qui permet a un utilisateur de s'inscrire au projet de l'auteur
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Exclure l'action "join" de la vérification de l'auteur
        if view.action in ["join", "unjoin"]:
            return True

        if view.action == "destroy":
            return obj.author == request.user

        return obj.author == request.user


class IsIssueCreator(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est dans la liste des contributeurs
    d'un projet pour lui permettre de créer des issues et d'assigner des contributeurs.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.contributed_projects.filter(pk=view.kwargs["project_pk"]).exists()

    def has_object_permission(self, request, view, obj):
        print(f"Issue author: {obj.author}, User: {request.user}")
        return obj.author == request.user


class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f"Comment author: {obj.author}, User: {request.user}")
        return obj.author == request.user
