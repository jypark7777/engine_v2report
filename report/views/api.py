from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from report.models.api import RequestAPI
from report.permissions import HasOrganizationAPIKey
from datetime import datetime

class FeaturingJSONRenderer(JSONRenderer):

    def render(self, data, media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code

        if status_code == 200:
            jsonData = {'resultCode' : 1, 'resultMessage' : 'success'}
        elif status_code == 401:
            jsonData = {'resultCode' : 101, 'resultMessage' : '유효하지 않은 요청입니다.'}
        elif status_code == 404:
            jsonData = {'resultCode' : 200, 'resultMessage' : '데이터(리스트)가 존재하지 않습니다.'}
        else:
            jsonData = {'resultCode' : 0, 'resultMessage' : '잘못된 접근 입니다.'}

        jsonData['data'] = data

        return super().render(jsonData, media_type, renderer_context)

class DefaultAPIView(APIView):
    renderer_classes = [FeaturingJSONRenderer]
    # permission_classes = [HasOrganizationAPIKey]
    request_api = None
    callback_url = None

    def dispatch(self, request, *args, **kwargs):
        self.callback_url = request.GET.get('callback_url', None)
        self.request_api = RequestAPI.saveRequestAPI(request)

        if self.callback_url != None:
            self.request_api.callback_url = self.callback_url
            self.request_api.is_callback = True
            self.request_api.save()

        return super().dispatch(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if self.request_api != None and self.callback_url == None:
            self.request_api.complete_at = datetime.now()
            self.request_api.is_complete = True
            self.request_api.save()

        if self.callback_url != None:
            response_callback = {}
            response_callback['request_key'] = self.request_api.request_key
            response_callback['request_at'] = self.request_api.request_at
            response = Response(response_callback)

        return super().finalize_response(request,response, *args, **kwargs)

class DefaultListAPIView(DefaultAPIView):
    pass
