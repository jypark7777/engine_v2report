from statistics import NormalDist


def cal_realfake_weight(src_effort, src_zero_comments, src_comment_like_rate): # Test
    """진짜 가짜의 확률을 구함 
        Args
            src_effort : 노력대비 성과 (포스팅 업로드당 반응 받은 수)
            src_zero_comments : 댓글 0개 
            src_comment_like_rate : 댓글 - 좋아요 비율
    """

    """진짜 샘플링"""
    real_zero_comments = NormalDist.from_samples([0,0,0,0,3,2,0,2,0,0,0])
    real_efforts = NormalDist.from_samples([6.37,0.70,0.86,1.16,1.84,3.79,3.97,6.60,0.43,2.39,4.14])
    real_comment_like_rate = NormalDist.from_samples([0.049,0.054,0.108,0.078,0.041,0.028,0.041,0.030,0.147,0.035,0.123])

    """가짜 샘플링"""
    fake_zero_comments = NormalDist.from_samples([6,8,0,0,7,0,0,2,1,8,0])
    fake_efforts = NormalDist.from_samples([0.29,40.33,2.40,32.09,6.91,61.87,22.51,3.66,1.51,0.14,1.53])
    fake_comment_like_rate = NormalDist.from_samples([0.089,0.009,0.031,0.083,0.073,0.013,0.007,0.063,0.013,0.015,0.029])

    prior_fake = 0.6 #사전 확률
    prior_real = 0.4 #사전 확률

    posterior_real = (prior_real * real_efforts.pdf(src_effort) * real_zero_comments.pdf(src_zero_comments) * real_comment_like_rate.pdf(src_comment_like_rate))
    posterior_fake = (prior_fake * fake_efforts.pdf(src_effort) * fake_zero_comments.pdf(src_zero_comments) * fake_comment_like_rate.pdf(src_comment_like_rate))

    real_fake_weight = 0
    if posterior_fake > posterior_real:
        real_fake_weight = posterior_fake * 100
        if real_fake_weight > 1.0:
            real_fake_weight = 1.0
    else:
        real_fake_weight = 0

    print(posterior_real, posterior_fake, real_fake_weight)

    return real_fake_weight



# import numpy as np
# from scipy import stats
# bounds = [0, 100]
# n = np.mean(bounds)
# # your distribution:
# distribution = stats.norm(loc=n, scale=20)
# # percentile point, the range for the inverse cumulative distribution function:
# bounds_for_range = distribution.cdf(bounds)
# # Linspace for the inverse cdf:
# pp = np.linspace(*bounds_for_range, num=1000)
# x = distribution.ppf(pp)
# # And just to check that it makes sense you can try:
# from matplotlib import pyplot as plt
# plt.hist(x)
# plt.show()


# # src_effort = 0.182916465697421
# # src_zero_comments = 6
# # src_com_like = 0.0891760346932761

# # cal_realfake_weight(src_effort, src_zero_comments,src_com_like )
