from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    desc  = models.CharField(max_length=255, null=True, blank=True)
    

    @staticmethod
    def get_category(category_name):
        category = Category.objects.get(name=category_name)
        return category

    def __str__(self):
        return f'{self.name} category'

class Attribute(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True)
    desc  = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.name} attribute'


class Tag(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True)
    code = models.CharField(max_length=25)

    attributes = models.ManyToManyField(Attribute, verbose_name="속성")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="분류")

    class Meta:
        unique_together = ('code', 'category')

    def __str__(self):
        return f'{self.name} tag ({self.category})'

class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='생성 시간', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='업데이트 시간', auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True


class Account(BaseModel):
    ig_pk = models.BigIntegerField(null=True, blank=True)
    yt_pk = models.BigIntegerField(null=True, blank=True)
    tk_pk = models.BigIntegerField(null=True, blank=True)
    

class IgStatisticsProfile(BaseModel):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='ig_profile_statistics',)

    username = models.CharField(max_length=32,null=True, blank=True)

    estimate_age = models.FloatField(null=True, blank=True)
    estimate_gender = models.FloatField(null=True, blank=True)
    language_code = models.CharField(max_length=10,null=True, blank=True)

    is_brand = models.BooleanField(verbose_name='브랜드', null=True, blank=True)
    is_celebrity = models.BooleanField(verbose_name='유명인', null=True, blank=True)
    is_fake = models.BooleanField(null=True, blank=True)
    is_bot = models.BooleanField(null=True, blank=True)
    is_advertiser = models.BooleanField(null=True, blank=True)
    is_not_reach = models.BooleanField(null=True, blank=True)
    is_not_active = models.BooleanField(null=True, blank=True)


    is_tag_classification = models.BooleanField(verbose_name="태그 분류 유무", default=False, blank=True)
    tag_classification_at = models.DateTimeField(auto_now=True, blank=True)

    def classifier(self, crawluserprofile):
        pass
        # ig_content_statistics_list = self.account.ig_content_statistics.all()
        # for ig_content_statistics in ig_content_statistics_list:
        #     tags = ig_content_statistics.tags.all()
        #     print('classifier : ' , tags)


class IgAccountRelation(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name='분석대상 계정' , related_name='relation')
    rel_account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='연관 계정')

    is_follower = models.BooleanField(verbose_name='팔로워 유무', null=True, blank=True)

    comment_count = models.IntegerField(verbose_name='댓글 갯수', null=True, blank=True)
    like_count = models.IntegerField(verbose_name='좋아요 갯수', null=True, blank=True)
    mention_count = models.IntegerField(verbose_name='멘션 갯수', null=True, blank=True)
    tag_count = models.IntegerField(verbose_name='태그 갯수', null=True, blank=True)



# class AnalyProfileBase(AnalyBase):
#     user_id =  models.BigIntegerField(verbose_name='분석대상 프로필 (insta_pk)', unique=True, null=True, blank=True)

#     # from_source =  models.ManyToManyField(ProfileFromSource, verbose_name='대상의 출처', blank=True)

#     class Meta:
#         abstract = True
#         verbose_name = "유저 분석"
#         verbose_name_plural = "유저 분석"


# class StatusProfile(AnalyProfileBase):
#     is_celebrity = models.BooleanField(verbose_name='유명인', null=True, blank=True)
#     is_from_bot = models.BooleanField(verbose_name='작업친 계정에서 나온 계정', null=True, blank=True)
#     is_from_real = models.BooleanField(verbose_name='진짜 계정에서 실제 친구들 계정', null=True, blank=True)
#     is_from_celebrity = models.BooleanField(verbose_name='유명인 계정에서 응답한 유저',null=True, blank=True)


# class StatisticsProfile(AnalyProfileBase):
#     age_type = {
#         (0, '10대 (~18)'),
#         (1, '20대초반 (18-24)'),
#         (2, '20대후반 (25-30)'),
#         (3, '30대초반'),
#         (4, '30대후반'),
#         (5, '40대'),
#         (6, '50대이상'),
#     }

#     gender_type = {
#         (0, '남자'),
#         (1, '여자'),
#     }

#     age_type = models.IntegerField(null=True,blank=True, choices=age_type)
#     gender_type = models.IntegerField(null=True,blank=True, choices=gender_type)
#     predict_face = models.ManyToManyField(ImageFaceDetectPredict, blank=True)

#     language_code = models.CharField(max_length=10,null=True, blank=True)

#     class Meta:
#         verbose_name = "유저 분석"
#         verbose_name_plural = "유저 분석"

# class AnalyProfile(AnalyProfileBase):
#     follower_count = models.BigIntegerField(null=True,blank=True)
#     following_count = models.IntegerField(null=True,blank=True)
#     media_count = models.IntegerField(null=True,blank=True)

#     is_fake = models.BooleanField(null=True, blank=True)
#     is_bot = models.BooleanField(null=True, blank=True)
#     is_advertiser = models.BooleanField(null=True, blank=True)
#     is_not_reach = models.BooleanField(null=True, blank=True)
#     is_not_active = models.BooleanField(null=True, blank=True)

#     fake_percent = models.DecimalField(verbose_name='가짜 확률', max_digits=5, decimal_places=2,null=True, blank=True, default=0.0)
#     bot_percent = models.DecimalField(verbose_name='봇 확률', max_digits=5, decimal_places=2,null=True, blank=True, default=0.0)
#     advertiser_percent = models.DecimalField(verbose_name='광고 확률', max_digits=5, decimal_places=2,null=True, blank=True, default=0.0)
#     not_reach_percent = models.DecimalField(verbose_name='도달 못할 확률', max_digits=5, decimal_places=2,null=True, blank=True, default=0.0)
#     not_active_percent = models.DecimalField(verbose_name='활동하지 않는 확률', max_digits=5, decimal_places=2,null=True, blank=True, default=0.0)

