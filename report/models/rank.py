from django.db import models
from django.conf import settings
from report.models.statistics import PlatformSection, FollowerSection, CategorySection, CountrySection
from datetime import datetime, timedelta

class RankStatus(models.Model):
    """랭킹 만들기"""
    ranking = models.BigIntegerField(verbose_name="디비 순위 (전체)", null=True, blank=True)
    ranking_rate = models.FloatField(verbose_name="디비 순위 백분위 (상위)(전체)", null=True, blank=True)

    section_ranking = models.BigIntegerField(verbose_name="섹션(팔로워,카테고리,국가) 디비 순위 (전체)", null=True, blank=True)
    section_ranking_rate = models.FloatField(verbose_name="섹션(팔로워,카테고리,국가) 디비 순위 백분위 (상위)(전체)", null=True, blank=True)

    estimate_ranking = models.BigIntegerField(verbose_name="추정 순위 (플랫폼 전체 풀)(전체)", null=True, blank=True)
    estimate_ranking_rate = models.FloatField(verbose_name="추정 순위 백분위(플랫폼 전체 풀)(전체)", null=True, blank=True)

    """
    섹션별 랭킹 
    """

    class Meta:
        abstract = True


class ComponentRankStatus(RankStatus):
    """섹션별 랭킹 만들기"""
    """없으면 전체 랭킹"""
    section_platform = models.ForeignKey(PlatformSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_follower = models.ForeignKey(FollowerSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_category = models.ForeignKey(CategorySection, on_delete=models.SET_NULL, null=True, blank=True)
    section_country = models.ForeignKey(CountrySection, on_delete=models.SET_NULL, null=True, blank=True)


def get_current_definedate():
    """매주 월요일 가져오기"""
    today = datetime.today().weekday()
    print(datetime.today(), today)
    return (datetime.today() - timedelta(days=today)).date()

class TermRankingAccount(RankStatus):
    """
    기간별 계정 산정 랭크 
    """
    ig_userinfo = models.ForeignKey('IGUserInfo', on_delete=models.SET_NULL, related_name='term_ranking' , null=True, blank=True, db_index=True)
    yt_channelinfo = models.ForeignKey('YTChannelInfo',on_delete=models.SET_NULL, related_name='term_ranking' , null=True, blank=True, db_index=True)
    tk_userinfo = models.ForeignKey('TKUserInfo', on_delete=models.SET_NULL, related_name='term_ranking' , null=True, blank=True, db_index=True)

    section_platform = models.ForeignKey(PlatformSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_follower = models.ForeignKey(FollowerSection, on_delete=models.SET_NULL, null=True, blank=True)
    section_category = models.ForeignKey(CategorySection, on_delete=models.SET_NULL, null=True, blank=True)
    section_country = models.ForeignKey(CountrySection, on_delete=models.SET_NULL, null=True, blank=True)

    define_date = models.DateField(verbose_name="기준날짜 (매주 월요일)", default=get_current_definedate)

    updated_at = models.DateTimeField(verbose_name='수정 시간', null=True, blank=True)

    @staticmethod
    def estimate_rank(term_ranking, follower_count):
        # ≥ 0 and < 500	872334
        # ≥ 500 and < 1,000	394234
        # ≥ 1,000 and < 2,000	163506
        # ≥ 2,000 and < 5,000	76235
        # ≥ 5,000 and < 10,000	74545
        # ≥ 10,000 and < 30,000	39952
        # ≥ 30,000 and < 50,000	25775
        # ≥ 50,000 and < 100,000	4513
        # ≥ 100,000 and < 200,000	3436
        # ≥ 200,000 and < 500,000	677
        # ≥ 500,000 and < 1,000,000	532
        # ≥ 1,000,000 and < 3,000,000	200
        # ≥ 3,000,000 and < +∞	1

        if follower_count >= 0 and follower_count < 500:
            estimate_ranking = 872334 + (term_ranking.ranking_rate * (24000000 - 872334))
        elif follower_count >= 500 and follower_count < 1000:
            estimate_ranking = 394234 + (term_ranking.ranking_rate * (872334 - 394234))
        elif follower_count >= 1000 and follower_count < 2000:
            estimate_ranking = 163506 + (term_ranking.ranking_rate * (394234 - 163506))
        elif follower_count >= 2000 and follower_count < 5000:
            estimate_ranking = 76235 + (term_ranking.ranking_rate * (163506 - 76235))
        elif follower_count >= 5000 and follower_count < 10000:
            estimate_ranking = 74545 + (term_ranking.ranking_rate * (76235 - 74545))
        elif follower_count >= 10000 and follower_count < 30000:
            estimate_ranking = 39952 + (term_ranking.ranking_rate * (74545 - 39952))
        elif follower_count >= 30000 and follower_count < 50000:
            estimate_ranking = 25775 + (term_ranking.ranking_rate * (39952 - 25775))
        elif follower_count >= 50000 and follower_count < 100000:
            estimate_ranking = 4513 + (term_ranking.ranking_rate * (25775 - 4513))
        elif follower_count >= 100000 and follower_count < 200000:
            estimate_ranking = 3436 + (term_ranking.ranking_rate * (4513 - 3436))
        elif follower_count >= 200000 and follower_count < 500000:
            estimate_ranking = 677 + (term_ranking.ranking_rate * (3436 - 677))
        elif follower_count >= 500000 and follower_count < 1000000:
            estimate_ranking = 532 + (term_ranking.ranking_rate * (677 - 532))
        elif follower_count >= 1000000 and follower_count < 3000000:
            estimate_ranking = 200 + (term_ranking.ranking_rate * (532 - 200))
        elif follower_count >= 3000000 and follower_count < 1000000000:
            estimate_ranking = 1 + (term_ranking.ranking_rate * (200 - 1))

        # [1, 200, 532, 677, 3436, 4513, 25775, 39952, 74545, 76235, 163506, 394234, 872334, 24000000]
        if term_ranking.ranking < 1000:
            return term_ranking.ranking, term_ranking.ranking_rate
        return int(estimate_ranking), estimate_ranking / 24000000

    class Meta:
        unique_together = ('ig_userinfo', 'tk_userinfo', 'yt_channelinfo', 'section_follower', 'section_category', 'section_country', 'define_date')
