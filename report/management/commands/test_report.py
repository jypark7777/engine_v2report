from django.core.management import BaseCommand
from report.models.report import ReachScore, IGUserInfo, RealInfluenceScore
import requests
import time
from report.make_stat import make_status_ig_user, rank_ig_user
from instagram_score.models import Scorev1, Reportv1Audience
from report.calculator import cal_realfake_weight

class Command(BaseCommand):
    def handle(self, *args, **options):

        #Store User
        # input_users = [
        #     # 'kim.zumma',
        #     # 'sal_gungli',
        #     # 'oliviahome',
        #     # 'yujinirang',
        #     # 'siwani.mom',
        #     # 'webelongmama',
        #     # 'jieun.kim__',
        #     # 'xx_moyasi',
        #     # 'hayan__jj',
        #     # 'reun_reun',
        #     # 'je_j8816',
        #     # 'ksqm',
        #     # '_bronze_silver',
        #     # 'lovely_2nana',
        #     # 'jini__11',
        #     # 'jun.woo_hj',
        #     # 'uu8864',
        #     # '_hyerim.2',
        #     # 'ganyvely',
        #     # 'all_for_home',
        #     # 'bogoomi_',
        #     # 'maybe_sweety',
        #     # 'sohnheejin',
        #     # 'laylaeugene'
        #     # 'seojeong_2',
        # ]

        #Insight User
        # input_users = [
        #     # 'zoimo',
        #     # 'heeruring',
        #     # 'hi_1204_',
        #     # 'beau__hee9',
        #     # 'pp.here',
        #     # '_2.seul',
        #     # 'ashleedrinkswine',
        #     # 'bar_ddustro',
        #     # 'yoonie.at.home',
        #     # 'ahjjang_home',
        #     # 'you___ri_',
        #     # '_hyerim.2',
        #     # 'ae.rami',
        #     # 'big.bigchoi',
        # ]
        
        #Real User
        real_fake_input_users = [
            "park_geunsik",
            "simpledays_jin",
            "august.6th",
            "zookeem",
            "koominji_s2",
            "cream._.gaeul",
            "suful415",
            "newkay__",
            "jmt_inseoul",
            "bubble2046",
            "keily.home",
            #Fake User
            "apple__mango__",
            "mini_chavely",
            "line_yeji",
            "noblestory_worldbeauty",
            "m._jxxn9",
            "phe_leac",
            "1013grace",
            "raim_elle",
            "jeonsy",
            "yeji_27",
            "blackstar57670",
            ##Target 
            'haribo.sss',
        ]
        

        # input_users = [
        #     'haribo.sss'
        # ]


        for username in real_fake_input_users:
            # print(f'{username} - Start')
            try:
                
                requests.get(f'https://feat.report/crawl_instagram_save?request_type=user&parameter={username}')
                time.sleep(5)
                make_status_ig_user(username)

                ig_userinfo = IGUserInfo.objects.get(username=username)

                rank_ig_user(ig_userinfo.pk)
            except:
                print("ERROR ------- ", username)

            # print(f"ig_userinfo : {ig_userinfo.username}, {ig_userinfo.json_userprofile['follower_count']}, {ig_userinfo.section_follower}")
            
            reach = ReachScore.objects.filter(ig_userinfo=ig_userinfo).last()
            realinfluence = RealInfluenceScore.objects.filter(ig_userinfo=ig_userinfo).last()
            # print(realinfluence.parent_components[0].pk)

            # result = getattr(self, f'get_{type}')(request, username, platform, calculate)
            scorev1 = Scorev1.objects.filter(userinfo__username=username).last()
            main_score = 0
            if scorev1 != None:
                main_score = scorev1.main_score
            audience = Reportv1Audience.objects.filter(reportv1__userinfo__username=username).last()
            fake_audience_rate = 1.0
            if audience != None:
                fake_audience_rate = audience.fake_audience_rate

            
            follower_count = ig_userinfo.json_userprofile['follower_count']
            media_count = ig_userinfo.json_userprofile['media_count']
            avg_comment_count = reach.json_parameter['avg_comment_count']
            avg_like_count = reach.json_parameter['avg_like_count']
            avg_text_length = reach.json_parameter['avg_text_length']
            media_textcount = media_count * avg_text_length / 1000

            highlight_reel_count = ig_userinfo.json_userprofile['highlight_reel_count']
            is_business = ig_userinfo.json_userprofile['is_business']
            is_professional = ig_userinfo.json_userprofile['is_professional']

            effort_performance = (follower_count*5+(avg_comment_count*3+avg_like_count)*media_count) / media_textcount / 1000


            # print(f"{username}, {effort_performance}")
            # print(f"{username}, {reach.json_parameter['avg_min_like_count']}")

            crawlusersimilar_res = requests.get(f'http://localhost:8001/instagram/crawlusersimilar/{ig_userinfo.pk}/list')
            crawlusersimilar_list = crawlusersimilar_res.json()

            crawlpost_usertags_res = requests.get(f'http://localhost:8001/instagram/crawlpost/{ig_userinfo.pk}/list/usertags?page_size=1')
            crawlpost_usertags_res = crawlpost_usertags_res.json()
            usertags  = crawlpost_usertags_res['count']

            crawlpost_hashtag_res = requests.get(f'http://localhost:8001/instagram/crawlpost/{ig_userinfo.pk}/list/hashtag?page_size=10')
            crawlpost_hashtag_res = crawlpost_hashtag_res.json()
            crawlpost_hashtag_list = []
            for result in crawlpost_hashtag_res['results']:
                crawlpost_hashtag_list.append(result['name'])
            hashtags  = ','.join(crawlpost_hashtag_list)
            
            zero_comment_count = reach.json_parameter['zero_comment_count']
            if zero_comment_count == -1:
                zero_comment_count = 0

            # print(f"{username}, {cal_realfake_weight(effort_performance, zero_comment_count, reach.json_parameter['avg_comment_like_rate'])}")

            print(f"{username}, {ig_userinfo.json_userprofile['follower_count']}, {reach.get_value()}, {realinfluence.get_value()}, {main_score}, {reach.json_parameter['avg_comment_count']}, {reach.json_parameter['avg_like_count']}, {reach.json_parameter['avg_comment_like_rate']}, {reach.json_parameter['zero_like_count']}, {reach.json_parameter['zero_comment_count']}, {fake_audience_rate}, {effort_performance}, {reach.json_parameter['avg_min_like_count']}, {crawlusersimilar_list['count']}, {usertags}, {highlight_reel_count}, {is_business}, {is_professional}, {hashtags}")