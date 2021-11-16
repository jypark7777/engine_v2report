from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from django.db.models import F, Value, CharField
import uuid

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class Organization(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="api_keys")

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Organization API key"
        verbose_name_plural = "Organization API keys"

class OrganizationAPIStatus(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name="status")
    last_organization_key = models.ForeignKey(OrganizationAPIKey, on_delete=models.SET_NULL, null=True, blank=True)

    request_all_limit_count = models.IntegerField(blank=True, default=100000)
    request_day_limit_count = models.IntegerField(blank=True, default=1000)
    request_month_limit_count = models.IntegerField(blank=True, default=10000)

    request_count = models.IntegerField(blank=True, default=0)

    updated_at = models.DateTimeField(verbose_name='업뎃 시간', auto_now_add=True, blank=True)
    created_at = models.DateTimeField(verbose_name='생성 시간', auto_now_add=True, blank=True)


class ApiURL(models.Model):
    request_path = models.CharField(max_length=500)
    is_permission = models.BooleanField(verbose_name='퍼미션 확인 유무', default=False, blank=True)
    is_request_limit_enable = models.BooleanField(verbose_name='요청 쿼리 제한 유무', default=False, blank=True)
    created_at = models.DateTimeField(verbose_name='생성 시간', auto_now_add=True, blank=True)
    is_enable = models.BooleanField(verbose_name='사용 유무', default=False, blank=True)

    @staticmethod
    def getApiUrl(request):
        # print('getApiUrl', request.path)
        return ApiURL.objects.annotate(path_field=Value(request.path, output_field=CharField())).filter(path_field__icontains = F('request_path'), is_enable=True).first()

    def __str__(self):
        return '%s' % (self.request_path)

class RequestLog(models.Model):
    created_at = models.DateTimeField(verbose_name='생성 시간',null=True, auto_now_add=True, blank=True)

    class Meta:
        abstract = True


class RequestAPI(RequestLog):
    request_key = models.UUIDField(default=uuid.uuid4, editable=False)

    api_url = models.ForeignKey(ApiURL, on_delete=models.SET_NULL, null=True, blank=True)

    request_path = models.CharField(max_length=500, null=True, blank=True)
    parameter = models.CharField(max_length=1000, null=True, blank=True)

    organization_key = models.ForeignKey(OrganizationAPIKey, on_delete=models.SET_NULL, null=True, blank=True)

    callback_url = models.URLField(max_length=500,null=True, blank=True)
    is_callback = models.BooleanField(verbose_name='콜백 유무', default=False, blank=True)
    is_complete = models.BooleanField(verbose_name='완료 유무', default=False, blank=True)
    request_at = models.DateTimeField(verbose_name='요청 시간', auto_now_add=True, blank=True)
    complete_at = models.DateTimeField(verbose_name='완료 시간', null=True, blank=True)

    cached_key = models.CharField(max_length=500, null=True, blank=True)
    ipaddress = models.CharField(max_length=50, null=True,blank=True, verbose_name='아이피')


    def __str__(self):
        return '%s' % (self.request_path)


    @staticmethod
    def saveRequestAPI(request):
        # pass
        from report.permissions import HasOrganizationAPIKey
        apiKey = HasOrganizationAPIKey()
        
        key = apiKey.get_key(request)
        if key == None:
            return None
        prefix, _, _ = key.partition(".")
        keyObject = apiKey.model.objects.get(prefix=prefix)

        apiUrl = ApiURL.getApiUrl(request)

        parameter = ''
        if request.method == 'GET':
            parameter = request.GET.urlencode()
        elif request.method == 'POST':
            parameter = request.POST.urlencode()

        ipaddress = get_client_ip(request)

        return RequestAPI.objects.create(api_url=apiUrl, organization_key=keyObject, request_path=request.path, parameter=parameter, ipaddress=ipaddress)
