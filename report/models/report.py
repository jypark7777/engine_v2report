from re import X
from django.db import models
from django.conf import settings
from django.db.models.deletion import SET_NULL
from django.db.models.expressions import Value
from component.models.account import Tag
from report.models.rank import ComponentRankStatus
from django.contrib.postgres.fields import ArrayField
from instagram_score.models import Reportv1
from report.models.exceptions import ReachDoesNotExist, EngagementDoesNotExist,RealInfluenceDoesNotExist,AudienceQualityDoesNotExist
import requests, json
import pandas as pd
import numpy as np
from scipy.stats import poisson
from report.models.statistics import PlatformSection, FollowerSection,CategorySection,CountrySection, ReportStatistics
from django.db.models import Avg, Q, Count
from component.models.account import Account
from component.pipeline import EgAnalyProtocol, EgDataProtocol
from report.calculator import cal_realfake_weight


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정 시간', auto_now=True, blank=True)

    modified_at = models.DateTimeField(verbose_name='어드민 수정 시간', null=True, blank=True)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='유저', null=True, blank=True, related_name='%(class)s',on_delete=models.DO_NOTHING, db_constraint=False)
    is_force_modify = models.BooleanField(verbose_name='어드민 수정값 고정하기', help_text='엔진 분석데이터 변화로 변경되지 않도록 값을 고정 합니다.', default=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True


class IGUserInfo(BaseModel):
    account = models.ForeignKey(Account, related_name='userinfo', on_delete=SET_NULL, null=True)

    id = models.BigIntegerField(verbose_name="Insta PK",primary_key=True)
    username = models.CharField(max_length=50, verbose_name='인스타 유저 네임',null=True, blank=True, db_index=True)

    section_follower = models.ForeignKey(FollowerSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_category = models.ForeignKey(CategorySection, on_delete=models.SET_NULL, null=True, blank=True)
    section_country = models.ForeignKey(CountrySection, on_delete=models.SET_NULL, null=True, blank=True)

    crawled_at = models.DateTimeField(verbose_name='수집 시간', blank=True, null=True)

    json_userprofile = models.JSONField(null=True, blank=True)
    json_post = models.JSONField(null=True, blank=True)

    def set_request_profile(self, crawluserprofile):
        self.json_userprofile = crawluserprofile

        self.username = crawluserprofile['username']
        self.crawled_at = crawluserprofile['updated_time']
        
        if self.account == None:
            self.account, _ = Account.objects.get_or_create(ig_pk=crawluserprofile['insta_pk'])

        #통계 데이터 저장
        follower_count = crawluserprofile['follower_count']
        section_follower = FollowerSection.get_follower_section(follower_count)
        self.section_follower = section_follower
        self.save()

    def request_ig_userinfo(self):
        """
        유저 정보 가져오기 
        """
        crawluserprofile = EgDataProtocol.request_userprofile(self.username, self.id)
        self.set_request_profile(crawluserprofile)
        
        return crawluserprofile
    
    def request_ig_post(self):
        """
        유저 정보 가져오기 
        """
        crawlpost_list = EgDataProtocol.request_post_list(self.id)

        self.json_post = crawlpost_list
        self.save()

        return crawlpost_list

    class Meta:
        verbose_name = '인스타그램 계정'
        verbose_name_plural = '인스타그램 계정들'


class YTChannelInfo(BaseModel):
    # account = models.ForeignKey(Account, related_name='userinfo') #컴포넌트 연결은 나중에 
    
    section_follower = models.ForeignKey(FollowerSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_category = models.ForeignKey(CategorySection, on_delete=models.SET_NULL, null=True, blank=True)
    section_country = models.ForeignKey(CountrySection, on_delete=models.SET_NULL, null=True, blank=True)

    crawled_at = models.DateTimeField(verbose_name='수집 시간', blank=True, null=True)

class TKUserInfo(BaseModel):
    # account = models.ForeignKey(Account, related_name='userinfo') #컴포넌트 연결은 나중에 

    section_follower = models.ForeignKey(FollowerSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_category = models.ForeignKey(CategorySection, on_delete=models.SET_NULL, null=True, blank=True)
    section_country = models.ForeignKey(CountrySection, on_delete=models.SET_NULL, null=True, blank=True)
    
    crawled_at = models.DateTimeField(verbose_name='수집 시간', blank=True, null=True)

class ComponentScore(BaseModel):
    """
    피처링의 모든 지표는 위의 모델을 상속 받는다. 

     (*) 계산식 산출 프로세스
     
     1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무
      1-1 : 기존 산술 결과 활용 가능
        가. 기존 산술식의 Engine 데이터가 존재
        나. 기존 산술식 계산에 필요한 최소 데이터가 있으면 ===> [결과로 저장]
      1-2 : 불가능 => 다음 프로세스로 이동


     2. 산술식의 최신 저장 데이터로 계산 할 수 있는지 유무
      2-1 : 최신 저장 데이터로 계산 가능하며 최신 데이터가 있을때
        가. 최신 저장 데이터 기반 * ex)팔로워수 변화로 신규 데이터 ===> [결과로 저장]
      2-2 : 최신 저장 데이터로 계산 불가능 => 다음 프로세스로 이동

    
     3. 기반 계산 지표(ex, 도달수)로 계산 하는 지표 인지 확인 
      3-1 : 기반 지표(ex, 도달수)로 계산되는 지표(ex, 진짜 영향력)일떄 
        가. 기반 지표 유무 확인, 없으면 => Exception
        나. 최소 필요 데이터 없으면 => 다음 프로세스로 이동
        다. 기반 지표 + 최소 필요 데이터로 계산 하여 신규 데이터 ===> [결과로 저장]
     
     4. 비슷한 집단의 평균치로 계산하는 지표 인지 확인 (디폴트값)

    
    """
    ig_userinfo = models.ForeignKey(IGUserInfo, on_delete=models.SET_NULL, related_name='%(class)s' , null=True, blank=True, db_index=True)
    yt_channelinfo = models.ForeignKey(YTChannelInfo,on_delete=models.SET_NULL, related_name='%(class)s' , null=True, blank=True, db_index=True)
    tk_userinfo = models.ForeignKey(TKUserInfo, on_delete=models.SET_NULL, related_name='%(class)s' , null=True, blank=True, db_index=True)

    json_parameter = models.JSONField(verbose_name='계산식 관련 원형 데이터', null=True, blank=True)

    
    rankstatuses = models.ManyToManyField(ComponentRankStatus, blank=True)


    """
    지표 계산 버전 
    """
    VERSION_REACH_BASE = 0
    VERSION_FEATURING_ENGINE = 1
    VERSION_CRAWL_BASE = 2
    VERSION = (
        (VERSION_REACH_BASE, '도달수 기반 계산'),
        (VERSION_FEATURING_ENGINE, '기존 피처링 엔진'),
        (VERSION_CRAWL_BASE, '수집된 데이터 기반'),
    )
    version_type = models.IntegerField(default=-1, choices=VERSION, blank=True)
    version_calculate = models.IntegerField(verbose_name="적용된 계산식 버전", default=-1, blank=True)

    crawled_at = models.DateTimeField(verbose_name='계산될때 기준 수집 시간', blank=True, null=True)


    """
    정확도
    """
    ACCURACY_VERYLOW_DEFAULT = 0
    ACCURACY_LOW = 1
    ACCURACY_MID = 2
    ACCURACY_HIGH = 3
    ACCURACY_VERY_HIGH = 4
    ACCURACY = (
        (ACCURACY_VERYLOW_DEFAULT, '매우낮음 (기본 초기값으로 설정)'),
        (ACCURACY_LOW, '낮음'),
        (ACCURACY_MID, '중간'),
        (ACCURACY_HIGH, '높음'),
        (ACCURACY_VERY_HIGH, '매우 높음'),
    )
    accuracy = models.IntegerField(verbose_name="정확도", choices=ACCURACY, default=-1, blank=True)

    TYPE_BOOL = 0
    TYPE_INT = 1
    TYPE_FLOAT = 2
    TYPE_CHAR = 3


    """
    지표 값들 타입
    """
    VALUE_TYPE = (
        (TYPE_BOOL, 'bool'),
        (TYPE_INT, 'int'),
        (TYPE_FLOAT, 'float'),
        (TYPE_CHAR, 'char'),
    )
    type = models.IntegerField(choices=VALUE_TYPE, default=TYPE_BOOL, blank=True)

    """
    지표 값들 (타입별로 정의 하여 한가지만 사용)
    """
    value_boolean = models.BooleanField(null=True, blank=True)
    value_boolean_admin = models.BooleanField(null=True, blank=True)

    value_int = models.BigIntegerField(null=True, blank=True, db_index=True)
    value_int_admin = models.BigIntegerField(null=True, blank=True)

    value_float = models.FloatField(null=True, blank=True, db_index=True)
    value_float_admin = models.FloatField(null=True, blank=True)

    value_char = models.CharField(max_length=1000, null=True, blank=True, db_index=True)
    value_char_admin = models.FloatField(max_length=1000, null=True, blank=True)

    """
    기반 지표 설정
    상속 받는 지표들은 구성하는 기반지표를 아래 List로 지정해야함 
    """
    parent_components = [] 

    """
    통계 지표 설정 
    각 상속받는 지표의 value 들은 기본으로 들어감
    """
    statistics_values = []
    
    def prepare_calculate(self):
        """
        계산하기전 데이터 상태 체크
        """
        
    def is_required_calculate(self):
        """
        계산이 필요한지 체크
        """
        if self.version_calculate < self.VERSION_CALCULATE:
            return True

        crawled_at = None
        if self.ig_userinfo == None:
            crawled_at = self.ig_userinfo.crawled_at

        if crawled_at != None and self.updated_at < crawled_at:
            return True


        """기반 지표들이 업데이트 되었으면 해당 지표도 업데이트 필요"""
        if len(self.parent_components) > 0:
            for parent_component in self.parent_components: # 지표들 
                component = getattr(self, parent_component)
                if component != None and component.updated_at > self.updated_at: #업데이트 날짜가 더 높으면 업데이트 필요 
                    return True
        
        return False

    def save(self, *args, **kwargs):
        """
        Value 타입 설정
        """
        if self.value_boolean != None: self.type = self.TYPE_BOOL
        elif self.value_int != None: self.type = self.TYPE_INT
        elif self.value_float != None: self.type = self.TYPE_FLOAT
        elif self.value_char != None: self.type = self.TYPE_CHAR

        #유저정보의 수집된 시간 
        if self.ig_userinfo != None:
            self.crawled_at = self.ig_userinfo.crawled_at

        super(ComponentScore, self).save(*args, **kwargs)

    def set_value(self, value):     

        if(type(value) is int): 
            self.type = self.TYPE_INT
            self.value_int = value
        elif(type(value) is float or type(value) is np.float64): 
            self.type = self.TYPE_FLOAT
            self.value_float = value
        elif(type(value) is bool): 
            self.type = self.TYPE_BOOL
            self.value_bool = value
        elif(type(value) is str): 
            self.type = self.TYPE_CHAR
            self.value_char = value

    def get_value(self):
        """
        Value 타입에 따라 리턴
        """
        value = None
        if self.type == self.TYPE_BOOL:
            value = self.value_boolean 
            if self.value_boolean_admin != None and (self.is_force_modify or (self.modified_at != None and self.modified_at > self.crawled_at)):
                value = self.value_boolean_admin
        
        if self.type == self.TYPE_INT:
            value = self.value_int 
            if self.value_int_admin != None and (self.is_force_modify or (self.modified_at != None and self.modified_at > self.crawled_at)):
                value = self.value_int_admin

        if self.type == self.TYPE_FLOAT:
            value = self.value_float 
            if self.value_float_admin != None and (self.is_force_modify or (self.modified_at != None and self.modified_at > self.crawled_at)):
                value = self.value_float_admin

        if self.type == self.TYPE_CHAR:
            value = self.value_char 
            if self.value_char_admin != None and (self.is_force_modify or (self.modified_at != None and self.modified_at > self.crawled_at)):
                value = self.value_char_admin
        
        return value

    get_value.short_description = '계산 값'


    def ranking(self) -> tuple:
        """전체 랭킹 순위"""
        rankstatus = self.get_rank_section(PlatformSection.get_platform_section('ig'))
        return rankstatus.ranking, rankstatus.ranking_rate
    
    def section_ranking(self) -> tuple:
        """섹션 랭킹 순위"""
        rankstatus = self.get_rank_section(PlatformSection.get_platform_section('ig'), self.ig_userinfo.section_follower, self.ig_userinfo.section_category, self.ig_userinfo.section_country)
        return rankstatus.ranking, rankstatus.ranking_rate
    

    def get_rank_section(self, section_platform, section_follower=None, section_category=None, section_country=None) -> ComponentRankStatus:
        """
            랭킹 테이블 값 가져오기 
            Args:
                section_follower : 팔로워
        """
        rankstatus = self.rankstatuses.filter(section_follower=section_follower, section_category=section_category, section_country=section_country).last()
        # print(rankstatus)
        if rankstatus == None:
            rankstatus = ComponentRankStatus.objects.create(section_platform=section_platform, section_follower=section_follower,section_category=section_category,section_country=section_country)
            # print(section_platform, section_follower, section_country)
            self.rankstatuses.add(rankstatus)
        

        return rankstatus

    


    def calculate_rank_section(self, section_platform,  section_follower, section_category, section_country):
        value = self.get_value()

        rankstatus = self.get_rank_section(section_platform, section_follower, section_category, section_country) #전체 랭킹

        filterQ = Q()

        if section_follower != None:
            if section_platform.type == section_platform.TYPE_INSTAGRAM:
                filterQ &= Q(ig_userinfo__section_follower=section_follower)

        if section_category != None:
            if section_platform.type == section_platform.TYPE_INSTAGRAM:
                filterQ &= Q(ig_userinfo__section_category=section_category)

        if section_country != None:
            if section_platform.type == section_platform.TYPE_INSTAGRAM:
                filterQ &= Q(ig_userinfo__section_country=section_country)

        filterQ &= Q(version_calculate=self.VERSION_CALCULATE)

        model = type(self)
        if self.type == self.TYPE_INT:
            rankstatus.ranking = model.objects.filter(filterQ,value_int__gt=value).order_by('-value_int').count()

        if self.type == self.TYPE_FLOAT:
            rankstatus.ranking = model.objects.filter(filterQ, value_float__gt=value).order_by('-value_float').count()

        if rankstatus.ranking != None:
            count = model.objects.filter(filterQ).count()

            if count == 0:
                count = 1 
            rankstatus.ranking_rate = float(rankstatus.ranking / count)
        
        rankstatus.save()


    def calculate_rank(self):
        """랭킹 계산하기"""
        value = self.get_value()

        if value == None:
            return None

        model = type(self)

        """전체 랭킹 계산"""
        rankstatus = self.get_rank_section(PlatformSection.get_platform_section('ig')) #전체 랭킹 

        if self.type == self.TYPE_INT:
            rankstatus.ranking = model.objects.filter(version_calculate=self.VERSION_CALCULATE, value_int__gt=value).order_by('-value_int').count()

        if self.type == self.TYPE_FLOAT:
            rankstatus.ranking = model.objects.filter(version_calculate=self.VERSION_CALCULATE, value_float__gt=value).order_by('-value_float').count()

        if rankstatus.ranking != None:
            count = model.objects.filter(version_calculate=self.VERSION_CALCULATE).count()
            if count == 0:
                count = 1 
            rankstatus.ranking_rate = float(rankstatus.ranking / count)

        """전체 공통 섹션 랭킹 계산"""
        self.calculate_rank_section(PlatformSection.get_platform_section('ig'), self.ig_userinfo.section_follower, self.ig_userinfo.section_category, self.ig_userinfo.section_country)

        """카테고리+국가 랭킹 계산"""
        self.calculate_rank_section(PlatformSection.get_platform_section('ig'), None, self.ig_userinfo.section_category, self.ig_userinfo.section_country)

        """팔로워+국가 랭킹 계산"""
        self.calculate_rank_section(PlatformSection.get_platform_section('ig'), self.ig_userinfo.section_follower, None, self.ig_userinfo.section_country)

        

    
    def get_avg_similar_count_and_value(self) -> tuple:
        """비슷한 계정들의 지표 평균값 가져오기
            @Return count, avg_value
        """
    
        crawlusersimilar = None
        user_id = self.ig_userinfo.pk
        if user_id != None:
            """비슷한 계정 가져오기"""
            similar_user_ids = []

            crawlusersimilar = EgDataProtocol.request_user_similar_list(user_id)
            if crawlusersimilar != None and crawlusersimilar['count'] > 0:
                for result in crawlusersimilar['results']:
                    if 'user' in result and result['user'] != None:
                        similar_user_ids.append(result['user']['insta_pk'])

            avg_value = 0
            avg_value_count = 0 #평균 추출한 비슷한 계정의 수

            if len(similar_user_ids) > 0: #비슷한 계정이 있을때
                obj_cls = self.__class__
                data = obj_cls.objects.filter(ig_userinfo__pk__in=similar_user_ids).all().aggregate(Count('value_int'),Count('value_float'), Avg('value_int'), Avg('value_float')) #비슷한 계정들의 평균값 가져오기

                value = 0.0
                if data['value_float__count'] < data['value_int__count']:
                    value = data['value_int__avg']
                    avg_value_count = data['value_int__count']
                else:
                    value = data['value_float__avg']
                    avg_value_count = data['value_float__count']

                if value != None and value > 0.0:
                    avg_value = value #비슷한 계정들의 평균값

                
            return avg_value_count, avg_value

    def get_avg_section_value(self):
        """같은 섹션에 있는 인플루언서 평균값 가져오기"""
        statistics, attributes = self.get_section_statistics_and_attributes()  
        return attributes.last().value

    
    def get_section_statistics_and_attributes(self) -> tuple:
        """해당 지표의 연관 통계값들과 통계지표 가져오기
           @Return statistics, attributes
        """
        if self.ig_userinfo != None:
            statistics = ReportStatistics.get_statistics(section_platform = PlatformSection.get_platform_section('ig'), 
                section_follower = self.ig_userinfo.section_follower, 
                section_category = self.ig_userinfo.section_category, 
                section_country = self.ig_userinfo.section_country
                )

            obj_cls = self.__class__

            # print(, obj_cls.__name__.lower())
            if statistics == None:
                return None, None
            attributes = statistics.attributes.filter(name__contains=obj_cls.__name__.lower()).all()
            return statistics, attributes

        
    class Meta:
        abstract = True
        unique_together = ('ig_userinfo', 'tk_userinfo', 'yt_channelinfo')

class ReachScore(ComponentScore):
    """
    도달 - 기준 지표
    """
    VERSION_CALCULATE = 0 #계산식 버전

    reach_sales = models.BigIntegerField(verbose_name="도달 예상 매출", null=True, blank=True) #도달 예상 매출 (원화)
    campaign_price = models.BigIntegerField(verbose_name="캠페인 예상 제휴 단가", null=True, blank=True) #캠페인 예상 제휴 단가 (원화)

    def calculate_ig(self):
        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- X
        """
        # 유저 정보 가져오기 
        crawluserprofile = self.ig_userinfo.request_ig_userinfo()
        json_parameter = {}
        
        # 팔로워 숫자
        json_parameter['follower_count'] = crawluserprofile['follower_count']
        
        # 포스팅 정보 가져오기 
        crawlpost_list = self.ig_userinfo.request_ig_post()


        """
        (*) 계산식 산출 프로세스
            2. 산술식의 최신 저장 데이터로 계산 할 수 있는지 유무 --- X
        """
        #최신 데이터로 계산함. 



        """
        (*) 계산식 산출 프로세스
            3. 기반 계산 지표(ex, 도달수)로 계산 하는 지표 인지 확인 --- O 
        """
        sum_like_count = 0
        sum_comment_count = 0
        sum_hashtag_count = 0
        sum_mention_count = 0
        sum_comment_like_rate = 0
        sum_text_length = 0
        like_counts = []
        zero_like_count = -1
        zero_comment_count = -1

        success_post_count = 0
        
        # print(crawlpost_list)
        if 'results' in crawlpost_list and len(crawlpost_list['results']):
            for post in crawlpost_list['results']:
                try:
                    like_count = post['like_count']
                    comment_count = post['comment_count']
                    
                    if 'crawlpostcaption' in post and post['crawlpostcaption'] != None and len(post['crawlpostcaption']) > 0:
                        text = post['crawlpostcaption'][0]['text']
                        hashtag_count = len(text.split('#'))-1
                        sum_hashtag_count += hashtag_count

                        sum_text_length += len(text)

                    if 'accessibility_caption' in post and post['accessibility_caption'] != None:
                        caption = post['accessibility_caption']
                        mention_count = len(caption.split('@'))-1
                        sum_mention_count += mention_count
                        
                    like_counts.append(like_count)
                    sum_like_count += like_count
                    sum_comment_count += comment_count

                    # 댓글 좋아요 비율
                    if like_count == 0: 
                        like_count = 1
                    sum_comment_like_rate += (comment_count/like_count)

                    # 좋아요 0개 카운팅
                    if like_count == 0: 
                        if zero_like_count == -1:
                            zero_like_count = 0
                        zero_like_count += 1
                     
                     # 댓글 0개 카운팅
                    if comment_count == 0: 
                        if zero_comment_count == -1:
                            zero_comment_count = 0
                        zero_comment_count += 1

                    success_post_count += 1
                except:
                    pass

            # print(success_post_count)
            if success_post_count > 0:
                json_parameter['success_post_count'] = success_post_count
                json_parameter['avg_hashtag_count'] = sum_hashtag_count/success_post_count
                json_parameter['avg_mention_count'] = sum_mention_count/success_post_count
                json_parameter['avg_like_count'] = sum_like_count/success_post_count
                json_parameter['avg_comment_count'] = sum_comment_count/success_post_count
                json_parameter['avg_comment_like_rate'] = sum_comment_like_rate/success_post_count
                json_parameter['avg_text_length'] = sum_text_length/success_post_count
                json_parameter['zero_like_count'] = zero_like_count
                json_parameter['zero_comment_count'] = zero_comment_count
                media_textcount = crawluserprofile['media_count'] * json_parameter['avg_text_length'] / 1000

                #반응 평균값들 구하기
                like_counts.sort()
                min_count = int(len(like_counts)/3)
                if min_count > 0:
                    json_parameter['avg_min_like_count'] = sum(like_counts[:min_count]) / min_count
                else:
                    json_parameter['avg_min_like_count'] = json_parameter['avg_like_count']
                json_parameter['effort_performance'] = (json_parameter['follower_count']*5+(json_parameter['avg_comment_count']*3+json_parameter['avg_like_count'])*crawluserprofile['media_count']) / media_textcount / 1000


                value_response_json = EgAnalyProtocol.request_calculator_reach(crawluserprofile, crawlpost_list['results'], json_parameter['avg_like_count'], json_parameter['avg_comment_count'])

                reach_value = int(value_response_json['value'])
                if reach_value < 0:
                    reach_value = int(json_parameter['avg_like_count']*json_parameter['avg_comment_count']/2)


                #예상 매출액
                like_mean = np.mean(like_counts)
                like_std = np.std(like_counts)
                if like_std > like_mean:
                    half_score = 0.1
                elif like_std < like_mean * 0.075:
                    half_score = 0.01
                else:
                    half_score = abs(min(1, like_std / like_mean))

                currencyfactor = 20000 #이만원 기준
                if crawluserprofile['follower_count'] > 1000000:
                    currencyfactor = 5000
                if crawluserprofile['follower_count'] > 10000000:
                    currencyfactor = 2000

                sales = poisson.interval(0.999999, half_score * like_mean)
                poisson.interval(0.99, like_std)
            
                self.reach_sales = int((sales[0]+sales[1])/2) * currencyfactor

                #캠페인 견적 
                currencyfactor = 1000 #천원 기준
                cal = (crawluserprofile['follower_count']/100+reach_value/10)/2
                cal = cal - (cal%5)
                self.campaign_price = cal * currencyfactor
                
                self.set_value(reach_value)
                self.version_type = self.VERSION_CRAWL_BASE

        # print(json_parameter)

        # 기본값 설정하기
        if self.value_int == None:
            # print(json_parameter)
            if 'follower_count' in json_parameter and json_parameter['follower_count'] != None :
                value = json_parameter['follower_count'] * 0.37
            self.set_value(int(value))
        
        self.version_calculate = self.VERSION_CALCULATE
        self.json_parameter = json_parameter

        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 도달수({self.get_value()})'

    class Meta:
        verbose_name = '도달수'
        verbose_name_plural = '도달수'
    
ReachScore._meta.get_field('value_int').verbose_name = '도달수'
ReachScore._meta.get_field('value_int_admin').verbose_name = '도달수(수정)'



class RealInfluenceScore(ComponentScore):
    """
    진짜 영향력
    """
    VERSION_CALCULATE = 0 #계산식 버전

    """
    기반지표 설정
    """
    audience_quality = models.ForeignKey('AudienceQuality', on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)
    reach = models.ForeignKey(ReachScore, on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)
    parent_components = ['reach', 'audience_quality'] #기반지표 (기반지표가 업데이트 되면 해당 지표도 업데이트 필요 체크하기 위함)

    def calculate_ig(self):
        # username = self.ig_userinfo.username
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()
        
        follower_count = self.ig_userinfo.json_userprofile['follower_count']
        json_parameter = {} 


        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- X
        """
        # if reportV1 != None and reportV1.score != None: 
        #     json_parameter['legacy_main_score'] = reportV1.score.main_score
        #     follower_count = reportV1.userinfo.follower_count
            
        #     self.value_int = reportV1.score.main_score
        #     self.version_type = self.VERSION_FEATURING_ENGINE
        #     self.accuracy == self.ACCURACY_HIGH
        

        
        """
        (*) 계산식 산출 프로세스
            2. 산술식의 최신 저장 데이터로 계산 할 수 있는지 유무 --- X
        """
        # if self.value_int and follower_count: #도달수 데이터 혹은 피처링 엔진데이터의 팔로워 데이터가 있을때, 계산 기준 지표 설정
        #     json_parameter['main_score_rate'] = self.value_int/follower_count


        """
        (*) 계산식 산출 프로세스
            3. 기반 계산 지표(ex, 도달수)로 계산 하는 지표 인지 확인 --- O
            4. 비슷한 집단의 평균치로 계산하는 지표 인지 확인 (디폴트값) --- O 
        """
        #계산지표 확인 
        self.reach = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.reach == None:
            raise ReachDoesNotExist()
        
        self.audience_quality = AudienceQuality.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.audience_quality == None:
            raise AudienceQualityDoesNotExist()
            
        if self.reach != None:  #기존 데이터 없을때
            follower_count = self.reach.json_parameter['follower_count']
            # if self.json_parameter != None and 'main_score_rate' in self.json_parameter and self.json_parameter['main_score_rate'] > 0.0: #기존 계산된 계삭데이터가 있으면 (main_score_rate - 계산 기준 지표)
            #     self.value_int = follower_count * self.json_parameter['main_score_rate']
            # else: #신규 계산
            reach_value = self.reach.get_value() #도달수
            audience_quality_value = self.audience_quality.get_value() #오디언스 퀄리티
            # print('audience_quality_value : ', audience_quality_value)

            mix_value = reach_value * 0.20 * audience_quality_value #도달수 * 구매 전환율(기본 - 20%) * 오디언스 퀄리티

            avg_similar_count, avg_similar_value = self.get_avg_similar_count_and_value() #비슷한 계정들(인스타) 평균값
            
            grades = [self.get_avg_section_value(), avg_similar_value, mix_value] # 섹션 평균, 비슷한 계정들 평균, 산출 값
            # print('realinfleuce : ' , grades)
            weights = [10, avg_similar_count/20, 50] # 섹션 평균, 비슷한 계정들 평균 (가중치 / 20), 산출 값 각 가중치
            value = round(sum([grades[i]*weights[i] for i in range(len(grades))])/sum(weights),2)

            # print(avg_similar_value, mix_value, value)

            self.value_int = int(value)
            json_parameter['main_score_rate'] = float(self.value_int/follower_count)

            self.accuracy == self.ACCURACY_MID
            self.version_type = self.VERSION_CRAWL_BASE
        

        self.set_value(int(self.value_int))
        self.version_calculate = self.VERSION_CALCULATE
        self.json_parameter = json_parameter
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 진짜 영향력({self.get_value()})'

    class Meta:
        verbose_name = '진짜 영향력'
        verbose_name_plural = '진짜 영향력'

RealInfluenceScore._meta.get_field('value_int').verbose_name = '진짜 영향력'
RealInfluenceScore._meta.get_field('value_int_admin').verbose_name = '진짜 영향력(수정)'


class FeaturingScore(ComponentScore):
    """
    피처링 스코어
    """
    VERSION_CALCULATE = 0 #계산식 버전

    real_influence = models.ForeignKey('RealInfluenceScore', on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)
    audience_quality = models.ForeignKey('AudienceQuality', on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)
    engagement = models.ForeignKey('Engagement', on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)
    reach = models.ForeignKey(ReachScore, on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)

    """
    기반지표 설정
    """
    parent_components = ['reach', 'real_influence', 'audience_quality', 'engagement']  #기반지표 (기반지표가 업데이트 되면 해당 지표도 업데이트 필요 체크하기 위함)
 
    def calculate_ig(self):
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()
        
        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- X
        """
        # if reportV1 != None: #기존 피처링 엔진 데이터
        #     self.version_type = self.VERSION_FEATURING_ENGINE

        """
        (*) 계산식 산출 프로세스
            2. 산술식의 최신 저장 데이터로 계산 할 수 있는지 유무 --- X
        """



        """
        (*) 계산식 산출 프로세스
            3. 기반 계산 지표(ex, 도달수)로 계산 하는 지표 인지 확인 --- O 
        """
        #계산지표 확인 
        self.reach = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.reach == None:
            raise ReachDoesNotExist()

        self.real_influence = RealInfluenceScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.real_influence == None:
            raise RealInfluenceDoesNotExist()

        self.audience_quality = AudienceQuality.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.audience_quality == None:
            raise AudienceQualityDoesNotExist()

        self.engagement = Engagement.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.engagement == None:
            raise EngagementDoesNotExist()

        if self.reach != None: # 도달수 기반
            self.version_type = self.VERSION_REACH_BASE


        _ , factor1 = self.real_influence.ranking()
        _ , factor2 = self.audience_quality.ranking()
        _ , factor3 = self.engagement.ranking()
        _ , factor4 = self.reach.ranking()

        # print(factor1, factor2,factor3, factor4)

        reach_complx_values = [factor1, factor2, factor3, factor4] #도달 
        weights = [0.2, 0.3, 0.4, 0.1]
        score = round(sum([reach_complx_values[i]*weights[i] for i in range(len(reach_complx_values))])/sum(weights),2)

        featuring_score = 1.0 - score
        # print('factor_score : ' , featuring_score, factor1,factor2,factor3,factor4)
        if score < 0.0:
            score = 0.01
        elif score > 1.0:
            score = 0.99
        
        # print(score)
        self.set_value(featuring_score * 100)
        
        self.version_calculate = self.VERSION_CALCULATE
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 피처링 스코어({self.get_value()})'

    class Meta:
        verbose_name = '피처링 스코어'
        verbose_name_plural = '피처링 스코어'
            
FeaturingScore._meta.get_field('value_float').verbose_name = '피처링 스코어'
FeaturingScore._meta.get_field('value_float_admin').verbose_name = '피처링 스코어(수정)'



class AudienceQuality(ComponentScore):
    """
    오디언스 퀄리티
    """
    VERSION_CALCULATE = 1 #계산식 버전
    reach = models.ForeignKey(ReachScore, on_delete=models.CASCADE, verbose_name='[계산지표] 도달', null=True, blank=True)
    parent_components = ['reach']  #기반지표 (기반지표가 업데이트 되면 해당 지표도 업데이트 필요 체크하기 위함)

    follower_count = models.IntegerField(null=True, blank=True)
    real_follower_count = models.IntegerField(null=True, blank=True)
    
    def calculate_ig(self):
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()
        value = None

        self.follower_count = self.ig_userinfo.json_userprofile['follower_count']
        
        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- O
        """
        if reportV1 != None and self.follower_count > 0: #기존 피처링 엔진 데이터, 팔로워 숫자 0보다 큼
            audience = reportV1.audience.order_by('-created_at').last()
            if audience != None and audience.real_audience_rate != None:
                value = float(audience.real_audience_rate)
                self.accuracy = self.ACCURACY_HIGH
                self.version_type = self.VERSION_FEATURING_ENGINE
        
        """
        (*) 계산식 산출 프로세스
            3. 기반 계산 지표(ex, 도달수)로 계산 하는 지표 인지 확인 --- O 
            4. 비슷한 집단의 평균치로 계산하는 지표 인지 확인 (디폴트값) --- O 
        """
        #계산지표 확인 
        self.reach = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.reach == None:
            raise ReachDoesNotExist()

        if self.reach != None and value == None:
            self.version_type = self.VERSION_REACH_BASE
            self.accuracy = self.ACCURACY_VERYLOW_DEFAULT
            
            avg_similar_count, avg_similar_value = self.get_avg_similar_count_and_value() #비슷한 계정들(인스타) 평균값
            
            grades = [self.get_avg_section_value(), avg_similar_value] # 섹션 평균, 비슷한 계정들 평균, 산출 값
            weights = [5, avg_similar_count] # 섹션 평균, 비슷한 계정들 평균, 산출 값 각 가중치
            value = round(sum([grades[i]*weights[i] for i in range(len(grades))])/sum(weights),2)
            
            _ , reach_section_ranking_rate = self.reach.section_ranking()
            #도달수 랭킹 백분위로 가중치 넣기
            reach_complx_values = [1.0 - reach_section_ranking_rate, value] #도달 
            weights = [5, 8]
            value = round(sum([reach_complx_values[i]*weights[i] for i in range(len(reach_complx_values))])/sum(weights),2)

            if self.ig_userinfo.json_userprofile['is_verified'] == True: #검증된 계정 (인스타 파란뱃지)
                value = value * 1.2 # 20프로 증가 
            else:
                # if 'effort_performance' in self.reach.json_parameter and self.reach.json_parameter['effort_performance'] > 20: #노력대비 성과가 너무 좋을때 
                #     value = value * 0.8 # 80프로로 감소 
                
                # 노력대비 성과, 댓글 0개, 댓글-좋아요 비율로 가짜 확률 구하기 
                if 'effort_performance' in self.reach.json_parameter and 'zero_comment_count' in self.reach.json_parameter:
                    zero_comment_count = self.reach.json_parameter['zero_comment_count']
                    if zero_comment_count == -1:
                        zero_comment_count = 0
                    realfake_weight = cal_realfake_weight(self.reach.json_parameter['effort_performance'], zero_comment_count, self.reach.json_parameter['avg_comment_like_rate'])
                    # print('realfake_weight : ', self.reach.json_parameter['avg_comment_like_rate'])

                    value = value - (realfake_weight/2) # 계산된 가짜 확률 가중치 값만큼 진짜비율에서 빼줌 
                    if value < 0.0:
                        value = 0.1

                if 'zero_comment_count' in self.reach.json_parameter and self.reach.json_parameter['zero_comment_count'] > 0: #댓글이 한개도 안달린 게시물 수
                    zero_comment_count = self.reach.json_parameter['zero_comment_count']
                    zero_percent_list = np.arange(0.0,0.26,0.02)  # 0.0 0.02, 0.04 .. 0.026 [12]
                    print(zero_comment_count,zero_percent_list)
                    value = value * (1.0 - zero_percent_list[zero_comment_count]) 

            if value > 1.0:
                value = 0.95
            value = float(value)

        self.real_follower_count = self.follower_count * value
        self.set_value(value)
        self.version_calculate = self.VERSION_CALCULATE
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 진짜 팔로워({self.get_value()})'

    class Meta:
        verbose_name = '진짜 팔로워'
        verbose_name_plural = '진짜 팔로워'

AudienceQuality._meta.get_field('value_float').verbose_name = '진짜 팔로워 비율'
AudienceQuality._meta.get_field('value_float_admin').verbose_name = '진짜 팔로워 비율(수정)'



class Engagement(ComponentScore):
    """
    반응률
    """
    VERSION_CALCULATE = 0 #계산식 버전
    reach = models.ForeignKey(ReachScore, on_delete=models.CASCADE, verbose_name='[계산지표] 반응률', null=True, blank=True)
    parent_components = ['reach']  #기반지표 (기반지표가 업데이트 되면 해당 지표도 업데이트 필요 체크하기 위함)

    like_engagement_rate = models.FloatField(null=True, blank=True)
    comment_engagement_rate = models.FloatField(null=True, blank=True)

    statistics_values = ['like_engagement_rate', 'comment_engagement_rate']

    def calculate_ig(self):
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()
        json_userprofile = self.ig_userinfo.json_userprofile
        if json_userprofile != None:
            follower_count = json_userprofile['follower_count']
        
        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- X
        """
        # if reportV1 != None:
        #     engagement = reportV1.engagement.order_by('-created_at').last()
        #     if engagement != None:
        #         self.value_float = engagement.engagement_rate
        #         if follower_count != None:
        #             if follower_count > 0:
        #                 self.like_engagement_rate = engagement.avg_post_likes/follower_count
        #                 self.comment_engagement_rate = engagement.avg_post_comment/follower_count
        #             else:
        #                 self.like_engagement_rate = 0
        #                 self.comment_engagement_rate = 0
        #         self.version_type = self.VERSION_FEATURING_ENGINE

        """
        (*) 계산식 산출 프로세스
            3. 기반 계산 지표(ex, 도달수)로 계산 하는 지표 인지 확인 --- O 
        """
        #계산지표 확인 
        self.reach = ReachScore.objects.filter(ig_userinfo=self.ig_userinfo).order_by('-updated_at').last()
        if self.reach == None:
            raise ReachDoesNotExist()


        if self.reach != None: #리포트 값이 없을때
            reach_json_parameter = self.reach.json_parameter        
            avg_like_count = reach_json_parameter['avg_like_count']
            avg_comment_count = reach_json_parameter['avg_comment_count']

            # print(avg_like_count,avg_comment_count,follower_count )
            
            if follower_count != None:
                if follower_count > 0:
                    self.like_engagement_rate = avg_like_count/follower_count
                    self.comment_engagement_rate = avg_comment_count/follower_count
                    self.value_float = (avg_like_count + avg_comment_count)/follower_count
                else:
                    self.like_engagement_rate = 0
                    self.comment_engagement_rate = 0
                    self.value_float = 0
            self.version_type = self.VERSION_REACH_BASE
        
        self.version_calculate = self.VERSION_CALCULATE
        # print(self.value_float)
        self.set_value(self.value_float)
        return self.get_value()
    
    def __str__(self):
        return f'{self.ig_userinfo.username} 반응({self.get_value()})'

    class Meta:
        verbose_name = '진짜 반응률'
        verbose_name_plural = '진짜 반응률'

Engagement._meta.get_field('value_float').verbose_name = '평균 반응률'
Engagement._meta.get_field('value_float_admin').verbose_name = '평균 반응률(수정)'



class DemographicsAge(ComponentScore):
    """
    오디언스 데모그래픽 - 나이
    """
    VERSION_CALCULATE = 0 #계산식 버전

    all_age_counts = ArrayField(models.IntegerField(), verbose_name='나이 갯수(갯수 콤마로 구분)', help_text='10대, 20대초반, 20대후반, 30대초반, 30대후반, 40대, 50대이상', null=True, blank=True, size=7)
    all_age_rates = ArrayField(models.FloatField(), verbose_name='나이 비율(1.0~0.0)', help_text='10대, 20대초반, 20대후반, 30대초반, 30대후반, 40대, 50대이상', null=True, blank=True, size=7)

    man_age_counts = ArrayField(models.IntegerField(), verbose_name='남자 나이 갯수(갯수 콤마로 구분)', help_text='10대, 20대초반, 20대후반, 30대초반, 30대후반, 40대, 50대이상', null=True, blank=True, size=7)
    man_age_rates = ArrayField(models.FloatField(), verbose_name='남자 나이 비율(1.0~0.0)', help_text='10대, 20대초반, 20대후반, 30대초반, 30대후반, 40대, 50대이상', null=True, blank=True, size=7)

    woman_age_counts = ArrayField(models.IntegerField(), verbose_name='여자 나이 갯수(갯수 콤마로 구분)', help_text='10대, 20대초반, 20대후반, 30대초반, 30대후반, 40대, 50대이상', null=True, blank=True, size=7)
    woman_age_rates = ArrayField(models.FloatField(), verbose_name='여자 나이 비율(1.0~0.0)', help_text='10대, 20대초반, 20대후반, 30대초반, 30대후반, 40대, 50대이상', null=True, blank=True, size=7)

    def calculate_ig(self):
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()

        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- O
        """
        #기존 리포트로 계산
        if reportV1 != None:
            demographics = reportV1.demographics.order_by('-created_at').last()
            if demographics != None:
                self.all_age_counts = list(map(int,demographics.all_age_ratetext.split(',')))
                self.man_age_counts = list(map(int,demographics.man_age_ratetext.split(',')))
                self.woman_age_counts = list(map(int,demographics.woman_age_ratetext.split(',')))

                self.all_age_rates = demographics.all_age_ratetext.split(',')
                self.man_age_rates = demographics.man_age_ratetext.split(',')
                self.woman_age_rates = demographics.woman_age_ratetext.split(',')
                self.accuracy = self.ACCURACY_HIGH #기존 리포트에 가져온 데이터면 정확도 높음

        """
        (*) 계산식 산출 프로세스
            4. 비슷한 집단의 평균치로 계산하는 지표 인지 확인 (디폴트값) --- O 
        """
        #기본값 설정
        if self.all_age_counts == None or sum(self.all_age_counts) == 0 or\
            self.man_age_counts == None or sum(self.man_age_counts) == 0 or\
                self.woman_age_counts == None or sum(self.woman_age_counts) == 0:

            self.all_age_rates = [0.0] * 7
            self.man_age_rates = [0.0] * 7
            self.woman_age_rates = [0.0] * 7

            self.all_age_counts = [1,4,4,3,2,1,1]
            self.man_age_counts = [0,1,2,1,1,1,0]
            self.woman_age_counts = [1,3,3,2,2,1,1]
            self.accuracy = self.ACCURACY_VERYLOW_DEFAULT #초기값으로 


        age_sum = 0
        age_count_sum = 0
        all_age_counts_sum = sum(self.all_age_counts)
        man_age_counts_sum = sum(self.man_age_counts)
        woman_age_counts_sum = sum(self.woman_age_counts)
        age_indexs = [10,20,28,32,36,40,55]
        for index, age_count in enumerate(self.all_age_counts): #10대(18~24), 20대중반(24~28), 20대후반(28~32), 30대중반(32~36), 30대후반(36~40), 40대, 50대이상
            age_index = age_indexs[index]
            age_sum += age_index * int(age_count)
            age_count_sum += int(age_count)

            self.all_age_rates[index] = self.all_age_counts[index]/all_age_counts_sum
            self.man_age_rates[index] = self.man_age_counts[index]/man_age_counts_sum
            self.woman_age_rates[index] = self.woman_age_counts[index]/woman_age_counts_sum
        
        self.value_float = age_sum/age_count_sum
        

        self.version_calculate = self.VERSION_CALCULATE
        self.set_value(self.value_float)
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 연령({self.get_value()})'

    class Meta:
        verbose_name = '연령'
        verbose_name_plural = '연령'

DemographicsAge._meta.get_field('value_float').verbose_name = '평균 연령'
DemographicsAge._meta.get_field('value_float_admin').verbose_name = '평균 연령(수정)'


class DemographicsGender(ComponentScore):
    """
    오디언스 데모그래픽 - 성별
    """
    VERSION_CALCULATE = 0 #계산식 버전

    def calculate_ig(self):
        # username = self.ig_userinfo.username
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()
        
        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- O
        """
        if reportV1 != None:
            demographics = reportV1.demographics.order_by('-created_at').last()
            if demographics != None and demographics.woman_rate != None:
                self.value_float = float(demographics.woman_rate)
        
        """
        (*) 계산식 산출 프로세스
            4. 비슷한 집단의 평균치로 계산하는 지표 인지 확인 (디폴트값) --- O 
        """
        if self.value_float == None:
            avg_similar_count, avg_similar_value = self.get_avg_similar_count_and_value() #비슷한 계정들(인스타) 평균값
            
            grades = [self.get_avg_section_value(), avg_similar_value] # 섹션 평균, 비슷한 계정들 평균, 산출 값
            weights = [5, avg_similar_count] # 섹션 평균, 비슷한 계정들 평균, 산출 값 각 가중치
            value = round(sum([grades[i]*weights[i] for i in range(len(grades))])/sum(weights),2)

            self.value_float = value


        self.version_calculate = self.VERSION_CALCULATE
        self.set_value(self.value_float)
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 성별({self.get_value()})'

    class Meta:
        verbose_name = '성별'
        verbose_name_plural = '성별'

DemographicsGender._meta.get_field('value_float').verbose_name = '여자 비율'
DemographicsGender._meta.get_field('value_float_admin').verbose_name = '여자 비율(수정)'

class DemographicsLanguages(ComponentScore):
    """
    오디언스 데모그래픽 - 언어
    """
    VERSION_CALCULATE = 0 #계산식 버전

    language_code = ArrayField(models.CharField(max_length=12), verbose_name='언어 코드 (ko, en..)', null=True, blank=True, size=5)
    language_code_counts = ArrayField(models.IntegerField(), verbose_name='언어 코드 숫자', null=True, blank=True, size=5)
    language_code_rates = ArrayField(models.FloatField(), verbose_name='언어 코드 비율', null=True, blank=True, size=5)

    def calculate_ig(self):
        # username = self.ig_userinfo.username
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()

        self.value_char = None


        codes = []
        codes_rate = []
        codes_count = []
        
        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- O
        """
        if reportV1 != None:
            demographics = reportV1.demographics.order_by('-created_at').last()
            if demographics != None:
                languages = demographics.languages.order_by('-language_count').all()
                if languages != None and len(languages) > 0:
                    max_count = 0
                    
                    for language in languages:
                        codes.append(language.language_code)
                        codes_count.append(language.language_count)
                        codes_rate.append(language.language_rate)

                        # print(language.language_code, language.language_count)


                        if max_count < language.language_count:
                            self.value_char = language.language_code
                            max_count = language.language_count

        if len(codes) == 0:
            crawlpost_list = self.ig_userinfo.json_post

            if 'results' in crawlpost_list and len(crawlpost_list['results']):
                texts = ""
                for post in crawlpost_list['results']:
                    try:
                        if 'crawlpostcaption' in post and post['crawlpostcaption'] != None and len(post['crawlpostcaption']) > 0:
                            texts += post['crawlpostcaption'][0]['text']
                    except:
                        pass


                # post_data = {
                #     "text" : texts,
                # }
                # text_languages_url = f'{self._get_analy_serverhost()}/text/languages' #포스팅 언어 분석 
                # value_response = requests.post(text_languages_url, json=post_data)
                value_response_json = EgAnalyProtocol.request_text_languages(texts)
                # if value_response.status_code == 200:
                if value_response_json != None:
                    max_count = 0
                    if len(value_response_json) > 0:
                        for language in value_response_json: # [{'code': 'ko', 'confidence': 95.0}]
                            codes.append(language['code'])
                            codes_count.append(language['confidence'])
                            codes_rate.append(language['confidence']/100)

                            if max_count < language['confidence']:
                                self.value_char = language['code']
                                max_count = language['confidence']
                                            
                    # print(value_response_json)

        self.language_code = codes
        self.language_code_rates = codes_rate
        self.language_code_counts = codes_count

        self.version_calculate = self.VERSION_CALCULATE
        self.set_value(self.value_char)
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 언어({self.get_value()})'

    class Meta:
        verbose_name = '언어'
        verbose_name_plural = '언어'

DemographicsLanguages._meta.get_field('value_char').verbose_name = '주요 언어 코드'
DemographicsLanguages._meta.get_field('value_char_admin').verbose_name = '주요 언어 코드(수정)'


class AudienceIndicator(ComponentScore):
    """
    오디언스 각 정보
    """
    VERSION_CALCULATE = 0 #계산식 버전

    avg_follower_count = models.FloatField(verbose_name='평균 팔로워 수', null=True, blank=True)
    avg_following_count = models.FloatField(verbose_name='평균 팔로워 수', null=True, blank=True)
    avg_media_count = models.FloatField(verbose_name='평균 팔로워 수', null=True, blank=True)
    avg_like_count = models.FloatField(verbose_name='평균 좋아요 수', null=True, blank=True)
    avg_comment_count = models.FloatField(verbose_name='평균 댓글 수', null=True, blank=True)

    audience_business_rate = models.FloatField(verbose_name='오디언스 비즈니스 계정 비율', null=True, blank=True)
    audience_aggressive_rate = models.FloatField(verbose_name='적극적인 오디언스 비율', null=True, blank=True)

    def calculate_ig(self):
        # username = self.ig_userinfo.username
        user_id = self.ig_userinfo.id
        reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()

        """
        (*) 계산식 산출 프로세스
            1. 기존 산술식(엔진v1)을 활용 할 수 있는지 유무 --- O
        """
        if reportV1 != None:
            audienceindicator = reportV1.audienceindicator.order_by('-created_at').last()
            if audienceindicator != None:
                self.avg_follower_count = audienceindicator.avg_follower_count
                self.avg_following_count = audienceindicator.avg_following_count
                self.avg_media_count = audienceindicator.avg_media_count
                self.avg_like_count = audienceindicator.avg_like_count
                self.avg_comment_count = audienceindicator.avg_comment_count

            audience = reportV1.audience.order_by('-created_at').last()
            if audience != None:
                self.audience_business_rate = audience.audience_business_rate
                self.audience_aggressive_rate = audience.audience_aggressive_rate

            audiencetendency = reportV1.audiencetendency.order_by('-created_at').last()
            if audiencetendency != None:
                self.value_char = audiencetendency.following_purpose.name
            
    
        if self.value_char == None:
            self.version_calculate = self.VERSION_CALCULATE
            self.value_char = '포스팅'

        self.set_value(self.value_char)
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 오디언스 지표({self.get_value()})'

    class Meta:
        verbose_name = '오디언스 지표'
        verbose_name_plural = '오디언스 지표'

AudienceIndicator._meta.get_field('value_char').verbose_name = '팔로잉 목적'
AudienceIndicator._meta.get_field('value_char_admin').verbose_name = '팔로잉 목적(수정)'


class Trend(ComponentScore):
    """
    트렌드 변화
    """
    VERSION_CALCULATE = 0 #계산식 버전

    def calculate_ig(self):
        # username = self.ig_userinfo.username
        user_id = self.ig_userinfo.id
        # reportV1 = Reportv1.objects.filter(userinfo__user_id=user_id).last()
        
        snap_list = EgDataProtocol.request_userprofilesnap_list(user_id)
        follower_counts = []
        snap_dates = []
        if snap_list['count'] > 0:
            for result in snap_list['results']:
                if 'follower_count' in result and result['follower_count'] != None:
                    follower_counts.append(result['follower_count'])
                    snap_dates.append(result['snap_date'])

        """초당 팔로워 증가율 구하기"""
        if len(follower_counts) > 1:
            df_plot = pd.DataFrame({
                    "Date" : pd.to_datetime(snap_dates),
                    "Follower" : np.array(follower_counts, dtype=np.uint32),
            })

            df_plot['Seconds'] = (pd.to_datetime(df_plot['Date']) - pd.Timestamp.now().normalize()).dt.total_seconds()
            # print(df_plot)
            pf = np.polyfit(df_plot['Seconds'], df_plot['Follower'], 1) #기울기,절편

            growth_rate = pf[0]*3600*12 # 12시간 동안 오른 팔로어 숫자
            if growth_rate > 100:
                growth_rate = growth_rate
        else:
            growth_rate = 30

        self.version_calculate = self.VERSION_CALCULATE
        self.value_int = int(growth_rate)

        self.set_value(self.value_int)
        return self.get_value()

    def __str__(self):
        return f'{self.ig_userinfo.username} 성장성({self.get_value()})'

    class Meta:
        verbose_name = '성장성'
        verbose_name_plural = '성장성'

Trend._meta.get_field('value_int').verbose_name = '성장성'
Trend._meta.get_field('value_int_admin').verbose_name = '성장성 (수정)'