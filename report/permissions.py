from rest_framework_api_key.permissions import BaseHasAPIKey
from report.models.api import OrganizationAPIKey, ApiURL, RequestAPI
from rest_framework import permissions
from django.conf import settings

class HasOrganizationAPIKey(BaseHasAPIKey):
    model = OrganizationAPIKey

    def has_permission(self, request, view):
        if settings.DEBUG:
            return True
            
        #API 퍼미션 확인
        apiUrl = ApiURL.getApiUrl(request)
        
        if apiUrl != None:
            if apiUrl.is_permission == False:
                return True

        is_permission = super().has_permission(request, view)

        if is_permission:
            key = self.get_key(request)
            prefix, _, _ = key.partition(".")
            keyObject = self.model.objects.get(prefix=prefix)

            # all_count = RequestAPI.objects.filter(organization_key=keyObject).count()
            # month_count = RequestAPI.objects.filter(organization_key=keyObject).count()
            # day_count = RequestAPI.objects.filter(organization_key=keyObject).count()

            # if keyObject.organization.status.exists():
            #     status = keyObject.organization.status
            #
            #     if status.request_all_limit_count <= all_count:
            #         return False
            #
            #     if status.request_month_limit_count <= month_count:
            #         return False
            #
            #     if status.request_day_limit_count <= day_count:
            #         return False

            return True

        return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
