from django.core.management import BaseCommand
import requests, traceback
from statistics import fmean
from report.make_stat import make_status_ig_user, rank_ig_user
from component.models.account import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        # names = [
        #     '사람들',
        # ]

        # names = [
        #     '패션의류',
        #     '스포츠/아웃도어 의류',
        #     '구두/운동화',
        #     '가방',
        #     '쥬얼리',
        #     '기타 잡화',
        #     '스킨케어',
        #     '클렌징/필링',
        #     '메이크업',
        #     '헤어케어',
        #     '바디케어',
        #     '네일케어',
        #     '향수',
        #     '미용 기기',
        #     '스포츠 용품',
        #     '아웃도어 용품',
        #     '자동차 용품',
        #     '자동차',
        #     '기타 동체',
        #     '조리 된 음식',
        #     '스낵',
        #     '과채류',
        #     '커피',
        #     '기타 음료',
        #     '건강 식품',
        #     '베이커리',
        #     '다이어트 식품',
        #     '반찬/조미료',
        #     '인스턴트',
        #     '유아 의류',
        #     '키즈 의류',
        #     '유아 용품/장난감',
        #     '키즈 용품/장난감',
        #     '유아 가구',
        #     '키즈 가구',
        #     '유아 식품',
        #     '주방 용품',
        #     '생활 용품',
        #     '욕실 용품',
        #     '청소 용품',
        #     '건강 용품',
        #     '수납 용품',
        #     '침실 가구',
        #     '거실 가구',
        #     '사무 가구',
        #     '주방 가구',
        #     '인테리어 소품',
        #     '엔터테인먼트 가전',
        #     '계절 가전',
        #     '주방 가전',
        #     '가전 소품',
        #     '생활 가전',
        #     '도서/음반',
        #     '문구/사무 용품',
        #     '악기',
        #     '취미/글귀',
        #     '반려동물 용품',
        #     '반려동물 식품',
        #     '반려동물 장난감',
        # ]

        # for name in names:
        #     category, _ = Category.objects.get_or_create(name="상품")
        #     tag, _ = Tag.objects.get_or_create(category=category, name=name, code=name)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_제이콥분류법")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_카테고리")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_글")
        #     tag.attributes.add(attr)

        
        # names = [
        #     '셀카',
        #     '인물',
        #     '배경',
        # ]

        # for name in names:
        #     category, _ = Category.objects.get_or_create(name="셀카/사람/배경")
        #     tag, _ = Tag.objects.get_or_create(category=category, name=name, code=name)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_제이콥분류법")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_카테고리")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_이미지")
        #     tag.attributes.add(attr)

    
        # names = [
        #     '개',
        #     '고양이',
        #     '음식',
        #     '패션',
        #     '키즈',
        #     '육아',
        #     '홈리빙',
        #     '자연',
        #     '식물',
        #     '꽃',
        #     '자연',
        #     '셀카',
        #     '디지털',
        #     '커피',
        #     '실외',
        #     '실내',
        #     '바다',
        #     '산',
        #     '하늘',
        #     '음료',
        #     '자동차',
        #     '과일',
        # ]

        # category, _ = Category.objects.get_or_create(name="Accessibility Caption")

        # for name in names:            
        #     tag, _ = Tag.objects.get_or_create(category=category, name=name, code=name)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_그램분류법")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램")
        #     tag.attributes.add(attr)

        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_카테고리")
        #     tag.attributes.add(attr)

        #     # attr, _ = Attribute.objects.get_or_create(name="인스타그램_글")
        #     attr, _ = Attribute.objects.get_or_create(name="인스타그램_이미지")
        #     tag.attributes.add(attr)

        names = [
            '귀여운',
            '맑은',
            '온화한',
            '경쾌한',
            '내츄럴한',
            '화려한',
            '우아한',
            '은은한',
            '다이나믹한',
            '모던한',
        ]

        category, _ = Category.objects.get_or_create(name="컬러톤")

        for name in names:            
            tag, _ = Tag.objects.get_or_create(category=category, name=name, code=name)

            attr, _ = Attribute.objects.get_or_create(name="인스타그램_그램분류법")
            tag.attributes.add(attr)

            attr, _ = Attribute.objects.get_or_create(name="인스타그램")
            tag.attributes.add(attr)

            attr, _ = Attribute.objects.get_or_create(name="인스타그램_카테고리")
            tag.attributes.add(attr)

            # attr, _ = Attribute.objects.get_or_create(name="인스타그램_글")
            attr, _ = Attribute.objects.get_or_create(name="인스타그램_이미지")
            tag.attributes.add(attr)