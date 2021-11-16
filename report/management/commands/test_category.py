from django.core.management import BaseCommand
from report.models.report import ReachScore, IGUserInfo, ComponentScore
from report.models.statistics import FollowerSection, ReportStatistics, PlatformSection
import requests
import inspect
from report.models import report 
from django.db.models import Avg, Count
from report.make_stat import rank_ig_user
from report.make_stat import make_status_ig_user
import csv
from collections import Counter
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        input_users = [
            # 'kim.zumma',
            # 'sal_gungli',
            # 'oliviahome',
            # 'yujinirang',
            # 'siwani.mom',
            # 'webelongmama',
            # 'jieun.kim__',
            # 'xx_moyasi',
            # 'hayan__jj',
            # 'reun_reun',
            # 'je_j8816',
            # 'ksqm',
            # '_bronze_silver',
            # 'lovely_2nana',
            # 'jini__11',
            # 'jun.woo_hj',
            # 'uu8864',
            # '_hyerim.2',
            # 'ganyvely',
            # 'all_for_home',
            # 'bogoomi_',
            # 'maybe_sweety',
            # 'sohnheejin',
            # 'laylaeugene',
            # 'seojeong_2',
            # 'jisuwoo__',
            # 'raemi_ddle'
            # '_mssssssss',
            'kkamankkong'
        ]






        ##스타그램 로직
        
        # keyword_map = {}

        # with open('category_test.csv', newline='') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         gram = row['gram']
        #         keyword = row['keyword']
        #         gram = gram.replace(" ","")
                
        #         if keyword not in keyword_map:
        #             keyword_map[keyword] = []
                
        #         keyword_map[keyword].extend(gram.split(','))

        #     for username in input_users:
        #         res = requests.get(f'https://feat.report/crawl_instagram_save?request_type=user&parameter={username}')
        #         time.sleep(6)
        #         make_status_ig_user(username)

        #         user_include_keyword = []
        #         user_include_keyword_nogram = []

        #         user_include_key = []
        #         user_include_key_nogram = []

        #         ig_userinfo = IGUserInfo.objects.get(username=username)
        #         json_post = ig_userinfo.json_post
        #         texts = ""
        #         if 'results' in json_post and len(json_post['results']):
        #             for post in json_post['results']:
        #                 try:
        #                     if 'crawlpostcaption' in post and post['crawlpostcaption'] != None and len(post['crawlpostcaption']) > 0:
        #                         texts  += post['crawlpostcaption'][0]['text']
        #                         print(post['accessibility_caption'])
        #                 except:
        #                     pass

        #         # texts = "#주말일상 #침실 #침실꾸미기 #원형테이블 #홈스타일링 #집스타그램 #홈스타그램 #집꾸미기 #오늘의집 #가을침구 #집순이 #원목침대 #원목가구 #우드인테리어 #침실인테리어 #bedroom #homesweethome #homestyling #주말일상 #침실 #침실꾸미기 #원형테이블 #홈스타일링 #집스타그램 #홈스타그램 #집꾸미기 #오늘의집 #가을침구 #집순이 #원목침대 #원목가구 #우드인테리어 #침실인테리어 #bedroom #homesweethome #homestyling @jieun.kim__ #아이방 #아이침실 #키즈룸 #룸데코 #홈데코 #원목가구 #원목침대 #엄마노리 #벽선반 #아이방인테리어 #아이방꾸미기 #집꾸미기 #원목교구 #여름이불 #매트리스커버 #kidsroom #playroom #오늘의집 #집스타그램 #홈스타그램 #babyroom #homedecor"
                
        #         for key in keyword_map.keys():
        #             value_list = keyword_map[key] #OO스타그램 리스트
        #             for value in value_list:
        #                 if value in texts and len(value) > 0: #텍스트에 OO스타그램 포함 유무
        #                     user_include_keyword.append(value)
        #                     user_include_key.append(key)
        #                     # if key not in user_include_keyword:
        #                     #     user_include_keyword[key] = 0
                            
        #                     # user_include_keyword[key] += 1
        #                     # print(key, value)

        #                 new_value = value.replace('스타그램', '')
        #                 new_value = new_value.replace('그램', '')
        #                 if new_value in texts and len(value) > 0: #텍스트에 스타그램 삭제한 OO 포함 유무
        #                     user_include_keyword_nogram.append(new_value)
        #                     user_include_key_nogram.append(key)
        #                     # if key not in user_include_keyword_nogram:
        #                     #     user_include_keyword_nogram[key] = 0
        #                     # print(key, new_value, value)
        #                     # user_include_keyword_nogram[key] += 1

                
        #         # print(username,' 포함 키워드 :', Counter(user_include_keyword).most_common(5))
        #         # print(username,' 포함 키워드(키워드만) :', Counter(user_include_keyword_nogram).most_common(5))
                
        #         print(username,' 포함 키워드 태그 :', Counter(user_include_key).most_common(5))
        #         print(username,' 포함 키워드 태그(키워드만) :', Counter(user_include_key_nogram).most_common(5))
                