from django.db import models
from django.conf import settings
from datetime import datetime
import inspect, requests
from django.db.models import Avg, Q, Count
from django.contrib.postgres.aggregates.general import ArrayAgg

class PlatformSection(models.Model):
    TYPE_INSTAGRAM = 0
    TYPE_YOUTUBE = 1
    TYPE_TIKTOK = 2

    platform_type = (
        (TYPE_INSTAGRAM, '인스타그램'),
        (TYPE_YOUTUBE, '유튜브'),
        (TYPE_TIKTOK, '틱톡'),
    )
    type = models.IntegerField(choices=platform_type, unique=True)


    CODE_INSTAGRAM = 'ig'
    CODE_YOUTUBE = 'yt'
    CODE_TIKTOK = 'tk'
    PLATFORM_CODE_CHOICES = [
        (CODE_INSTAGRAM, 'Instagram'),
        (CODE_YOUTUBE, 'Youtube'),
        (CODE_TIKTOK, 'Tiktok'),
    ]
    
    platform_code = models.CharField(max_length=5, choices=PLATFORM_CODE_CHOICES, unique=True)

    @staticmethod
    def get_platform_section(platform_code):
        return PlatformSection.objects.get_or_create(platform_code=platform_code)[0]

    def __str__(self):
        return f'{self.get_type_display()}({self.platform_code})'


class FollowerSection(models.Model):
    min_follower = models.IntegerField(verbose_name="이상 값", null=True, blank=True)
    max_follower = models.IntegerField(verbose_name="미만 값", null=True, blank=True)

    @staticmethod
    def get_follower_section(follower_count):
        return FollowerSection.objects.filter(min_follower__lte=follower_count, max_follower__gt=follower_count).last()

    def __str__(self):
        return f'{self.min_follower} 이상 ~ {self.max_follower} 미만'

class CategorySection(models.Model):
    title = models.CharField(max_length=25)
    category_code = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.title}({self.category_code})'


class CountrySection(models.Model):
    title = models.CharField(max_length=25)
    country_code = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.title}({self.country_code})'

class ReportStatistics(models.Model):
    section_platform = models.ForeignKey(PlatformSection, on_delete=models.CASCADE, null=True, blank=True)
    section_follower = models.ForeignKey(FollowerSection, on_delete=models.CASCADE, null=True, blank=True)
    section_category = models.ForeignKey(CategorySection, on_delete=models.CASCADE, null=True, blank=True)
    section_country = models.ForeignKey(CountrySection, on_delete=models.CASCADE, null=True, blank=True)

    date = models.DateField(verbose_name='기준 날짜', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='갱신일')

    class Meta:
        unique_together = ('section_platform', 'section_follower', 'section_category', 'section_country', 'date')

    def __str__(self):
        return f'[{self.section_platform}] {self.section_follower} {self.section_category} {self.section_country} - {self.date}'

    @staticmethod
    def get_statistics(section_platform, section_follower, section_category, section_country):
        statistics = ReportStatistics.objects.filter(section_platform=section_platform, section_follower=section_follower, section_category=section_category, section_country=section_country).last()

        return statistics


    @staticmethod
    def update_statistics(section_platform, section_follower, section_category, section_country):
        statistics, _ = ReportStatistics.objects.get_or_create(section_platform=section_platform, section_follower=section_follower, section_category=section_category, section_country=section_country, date=datetime.now())
        
        from report.models import report 

        for name, obj in inspect.getmembers(report):
            if inspect.isclass(obj):
                parent = obj.__bases__
                try:
                    index = parent.index(report.ComponentScore)
                    filterQ = Q()

                    if section_platform != None and section_platform == PlatformSection.get_platform_section('ig'):
                        if section_follower != None:
                            filterQ &= Q(ig_userinfo__section_follower=section_follower)
                        
                        if section_category != None:
                            filterQ &= Q(ig_userinfo__section_category=section_category)
                        
                        if section_country != None:
                            filterQ &= Q(ig_userinfo__section_country=section_country)
                    elif section_platform != None and section_platform == PlatformSection.get_platform_section('yt'):
                        if section_follower != None:
                            filterQ &= Q(yt_channelinfo__section_follower=section_follower)
                        
                        if section_category != None:
                            filterQ &= Q(yt_channelinfo__section_category=section_category)
                        
                        if section_country != None:
                            filterQ &= Q(yt_channelinfo__section_country=section_country)


                   
                    #기본 지표 계산 (평균)
                    data = obj.objects.filter(filterQ).all().aggregate(Count('value_int'),Count('value_float'), Avg('value_int'), Avg('value_float'))

                    value = 0.0
                    if data['value_float__count'] < data['value_int__count']:
                        value = data['value_int__avg']
                    else:
                        value = data['value_float__avg']

                    # print(f'{statistics} - {name} : {value}' )

                    if value != None:
                        name = "%s_%s" % (ReportStatisticsAttribute.PREFIEX_TYPE_AVG,obj.__name__.lower())
                        ReportStatisticsAttribute.update_attr(statistics, name, value)
                    
                    for statistics_value in obj.statistics_values:
                        data = obj.objects.filter(filterQ).all().aggregate(Avg(statistics_value))
                        value = data[f'{statistics_value}__avg']
                        print(name, value)
                        name = "%s_%s_%s" % (ReportStatisticsAttribute.PREFIEX_TYPE_AVG,obj.__name__.lower(),statistics_value)
                        ReportStatisticsAttribute.update_attr(statistics, name, value)
                        
                    
                except ValueError:
                    pass


class ReportStatisticsAttribute(models.Model):
    
    PREFIEX_TYPE_AVG = "average"

    statistics = models.ForeignKey(ReportStatistics, on_delete=models.CASCADE, related_name='attributes')

    name = models.CharField(max_length=100, verbose_name='속성명', null=True, blank=True)
    value = models.FloatField(default=0, verbose_name='속성값')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='갱신일')

    @staticmethod
    def update_attr(statistics,name,value):
        attr, _ = ReportStatisticsAttribute.objects.get_or_create(statistics=statistics, name=name)
        attr.value = value
        attr.save()

    @staticmethod
    def get_value(statistics, name):
        try:
            attr = ReportStatisticsAttribute.objects.get(statistics=statistics, name=name)
            return attr.value
        except:
            return 0

    def __str__(self):
        return f"{self.name} - {self.value}"

    class Meta:
        unique_together = ('statistics', 'name')
