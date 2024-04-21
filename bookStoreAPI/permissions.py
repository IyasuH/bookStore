from rest_framework.permissions import BasePermission, IsAdminUser

class ReadOnlyPermission(BasePermission):
    """
    this permission allows normal users to only Read and List
    """
    def has_permission(self, request, view):
        if request.user:
            if IsAdminUser().has_permission(request, view):
                return True
            elif view.action in ['retrieve', 'list']:
                return True
        return False
        # return super().has_permission(request, view)

# people can only update/delete their own review
# other users and anonymous users can only read
class IsReviewOwner(BasePermission):
    """
    Allows GET for all
    - PUT, PATCH, DELETE - only the author of the review
    - user can only create review for themself
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.user == request.user
        elif request.method == 'POST':
            return request.user.is_authenticated
        return True
