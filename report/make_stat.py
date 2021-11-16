from django.core.management import BaseCommand
from report.models.report import *
from instagram_score.models import Userinfo, Scorev1
from component.pipeline import EgDataProtocol, EgAnalyProtocol
import requests, traceback

def make_status_ig_user(username, insta_pk=None):
    crawluserprofile = EgDataProtocol.request_userprofile(username, insta_pk)
    if crawluserprofile != None: #유저 정보 생성
        username = crawluserprofile['username']
        ig_userinfo, _ = IGUserInfo.objects.get_or_create(id=crawluserprofile['insta_pk'])
        ig_userinfo.set_request_profile(crawluserprofile)

        component, _ = ReachScore.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] ReachScore : {value}')


        component, _ = AudienceQuality.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] AudienceQuality : {value}')


        component, _ = RealInfluenceScore.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] RealInfluenceScore : {value}')



        component, _ = Engagement.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] Engagement : {value}')

        
        component, _ = FeaturingScore.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] FeaturingScore : {value}')


        component, _ = DemographicsAge.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] DemographicsAge : {value}')

        
        component, _ = DemographicsGender.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] DemographicsGender : {value}')

        component, _ = DemographicsLanguages.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] DemographicsLanguages : {value}')
        
        component, _ = Trend.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] Trend : {value}')


        component, _ = AudienceIndicator.objects.get_or_create(ig_userinfo=ig_userinfo)
        value = component.calculate_ig()
        component.calculate_rank()
        component.save()
        print(f'[{username}] AudienceIndicator : {value}')

def rank_ig_user(insta_pk=None):
    if IGUserInfo.objects.filter(pk=insta_pk).exists():
        ig_userinfo = IGUserInfo.objects.get(pk=insta_pk)
        component = ReachScore.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()

        component = RealInfluenceScore.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()


        component = AudienceQuality.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()


        component = Engagement.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()

        
        component = FeaturingScore.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()


        component = DemographicsAge.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()

        
        component = DemographicsGender.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()

        component = DemographicsLanguages.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()
        
        component = Trend.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()


        component = AudienceIndicator.objects.get(ig_userinfo=ig_userinfo)
        component.calculate_rank()
        component.save()
        print(f'[{ig_userinfo.username}] Rank Complete')            