from django.db import models
from component.models.account import BaseModel, Account, Category, Tag
import os
from component.pipeline import EgDataProtocol, EgAnalyProtocol
from collections import Counter

# Create your models here.
class Content(BaseModel):
    ig_pk = models.BigIntegerField(null=True, blank=True)
    yt_pk = models.BigIntegerField(null=True, blank=True)
    tk_pk = models.BigIntegerField(null=True, blank=True)

class IgStatisticsContent(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ig_content_statistics')
    content = models.OneToOneField(Content, on_delete=models.CASCADE, related_name='ig_content_statistics', null=True)

    code = models.CharField(max_length=12,null=True, blank=True)

    estimate_age = models.FloatField(null=True, blank=True)
    estimate_gender = models.FloatField(null=True, blank=True)
    language_code = models.CharField(max_length=10,null=True, blank=True)

    palette_colors = models.JSONField(null=True, blank=True, help_text="[{hex:Char,r:Int,g:Int,b:Int}, ..]")


    is_tag_classification = models.BooleanField(verbose_name="태그 분류 유무", default=False, blank=True)
    tag_classification_at = models.DateTimeField(auto_now=True, blank=True)

    def classifier(self, crawlpost):
        tags = list()
        if 'crawlpostcaption' in crawlpost and len(crawlpost['crawlpostcaption']) > 0:
            crawlpostcaption = crawlpost['crawlpostcaption'][0]
        #     #포스팅 글 분류 , Category - 스타그램, Category - 상품
            classifier_post = EgAnalyProtocol.request_classifier_posttext(crawlpostcaption['text'])
            if classifier_post != None:
                if 'matching_stargram_keywords' in classifier_post: #Category - 스타그램
                    category = Category.get_category('스타그램') # 스타그램 카테고리

                    matching_stargram_keywords = classifier_post['matching_stargram_keywords']
                    counts = Counter(matching_stargram_keywords).most_common(1) #가장 많은 키워드 1개만 뽑음
                
                    for item in counts:                                
                        tag = Tag.objects.filter(name=item[0], category=category).last()
                        if tag != None:
                            tags.append(tag)
                    
                if 'category_data' in classifier_post: #Category - 상품
                    category = Category.get_category('상품') # 스타그램 카테고리
                    category_data = classifier_post['category_data']
                    tag = Tag.objects.filter(name=category_data, category=category).last()
                    if tag != None:
                        tags.append(tag)


        # #포스팅 accessibility_caption 분류, Category - Accessibility Caption
        access_keywords = None
        if 'accessibility_caption' in crawlpost:
            accessibility_caption = crawlpost['accessibility_caption']
            classifier_access_tags, access_keywords = IgStatisticsContent.classifier_accessibility_caption(accessibility_caption)
            if classifier_access_tags != None:
                for tag in classifier_access_tags:
                    tags.append(tag)
        

        # #셀카/사람/배경 분류 
        if access_keywords != None:
            category = Category.get_category('셀카/사람/배경') # 셀카/사람/배경 카테고리

            for access_keyword in access_keywords:
                is_person = False
                if 'person' in access_keyword or 'people' in access_keyword:
                    is_person = True
                    tag = Tag.objects.filter(name='인물', category=category).last()
                    tags.append(tag)
                    
                    if 'people' in access_keyword:
                        tag = Tag.objects.filter(name='다수인물', category=category).last()
                        tags.append(tag)

                if 'selfie' in access_keyword or (is_person and 'closeup' in access_keyword):
                    tag = Tag.objects.filter(name='셀카', category=category).last()
                    tags.append(tag)

        # #포스팅 얼굴 분류 
        if 'thumbnail' in crawlpost:
            thumbnail_url = crawlpost['thumbnail']
            analy_faces = EgAnalyProtocol.request_image_analyze_face(thumbnail_url)
            if analy_faces != None:
                for face in analy_faces[:1]:
                    self.estimate_age = face['age']
                    self.estimate_gender = 0.0 if face['gender'] == 'man' else 1.0
        

            # #포스팅 오브젝트 탐색 
            # analy_object = EgAnalyProtocol.request_image_analyze_object(thumbnail_url)
            # print(analy_object)
            # if analy_object != None and len(analy_object) > 0:
            #     print(crawlpostcaption, analy_object)
            #     for object in analy_object:
            #         object_cls_name = object[0] #발견된 오브젝트
            #         object_cls_predict = object[1] #발견된 오브젝트 확률

            # 컬러톤 탐색
            color_tone = EgAnalyProtocol.request_image_analyze_colortone(thumbnail_url)
            if color_tone != None and len(color_tone) > 1:
                #팔레톤 저장
                palette_colors = color_tone[0] # ['b17c95', 'da96e0', '80515d',
                palette_color_json = []
                if palette_colors != None and len(palette_colors) > 0:
                    for palette_color in palette_colors:
                        lv = len(palette_color)
                        rgb = tuple(int(palette_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                        item = {"hex" : palette_color, "r" : rgb[0], "g" : rgb[1], "b" : rgb[2]}

                        palette_color_json.append(item)
                    
                    self.palette_colors = palette_color_json

                #컬러톤 저장 
                colortones = color_tone[1]
                if colortones != None and len(colortones) > 0: # [['화려한', 3], ['온화한', 1], [
                    category = Category.get_category('컬러톤') # 스타그램 카테고리
                    for tone in colortones:
                        tone_name = tone[0]
                        tone_count = tone[1]
                        if tone_count > 1:
                            tag = Tag.objects.filter(name=tone_name, category=category).last()
                            tags.append(tag)
                # print(palette_colors, colortones)

        # print(tags)
        if len(tags) > 0:
            self.tags.clear()
            self.tags.add(*tags)
        self.is_tag_classification = True
        self.save()

    @staticmethod
    def classifier_accessibility_caption(accessibility_caption):
        """포스팅의 accessibility_caption을 태그 및 이미지 분석 키워드로 분류함
        
        Args:
            accessibility_caption - accessibility_caption 텍스트 
        
        Returns:
            tags(list) - Tag Object List
            keywords(list) - Keyword List 
        """
        caption_split = None

        #ex) Photo by 인사이트 뷰티 on November 02, 2020. Image may contain: one or more people and closeup, text that says '인사이트 환불원정대 뮤비 촬영서 미친 비주얼 뿜낸 천옥이 MBC 뭐하니?''.
        if accessibility_caption == None:
            return None, None
        elif 'Image may contain: ' in accessibility_caption: # Image may contain: 뒤에 문장 가져오기
            caption_splits = accessibility_caption.split('Image may contain: ')
            caption_split = caption_splits[1]
        elif 'May be an image of' in accessibility_caption: # May be an image of 뒤에 문장 가져오기
            caption_splits = accessibility_caption.split('May be an image of')
            caption_split = caption_splits[1]
        else:
            return None, None
    
        caption_splits = caption_split.split('text that says') # text that says 앞에 문장 가져오기
        caption_split = caption_splits[0]
        
        tags = [] #태그들로 변환하여 반환
        keywords = []
        # caption_split = caption_split.replace(' ', '') #공백 제거
        caption_splits = caption_split.split(',') #콤마로 구분
        for caption in caption_splits:
            keywords.extend(caption.split('and'))
        

        # accessibility_caption_list로 키워드 맵핑 맵 만들기
        dir = os.path.join(os.path.dirname(__file__))
        filepath = os.path.join(dir, 'data/accessibility_caption_list')
        keyword_map = {}
        with open(filepath) as accessibility_caption_list:
            lines = accessibility_caption_list.readlines()
            for line in lines:
                line = line.strip()
                item = line.split(',')
                keyword_map[item[0]] = item[1]

            
        category = Category.get_category('Accessibility Caption')
        for keyword in keywords:
            keyword = keyword.replace(' ', '')
            keyword = keyword.replace('.','')
            if keyword in keyword_map:
                
                name = keyword_map[keyword]
                tag = Tag.objects.filter(name=name, category=category).last()
                tags.append(tag)
        
        return tags, keywords
        

class ContentRelation(BaseModel):
    pass

