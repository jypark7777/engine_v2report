from django.core.management import BaseCommand
from report.models.report import *
from instagram_score.models import Userinfo, Scorev1
import requests, traceback,csv
from collections import Counter
import time
from statistics import fmean
from report.make_stat import make_status_ig_user, rank_ig_user
from component.views import classifier_user
class Command(BaseCommand):
    def handle(self, *args, **options):

        input_users = [
            # 'karuselli_', #롯데마켓
            # 'sohnheejin',
            # 'oneweek__',
            # 'silverrain52',
            # 'ehcl15',
            # 'luv.__.yul',
            # '0720_b',
            # 'triple3_jjj',
            # 'elly.jeon',
            # 'things__is2',
            # 'j_merry_j',
            # 'curryuri',
            # 's5llala',
            # 'gyugyu_home', #슬밋 - 인센스 
            # 'sungsung.mom',
            # 'xzxxin',
            # 'd_ia_n_',
            # 'keemhyemin',
            # 'to.dol',
            # 'r.tari',
            # 'ownfloa',
            # 'li.luna_',
            # 'eunsong_yoo_c',
            # 'soma_kim',
            # 'charminghee__',
            # 'Heoyeonzu',
            # 'juhyunkkk',
            # 'suminieeq',
            # 'gowoonal',
            # 'sheemlog',
            # 'yu___jo',
            # 'saena.home',
            # '_luv.reun_',
            # 'you___ri_',
            # '_om.ys',
            # 'hyein2ee',
            # 'y.05_06',
            # 'iffffy__',
            # 'simsvely',
            # 'serala__',
            # 'haehae.__',
            # 'an_raccoon',
            # 'aboutdesouffle_', #슬밋 - 세럼 
            # 'slowkitchen',
            # 'kmj_arielle',
            # 'torys_',
            # '0211___0g',
            # '_h_xx_n_',
            # 'parkyoonoo',
            # 'bitte.v',
            # 'xinyoha',
            # '95.1star',
            # 'kimsyamy',
            # 'jngwn____',
            # '101floorelevators',
            # 'ttommie',
            # 'pin_choy',
            # 'octoberholly',
            # 'rucygray',
            # 'lecristal',
            # 'daeun.home',
            # 'o_o_full',
            # 'ahnyyu',
            # 'my_juuu_',
            # 'loeybad',
            # 'sat.12am',
            # 'loosish_',
            # 'moooninwinter',
        ]

        # input_users = [
        #     'yook_can_do_it',
        #     'ryusdb',
        #     'minah320_97',
        #     'jxxvvxxk',
        #     'gfriendofficial',
        #     'youna_1997',
        #     'juanxkui',
        #     'hellopapa11',
        #     'sh_9513',
        #     'official_kard',
        #     'bobbyindaeyo',
        #     'joshu_acoustic',
        #     'leehi_hi',
        #     'wannaone.official',
        #     'aagbanjh',
        #     'imhyoseop',
        #     'kim_msl',
        #     'marcellasne_',
        #     'juneeeeeeya',
        #     'pledis_boos',
        #     'kwakdongyeon0',
        #     '_minzy_mz',
        #     'jin_a_nana',
        #     'chwenotchew',
        #     'clean_0828',
        #     'seo_cccc',
        #     'tvndrama.official',
        #     'arden_cho',
        #     'ron_sae',
        #     'sjkuksee',
        #     'jilwww',
        #     'mr_kanggun',
        #     'mo.on_air',
        #     'xhyolynx',
        #     'moon_ko_ng',
        #     'hye_yoon1110',
        #     '1004yul_i',
        #     'gnani_____',
        #     'rain_oppa',
        #     'dlstmxkakwldrl',
        #     'bts.bighit.__',
        #     'leejungshin91',
        #     'y_haa.n',
        #     'w_n_r00',
        #     'leesiyoung38',
        #     'ddana_yoon',
        #     'chang._.a',
        #     'blobyblo',
        #     'bigmatthewww',
        #     'callmegray',
        #     'bighit7official',
        #     'akmu_suhyun',
        #     'hyominnn',
        #     'ohvely22',
        #     'zennyrt',
        #     'woozi_universefactory',
        #     'minhyuk202523',
        #     'rovvxhyo',
        #     'sbs_runningman_sbs',
        #     'sound_of_coups',
        #     'jungkookbts',
        #     'jungkook_forever',
        #     'inkyung97',
        #     'leesoohyuk',
        #     'earlyboysd',
        #     'official_everglow',
        #     'shinhs831',
        #     'jyheffect0622',
        #     'smtownandstore',
        #     'songilkook',
        #     'sssong_yh',
        #     'official_theboyz',
        #     'voguekorea',
        #     'jeeseokjin',
        #     'i_icaruswalks',
        #     'actor_jingoo',
        #     'chan_w000',
        #     'day6kilogram',
        #     'choiminho_1209',
        #     'momoland_official',
        #     'netflixkr',
        #     'soooo_you',
        #     'elina_4_22',
        #     'crush9244',
        #     '____kimwoobin',
        #     'cube_ptg',
        #     'ireneisgood',
        #     'ast_jinjin',
        #     '_dong_ii',
        #     'd_a___m_i',
        #     'han_ye_seul_',
        #     'illusomina',
        #     'overdokyungsoo',
        #     'artist_eunji',
        #     'mj_7.7.7',
        #     'ncit_kimjw',
        #     'skullhong12',
        #     'blackpinkcofficial',
        #     'samuliesword',
        #     'hihyunwoo',
        #     'solarkeem',
        #     'newharoobompark',
        #     'kumajaewoo',
        #     'bts__jungk00k',
        #     'sambahong',
        #     'whee_inthemood',
        #     'hanjiji54',
        #     'hongsick',
        #     'j_chaeyeoni',
        #     'hyorin_min',
        #     'somin_jeon0822',
        #     'loonatheworld',
        #     'heizeheize',
        #     'iammingki',
        #     '_zziwooo0',
        #     'marieclairekorea',
        #     'yunho2154',
        #     'taecyeonokay',
        #     'betterlee_0824',
        #     'bts.0fficials',
        #     'goyounjung',
        #     'ellekorea',
        #     'kookoo900',
        #     'awesomehaeun',
        #     'dntlrdl',
        #     'e.jiah',
        #     'dahee0315',
        #     're_mini_scene',
        #     'jaehwan0527',
        #     'satgotloco',
        #     'maetamong',
        #     'jj_1986_jj',
        #     'yg_ent_official',
        #     'ziont',
        #     'real.be',
        #     'hyunjoong860606',
        #     'yoo_yeonseok',
        #     'kim_d.he',
        #     'hjonghyun',
        #     'candyseul',
        #     'deantrbl',
        #     'gyuram88',
        #     'wooju1025',
        #     'yura_936',
        #     '_yoonj1sung_',
        #     'changmin88',
        #     'taeri__taeri',
        #     'jinyoung0423',
        #     '2km2km',
        #     'imjennim',
        #     'k_hanna_',
        #     'nancyjewel_mcdonie_',
        #     'cxxsomi',
        #     'j.seph_',
        #     'kimyk10',
        #     'gooreumseng',
        #     '__shinyeeun',
        #     'somin_jj',
        #     'le2jh',
        #     'xxjjjwww',
        #     'longlivesmdc',
        #     'official_jimiin',
        #     'ravithecrackkidz',
        #     'sunghoon1983',
        #     'tabloisdad',
        #     'eugene810303',
        #     'sodam_park_0908',
        #     'hutazone',
        #     'kimminkyu_0312',
        #     'hanhyojoo222',
        #     'labels.hybe',
        #     'eajpark',
        #     'jiminxjamie',
        #     'ab6ix_official',
        #     'bohyunahn',
        #     'official_oneus',
        #     '42psy42',
        #     'winnercity',
        #     'koohara__',
        #     'hermosavidaluna',
        #     'williamhammington',
        #     'chengxiao_0715',
        #     'meow91__',
        #     'sonsungdeuk',
        #     'dj_gpark',
        #     'bts.7',
        #     'achahakyeon',
        #     'aileeonline',
        #     'honey_lee32',
        #     'kbsdrama',
        #     'susemee',
        #     'stylenanda_korea',
        #     'komurola',
        #     'sysysy1102',
        #     'for_everyoung10',
        #     'melovemealot',
        #     'inhyuk_bb',
        #     'parkb0gum',
        #     'nwh91',
        #     'w_o_o_y_a',
        #     '3.48kg',
        #     'jinmiran_',
        #     'woo.ddadda',
        #     'lavieenbluu',
        #     'woodz_dnwm',
        #     'soominn_jo',
        #     'b__yccn',
        #     'dk_is_dokyeom',
        #     'produce_x_101',
        #     'btsjungk00kie',
        #     'justin_jisung',
        #     'zzyuridayo',
        #     'khunsta0624',
        #     'yooranna',
        #     '0myoung_0526',
        #     'yoanaloves',
        #     'akmuchanhk',
        #     '_____silverstone_____',
        #     'cookat_korea',
        #     'parkhaejin_official',
        #     'lafilledhiver_',
        #     'imnameim',
        #     'dlehdgnl',
        #     'kanginnim',
        #     'yute_v',
        #     'wm_ohmygirl',
        #     'bentleyhammington',
        #     'kimwon.pil',
        #     'kasper0524',
        #     'yubi_190',
        #     'aksakfn12',
        #     'glorypath',
        #     'boyoung0212_official',
        #     'taeuniverse',
        #     'yookihhh',
        #     'nayoungkeem',
        #     'dbqudwo333',
        #     'yuqisong.923',
        #     'bbang_93',
        #     'roma.emo',
        #     'jeonghaniyoo_n',
        #     'mrs_macarons',
        #     'actorctj',
        #     'kim_bora95',
        #     'pyojihoon_official',
        #     'mingi_1122',
        #     'todayhouse',
        #     'soobinms',
        #     'ye._.vely618',
        #     'every__nn',
        #     'from_youngk',
        #     'hyukoh2000',
        #     'kyj._.95',
        #     'jeonghwa_0508',
        #     'ara_go_0211',
        #     'blackpinks',
        #     'jeonjungkook__bts',
        #     'cix.official',
        #     'yysbeast',
        #     'souththth',
        #     'jsomin86',
        #     'everyone_woo',
        #     'holly608',
        #     'jeon.yeobeen',
        #     'min.nicha',
        #     '2xj_hee',
        #     'pockyjr',
        #     'rlo.ldl',
        #     'youngji_02',
        #     'hv_nara',
        #     'kwon_jo',
        #     'hyuniiiiiii_95917',
        #     'yoonjujang',
        #     'minn.__.ju',
        #     'sangyeob',
        #     'ddablue',
        #     'd.ddablue',
        #     'girlsgeneration',
        #     'gominsi',
        #     'nuest_official',
        #     'doflwl',
        #     'chaileeson',
        #     'travelholic_insta',
        #     'leo_jungtw',
        #     'yu.n_wk',
        #     'hyemhyemu',
        #     'moonjaein',
        #     'eden_table',
        #     'btobpeniel',
        #     'boram__jj',
        #     'gojoonhee',
        #     'vely.mom',
        #     'xodambi',
        #     '_yujin_an',
        #     '_happiness_o',
        #     'pyoapple',
        #     'ummmmm_j.i',
        #     'onedayxne',
        #     'min_namkoong',
        #     'cravity_official',
        #     'soul.g_heo',
        #     'official.apink2011',
        #     'jstar_allallj',
        #     'sunbin_eyesmag',
        #     'official_a.c.e7',
        #     'mcnd_official',
        #     'prince_kwanghee',
        #     'etudeofficial',
        #     'kkachi99',
        #     'mjbaby0203',
        #     's911010',
        #     'bscenez',
        #     'bitnara1105',
        #     'bts.0fficail',
        #     'exidofficial',
        #     'sora_pppp',
        #     'hyeliniseo',
        #     'kimdwan_',
        #     'aomgofficial',
        #     'songseungheon1005',
        #     'btob_silver_light',
        #     'hwa.min',
        #     '_______youngmoney',
        #     'cube_clc_official',
        #     'smtownstation',
        #     'jungkookjeon7',
        #     'liakimhappy',
        #     'gookju',
        #     'mingue.k',
        #     'ljh_babysun',
        #     '10000recipe',
        #     'xxadoraa',
        #     'mulgokizary',
        #     'dprlive',
        #     'vixx_stargram',
        #     'ho5hi_kwon',
        #     'jtbcdrama',
        #     'haneulina',
        #     'yuuzth',
        #     'som0506',
        #     'real_jinhyuk',
        #     'kjh_official',
        #     'x_xellybabyx',
        #     'yim_siwang',
        #     'wjsn_cosmic',
        #     'deukie_______',
        #     'bk_arta',
        #     'kanggary_yangban',
        #     'moonjungwon',
        #     'hyun.jxx0_p',
        #     'modelhanhyejin',
        #     'giriboy91',
        #     'vliveofficial',
        #     'dok2gonzo',
        #     'jangsk83',
        #     'noodle.zip',
        #     'madongseok_',
        #     'ff0427',
        #     'dispatch_style',
        #     'holland_vvv',
        #     'demi_kimee',
        #     'jaeuck.kim',
        #     'yeh.shaa_',
        #     'reveramess_',
        #     '_ohhayoung_',
        #     'risabae_art',
        #     'officialfromis_9',
        #     'ryuniverse328',
        #     'realisshoman',
        #     'jrjswn',
        #     'jihye8024',
        #     'ohttomom',
        #     'chaestival_',
        #     'silver_rain.__',
        #     'jungeum84',
        #     'kopular',
        #     'lee_cs_btob',
        #     'taehyuntxt_official',
        #     'park_yury',
        #     'tiny.pretty.j',
        #     'tiny.pretty.j',
        #     '_chaechae_1',
        #     '__yoonbomi__',
        #     'shownuayo',
        #     'ysh6834',
        #     'vtcosmetics_official',
        #     'lee_si_eon',
        #     'imhyunsik',
        #     'wanna._b',
        #     'hazzisss',
        #     'c_chani_i',
        #     'hongsuzu',
        #     'soobin1119',
        #     'dbeoddl__',
        #     'woooojin0408',
        #     'yujin_so',
        #     'innisfreeofficial',
        #     'leejehoon_official',
        #     'beatburgerjae',
        #     'greedeat',
        #     'iu_leejieun516',
        #     'yena.jigumina',
        #     'doonabae',
        #     'shinee_jp_official',
        #     'henn_kim',
        #     'baebaealice',
        #     'don9_han',
        #     'chaejh_',
        #     'sbsnow_insta',
        #     'bts.jungkookt',
        #     'jinjoo1224',
        #     'ggumigi',
        #     'eunjung.hahm',
        #     'y.na__',
        #     'jeee622',
        #     'kimbutter_daddy',
        #     'taeyang_0228',
        #     'kisy0729',
        #     'yoo__sha',
        #     'kookies_luv',
        #     '216jung',
        #     'bts.bang1an',
        #     'tobenstagram',
        #     'sarangdungy',
        #     'leeminho_mino',
        #     'bemy_rin',
        #     'changmo_',
        #     'socun89',
        #     '2ah.in',
        #     '_weeekly',
        #     'beautyplmagazine',
        #     'type4graphic',
        #     'knhs2',
        #     'slowswan',
        #     'kangmeen',
        #     'ph1boyyy',
        #     'sejinming',
        #     'manyo_yoojin',
        #     'gu9udan',
        #     '0seungyeon',
        #     'byzelo',
        #     'mayj517',
        #     'gentlemonster',
        #     'kkmmmkk',
        #     'bangstergram',
        #     'ophen28',
        #     '1995.mj',
        #     'mbcdrama_now',
        #     'bts',
        #     'nuestaron',
        #     'tae_rii_',
        #     'jungkookjeon',
        #     's_sohye',
        #     'ch_amii',
        #     'zo__glasss',
        #     'insight.co.kr',
        #     'jane.asmr',
        #     'jfla',
        #     'official_sunmi',
        #     'yebin__',
        #     'official_jdh',
        #     'jang.doyoun',
        #     'khxxn_',
        #     'woohye0n',
        #     'coenffl',
        #     'luvlk89',
        #     'junha0465',
        #     'tvxq.official',
        #     'ssozi_sojin',
        #     'chosaeho',
        #     'billboard_korea',
        #     'yerin_the_genuine',
        #     'bewhy.meshasoulja',
        #     'official_therose',
        #     'hyun_woo_tv',
        #     '__leeheeeun__',
        #     'han_kyung__',
        #     'gini_s2_',
        #     'young_g_hur',
        #     'kevinwoo_official',
        #     'nail_unistella',
        #     'yangse2848',
        #     'thequiett',
        #     'vivamoon',
        #     'jimincut',
        #     'official.hasungwoon',
        #     'nakedbibi',
        #     'danielhenney',
        #     'yoonjongactor_official',
        #     'hhy6588',
        #     'shinhancard_official',
        #     'namdareum_mom',
        #     'jungdabiny',
        #     'seojin_ban',
        #     'dei8ht',
        #     'stephanielee199',
        #     'bn_95819',
        #     'bn_95819',
        #     'mixxmix_seoul',
        #     'zipcy',
        #     'cs__min',
        #     '4000man_',
        #     'leetaehwan0221',
        #     'leetaehwan0221',
        #     '_choiiii__',
        #     'yj_loves',
        #     'weki_meki',
        #     'djjina_official',
        #     'kim.tae95bts',
        #     'got7updates_',
        #     'estapramanita',
        #     'ulael_',
        #     'yunakim',
        #     'zzangjeolmi',
        #     'fila_korea',
        #     '_angel_elijah_',
        #     'rh_ab',
        #     'lilyiu_',
        #     'gyeongree',
        #     'therealminnn',
        #     'gyeongree',
        #     'kbsworldtv',
        #     'nam_yoonsu',
        #     'imvely_jihyun',
        #     'code_kunst',
        #     'kieunse',
        #     'ssoheean',
        #     'bts.taehyung',
        #     '_taeyeonfanpage',
        #     'seungwon_jeong',
        #     '0__0man',
        #     'hanna91914',
        #     'lovelyjoohee',
        #     'dj_siena',
        #     'jun._.0512',
        #     'superstar_jhs',
        #     'tvn_joy',
        #     'candyz_hyojung',
        #     'jypactors_official',
        #     'younghotyellow94',
        #     'dindinem',
        #     'tojws',
        #     'munchinthepool',
        #     '_kimjaekyung_',
        #     'kongkong2_kim',
        #     'dengdeng_e',
        #     'subinyu1106',
        #     'ssoyang84',
        #     'samhammington',
        #     'naturerepublic_kr',
        #     '_minjukim_',
        #     'suminzz',
        #     'dxhxnxe',
        #     'qtfreet',
        #     'exo',
        #     'lovely.katie.k',
        #     'kto940620',
        #     'keykney',
        #     'woo_o9o',
        #     'yoon_ambush',
        #     'kkamooong',
        #     'cube_official_btob',
        #     '1993kg',
        #     'cherrybullet',
        #     'designdain',
        #     'tangle_mimi',
        #     'thebangtanboy.bts',
        #     'emartstore',
        #     'ttokkii',
        #     'jiyeon.s_0',
        #     'bts_0fficail',
        #     '10042n00',
        #     'ssaaaann__22',
        #     'kkwonsso_94',
        #     'yg_kplus',
        #     'banyoonhee',
        #     'sola5532',
        #     'chloelxxlxx',
        #     'dongdong810',
        #     'sooviin38',
        #     'seola_s',
        #     'bimil_jieun',
        #     'godjp',
        #     'lloveeely',
        #     'taekook.tv',
        #     'l_hajoon',
        #     'super_d.j',
        #     'super_d.j',
        #     'soltattoo',
        #     'for_gomroni_',
        #     '_____jjh',
        #     'clorlk',
        #     'hyunheehong',
        #     'ash.island',
        #     'thousand_wooo',
        #     'the_verivery',
        #     '_liustudio_',
        #     'byeonwooseok',
        #     'd.of.j.c',
        #     'park_bosung',
        #     'uyj__0803',
        #     'sunmiub',
        #     'jung.y00n',
        #     'kaijexo',
        #     'kimehwa',
        #     'bh_bts7',
        #     'rkm0855',
        #     'yyyyeeun',
        #     'chulsoon_official',
        #     'ssss3063',
        #     'kimheebibi',
        #     'supermom_sujin',
        #     'r_yuhyeju',
        #     'official_gncd11',
        #     'leejongsuky',
        #     'seonkyounglongest',
        #     'taevin.lee',
        #     'amourfor_u',
        #     'jungnam_bae',
        #     'lee____bora',
        #     'innisfree.instalog',
        #     'j_oo.e_0en',
        #     'se7enofficial',
        #     'h1ghrmusic',
        #     'itsjustswings',
        #     'yjiinp',
        #     '__chommy',
        #     'eeunseo._.v',
        #     'melodysoyani',
        #     'do.hyeon_im',
        #     'oneroom.make',
        #     'mgain83',
        #     '_seong_hee',
        #     'choehyeokgeun',
        #     'got7_fanclub',
        #     'joohoneywalker',
        #     'hyo_joo',
        #     'oxxooi',
        #     'syv0428',
        #     'superb_ean',
        #     'fashionandstyle.official',
        #     'hunter.kang',
        #     'shin_sung_rok',
        #     'garin_ss',
        #     'damikwon_',
        #     'yoonhyunmin',
        #     'dglee20',
        #     'official_yooseonho',
        #     'lsod.d',
        #     'yjaybaby',
        #     'jupppal',
        #     'sung_yuri_',
        #     'jess.02.23',
        #     'junghyesung91',
        #     'chanmi_96a',
        #     'dlgofl85',
        #     'peripera_official',
        #     'bangtanparkjimin',
        #     'cindynoona',
        #     'cu_official',
        #     'chuu_official',
        #     'exy_s2',
        #     'eatmother',
        #     'grim_b',
        #     'hello_dongwon',
        #     'babebani',
        #     'saico0111',
        #     'kjjzz87',
        #     'h1003141592',
        #     'ukiss_jun97',
        #     'seyoung_10',
        #     '_asia_prince_jks',
        #     'clio_official',
        #     'daxbin',
        #     'dasom_lovely',
        #     'hsh0705',
        #     'heeae_official',
        #     'zihwa_tattooer',
        #     'real_2pmstagram',
        #     'lalalalisa_ma',
        #     'z_hera',
        #     '92_hyungseok',
        #     'mlnhe',
        #     'tt_trend',
        #     'playlist_studio',
        #     'wonlog',
        #     'braveg_yj',
        #     '94_j.a',
        #     'minyoung_aori',
        #     'jinwoon52',
        #     'giantpengsoo',
        #     'chaelisa.area',
        #     'leanavvab',
        #     'bts7_txt',
        #     'kidcozyboy',
        #     'yjoo_oh',
        #     'pigmong___',
        #     'r0s8y_',
        #     'oddhw',
        #     'ggulhouse',
        #     'moonjongyeup',
        #     '_maoi_yua_hyun_',
        #     'mayersung',
        #     'oliveyoung_official',
        #     'btsjungkooki_',
        #     'sungcheol2',
        #     'baroganatanatda',
        #     'k_jenny_k',
        #     'ahoi_ing',
        #     'chungjizzle',
        #     'foodyinkorea',
        #     'aahnjaehong',
        #     'yoojunglee11',
        #     'jiyoon_park_',
        #     'saegeemtattoo',
        #     'nana.un',
        #     'nayoung_lim95',
        #     'ssovely1024',
        #     'sungziyoung',
        #     'euddeume_',
        #     'noahmik',
        #     'leechungah',
        #     'theeasychan',
        #     'midorithais',
        #     'hyesuuuuuya',
        #     'pkalbum',
        #     'a12486',
        #     'joowon.unnie',
        #     'ayeoniiiiii',
        #     'hajunn_mom',
        #     'thesy88',
        #     'han_bling_',
        #     'highcutstar',
        #     'cog.j_92',
        #     'ch.yoooon',
        #     'jihoa_f',
        #     'yn_s_1230',
        #     'jinkyung3_3',
        #     'xiaxiaxia1215',
        #     'n.d.kim',
        #     'cook_and_candle',
        #     'gunheenim',
        #     '7elevenkorea',
        #     'luv__ribbon',
        #     'hyunbeenshin',
        #     'englishforkorean',
        #     'yoonara_mood',
        #     'tv_blackpink',
        #     'lisablackspink',
        #     'callmenahna',
        #     '___solvely___',
        #     'ttovely__',
        #     'lee_mido',
        #     'hehehe0',
        #     'jeong.woo.joo',
        #     'wg_lim',
        #     'kisum0120',
        #     'j_10.2_76',
        #     'woooozzzzz',
        #     'officialc9ent',
        #     'ioi_official_ig',
        #     'frombeginning_',
        #     'cheap_box',
        #     'jye._.e',
        #     'xxjominxx',
        #     'koreanenglishman',
        #     'haseokjin',
        #     'boori_boo',
        #     'official_lvlz8_',
        #     'seon_uoo',
        #     'mido_ring',
        #     'faker',
        #     '131moon_',
        #     'dear.zia',
        #     'hatfelt',
        #     'dayomi99',
        #     'jtbc.insta',
        #     'nizinanjjang',
        #     'yoonmida',
        #     'khmnim1513',
        #     'soonmoo_cat',
        #     '8eomatom',
        #     'ivenoven',
        #     '2__yun__2',
        #     'btsjungkook.97',
        #     '_eunz1nara_',
        #     'ssung916',
        #     'graziakorea',
        #     'converse_kr',
        #     'on_do__',
        #     'yeonions',
        #     'subsubey',
        #     'bts._.7boys',
        #     'jaelim_song',
        #     'im_hyeonzzu',
        #     'hazelnut_dog',
        #     'moonheeyul',
        #     'soojunglim_',
        #     'pinkgabong',
        #     'lalisa_blackpinks',
        #     'bts.igs',
        #     'smitruti1010',
        #     'soribaby',
        #     'yoou.ch',
        #     'laneige_kr',
        #     'my.o_',
        #     'dasolmom_',
        #     'queenchoa_',
        #     'originals_kr',
        #     'krunk_official',
        #     'iluvyub',
        #     'phh1013',
        #     'vminkook_tv',
        #     'sonhojun_officia',
        #     'hashblanccoa',
        #     'ohseunghee_official_',
        #     'hyexok_',
        #     'ue1124',
        #     'lesleyhee',
        #     'sanethebigboy',
        #     'seungwoolee',
        # ]

        input_users = [
            '_spella',
            'iffffy__',
            'you___ri_',
            'kimsyamy',
            '95.1star',
            'soma_kim',
            'torys_',
            'r.tari',
            'd_ia_n_',
        ]
        
        with open('export/output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            colum = ['유저명', '상품', '스타그램', '이미지', '셀카/사람/배경', "컬러톤"]
            writer.writerow(colum)
            for username in input_users:
                # try:
                    # print(f'{username} - Start')
                    # res = requests.get(f'https://feat.report/crawl_instagram_save?request_type=user&parameter={username}')
                    # time.sleep(5)
                    
                    # make_status_ig_user(username)
                    # ig_userinfo = IGUserInfo.objects.get(username=username)
                    # rank_ig_user(ig_userinfo.pk)

                    # try:
                    #   classifier_user(username, is_force=True)
                    # except:
                    #     print("ERROR classifier_user------- ", username)

                    ig_userinfo = IGUserInfo.objects.filter(username=username).last()
                    print(ig_userinfo)
                    if ig_userinfo == None:
                        continue
                    
                    account, _ = Account.objects.get_or_create(ig_pk=ig_userinfo.pk) 

                    category = {}

                    ig_content_statistics_list = account.ig_content_statistics.all()
                    for ig_content_statistics in ig_content_statistics_list:
                        tags = ig_content_statistics.tags.all()
                        for tag in tags:
                            if tag.category.name not in category:
                                category[tag.category.name] = []

                            category[tag.category.name].append(tag.name)

                    # print(category)

                    product = ''
                    if '상품' in category:
                        product = Counter(category['상품']).most_common()

                    stargram = ''
                    if '스타그램' in category:
                        stargram = Counter(category['스타그램']).most_common()

                    accessibility = ''
                    if 'Accessibility Caption' in category:
                        accessibility = Counter(category['Accessibility Caption']).most_common()
                    
                    selfie = ''
                    if '셀카/사람/배경' in category:
                        selfie = Counter(category['셀카/사람/배경']).most_common()
                    
                    colortone = ''
                    if '컬러톤' in category:
                        colortone = Counter(category['컬러톤']).most_common()

                    writer.writerow([username,product, stargram, accessibility, selfie, colortone])

                # except:
                #     print("ERROR ------- ", username)

        """
        포스팅 기준으로 뽑기
        """
        with open('export/output_posting.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            colum = ['유저명', 'code', '포스팅', '상품', '스타그램', '이미지', '셀카/사람/배경', '컬러톤']
            writer.writerow(colum)
            for username in input_users:

                ig_userinfo = IGUserInfo.objects.filter(username=username).last()
                if ig_userinfo == None:
                    continue

                json_post = ig_userinfo.json_post
        
                account, _ = Account.objects.get_or_create(ig_pk=ig_userinfo.pk) 

                for crawlpost in json_post['results']:
                    try:
                        post_insta_pk = crawlpost['insta_pk']
                        code = f"https://instagram.com/p/{crawlpost['code']}"

                        if 'crawlpostcaption' in crawlpost and len(crawlpost['crawlpostcaption']) > 0:
                            crawlpostcaption = crawlpost['crawlpostcaption'][0]
                            #포스팅 글 분류 , Category - 스타그램, Category - 상품
                            text = crawlpostcaption['text']
                            stat = account.ig_content_statistics.filter(content__ig_pk=post_insta_pk).last()
                            
                            category = {}
                            tags = stat.tags.all()
                            for tag in tags:
                                if tag.category.name not in category:
                                    category[tag.category.name] = []

                                category[tag.category.name].append(tag.name)

                                # print(category)

                                product = ''
                                if '상품' in category:
                                    product = Counter(category['상품']).most_common()

                                stargram = ''
                                if '스타그램' in category:
                                    stargram = Counter(category['스타그램']).most_common()

                                accessibility = ''
                                if 'Accessibility Caption' in category:
                                    accessibility = Counter(category['Accessibility Caption']).most_common()
                                
                                selfie = ''
                                if '셀카/사람/배경' in category:
                                    selfie = Counter(category['셀카/사람/배경']).most_common()

                                colortone = ''
                                if '컬러톤' in category:
                                    colortone = Counter(category['컬러톤']).most_common()

                            writer.writerow([username, code, text, product, stargram, accessibility, selfie, colortone])
                    except:
                        pass
        