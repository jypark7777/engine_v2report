from inspect import Attribute
from rest_framework.serializers import ModelSerializer
from report.models.report import IGUserInfo,ReachScore, RealInfluenceScore, FeaturingScore, AudienceQuality, Engagement, DemographicsAge, DemographicsGender,AudienceIndicator,Trend,DemographicsLanguages
from report.models.statistics import ReportStatistics, PlatformSection
from rest_framework import serializers
from report.serializers.statistics import  ReportStatisticsSerializer, ReportStatisticsAttributeSerializer
from report.serializers.rank import ComponentRankStatusSerializer

class ComponentModelSerializer(ModelSerializer):
    value = serializers.SerializerMethodField('_get_value')
    ranking = serializers.SerializerMethodField('_get_ranking')
    ranking_rate = serializers.SerializerMethodField('_get_ranking_rate')

    #팔로워 그룹만
    section_ranking = serializers.SerializerMethodField('_get_section_ranking')
    section_ranking_rate = serializers.SerializerMethodField('_get_section_ranking_rate')

    section_follower_ranking = serializers.SerializerMethodField('_get_section_ranking')
    section_follower_ranking_rate = serializers.SerializerMethodField('_get_section_ranking_rate')


    rankstatuses = ComponentRankStatusSerializer(many=True)

    section_statistics = serializers.SerializerMethodField('_get_section_statistics')

    def _get_section_ranking(self,obj):
        rankstatus = obj.rankstatuses.filter(section_category=None,section_country=None).exclude(section_follower=None).last()
        if rankstatus != None and rankstatus.ranking != None:
            return rankstatus.ranking+1
        return None

    def _get_section_ranking_rate(self,obj):
        rankstatus = obj.rankstatuses.filter(section_category=None,section_country=None).exclude(section_follower=None).last()
        if rankstatus != None:
            return rankstatus.ranking_rate
        return None

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        if exclude == None:
            exclude = ('value_boolean','value_boolean_admin', 'value_int', 
            'value_int_admin', 'value_float', 'value_float_admin', 'value_char', 
            'value_char_admin', 'created_at', 'id', 'is_force_modify', 'modifier'
            )
        else:
            exclude.extend(('value_boolean','value_boolean_admin'))

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif exclude is not None:  
            for field_name in set(exclude):
                self.fields.pop(field_name)

    def truncate(self, num, n):
        integer = int(num * (10**n))/(10**n)
        return float(integer)
        
    def _get_value(self,obj):
        if obj.type == obj.TYPE_FLOAT:
            return self.truncate(obj.get_value(),6)
        return obj.get_value()

    def _get_ranking(self,obj):
        ranking, ranking_rate = obj.ranking()
        if ranking != None:
            return ranking+1
        return ranking

    def _get_ranking_rate(self,obj):
        ranking, ranking_rate = obj.ranking()
        return ranking_rate

    def _get_section_statistics(self,obj):
        if obj.ig_userinfo != None:
            statistics, attributes = obj.get_section_statistics_and_attributes()
            json = ReportStatisticsSerializer(statistics, many=False).data
            json['attributes'] = ReportStatisticsAttributeSerializer(attributes, many=True).data
            return json


        return None


    class Meta:
        exclude = ('value_boolean','value_boolean_admin')

class IGUserInfoSerializer(ModelSerializer):
    class Meta:
        model = IGUserInfo
        fields = '__all__'

class ReachScoreSerializer(ComponentModelSerializer):
    class Meta:
        model = ReachScore
        fields = '__all__'

class RealInfluenceScoreSerializer(ComponentModelSerializer):
    class Meta:
        model = RealInfluenceScore
        fields = '__all__'


class FeaturingScoreSerializer(ComponentModelSerializer):
    class Meta:
        model = FeaturingScore
        fields = '__all__'


class AudienceQualitySerializer(ComponentModelSerializer):
    class Meta:
        model = AudienceQuality
        fields = '__all__'


class EngagementSerializer(ComponentModelSerializer):
    class Meta:
        model = Engagement
        fields = '__all__'


class DemographicsGenderSerializer(ComponentModelSerializer):
    class Meta:
        model = DemographicsGender
        fields = '__all__'

class DemographicsAgeSerializer(ComponentModelSerializer):
    class Meta:
        model = DemographicsAge
        fields = '__all__'

class DemographicsLanguagesSerializer(ComponentModelSerializer):
    class Meta:
        model = DemographicsLanguages
        fields = '__all__'

class AudienceIndicatorSerializer(ComponentModelSerializer):
    class Meta:
        model = AudienceIndicator
        fields = '__all__'

class TrendSerializer(ComponentModelSerializer):
    class Meta:
        model = Trend
        fields = '__all__'

