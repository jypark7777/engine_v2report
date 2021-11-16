from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.serializers import Serializer
from report.views.api import DefaultAPIView
from component.pipeline import EgDataProtocol, EgAnalyProtocol
from component.models.content import IgStatisticsContent, Content
from component.models.account import Account, Category, IgStatisticsProfile, Tag
from collections import Counter
from component.serializers import TagSerializer

"""
분류하기
"""
def classifier_user(username, is_force=False):
    """유저의 포스팅을 분류함
        Args:
            is_force : 기존에 되있던 것 무시하고 강제로 분석 
    """
    context = {}

    crawluserprofile = EgDataProtocol.request_userprofile(username)
    insta_pk = crawluserprofile['insta_pk']
    if crawluserprofile == None:
        return None

    # 계정 정보 가져오기 
    account, _ = Account.objects.get_or_create(ig_pk=insta_pk) 
    stat_profile, _ = IgStatisticsProfile.objects.get_or_create(account=account)

    crawlpost_list = EgDataProtocol.request_post_list(insta_pk) #포스팅 가져오기
    if crawlpost_list != None:
        results = crawlpost_list['results']
        context['post_list'] = list()
        
        for crawlpost in results: #포스팅들 분석
            post_insta_pk = crawlpost['insta_pk']
            
            if post_insta_pk == None: 
                continue
            
            # 콘텐츠(포스팅) 정보 가져오기 
            content, _ = Content.objects.get_or_create(ig_pk=post_insta_pk)
            stat_content, _ = IgStatisticsContent.objects.get_or_create(content=content, account=account)
            
            if stat_content.is_tag_classification == False or is_force:
                stat_content.classifier(crawlpost) #분류 분석!                    
                
            serializer = TagSerializer(stat_content.tags.all(), many=True)
            context['post_list'].append(serializer.data)
    
    if stat_profile.is_tag_classification == False or is_force:
        stat_profile.classifier(crawluserprofile) #분류 분석!            
    
    serializer = TagSerializer(stat_profile.tags.all(), many=True)
    context['user'] = serializer.data

    return context

class RequestUserTag(DefaultAPIView):

    def get(self, request, username):
        context = classifier_user(username)
        if context == None:
            return HttpResponse(status=404)
        return JsonResponse(context)
                
