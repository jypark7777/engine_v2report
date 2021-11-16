from datetime import timedelta
from inspect import Attribute
from rest_framework.serializers import ModelSerializer
from report.models.rank import TermRankingAccount,ComponentRankStatus
from rest_framework import serializers


class ComponentRankStatusSerializer(ModelSerializer):
    ranking = serializers.SerializerMethodField()

    section_follower = serializers.StringRelatedField()
    section_platform = serializers.StringRelatedField()
    section_category = serializers.StringRelatedField()
    section_country = serializers.StringRelatedField()

    def get_ranking(self,obj):
        if obj.ranking == None:
            return None
        return obj.ranking + 1

    class Meta:
        model = ComponentRankStatus
        exclude = ('id','section_ranking','section_ranking_rate')


class TermRankingAccountSerializer(ModelSerializer):

    previous_week = serializers.SerializerMethodField('_get_previous_week')
    previous = serializers.SerializerMethodField('_get_previous')

    def _get_previous_week(self, obj):
        is_previous = self.context.get("is_previous")
        if is_previous:
            return None
            
        preivous_define_date = obj.define_date - timedelta(days=7)
        try:
            rank = TermRankingAccount.objects.get(ig_userinfo=obj.ig_userinfo, tk_userinfo=obj.tk_userinfo, yt_channelinfo=obj.yt_channelinfo, section_follower=obj.section_follower, section_category=obj.section_category, section_country=obj.section_country, define_date=preivous_define_date)

            return TermRankingAccountSerializer(rank, context={'is_previous': True}).data

        except:
            return None

    def _get_previous(self, obj):
        is_previous = self.context.get("is_previous")
        if is_previous:
            return None

        try:
            rank = TermRankingAccount.objects.filter(ig_userinfo=obj.ig_userinfo, tk_userinfo=obj.tk_userinfo, yt_channelinfo=obj.yt_channelinfo, section_follower=obj.section_follower, section_category=obj.section_category, section_country=obj.section_country, define_date__lt=obj.define_date).exclude(ranking=None).last()

            return TermRankingAccountSerializer(rank, context={'is_previous': True}).data

        except:
            return None


    class Meta:
        model = TermRankingAccount
        exclude = ('id','section_ranking','section_ranking_rate', 'updated_at', 'ig_userinfo', 'yt_channelinfo', 'tk_userinfo')