#     follower_following_rate = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True, default=0.0)
#     media_following_rate  = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True, default=0.0)
#     biography_advertise_word_count = models.IntegerField(null=True, blank=True)

#     object_detector_value = models.TextField(null=True, verbose_name='ObjectDetector 값')
#     content_analy_value = models.TextField(null=True, verbose_name='content_analy 값')

#     class Meta:
#         verbose_name = "유저 분석"
#         verbose_name_plural = "유저 분석"


# class ActivityProfile(AnalyProfileBase):
#     real_activity_count = models.IntegerField(verbose_name='정상적인 활동 수', null=True, blank=True)
#     last_activitied_at = models.DateTimeField(verbose_name='마지막 활동 시간', null=True, blank=True)

#     class Meta:
#         verbose_name = "유저 분석"
#         verbose_name_plural = "유저 분석"


# class ProfileRelationUserStatus(AnalyProfileBase):
#     user_id =  models.BigIntegerField(verbose_name='분석대상 프로필 (insta_pk)', null=True, blank=True, db_index=True)
#     rel_user_id =  models.BigIntegerField(verbose_name='연관 유저 프로필 (insta_pk)', null=True, blank=True, db_index=True)

#     like_count = models.IntegerField(null=True, blank=True)
#     comment_count = models.IntegerField(null=True, blank=True)
#     metion_count = models.IntegerField(null=True, blank=True)
#     is_follower = models.BooleanField(null=True, blank=True)

#     @staticmethod
#     def createRelation(user_id, rel_user_id, is_follower=None):
#         status, is_created = ProfileRelationUserStatus.objects.get_or_create(user_id=user_id, rel_user_id=rel_user_id)

#         if status.is_analy_complete != True:
#             status.like_count = CrawlPostLiker.objects.filter(post__user__insta_pk=user_id, user__insta_pk=rel_user_id).count()
#             status.comment_count = CrawlPostComment.objects.filter(post__user__insta_pk=user_id, user__insta_pk=rel_user_id).count()
#             status.metion_count = AnalyPostMention.objects.filter(from_source__from_user_id =user_id, user_id=rel_user_id).count()
#             if is_follower != None:
#                 status.is_follower = is_follower
#             else:
#                 status.is_follower = CrawlUserFollower.objects.filter(target_user__insta_pk=user_id, user__insta_pk=rel_user_id).exists()
#             status.is_analy_complete = True
#             status.save()

#     class Meta:
#         verbose_name = "유저 관계 분석"
#         verbose_name_plural = "유저 관계 분석"
#         unique_together = ('user_id', 'rel_user_id')

# class ProfileRelationKeywordStatus(AnalyProfileBase):
#     user_id =  models.BigIntegerField(verbose_name='분석대상 프로필 (insta_pk)', blank=True)
#     rel_word = models.ForeignKey('WordNaturalLanguageResult', on_delete=models.CASCADE , blank=True)

#     post_write_count = models.IntegerField(blank=True, default=0)
#     biograhpy_write_count = models.IntegerField(default=0, blank=True)

#     comment_write_count = models.IntegerField(default=0, blank=True)
#     comment_other_write_count = models.IntegerField(default=0, blank=True)

#     hashtag_write_count = models.IntegerField(default=0, blank=True)

#     @staticmethod
#     def resetCounter(user_id):
#         ProfileRelationKeywordStatus.objects.filter(user_id=user_id).update(post_write_count=0, biograhpy_write_count=0, comment_write_count=0, comment_other_write_count=0,hashtag_write_count=0)

#     @staticmethod
#     def countUpPostWrite(user_id, word, rel_word):
#         status , is_created = ProfileRelationKeywordStatus.objects.get_or_create(user_id=user_id, rel_word=rel_word)
#         status.post_write_count = F('post_write_count')+1
#         status.save()

#     @staticmethod
#     def countUpBiographyWrite(user_id, word, rel_word):
#         status , is_created = ProfileRelationKeywordStatus.objects.get_or_create(user_id=user_id, rel_word=rel_word)
#         status.biograhpy_write_count = F('biograhpy_write_count')+1
#         status.save()

#     @staticmethod
#     def countUpCommentWrite(user_id, word, rel_word):
#         status , is_created = ProfileRelationKeywordStatus.objects.get_or_create(user_id=user_id, rel_word=rel_word)
#         status.comment_write_count = F('comment_write_count')+1
#         status.save()

#     @staticmethod
#     def countUpCommentOtherWrite(user_id, word, rel_word):
#         status , is_created = ProfileRelationKeywordStatus.objects.get_or_create(user_id=user_id, rel_word=rel_word)
#         status.comment_other_write_count = F('comment_other_write_count')+1
#         status.save()

#     @staticmethod
#     def countUpHashTagWrite(user_id, word, rel_word):
#         status , is_created = ProfileRelationKeywordStatus.objects.get_or_create(user_id=user_id, rel_word=rel_word)
#         status.hashtag_write_count = F('hashtag_write_count')+1
#         status.save()

#     class Meta:
#         verbose_name = "유저 단어 분석"
#         verbose_name_plural = "유저 단어 분석"
#         unique_together = ('user_id', 'rel_word')


# class ProfileRelationCategory(BaseRelationCategory):
#     pass

# class ProfileRelationAudiecenCategory(BaseRelationCategory):
#     pass
