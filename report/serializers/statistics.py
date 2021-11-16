from inspect import Attribute
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from report.models.statistics import ReportStatistics, ReportStatisticsAttribute

class ReportStatisticsAttributeSerializer(ModelSerializer):
    # statistics = ReportStatisticsSerializer(many=False)

    class Meta:
        model = ReportStatisticsAttribute
        exclude = ('id',)

class ReportStatisticsSerializer(ModelSerializer):
    
    section_follower = serializers.StringRelatedField()
    section_platform = serializers.StringRelatedField()
    section_category = serializers.StringRelatedField()
    section_country = serializers.StringRelatedField()

    # attributes = ReportStatisticsAttributeSerializer(many=True)

    class Meta:
        model = ReportStatistics
        exclude = ('id','updated_at')

