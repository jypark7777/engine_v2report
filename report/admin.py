from django.contrib import admin
from django.apps import apps

from report.models.report import AudienceIndicator, AudienceQuality, DemographicsAge, DemographicsGender, DemographicsLanguages, Engagement, FeaturingScore, IGUserInfo, ReachScore, RealInfluenceScore, Trend
from django.utils.html import format_html
from django.db.models import JSONField
from jsoneditor.forms import JSONEditor

class ComponentInlineAdmin(admin.TabularInline):
    readonly_fields = ['get_value']
    fields = ['get_value', 'value_boolean_admin', 'value_int_admin', 'value_float_admin', 'value_char_admin', 'is_force_modify']


    def __init__(self, parent_model, admin_site):
        super(ComponentInlineAdmin, self).__init__(parent_model, admin_site)

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False    

    def get_fields(self, request, obj=None):
        # print(obj)
        return super(ComponentInlineAdmin, self).get_fields(request, obj)

class ReachScoreInline(ComponentInlineAdmin):
    model = ReachScore
    fields = ['get_value', 'value_int_admin', 'is_force_modify' ,'modified_at']

class RealInfluenceScoreInline(ComponentInlineAdmin):
    model = RealInfluenceScore
    fields = ['get_value', 'value_int_admin', 'is_force_modify','modified_at']

class FeaturingScoreInline(ComponentInlineAdmin):
    model = FeaturingScore
    fields = ['get_value', 'value_float_admin', 'is_force_modify','modified_at']

class AudienceQualityInline(ComponentInlineAdmin):
    model = AudienceQuality
    fields = ['get_value', 'value_float_admin', 'is_force_modify','modified_at']

class EngagementInline(ComponentInlineAdmin):
    model = Engagement
    fields = ['get_value', 'value_float_admin', 'is_force_modify','modified_at']

class DemographicsAgeInline(ComponentInlineAdmin):
    model = DemographicsAge
    fields = ['get_value', 'value_float_admin', 'is_force_modify','modified_at']

class DemographicsGenderInline(ComponentInlineAdmin):
    model = DemographicsGender
    fields = ['get_value', 'value_float_admin', 'is_force_modify','modified_at']

class DemographicsLanguagesInline(ComponentInlineAdmin):
    model = DemographicsLanguages
    fields = ['get_value', 'value_char_admin', 'is_force_modify','modified_at']

class AudienceIndicatorInline(ComponentInlineAdmin):
    model = AudienceIndicator
    fields = ['get_value', 'value_char_admin', 'is_force_modify','modified_at']

class TrendInline(ComponentInlineAdmin):
    model = Trend
    fields = ['get_value', 'value_int_admin', 'is_force_modify','modified_at']
    
    
class IGUserInfoAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = ['id', 'get_instagram_info', 'get_instagram_stat', 'get_featuring_score', 'get_real_influence', 'get_follower', 'get_real_follower', 'get_reach', 'get_avg_like', 'get_avg_comment', 'get_demographic_language', 'get_woman_rate', 'get_demographic_age']
    fields = ['id', 'username', 'section_follower', 'section_category', 'section_country', 'json_userprofile', 'json_post' , 'tags', 'crawled_at']
    readonly_fields = ['id',]

    list_per_page = 20

    formfield_overrides = {
        JSONField:{ 'widget':JSONEditor },
    }

    """피처링 스코어"""
    def get_featuring_score(self,obj): 
        try:
            featuringscore = obj.featuringscore.last()
            return int(featuringscore.get_value())
        except:
            return '-'
    get_featuring_score.short_description = "피처링 스코어"


    """진짜 영향력 가져오기"""
    def get_real_influence(self,obj): 
        try:
            realinfluencescore = obj.realinfluencescore.last()
            return realinfluencescore.get_value()
        except:
            return '-'
       
    get_real_influence.short_description = "진짜 영향력"

    """팔로워 숫자"""
    def get_follower(self,obj): 
        try:
            follower_count = obj.json_userprofile['follower_count']
            return follower_count
        except:
            return '-'
       
    get_follower.short_description = "팔로워"

    """진짜 팔로워 숫자"""
    def get_real_follower(self,obj): 
        try:
            follower_count = obj.json_userprofile['follower_count']
            audiencequality = obj.audiencequality.last()
            return int(follower_count * audiencequality.get_value())
        except:
            return '-'

    get_real_follower.short_description = "진짜 팔로워"


    """도달수 가져오기"""
    def get_reach(self,obj): 
        try:
            reachscore = obj.reachscore.last()
            return reachscore.get_value()
        except:
            return '-'
    get_reach.short_description = "평균 예측 도달수"


    """평균 좋아요"""
    def get_avg_like(self,obj): 
        try:
            reachscore = obj.reachscore.last()
            return round(reachscore.json_parameter['avg_like_count'],2)
        except:
            return '-'
    get_avg_like.short_description = "평균 좋아요"


    """평균 댓글"""
    def get_avg_comment(self,obj): 
        try:
            reachscore = obj.reachscore.last()
            return round(reachscore.json_parameter['avg_comment_count'],2)
        except:
            return '-'
    get_avg_comment.short_description = "평균 댓글수"

    """언어 비율"""
    def get_demographic_language(self,obj): 
        try:
            demographicslanguages = obj.demographicslanguages.last()
            return demographicslanguages.get_value()
        except:
            return '-'
    get_demographic_language.short_description = "오디언스 TOP 언어"

    """여성 비율"""
    def get_woman_rate(self,obj): 
        try:
            demographicsgender = obj.demographicsgender.last()
            gender = demographicsgender.get_value()
            return f"{int(gender*100)}%"
        except:
            return '-'
    get_woman_rate.short_description = "여성 비율 (%)"

    """오디언스 연령 TOP"""
    def get_demographic_age(self,obj): 
        try:
            demographicsage = obj.demographicsage.last()
            avg_age = demographicsage.get_value()
            return f"{int(avg_age/10)*10}대"
        except:
            return '-'
    get_demographic_age.short_description = "오디언스 연령대"
    
    def get_instagram_info(self,obj):
        if obj.json_userprofile:
            return format_html(f"{obj.username} (<span style='color:gray; font-size:0.5rem;'>{obj.json_userprofile['full_name']}</span>)")
    get_instagram_info.short_description = '인스타그램 기본정보'

    def get_instagram_stat(self,obj):
        if obj.json_userprofile:
            return format_html(f"""
                    팔로워 : {obj.json_userprofile['follower_count']}<br>
                    팔로잉 : {obj.json_userprofile['following_count']}<br>
                    팔로잉 : {obj.json_userprofile['following_count']}<br>
                """)
    get_instagram_stat.short_description = '인스타그램 수치'

    inlines = (ReachScoreInline, AudienceIndicatorInline, AudienceQualityInline, DemographicsAgeInline, DemographicsGenderInline, DemographicsLanguagesInline, EngagementInline, FeaturingScoreInline, RealInfluenceScoreInline)


admin.site.register(IGUserInfo, IGUserInfoAdmin)

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)

class ListModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(ListModelAdmin, self).__init__(model, admin_site)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        if 'django.' not in str(model) and __package__ in str(model):
            admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
