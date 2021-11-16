from report.views.report import RequestReportComponent
from django.urls import path

urlpatterns = [
    path('component/<type>/<username>/', RequestReportComponent.as_view(), name='component')
    # path('featuring_ranking/',  get_featuring_ranking, name='featuring_ranking'),
    # path('real_influence/',  get_real_influence, name='real_influence'),
    # path('featuring_score/', get_featuring_score, name='featuring_score'),
    # path('keyword_hashtag/', get_keyword_hashtag, name='keyword_hashtag'),
    # path('keyword_cloud_post/', get_keyword_cloud_post, name='keyword_cloud_post'), 
    # path('keyword_cloud_comment/', get_keyword_cloud_comment, name='keyword_cloud_comment'),
    # path('keyword_cloud_biography/', get_keyword_cloud_biography, name='keyword_cloud_biography'),
    # path('audience_quality/', get_audience_quality, name='audience_quality'),
    # path('real_engagement/', get_real_engagement, name='real_engagement'),
    # path('real_reach/', get_real_reach, name='real_reach'),
    # path('trend/', get_trend, name='trend'),
    # path('demographics/', get_demographics, name='demographics'),
    # path('audience/', get_audience, name='audience'),
]
