from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == 'GET' or admin_permission
    
    
    # We can also do it in below format
        if request.method in permissions.SAFE_METHODS:
                # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            return bool(request.user and request.user.is_staff)
    
    
    
 
class IsReviewUserOrReadOnly(permissions.BasePermission):
    
     def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            return obj.review_user == request.user or request.user.is_staff