
from rest_framework import permissions

class EstProprietaireOuLectureSeulement(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que les propriétaires d'un objet à l'éditer.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.proprietaire == request.user
