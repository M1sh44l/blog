from rest_framework.permissions import BasePermission
from django.utils import timezone


class AuthorOrStaff(BasePermission):
	message = "You must be the author of this post"

	def has_object_permission(self, request, view, obj):
		date = timezone.now().date()
		if obj.publish > date or obj.draft:
			if not(request.user.is_staff or (obj.author == request.user)):
				return False
			else:
				return True
		else:
			return True

# class StaffOrAuthor(BasePermission):

# 	def has_object_permission(self, request, view, obj):
# 		if (draft == False) or not obj.publish:
# 			if request.user.is_staff or (obj.author == request.user):
# 				return True
# 			else:
# 				return False

