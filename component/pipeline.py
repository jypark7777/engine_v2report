import requests
from django.conf import settings

class EgDataProtocol(object):
    """Engine Data 프로젝트와 연동 API 정의"""

    @staticmethod
    def _get_serverhost():
        if settings.DEBUG:
            return 'http://localhost:8001'
        return 'https://data.featuringscore.ai'

    
    @staticmethod
    def request_userprofile(username, user_id=None):
        """유저이름 혹은 아이디로 유저프로필 가져오기"""
        HOST = EgDataProtocol._get_serverhost()
        crawluserprofile = None
        
        if user_id != None:
            crawluserprofile_url = f'{HOST}/instagram/crawluserprofile/{user_id}/'
            crawluserprofile_response = requests.get(crawluserprofile_url)
            if crawluserprofile_response.status_code == 200:
                crawluserprofile = crawluserprofile_response.json()
        else:
            crawluserprofile_url = f'{HOST}/instagram/crawluserprofile/u/{username}/'
            crawluserprofile_response = requests.get(crawluserprofile_url)
            # print(f'{username} - ', crawluserprofile_response)
            if crawluserprofile_response.status_code == 200:
                crawluserprofile = crawluserprofile_response.json()

        return crawluserprofile

    @staticmethod
    def request_userprofilesnap_list(user_id, page=1):
        """유저 아이디로 유저프로필 스냅 히스토리 가져오기"""
        HOST = EgDataProtocol._get_serverhost()

        if user_id != None:
            crawluserprofilesnapshot_url = f'{HOST}/instagram/crawluserprofilesnapshot/{user_id}/list?page={page}&page_size=100'
            crawluserprofilesnapshot_response = requests.get(crawluserprofilesnapshot_url)
            crawluserprofilesnapshot_list = crawluserprofilesnapshot_response.json()

        return crawluserprofilesnapshot_list

    @staticmethod
    def request_post_list(user_id):
        """유저 아이디로 포스팅 리스트 가져오기"""
        HOST = EgDataProtocol._get_serverhost()

        if user_id != None:
            crawlpost_list_url = f'{HOST}/instagram/crawlpost/{user_id}/list/'
            crawlpost_list_url_response = requests.get(crawlpost_list_url)
            crawlpost_list = crawlpost_list_url_response.json()

        return crawlpost_list

    @staticmethod
    def request_post_list_hashtag(user_id, page=1):
        """유저 아이디로 해시태그 리스트 가져오기"""
        HOST = EgDataProtocol._get_serverhost()

        if user_id != None:
            crawlpost_list_url = f'{HOST}/instagram/crawlpost/{user_id}/list/hashtag?page={page}&page_size=10'
            crawlpost_list_url_response = requests.get(crawlpost_list_url)
            crawlpost_list = crawlpost_list_url_response.json()

        return crawlpost_list

    @staticmethod
    def request_post_list_tophashtag(user_id, page=1):
        """유저 아이디로 해시태그 인기 포스팅 리스트 가져오기"""
        HOST = EgDataProtocol._get_serverhost()

        if user_id != None:
            crawlpost_list_url = f'{HOST}/instagram/crawlpost/{user_id}/list/tophashtag?page={page}&page_size=10'
            crawlpost_list_url_response = requests.get(crawlpost_list_url)
            crawlpost_list = crawlpost_list_url_response.json()

        return crawlpost_list

    @staticmethod
    def request_post_list_usertags(user_id, page=1):
        """유저 아이디로 태깅한 포스팅 리스트 가져오기"""
        HOST = EgDataProtocol._get_serverhost()

        if user_id != None:
            crawlpost_list_url = f'{HOST}/instagram/crawlpost/{user_id}/list/usertags?page={page}&page_size=10'
            crawlpost_list_url_response = requests.get(crawlpost_list_url)
            crawlpost_list = crawlpost_list_url_response.json()

        return crawlpost_list

    
    @staticmethod
    def request_user_similar_list(user_id, page=1):
        """유저 아이디로 태깅한 포스팅 리스트 가져오기"""
        HOST = EgDataProtocol._get_serverhost()

        if user_id != None:
            crawlusersimilar_url = f'{HOST}/instagram/crawlusersimilar/{user_id}/list?page_size=100'
            crawlusersimilar_response = requests.get(crawlusersimilar_url)
            if crawlusersimilar_response.status_code == 200:
                crawlusersimilar = crawlusersimilar_response.json()


        return crawlusersimilar


class EgAnalyProtocol(object):
    """Engine Analy 프로젝트와 연동 API 정의"""

    @staticmethod
    def _get_serverhost():
        if settings.DEBUG:
            return 'http://localhost:8003'
        return 'https://analy.featuringscore.ai'

    @staticmethod
    def request_image_analyze_face(image_url):
        """이미지의 얼굴 탐색 후 연령,성별 예측"""
        post_data = {
            "image_url" : image_url,
        }
        text_languages_url = f'{EgAnalyProtocol._get_serverhost()}/image/analyze/face' #얼굴 분석
        value_response = requests.post(text_languages_url, json=post_data)
        if value_response.status_code != 200:
            return None
        value_response_json = value_response.json()
        return value_response_json

    @staticmethod
    def request_image_analyze_object(image_url):
        """이미지의 사물 탐색"""
        post_data = {
            "image_url" : image_url,
        }
        request_url = f'{EgAnalyProtocol._get_serverhost()}/image/analyze/object' #사물 분석
        value_response = requests.post(request_url, json=post_data)
        if value_response.status_code != 200:
            return None
        value_response_json = value_response.json()
        return value_response_json

    @staticmethod
    def request_image_analyze_colortone(image_url):
        """이미지의 사물 탐색"""
        post_data = {
            "image_url" : image_url,
        }
        request_url = f'{EgAnalyProtocol._get_serverhost()}/image/analyze/colortone' #사물 분석
        value_response = requests.post(request_url, json=post_data)
        if value_response.status_code != 200:
            return None
        value_response_json = value_response.json()
        return value_response_json


    @staticmethod
    def request_classifier_posttext(text):
        """포스팅 분류하기"""
        post_data = {
            "text" : text,
        }
        text_languages_url = f'{EgAnalyProtocol._get_serverhost()}/classifier/posttext' #콘텐츠 분류
        value_response = requests.post(text_languages_url, json=post_data)
        if value_response.status_code != 200:
            return None
        value_response_json = value_response.json()
        return value_response_json


    @staticmethod
    def request_text_languages(texts):
        """텍스트의 언어코드 추출하기 """
        post_data = {
            "text" : texts,
        }
                
        text_languages_url = f'{EgAnalyProtocol._get_serverhost()}/text/languages' #포스팅 언어 분석 
        value_response = requests.post(text_languages_url, json=post_data)
        if value_response.status_code != 200:
            return None
        value_response_json = value_response.json()
        return value_response_json

    @staticmethod
    def request_calculator_reach(profile_dict,post_list,avg_like_count,avg_comment_count):
        """예상 도달수 """
        #예상 도달수 -> Analy 요청 
        post_data = {
            "profile_dict" : profile_dict,
            "post_list": post_list,
            "avg_like_count":avg_like_count,
            "avg_comment_count":avg_comment_count
        }
        reach_url = f'{EgAnalyProtocol._get_serverhost()}/calculator/reach'
        value_response = requests.post(reach_url, json=post_data)
        if value_response.status_code != 200:
            return None
        value_response_json = value_response.json()
        return value_response_json