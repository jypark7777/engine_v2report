class BaseComponentDoesNotExist(Exception):
    """계산이 필요한 지표가 없을때"""
    def __init__(self):
        super().__init__()

    def __str__(self): return self.message


class ReachDoesNotExist(BaseComponentDoesNotExist):
    """[도달] 계산이 필요한 지표가 없을때"""
    message = '[도달]해당 계산에 필요한 지표가 없습니다.'

class RealInfluenceDoesNotExist(BaseComponentDoesNotExist):
    """[진짜영향력] 계산이 필요한 지표가 없을때"""
    message = '[진짜영향력]해당 계산에 필요한 지표가 없습니다.'

class AudienceQualityDoesNotExist(BaseComponentDoesNotExist):
    """[오디언스퀄리티] 계산이 필요한 지표가 없을때"""
    message = '[오디언스퀄리티]해당 계산에 필요한 지표가 없습니다.'

class EngagementDoesNotExist(BaseComponentDoesNotExist):
    """[반응] 계산이 필요한 지표가 없을때"""
    message = '[반응]해당 계산에 필요한 지표가 없습니다.'

