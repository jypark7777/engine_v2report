from django.db.models.expressions import Exists
from component.pipeline import EgDataProtocol, EgAnalyProtocol
from report.models.rank import TermRankingAccount
from report.serializers.report import AudienceIndicatorSerializer, AudienceQualitySerializer, DemographicsAgeSerializer, DemographicsGenderSerializer, EngagementSerializer, FeaturingScoreSerializer, ReachScoreSerializer, RealInfluenceScoreSerializer, TrendSerializer, DemographicsLanguagesSerializer
from report.models.report import AudienceIndicator, AudienceQuality, DemographicsAge, DemographicsGender, DemographicsLanguages, Engagement, FeaturingScore, IGUserInfo, ReachScore, RealInfluenceScore, Trend
from django.http import HttpResponse, JsonResponse
from report.views.api import DefaultAPIView, DefaultListAPIView
from datetime import datetime
from django.conf import settings
import requests
from report.models.rank import get_current_definedate
from report.serializers.rank import TermRankingAccountSerializer
from component.models.account import Account

class RequestReportComponent(DefaultAPIView):
    ig_userinfo = None 

    def updated_status_context(self, context, key, componentscore):
        if componentscore != None:
            context[key] = {
            'is_required_calculate' : componentscore.is_required_calculate(),
            'updated_at' : componentscore.updated_at,
            'version' : componentscore.version_calculate
            }
        else:
            context[key] = {
                'is_required_calculate' : True,
                'updated_at' : datetime.now(),
                'version' : -1
            }
        return context

    def get_status(self, request, username, platform, calcaulate=None):
        component = {}

        reach = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        self.updated_status_context(component, 'featuring_ranking', reach)
        self.updated_status_context(component, 'real_reach', reach)

        self.updated_status_context(component, 'featuring_score', FeaturingScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())
        self.updated_status_context(component, 'real_influence', RealInfluenceScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())

        self.updated_status_context(component, 'audience_quality', AudienceQuality.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())
        self.updated_status_context(component, 'real_engagement', Engagement.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())

        self.updated_status_context(component, 'keyword_cloud_post', None)
        self.updated_status_context(component, 'keyword_cloud_comment', None)
        self.updated_status_context(component, 'keyword_cloud_biography', None)
        self.updated_status_context(component, 'keyword_hashtag', None)

        self.updated_status_context(component, 'trend', Trend.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())
        self.updated_status_context(component, 'demographics', DemographicsGender.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())
        self.updated_status_context(component, 'audience', AudienceIndicator.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last())

        return component
    
    def get_featuring_ranking(self, request, username, platform, calcaulate=None):
        """
        피처링 랭킹
        """
        featuring_ranking = -1
        featuring_ranking_rate = 1.0

        if platform == 'ig':
            define_date = get_current_definedate()
            
            term_ranking = TermRankingAccount.objects.filter(ig_userinfo=self.ig_userinfo, define_date=define_date).last()
           
            if term_ranking == None:
                term_ranking, _ = TermRankingAccount.objects.get_or_create(ig_userinfo=self.ig_userinfo, define_date=define_date)

            # print(term_ranking.define_date, define_date)
            #산정 되어있는 랭킹이 없을때 
            # if term_ranking.ranking == None:
            component = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
            if component == None:
                component, _ = ReachScore.objects.get_or_create(ig_userinfo=self.ig_userinfo)

            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.calculate_rank()
                component.save()
            
            #랭킹 넣기
            term_ranking.ranking, term_ranking.ranking_rate = component.ranking()
            term_ranking.estimate_ranking, term_ranking.estimate_ranking_rate = TermRankingAccount.estimate_rank(term_ranking, self.ig_userinfo.json_userprofile['follower_count'])
            
            while True:
                exists = TermRankingAccount.objects.filter(define_date=define_date, estimate_ranking=term_ranking.estimate_ranking).exclude(ig_userinfo=self.ig_userinfo).exists()
                if exists: term_ranking.estimate_ranking += 1  #같은 랭킹 있을때
                else: break
            
            term_ranking.save()


            featuring_ranking = term_ranking.estimate_ranking
            featuring_ranking_rate = term_ranking.estimate_ranking_rate

            # print(term_ranking.define_date)
            serializer = TermRankingAccountSerializer(term_ranking)
            return serializer.data

        # serializer = {
        #     'featuring_ranking' : featuring_ranking,
        #     'ranking_rate'  : featuring_ranking_rate,
        #     'ranking'  : featuring_ranking,
        #     'define_date' : term_ranking.define_date,
        #     'version' : 0,
        #     'accuracy' : 1,
        # }

        return {}

    def get_real_influence(self, request, username, platform, calcaulate=None):
        """
        진짜 영향력
        """
        if platform == 'ig':
            component = RealInfluenceScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component, _ = RealInfluenceScore.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.calculate_rank()
                component.save()
            
            serializer = RealInfluenceScoreSerializer(component)

        return serializer.data



    def get_featuring_score(self, request, username, platform, calcaulate=None):
        """
        피처링 스코어
        """
        if platform == 'ig':
            component = FeaturingScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component, _ = FeaturingScore.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.calculate_rank()
                component.save()
            
            serializer = FeaturingScoreSerializer(component)

        return serializer.data

    def get_audience_quality(self, request,username, platform, calcaulate=None):
        """
        오디언스 퀄리티, 진짜 팔로워
        """
        if platform == 'ig':
            component = AudienceQuality.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component, _ = AudienceQuality.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.calculate_rank()
                component.save()
            
            serializer = AudienceQualitySerializer(component)
            
        return serializer.data
        
    def get_real_engagement(self, request,username, platform, calcaulate=None):
        """
        진짜 반응률
        """
        if platform == 'ig':
            component = Engagement.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last() 

            if component == None:
                component, _ = Engagement.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.calculate_rank()
                component.save()
            
            serializer = EngagementSerializer(component)
            
        return serializer.data
        
    def get_real_reach(self, request,username, platform, calcaulate=None):
        """
        진짜 도달수
        """
        if platform == 'ig':
            component = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component, _ = ReachScore.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.calculate_rank()
                component.save()
            
            serializer = ReachScoreSerializer(component)
            
        return serializer.data

    def get_trend(self, request,username, platform, calcaulate=None):
        """
        트렌드 데이터
        """
        context = {}
        if platform == 'ig':
            response = EgDataProtocol.request_userprofilesnap_list(self.ig_userinfo.id)
            trends = {}
            if 'results' in response and len(response['results']):
                trends['list'] = response['results']
                trends['count'] = response['count']
                # for snap in response['results']:
                #     snap['media_count']
                #     snap['follower_count']
                #     snap['following_count']
                #     snap['snap_date']

            component = Trend.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component, _ = Trend.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate or calcaulate:
                component.calculate_ig()
                component.save()
            
            serializer = TrendSerializer(component)
                
            context = serializer.data
            context['trend'] = trends['list']

        return context

    def get_demographics_age(self, request,username, platform, calcaulate=None):
        """
        연령
        """
        if platform == 'ig':
            component = DemographicsAge.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component,_ = DemographicsAge.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            print('calcaulate : ', calcaulate)
            if component.is_required_calculate() or calcaulate:
                component.calculate_ig()
                component.save()
            
            serializer = DemographicsAgeSerializer(component)
            
        return serializer.data

    def get_demographics_gender(self, request,username, platform, calcaulate=None):
        """
        성별
        """
        if platform == 'ig':
            component = DemographicsGender.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component,_ = DemographicsGender.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate() or calcaulate:
                component.calculate_ig()
                component.save()
            
            serializer = DemographicsGenderSerializer(component)
            
        return serializer.data

    def get_demographics_languages(self, request,username, platform, calcaulate=None):
        """
        언어
        """
        if platform == 'ig':
            component = DemographicsLanguages.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component,_ = DemographicsLanguages.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate() or calcaulate:
                component.calculate_ig()
                component.save()
            
            serializer = DemographicsLanguagesSerializer(component)
            
        return serializer.data


    def get_demographics(self, request, username, platform, calcaulate=None):
        """
        연령, 성별
        """
        context = {}
        context['age'] = self.get_demographics_age(request, username, platform,calcaulate)
        context['gender'] = self.get_demographics_gender(request, username, platform,calcaulate)
        context['languages'] = self.get_demographics_languages(request, username, platform,calcaulate)

        return context

        
    def get_audience(self, request,username, platform, calcaulate=None):
        """
        오디언스 정보
        """
        if platform == 'ig':
            component = AudienceIndicator.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()

            if component == None:
                component, _ = AudienceIndicator.objects.get_or_create(ig_userinfo=self.ig_userinfo)
            
            if component.is_required_calculate() or calcaulate:
                component.calculate_ig()
                component.save()
            
            serializer = AudienceIndicatorSerializer(component)
            
        return serializer.data

    def get_keyword_hashtag(self, request,username, platform, calcaulate=None):
        """
        해시태그 주요 키워드 
        """
        self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
        if platform == 'ig':
            response = EgDataProtocol.request_post_list_hashtag(self.ig_userinfo.id)
            tophashtag_posts = {}
            if 'results' in response and len(response['results']):
                tophashtag_posts['list'] = response['results']
                tophashtag_posts['count'] = response['count']

        return tophashtag_posts
        
    def get_keyword_cloud_post(self, request,username, platform, calcaulate=None):
        """
        포스팅 주요 키워드 
        """
        self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
        texts = ""
        crawlpost_list = self.ig_userinfo.json_post
        if 'results' in crawlpost_list and len(crawlpost_list['results']):
            for post in crawlpost_list['results']:
                try:
                    if 'crawlpostcaption' in post and post['crawlpostcaption'] != None and len(post['crawlpostcaption']) > 0:
                        texts += post['crawlpostcaption'][0]['text']
                except:
                    pass


        host = 'https://analy.featuringscore.ai' 
        if settings.DEBUG:
            host = 'http://localhost:8003'

        reach_url = f'{host}/text/cloud'
        value_response = requests.post(reach_url, json={'text':texts})
        value_response_json = value_response.json()

        keywords = {}
        for value in value_response_json:
            keywords[value[0]] =  value[1]


        return {'keywords' : keywords}

    def get_keyword_cloud_comment(self, request,username, platform, calcaulate=None):
        """
        댓글 주요 키워드 
        """
        self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
        
    def get_keyword_cloud_biography(self, request,username, platform, calcaulate=None):
        """
        바이오그래피 주요 키워드 
        """
        self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
        
    def get_top_hashtag_post(self, request,username, platform, calcaulate=None):
        """
        인기 해시태그에 올라온 포스팅
        """
        if platform == 'ig':
            self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
            response = EgDataProtocol.request_post_list_tophashtag(self.ig_userinfo.id)
            tophashtag_posts = {}
            if 'results' in response and len(response['results']):
                tophashtag_posts['list'] = response['results']
                tophashtag_posts['count'] = response['count']

        return tophashtag_posts

    def get_usertags_post(self, request,username, platform, calcaulate=None):
        """
        태깅된 포스팅 
        """
        if platform == 'ig':
            self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
            response = EgDataProtocol.request_post_list_usertags(self.ig_userinfo.id)
            usertags_posts = {}
            if 'results' in response and len(response['results']):
                usertags_posts['list'] = response['results']
                usertags_posts['count'] = response['count']

        return usertags_posts

    
    def get_similar_user(self, request, username, platform, calculate=None):
        if platform == 'ig':
            self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
            response = EgDataProtocol.request_user_similar_list(self.ig_userinfo.id)
            similar_users = {}
            if 'results' in response and len(response['results']):
                similar_users['list'] = response['results']
                similar_users['count'] = response['count']

        return similar_users

    def get_top_hashtag_post_user(self, request,username, platform, calcaulate=None):
        """
        인기 해시태그에 올라온 포스팅들의 유저들
        """
        if platform == 'ig':
            self.ig_userinfo = IGUserInfo.objects.filter(username=username).last()
            response = EgDataProtocol.request_post_list_tophashtag(self.ig_userinfo.id)
            tophashtag_posts = {}
            if 'results' in response and len(response['results']):
                tophashtag_posts['list'] = response['results']
                tophashtag_posts['count'] = response['count']

        return tophashtag_posts


    def get(self, request, type, username ):
        calculate = request.GET.get('calculate', None)

        self.ig_userinfo = IGUserInfo.objects.filter(username=username).last() #유저 정보 가져오기 
        response = EgDataProtocol.request_userprofile(username)
        if response != None: #유저 정보 생성
            self.ig_userinfo, _ = IGUserInfo.objects.get_or_create(id=response['insta_pk'])
            self.ig_userinfo.set_request_profile(response)
        else:
            return HttpResponse(404)
    

        platform = request.GET.get('platform', 'ig')
        result = getattr(self, f'get_{type}')(request, username, platform, calculate)

        return JsonResponse(result)



# class ReportSearch(DefaultListAPIView):
#     # def get(self, request, type, keyword):
