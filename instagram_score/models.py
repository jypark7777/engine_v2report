# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Brandattribute(models.Model):
    attribute_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    attribute_type = models.ForeignKey('Brandattributetype', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_brandattribute'


class Brandattributetype(models.Model):
    attribute_type_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_brandattributetype'


class Categorybridge(models.Model):
    name = models.CharField(max_length=100)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_categorybridge'


class Commenttype(models.Model):
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()
    name = models.CharField(max_length=50)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_commenttype'


class CommenttypeCategorys(models.Model):
    commenttype = models.ForeignKey(Commenttype, models.DO_NOTHING)
    categorybridge = models.ForeignKey(Categorybridge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_commenttype_categorys'
        unique_together = (('commenttype', 'categorybridge'),)


class Filtercategory(models.Model):
    filter_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_filtercategory'


class FiltercategoryCategorys(models.Model):
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)
    categorybridge = models.ForeignKey(Categorybridge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_filtercategory_categorys'
        unique_together = (('filtercategory', 'categorybridge'),)


class Followertype(models.Model):
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()
    name = models.CharField(max_length=50)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_followertype'


class FollowertypeCategorys(models.Model):
    followertype = models.ForeignKey(Followertype, models.DO_NOTHING)
    categorybridge = models.ForeignKey(Categorybridge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_followertype_categorys'
        unique_together = (('followertype', 'categorybridge'),)


class Influencersection(models.Model):
    section = models.IntegerField(unique=True)
    min_follower = models.IntegerField()
    max_follower = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_influencersection'


class Influencersectionsummary(models.Model):
    profile_count = models.IntegerField()
    report_count = models.IntegerField()
    avg_follower_count = models.FloatField()
    avg_following_count = models.FloatField()
    avg_post_count = models.FloatField()
    created_at = models.DateTimeField()
    section = models.ForeignKey(Influencersection, models.DO_NOTHING, blank=True, null=True)
    avg_post_comment = models.FloatField()
    avg_post_likes = models.FloatField()
    avg_likercommenter_rate = models.FloatField()
    avg_likercommenterfollower_rate = models.FloatField()
    avg_post_real_comment = models.FloatField()
    avg_post_real_likes = models.FloatField()

    class Meta:
        managed = False
        db_table = 'instagram_score_influencersectionsummary'


class Listupcomponent(models.Model):

    class Meta:
        managed = False
        db_table = 'instagram_score_listupcomponent'


class Listupinfo(models.Model):
    key = models.CharField(unique=True, max_length=8, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    component = models.ForeignKey(Listupcomponent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_listupinfo'


class ListupinfoReports(models.Model):
    listupinfo = models.ForeignKey(Listupinfo, models.DO_NOTHING)
    reportv1 = models.ForeignKey('Reportv1', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_listupinfo_reports'
        unique_together = (('listupinfo', 'reportv1'),)


class Outputmetriclog(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    input_users_length = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    complete_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_outputmetriclog'


class Postcampaigntype(models.Model):
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'instagram_score_postcampaigntype'


class PostcampaigntypeCategorys(models.Model):
    postcampaigntype = models.ForeignKey(Postcampaigntype, models.DO_NOTHING)
    categorybridge = models.ForeignKey(Categorybridge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_postcampaigntype_categorys'
        unique_together = (('postcampaigntype', 'categorybridge'),)


class Posttype(models.Model):
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()
    name = models.CharField(max_length=50)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_posttype'


class PosttypeCategorys(models.Model):
    posttype = models.ForeignKey(Posttype, models.DO_NOTHING)
    categorybridge = models.ForeignKey(Categorybridge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_posttype_categorys'
        unique_together = (('posttype', 'categorybridge'),)


class Reportbrandcalsnap(models.Model):
    usertags_count = models.IntegerField()
    usertags_increases = models.FloatField()
    cal_like = models.IntegerField()
    likes_increses = models.FloatField()
    follower_count = models.IntegerField()
    follower_increase = models.FloatField()
    created_at = models.DateTimeField()
    brand_report = models.ForeignKey('Reportbrandv1', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportbrandcalsnap'


class Reportbrandv1(models.Model):
    created_at = models.DateTimeField()
    version = models.IntegerField()
    tag_count = models.IntegerField()
    account_count = models.IntegerField()
    upload_count = models.TextField()
    mention_brand = models.TextField()
    mention_hashtag = models.TextField()
    keyword = models.TextField()
    top_image = models.TextField()
    ages = models.TextField(blank=True, null=True)
    genders = models.TextField(blank=True, null=True)
    profile_image = models.CharField(max_length=500, blank=True, null=True)
    is_tpo_cal = models.BooleanField()
    updated_at = models.DateTimeField(blank=True, null=True)
    analy_at = models.DateTimeField(blank=True, null=True)
    crawled_at = models.DateTimeField(blank=True, null=True)
    taginfo = models.ForeignKey('Taginfo', models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField()
    userinfo = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportbrandv1'


class Reportbrandv1Looks(models.Model):
    reportbrandv1 = models.ForeignKey(Reportbrandv1, models.DO_NOTHING)
    brandattribute = models.ForeignKey(Brandattribute, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportbrandv1_looks'
        unique_together = (('reportbrandv1', 'brandattribute'),)


class Reportcalculationrate(models.Model):
    reportv1 = models.ForeignKey('Reportv1', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportcalculationrate'


class Reportcomponent(models.Model):
    is_profile = models.BooleanField()
    is_profile_perfect = models.BooleanField()
    is_follower = models.BooleanField()
    is_follower_perfect = models.BooleanField()
    is_post = models.BooleanField()
    is_post_perfect = models.BooleanField()
    is_post_comment_perfect = models.BooleanField()
    is_post_like_perfect = models.BooleanField()
    user_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    is_post_comment = models.BooleanField()
    is_post_like = models.BooleanField()
    is_analy = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportcomponent'


class Reportdefine(models.Model):
    report_name = models.CharField(max_length=100)
    version = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportdefine'


class Reportelementdefine(models.Model):
    value_type = models.IntegerField()
    name = models.CharField(max_length=100)
    key_name = models.CharField(max_length=100)
    version = models.IntegerField()
    element_order = models.IntegerField()
    is_enable = models.BooleanField()
    created_at = models.DateTimeField()
    section = models.ForeignKey('Reportsectiondefine', models.DO_NOTHING, blank=True, null=True)
    element_make_function = models.CharField(max_length=100, blank=True, null=True)
    element_function = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportelementdefine'


class Reportgroupdefine(models.Model):
    name = models.CharField(max_length=100)
    version = models.IntegerField()
    key_name = models.CharField(max_length=100)
    order = models.IntegerField()
    is_enable = models.BooleanField()
    created_at = models.DateTimeField()
    report = models.ForeignKey(Reportdefine, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportgroupdefine'


class Reportsectiondefine(models.Model):
    name = models.CharField(max_length=100)
    version = models.IntegerField()
    key_name = models.CharField(max_length=100)
    order = models.IntegerField()
    is_enable = models.BooleanField()
    created_at = models.DateTimeField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    report = models.ForeignKey(Reportdefine, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Reportgroupdefine, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportsectiondefine'


class Reportsectionsummarydistribution(models.Model):
    type = models.IntegerField()
    percentile = models.FloatField()
    real_rate = models.FloatField()
    fake_rate = models.FloatField()
    real_engagement_rate = models.FloatField()
    fake_engagement_rate = models.FloatField()
    audience_male_rate = models.FloatField()
    audience_female_rate = models.FloatField()
    main_score = models.FloatField()
    audience_age = models.FloatField()
    section = models.ForeignKey(Influencersection, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    total_reach = models.FloatField()
    engagement_rate = models.FloatField()
    type_benchmark = models.IntegerField()
    growth_score = models.FloatField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportsectionsummarydistribution'


class Reportsummary(models.Model):
    profile_count = models.IntegerField()
    profile_info_count = models.IntegerField()
    influencer_count = models.IntegerField()
    report_count = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportsummary'


class Reportv1(models.Model):
    created_at = models.DateTimeField()
    version = models.IntegerField()
    userinfo = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    score = models.ForeignKey('Scorev1', models.DO_NOTHING, blank=True, null=True)
    analy_at = models.DateTimeField(blank=True, null=True)
    crawled_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    taginfo = models.ForeignKey('Taginfo', models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1'


class Reportv1Audience(models.Model):
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True, related_name='audience')
    ranking_rate = models.FloatField(blank=True, null=True)
    all_audience_count = models.IntegerField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    fake_audience_count = models.IntegerField(blank=True, null=True)
    fake_audience_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    real_audience_count = models.IntegerField(blank=True, null=True)
    real_audience_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()
    fake_audience_advertise_rate = models.FloatField(blank=True, null=True)
    fake_audience_bot_rate = models.FloatField(blank=True, null=True)
    fake_audience_notactive_rate = models.FloatField(blank=True, null=True)
    fake_audience_notreach_rate = models.FloatField(blank=True, null=True)
    audience_business_rate = models.FloatField(blank=True, null=True)
    audience_aggressive_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1audience'
        unique_together = (('reportv1', 'version'),)


class Reportv1Audiencefollowertypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    rate = models.FloatField(blank=True, null=True)
    audience = models.ForeignKey(Reportv1Audience, models.DO_NOTHING, blank=True, null=True)
    followertype = models.ForeignKey(Followertype, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1audiencefollowertypes'


class Reportv1Audiencepersonalindicator(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    avg_follower_count = models.FloatField(blank=True, null=True)
    avg_following_count = models.FloatField(blank=True, null=True)
    avg_media_count = models.FloatField(blank=True, null=True)
    avg_comment_count = models.FloatField(blank=True, null=True)
    avg_like_count = models.FloatField(blank=True, null=True)
    audience = models.ForeignKey(Reportv1Audience, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True, related_name='audienceindicator')

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1audiencepersonalindicator'


class Reportv1Audiencetendency(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    following_purpose = models.ForeignKey(Followertype, models.DO_NOTHING, blank=True, null=True)
    audience = models.ForeignKey(Reportv1Audience, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True, related_name='audiencetendency')

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1audiencetendency'


class Reportv1Audiencetendencycategory(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    rate = models.FloatField(blank=True, null=True)
    audience = models.ForeignKey(Reportv1Audience, models.DO_NOTHING, blank=True, null=True)
    audience_tendency = models.ForeignKey(Reportv1Audiencetendency, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Filtercategory, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1audiencetendencycategory'


class Reportv1Demographics(models.Model):
    man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True, related_name='demographics')
    all_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    man_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    woman_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1demographics'
        unique_together = (('reportv1', 'version'),)


class Reportv1Demographicslangauge(models.Model):
    language_code = models.CharField(max_length=20, blank=True, null=True)
    language_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    demographics = models.ForeignKey(Reportv1Demographics, models.DO_NOTHING, blank=True, null=True, related_name="languages")
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True, related_name='demographicslanguage')
    language_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1demographicslangauge'


class Reportv1Engagement(models.Model):
    frequent_commenter_count = models.IntegerField(blank=True, null=True)
    engagement_rate = models.FloatField(blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True, related_name='engagement')
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    avg_post_comment = models.FloatField(blank=True, null=True)
    avg_post_likes = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    real_engagement_rate = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()
    fake_comment_count = models.IntegerField(blank=True, null=True)
    fake_like_count = models.IntegerField(blank=True, null=True)
    likercommenter_count = models.IntegerField(blank=True, null=True)
    likercommenterfollower_count = models.IntegerField(blank=True, null=True)
    real_comment_count = models.IntegerField(blank=True, null=True)
    real_like_count = models.IntegerField(blank=True, null=True)
    likercommenter_rate = models.FloatField(blank=True, null=True)
    likercommenterfollower_rate = models.FloatField(blank=True, null=True)
    avg_post_real_comment = models.FloatField(blank=True, null=True)
    avg_post_real_likes = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1engagement'
        unique_together = (('reportv1', 'version'),)


class Reportv1Engagementcommenttypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    rate = models.FloatField(blank=True, null=True)
    commenttype = models.ForeignKey(Commenttype, models.DO_NOTHING, blank=True, null=True)
    engagement = models.ForeignKey(Reportv1Engagement, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1engagementcommenttypes'


class Reportv1Engagementdemographics(models.Model):
    likecomment_man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    likecomment_woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    like_man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    like_woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    comment_man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    comment_woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    likecomment_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    like_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    comment_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1engagementdemographics'
        unique_together = (('reportv1', 'version'),)


class Reportv1Engagementfollowerkeyword(models.Model):
    keyword = models.CharField(max_length=50, blank=True, null=True)
    keyword_post_count = models.IntegerField(blank=True, null=True)
    engagement = models.ForeignKey(Reportv1Engagement, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    engagement_rate = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1engagementfollowerkeyword'


class Reportv1Engagementpostcategorys(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    engagement_rate = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Categorybridge, models.DO_NOTHING, blank=True, null=True)
    engagement = models.ForeignKey(Reportv1Engagement, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1engagementpostcategorys'


class Reportv1Engagementtrends(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    post_insta_pk = models.BigIntegerField(blank=True, null=True)
    engagement_rate = models.FloatField(blank=True, null=True)
    real_engagement_rate = models.FloatField(blank=True, null=True)
    engagement = models.ForeignKey(Reportv1Engagement, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1engagementtrends'


class Reportv1Growth(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    growth_score = models.FloatField(blank=True, null=True)
    week_follower_up_rate = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1growth'


class Reportv1Post(models.Model):
    recent_posting_rate = models.FloatField(blank=True, null=True)
    top_post_palette_color = models.CharField(max_length=100, blank=True, null=True)
    post_palette_color = models.CharField(max_length=100, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()
    day_posting_count = models.CharField(max_length=100, blank=True, null=True)
    time_posting_count = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1post'
        unique_together = (('reportv1', 'version'),)


class Reportv1Postcampaign(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    avg_campaign_likes = models.IntegerField(blank=True, null=True)
    avg_campaign_comment = models.IntegerField(blank=True, null=True)
    campaign_estimated_price = models.FloatField(blank=True, null=True)
    campaign_sales_estimated_price = models.FloatField(blank=True, null=True)
    brand_communication_aggressive = models.FloatField(blank=True, null=True)
    audience_communication_aggressive = models.FloatField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    recent_posting_campaign_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postcampaign'


class Reportv1Postcampaignengagements(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    engagement_rate = models.FloatField(blank=True, null=True)
    campaigntype = models.ForeignKey(Postcampaigntype, models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    post_campaign = models.ForeignKey(Reportv1Postcampaign, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    post_insta_pk = models.BigIntegerField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postcampaignengagements'


class Reportv1Postcampaigntypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    campaign_rate = models.FloatField(blank=True, null=True)
    campaigntype = models.ForeignKey(Postcampaigntype, models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    post_campaign = models.ForeignKey(Reportv1Postcampaign, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postcampaigntypes'


class Reportv1Postengagementtrends(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    post_insta_pk = models.BigIntegerField(blank=True, null=True)
    real_like_count = models.IntegerField(blank=True, null=True)
    fake_like_count = models.IntegerField(blank=True, null=True)
    real_comment_count = models.IntegerField(blank=True, null=True)
    fake_comment_count = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postengagementtrends'


class Reportv1Postengagementtypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    category_name = models.CharField(max_length=50, blank=True, null=True)
    engagement_rate = models.FloatField(blank=True, null=True)
    engagement = models.ForeignKey(Reportv1Engagement, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postengagementtypes'


class Reportv1Postfavoritekeyword(models.Model):
    keyword = models.CharField(max_length=50, blank=True, null=True)
    keyword_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postfavoritekeyword'


class Reportv1Postfrequent(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    frequent_commenter_count = models.IntegerField(blank=True, null=True)
    frequent_like_count = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    post_insta_pk = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postfrequent'


class Reportv1Postmentionbrand(models.Model):
    mention = models.CharField(max_length=50, blank=True, null=True)
    post_like_count = models.IntegerField(blank=True, null=True)
    post_comment_count = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    profile_image = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()
    type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1postmentionbrand'


class Reportv1Posttop(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    top_post_count = models.IntegerField(blank=True, null=True)
    top_post_rate = models.FloatField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1posttop'


class Reportv1Posttophashtags(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    name = models.CharField(max_length=50, blank=True, null=True)
    media_count = models.IntegerField(blank=True, null=True)
    post_count = models.IntegerField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1posttophashtags'


class Reportv1Posttypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    posttype_rate = models.FloatField(blank=True, null=True)
    post = models.ForeignKey(Reportv1Post, models.DO_NOTHING, blank=True, null=True)
    posttype = models.ForeignKey(Posttype, models.DO_NOTHING, blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1posttypes'


class Reportv1Reach(models.Model):
    total_reach = models.IntegerField(blank=True, null=True)
    follower_reach = models.IntegerField(blank=True, null=True)
    non_follower_reach = models.IntegerField(blank=True, null=True)
    follower_post_count = models.IntegerField(blank=True, null=True)
    follower_following_count = models.IntegerField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)
    total_reach_engagement = models.IntegerField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    is_complete = models.BooleanField()
    version = models.IntegerField()
    follower_reach_engagement = models.IntegerField(blank=True, null=True)
    nonfollower_reach_engagement = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1reach'
        unique_together = (('reportv1', 'version'),)


class Reportv1Similar(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    version = models.IntegerField()
    similar_user = models.TextField(blank=True, null=True)
    reportv1 = models.ForeignKey(Reportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv1similar'
        unique_together = (('reportv1', 'version'),)


class Reportv2(models.Model):
    created_at = models.DateTimeField()
    version = models.IntegerField()
    crawled_at = models.DateTimeField(blank=True, null=True)
    analy_at = models.DateTimeField(blank=True, null=True)
    define = models.ForeignKey(Reportdefine, models.DO_NOTHING, blank=True, null=True)
    score = models.ForeignKey('Scorev1', models.DO_NOTHING, blank=True, null=True)
    userinfo = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    taginfo = models.ForeignKey('Taginfo', models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2'


class Reportv2Audiencedemographics(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2audiencedemographics'


class Reportv2Audiencefanpower(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2audiencefanpower'


class Reportv2Campaignengagement(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2campaignengagement'


class Reportv2Campaignestimated(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2campaignestimated'


class Reportv2Campaignhighengagementtype(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2campaignhighengagementtype'


class Reportv2Campaignpositiveness(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2campaignpositiveness'


class Reportv2Campaigntype(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2campaigntype'


class Reportv2Commenttype(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2commenttype'


class Reportv2Engagement(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2engagement'


class Reportv2Followerlanguages(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2followerlanguages'


class Reportv2Followerlikekeyword(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2followerlikekeyword'


class Reportv2Followertype(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2followertype'


class Reportv2Growthcommenttrend(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2growthcommenttrend'


class Reportv2Growthengagementtrend(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2growthengagementtrend'


class Reportv2Growthfollowertrend(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2growthfollowertrend'


class Reportv2Growthliketrend(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2growthliketrend'


class Reportv2Growthrealengagement(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2growthrealengagement'


class Reportv2Mainaudiencequalityscore(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2mainaudiencequalityscore'


class Reportv2Mainlevel(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2mainlevel'


class Reportv2Mainreachprediction(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2mainreachprediction'


class Reportv2Mainrealengagement(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2mainrealengagement'


class Reportv2Postcolor(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2postcolor'


class Reportv2Postmainkeyword(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2postmainkeyword'


class Reportv2Postmetionbrand(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2postmetionbrand'


class Reportv2Posttendency(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2posttendency'


class Reportv2Posttype(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_reportv2posttype'


class Scorev1(models.Model):
    main_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    version = models.IntegerField()
    userinfo = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    analy_list_count = models.IntegerField()
    analy_profile_follower_count = models.IntegerField()
    real_follower_count = models.IntegerField()
    real_liker_count = models.IntegerField()
    profile_analy_follower_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    profile_analy_like_rate = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    recent_posts_liker_count = models.IntegerField()
    account_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_scorev1'


class Scorev1Snapshot(models.Model):
    main_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    version = models.IntegerField()
    analy_list_count = models.IntegerField()
    analy_profile_follower_count = models.IntegerField()
    real_follower_count = models.IntegerField()
    recent_posts_liker_count = models.IntegerField()
    real_liker_count = models.IntegerField()
    profile_analy_follower_rate = models.FloatField(blank=True, null=True)
    profile_analy_like_rate = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    userinfo = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    account_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_scorev1snapshot'
        unique_together = (('userinfo', 'main_score'),)


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('Tagtype', models.DO_NOTHING, blank=True, null=True)
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_tag'


class Taginfo(models.Model):
    tag_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50)
    profile_pic_url = models.CharField(max_length=500, blank=True, null=True)
    media_count = models.IntegerField(blank=True, null=True)
    crawled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    component = models.ForeignKey('Tagreportcomponent', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_taginfo'


class Taginfosummary(models.Model):
    audience_age_division = models.ForeignKey('Useragedivision', models.DO_NOTHING, blank=True, null=True)
    audience_gender_division = models.ForeignKey('Usergenderdivision', models.DO_NOTHING, blank=True, null=True)
    audience_language_division = models.ForeignKey('Userlanguagedivision', models.DO_NOTHING, blank=True, null=True)
    main_category = models.ForeignKey(Filtercategory, models.DO_NOTHING, blank=True, null=True, related_name='taginfosummary')
    main_category_admin = models.ForeignKey(Filtercategory, models.DO_NOTHING, blank=True, null=True, related_name='taginfosummary_admin')
    taginfo = models.OneToOneField(Taginfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_taginfosummary'


class TaginfosummaryAudienceCategory(models.Model):
    taginfosummary = models.ForeignKey(Taginfosummary, models.DO_NOTHING)
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_taginfosummary_audience_category'
        unique_together = (('taginfosummary', 'filtercategory'),)


class TaginfosummaryCategory(models.Model):
    taginfosummary = models.ForeignKey(Taginfosummary, models.DO_NOTHING)
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_taginfosummary_category'
        unique_together = (('taginfosummary', 'filtercategory'),)


class TaginfosummaryCategoryAdmin(models.Model):
    taginfosummary = models.ForeignKey(Taginfosummary, models.DO_NOTHING)
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_taginfosummary_category_admin'
        unique_together = (('taginfosummary', 'filtercategory'),)


class TaginfosummaryTag(models.Model):
    taginfosummary = models.ForeignKey(Taginfosummary, models.DO_NOTHING)
    tag = models.ForeignKey(Tag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_taginfosummary_tag'
        unique_together = (('taginfosummary', 'tag'),)


class Tagreportcomponent(models.Model):
    tag_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50)
    is_tag_mediacount = models.BooleanField()
    is_tag_related = models.BooleanField()
    is_tag_explore = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportcomponent'


class Tagreportv1(models.Model):
    created_at = models.DateTimeField()
    version = models.IntegerField()
    crawled_at = models.DateTimeField(blank=True, null=True)
    analy_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tagscore = models.ForeignKey('Tagscorev1', models.DO_NOTHING, blank=True, null=True)
    userinfo = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    taginfo = models.ForeignKey(Taginfo, models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1'


class Tagreportv1Audience(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    real_audience_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fake_audience_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)
    fake_audience_advertise_rate = models.FloatField(blank=True, null=True)
    fake_audience_bot_rate = models.FloatField(blank=True, null=True)
    fake_audience_notactive_rate = models.FloatField(blank=True, null=True)
    fake_audience_notreach_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1audience'
        unique_together = (('tagreportv1', 'version'),)


class Tagreportv1Audiencetendency(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    following_purpose = models.IntegerField(blank=True, null=True)
    tagaudience = models.ForeignKey(Tagreportv1Audience, models.DO_NOTHING, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1audiencetendency'


class Tagreportv1Audiencetendencycategory(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    rate = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Filtercategory, models.DO_NOTHING, blank=True, null=True)
    tagaudience = models.ForeignKey(Tagreportv1Audience, models.DO_NOTHING, blank=True, null=True)
    tagaudience_tendency = models.ForeignKey(Tagreportv1Audiencetendency, models.DO_NOTHING, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1audiencetendencycategory'


class Tagreportv1Demographics(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    all_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    man_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    woman_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1demographics'
        unique_together = (('tagreportv1', 'version'),)


class Tagreportv1Engagement(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    avg_engagement_rate = models.FloatField(blank=True, null=True)
    avg_real_engagement_rate = models.FloatField(blank=True, null=True)
    avg_post_likes = models.FloatField(blank=True, null=True)
    avg_post_comment = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    avg_real_like_count = models.IntegerField(blank=True, null=True)
    avg_fake_like_count = models.IntegerField(blank=True, null=True)
    avg_real_comment_count = models.IntegerField(blank=True, null=True)
    avg_fake_comment_count = models.IntegerField(blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)
    recent_like_rate = models.FloatField(blank=True, null=True)
    recent_like_rate_day = models.FloatField(blank=True, null=True)
    recent_like_rate_hour = models.FloatField(blank=True, null=True)
    recent_like_rate_minute = models.FloatField(blank=True, null=True)
    recent_like_rate_week = models.FloatField(blank=True, null=True)
    recent_comment_rate = models.FloatField(blank=True, null=True)
    recent_comment_rate_day = models.FloatField(blank=True, null=True)
    recent_comment_rate_hour = models.FloatField(blank=True, null=True)
    recent_comment_rate_minute = models.FloatField(blank=True, null=True)
    recent_comment_rate_week = models.FloatField(blank=True, null=True)
    recent_rate = models.FloatField(blank=True, null=True)
    recent_rate_day = models.FloatField(blank=True, null=True)
    recent_rate_hour = models.FloatField(blank=True, null=True)
    recent_rate_minute = models.FloatField(blank=True, null=True)
    recent_rate_week = models.FloatField(blank=True, null=True)
    avg_top_engagement_rate = models.FloatField(blank=True, null=True)
    avg_top_post_comment = models.FloatField(blank=True, null=True)
    avg_top_post_likes = models.FloatField(blank=True, null=True)
    avg_top_real_engagement_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1engagement'
        unique_together = (('tagreportv1', 'version'),)


class Tagreportv1Engagementdemographics(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    avg_likecomment_man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    avg_likecomment_woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    avg_like_man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    avg_like_woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    avg_comment_man_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    avg_comment_woman_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    avg_likecomment_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    avg_like_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    avg_comment_age_ratetext = models.CharField(max_length=30, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1engagementdemographics'
        unique_together = (('tagreportv1', 'version'),)


class Tagreportv1Post(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    recent_posting_rate = models.FloatField(blank=True, null=True)
    day_posting_count = models.CharField(max_length=100, blank=True, null=True)
    time_posting_count = models.CharField(max_length=100, blank=True, null=True)
    top_post_palette_color = models.CharField(max_length=100, blank=True, null=True)
    post_palette_color = models.CharField(max_length=100, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)
    recent_posting_rate_week = models.FloatField(blank=True, null=True)
    recent_posting_rate_day = models.FloatField(blank=True, null=True)
    recent_posting_rate_hour = models.FloatField(blank=True, null=True)
    recent_posting_rate_minute = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1post'
        unique_together = (('tagreportv1', 'version'),)


class Tagreportv1Postcampaign(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    recent_posting_campaign_rate = models.FloatField(blank=True, null=True)
    avg_campaign_likes = models.IntegerField(blank=True, null=True)
    avg_campaign_comment = models.IntegerField(blank=True, null=True)
    campaign_estimated_price = models.FloatField(blank=True, null=True)
    campaign_sales_estimated_price = models.FloatField(blank=True, null=True)
    avg_campaign_estimated_price = models.FloatField(blank=True, null=True)
    avg_campaign_sales_estimated_price = models.FloatField(blank=True, null=True)
    brand_communication_aggressive = models.FloatField(blank=True, null=True)
    audience_communication_aggressive = models.FloatField(blank=True, null=True)
    tagpost = models.ForeignKey(Tagreportv1Post, models.DO_NOTHING, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1postcampaign'


class Tagreportv1Postcampaigntypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    campaign_rate = models.FloatField(blank=True, null=True)
    campaigntype = models.ForeignKey(Postcampaigntype, models.DO_NOTHING, blank=True, null=True)
    tagpost = models.ForeignKey(Tagreportv1Post, models.DO_NOTHING, blank=True, null=True)
    tagpost_campaign = models.ForeignKey(Tagreportv1Postcampaign, models.DO_NOTHING, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1postcampaigntypes'


class Tagreportv1Postengagementtypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    category_name = models.CharField(max_length=50, blank=True, null=True)
    engagement_rate = models.FloatField(blank=True, null=True)
    tagengagement = models.ForeignKey(Tagreportv1Engagement, models.DO_NOTHING, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1postengagementtypes'


class Tagreportv1Posttypes(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    posttype_rate = models.FloatField(blank=True, null=True)
    posttype = models.ForeignKey(Posttype, models.DO_NOTHING, blank=True, null=True)
    tagpost = models.ForeignKey(Tagreportv1Post, models.DO_NOTHING, blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1posttypes'


class Tagreportv1Reach(models.Model):
    is_complete = models.BooleanField()
    created_at = models.DateTimeField()
    version = models.IntegerField()
    post_total_reach = models.IntegerField(blank=True, null=True)
    post_total_reach_engagement = models.IntegerField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    tagreportv1 = models.ForeignKey(Tagreportv1, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagreportv1reach'
        unique_together = (('tagreportv1', 'version'),)


class Tagscorev1(models.Model):
    main_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    version = models.IntegerField()
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    taginfo = models.ForeignKey(Taginfo, models.DO_NOTHING, blank=True, null=True)
    engagement_score = models.FloatField(blank=True, null=True)
    trend_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_tagscorev1'


class Tagtype(models.Model):
    type_name = models.CharField(max_length=50)
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_tagtype'


class Useragedivision(models.Model):
    age_name = models.CharField(max_length=50)
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_useragedivision'


class Usercountrydivision(models.Model):
    country_name = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    language = models.ForeignKey('Userlanguagedivision', models.DO_NOTHING, blank=True, null=True)
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_usercountrydivision'


class Usergenderdivision(models.Model):
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()
    gender_name = models.CharField(max_length=50)
    gender_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_usergenderdivision'


class Userinfo(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    profile_pic_url = models.CharField(max_length=500, blank=True, null=True)
    media_count = models.IntegerField(blank=True, null=True)
    following_count = models.IntegerField(blank=True, null=True)
    follower_count = models.IntegerField(blank=True, null=True)
    public_phone_number = models.CharField(max_length=100, blank=True, null=True)
    public_email = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.BigIntegerField(unique=True, blank=True, null=True)
    crawled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    component = models.ForeignKey(Reportcomponent, models.DO_NOTHING, blank=True, null=True)
    public_url = models.CharField(max_length=500, blank=True, null=True)
    usertags_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instagram_score_userinfo'


class Userinfosummary(models.Model):
    age_division = models.ForeignKey(Useragedivision, models.DO_NOTHING, blank=True, null=True,related_name='summary')
    audience_age_division = models.ForeignKey(Useragedivision, models.DO_NOTHING, blank=True, null=True, related_name='summary_audience')
    language_division = models.ForeignKey('Userlanguagedivision', models.DO_NOTHING, blank=True, null=True,related_name='summary')
    userinfo = models.OneToOneField(Userinfo, models.DO_NOTHING, blank=True, null=True, related_name='summary')
    country_division = models.ForeignKey(Usercountrydivision, models.DO_NOTHING, blank=True, null=True,related_name='summary')
    audience_language_division = models.ForeignKey('Userlanguagedivision', models.DO_NOTHING, blank=True, null=True, related_name='summary_audience')
    audience_gender_division = models.ForeignKey(Usergenderdivision, models.DO_NOTHING, blank=True, null=True, related_name='summary_audience')
    gender_division = models.ForeignKey(Usergenderdivision, models.DO_NOTHING, blank=True, null=True,related_name='summary')
    main_category = models.ForeignKey(Filtercategory, models.DO_NOTHING, blank=True, null=True, related_name='summary')
    main_category_admin = models.ForeignKey(Filtercategory, models.DO_NOTHING, blank=True, null=True, related_name='summary_admin')

    class Meta:
        managed = False
        db_table = 'instagram_score_userinfosummary'


class UserinfosummaryAudienceCategory(models.Model):
    userinfosummary = models.ForeignKey(Userinfosummary, models.DO_NOTHING)
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_userinfosummary_audience_category'
        unique_together = (('userinfosummary', 'filtercategory'),)


class UserinfosummaryCategory(models.Model):
    userinfosummary = models.ForeignKey(Userinfosummary, models.DO_NOTHING)
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_userinfosummary_category'
        unique_together = (('userinfosummary', 'filtercategory'),)


class UserinfosummaryCategoryAdmin(models.Model):
    userinfosummary = models.ForeignKey(Userinfosummary, models.DO_NOTHING)
    filtercategory = models.ForeignKey(Filtercategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_userinfosummary_category_admin'
        unique_together = (('userinfosummary', 'filtercategory'),)


class UserinfosummaryTag(models.Model):
    userinfosummary = models.ForeignKey(Userinfosummary, models.DO_NOTHING)
    tag = models.ForeignKey(Tag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'instagram_score_userinfosummary_tag'
        unique_together = (('userinfosummary', 'tag'),)


class Userlanguagedivision(models.Model):
    language_code = models.CharField(max_length=10)
    language_name = models.CharField(max_length=50)
    is_public = models.BooleanField()
    division_code = models.IntegerField()
    is_audience = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'instagram_score_userlanguagedivision'



class YoutubeScoreRelationcategory(models.Model):
    category = models.CharField(max_length=255)
    like_count = models.FloatField()
    dislike_count = models.FloatField()
    view_count = models.FloatField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'youtube_score_relationcategory'


class YoutubeScoreYoutubeage(models.Model):
    group_10 = models.ForeignKey('YoutubeScoreYoutubegender', models.DO_NOTHING, blank=True, null=True, related_name='age_group_10')
    group_20 = models.ForeignKey('YoutubeScoreYoutubegender', models.DO_NOTHING, blank=True, null=True, related_name='age_group_20')
    group_30 = models.ForeignKey('YoutubeScoreYoutubegender', models.DO_NOTHING, blank=True, null=True, related_name='age_group_30')
    group_40 = models.ForeignKey('YoutubeScoreYoutubegender', models.DO_NOTHING, blank=True, null=True, related_name='age_group_40')

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubeage'


class YoutubeScoreYoutubecaladvsnap(models.Model):
    nor_upload_count = models.IntegerField()
    nor_upload_rate = models.FloatField()
    adv_upload_count = models.IntegerField()
    adv_upload_rate = models.FloatField()
    nor_avg_view = models.FloatField()
    nor_avg_view_rate = models.FloatField()
    adv_avg_view = models.FloatField()
    adv_avg_view_rate = models.FloatField()
    nor_dislike_count = models.FloatField()
    nor_dislike_rate = models.FloatField()
    adv_dislike_count = models.FloatField()
    adv_dislike_rate = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    channel = models.ForeignKey('YoutubeScoreYoutubechannelinfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubecaladvsnap'


class YoutubeScoreYoutubecalsnap(models.Model):
    current_subscriber_count = models.IntegerField()
    current_subscriber_rate = models.FloatField()
    current_view_count = models.IntegerField()
    current_view_rate = models.FloatField()
    channel = models.ForeignKey('YoutubeScoreYoutubechannelinfo', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    standard_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubecalsnap'


class YoutubeScoreYoutubecategory(models.Model):
    category_location = models.IntegerField()
    name = models.CharField(max_length=150, blank=True, null=True)
    channel_category_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubecategory'


class YoutubeScoreYoutubecategoryrelation(models.Model):
    category_type = models.IntegerField()
    category = models.ForeignKey(YoutubeScoreYoutubecategory, models.DO_NOTHING, blank=True, null=True)
    report = models.ForeignKey('YoutubeScoreYoutubereportv1', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubecategoryrelation'


class YoutubeScoreYoutubecategorysetavg(models.Model):
    model_count = models.IntegerField()
    comment_avg = models.FloatField()
    like_avg = models.FloatField()
    dislike_avg = models.FloatField()
    created_at = models.DateTimeField()
    category = models.ForeignKey(YoutubeScoreYoutubecategory, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubecategorysetavg'


class YoutubeScoreYoutubechannelinfo(models.Model):
    channel_id = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    viewcount = models.BigIntegerField(db_column='viewCount', blank=True, null=True)  # Field name made lowercase.
    commentcount = models.BigIntegerField(db_column='commentCount', blank=True, null=True)  # Field name made lowercase.
    subscribercount = models.BigIntegerField(db_column='subscriberCount', blank=True, null=True)  # Field name made lowercase.
    hiddensubscribercount = models.BooleanField(db_column='hiddenSubscriberCount', blank=True, null=True)  # Field name made lowercase.
    videocount = models.BigIntegerField(db_column='videoCount', blank=True, null=True)  # Field name made lowercase.
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    lastest_upload_at = models.DateTimeField(blank=True, null=True)
    upload_frequency = models.IntegerField()
    profile_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubechannelinfo'


class YoutubeScoreYoutubegender(models.Model):
    male = models.IntegerField()
    female = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubegender'


class YoutubeScoreYoutubereportv1(models.Model):
    version = models.IntegerField()
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    content_category = models.TextField(blank=True, null=True)
    hidden_tags = models.TextField(blank=True, null=True)
    gender = models.TextField()
    age = models.TextField()
    language = models.TextField()
    participation = models.TextField()
    keyword = models.TextField()
    adv_type = models.TextField()
    userinfo = models.ForeignKey(YoutubeScoreYoutubechannelinfo, models.DO_NOTHING, blank=True, null=True)
    adv_category = models.TextField(blank=True, null=True)
    adv_content_detail = models.TextField(blank=True, null=True)
    adv_comment = models.IntegerField()
    adv_like = models.IntegerField()
    adv_view = models.IntegerField()
    nor_comment = models.IntegerField()
    nor_like = models.IntegerField()
    nor_view = models.IntegerField()
    comment_avg = models.FloatField()
    dislike_avg = models.FloatField()
    like_avg = models.FloatField()
    adv_count = models.IntegerField()
    nor_adv_count = models.IntegerField()
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    estimate_view = models.FloatField(blank=True, null=True)
    main_score = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubereportv1'


class YoutubeScoreYoutubereportv2(models.Model):
    version = models.IntegerField()
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField()
    channel_id = models.CharField(unique=True, max_length=255)
    main_score = models.FloatField(blank=True, null=True)
    estimate_view = models.FloatField(blank=True, null=True)
    ranking_rate = models.FloatField(blank=True, null=True)
    better_than_similar_rate = models.FloatField(blank=True, null=True)
    content_category = models.TextField(blank=True, null=True)
    language = models.TextField()
    keyword = models.TextField()
    video_title_tag = models.TextField()
    adv_category = models.TextField(blank=True, null=True)
    adv_content_detail = models.TextField(blank=True, null=True)
    nor_view = models.IntegerField()
    adv_view = models.IntegerField()
    nor_like = models.IntegerField()
    adv_like = models.IntegerField()
    nor_dislike = models.IntegerField()
    adv_dislike = models.IntegerField()
    age = models.ForeignKey(YoutubeScoreYoutubeage, models.DO_NOTHING, blank=True, null=True)
    gender = models.ForeignKey(YoutubeScoreYoutubegender, models.DO_NOTHING, blank=True, null=True)
    adv_like_dislike_count = models.IntegerField()
    adv_upload_rate = models.FloatField()
    adv_video_count = models.IntegerField()
    adv_view_video_count = models.IntegerField()
    nor_adv_like_dislike_count = models.IntegerField()
    nor_adv_upload_rate = models.FloatField()
    nor_adv_video_count = models.IntegerField()
    nor_adv_view_video_count = models.IntegerField()
    adv_video = models.TextField(blank=True, null=True)
    avg_category = models.ForeignKey(YoutubeScoreRelationcategory, models.DO_NOTHING, blank=True, null=True)
    adv_comment = models.IntegerField()
    adv_comment_count = models.IntegerField()
    nor_adv_comment_count = models.IntegerField()
    nor_comment = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubereportv2'


class YoutubeScoreYoutubereportv2HiddenTags(models.Model):
    youtubereportv2 = models.ForeignKey(YoutubeScoreYoutubereportv2, models.DO_NOTHING)
    youtubetag = models.ForeignKey('YoutubeScoreYoutubetag', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubereportv2_hidden_tags'
        unique_together = (('youtubereportv2', 'youtubetag'),)


class YoutubeScoreYoutubetag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubetag'


class YoutubeScoreYoutubetagrelation(models.Model):
    report = models.ForeignKey(YoutubeScoreYoutubereportv1, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey(YoutubeScoreYoutubetag, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youtube_score_youtubetagrelation'
