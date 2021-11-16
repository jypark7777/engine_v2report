from django.core.management import BaseCommand
from report.models.report import ReachScore, IGUserInfo, ComponentScore
from report.models.statistics import FollowerSection, ReportStatistics, PlatformSection
import requests
import inspect
from report.models import report 
from django.db.models import Avg, Count
from report.make_stat import rank_ig_user

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        랭크 계산 
        """
        # for ig_userinfo in IGUserInfo.objects.all():
        #     ig_userinfo.request_ig_userinfo()
        #     rank_ig_user(ig_userinfo.pk)
        
        
        """
        Username 없는것 찾기 
        """
        # ig_userinfo = IGUserInfo.objects.filter(username=None).delete()
        # print(ig_userinfo)
        
        """
        통계 값 내기
        """
        # section_followers = FollowerSection.objects.filter().all()

        # for section_follower in section_followers:
        #     ReportStatistics.update_statistics(PlatformSection.get_platform_section('ig'), section_follower, None, None)
                    