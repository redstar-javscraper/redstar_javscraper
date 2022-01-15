# -*- coding: utf-8 -*-
import re
import random
import urllib
import urllib2
import urlparse
import json
import ssl
from datetime import datetime
from cStringIO import StringIO
import inspect
import os
import json

# import certifi
# import urllib3

HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

HDR_javdb = {
    'authority': 'javdb.com',
    'method': 'GET',
    'path': '/search?q=STARS-466&f=all',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'cookie': 'theme=auto; locale=zh; _ym_d=1641773830; _ym_uid=1641773830421828005; over18=1; _ym_isad=1; _jdb_session=XGuc6iwKyCx9gczSDfl7X0tcTwIRkN8sYNaCAeSS1QRBJIqFdojWK%2F9%2BfPLQjUcMfyHs5pIwRB4HamIiaN22%2BTbT6YbZkf5HVZ34CycIdaO3qdXibuTaIYOhYEnRyCTK8bGOWqWLJHikAPYKbKjr6UD1EkIxRXdUFgo%2Fwl0kYTGSPmQdgB3WGe0WTuLcGSWo7%2FsoDJBGJn98d%2Ft90tOairODQNCJhaOSUP9JA0jlOV265iFD5NXcRci9%2BVH9AIHP3uQWZL9HMH5dVwv3weA5IAWnyNJcSO%2FDyiKRxXiJRx5B1NsglRHCTKhO--LqQLVGBdNKM0cpIS--G8qBjputuvCNZkb%2BoIqW6g%3D%3D',
    'if-none-match': 'W/"7d8428bfc9404c412b88f8b56a2bc45c"',
    'referer': 'https://javdb.com/search?q=STARS-466&f=all',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }


HDR_AVDBS = {'authority': 'www.avdbs.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

HDR_R18 = {'authority': 'www.r18.com',
        'method':'GET',
        'path':'/api/v4f/contents/hnd00038?lang=en&unit=USD',
        'scheme':'https',
        'accept':'application/json, text/plain, */*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        'access-control-allow-origin':'*',
        'cookie':'country=kr; ex=USD; ab=b; mack=1; lg=en; _gali=floors',
        'referer':'https://www.r18.com/videos/vod/movies/detail/-/id=hnd00038/',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

HDR_JAVBUS = {'authority': 'www.javbus.com',
    'method': 'GET',
    'path': '/FSDSS-350',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': 'existmag=mag; PHPSESSID=r7u3bnc4jg8gnlltm4p9fvmec5',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

def Papago_Trans(txt,lang='en'):
    # 번역언어: # ko 한국어 # en 영어 # ja 일본어 # zh-CN 중국어 간체 # zh-TW 중국어 번체 # vi 베트남어
    # id 인도네시아어 # th 태국어 # de 독일어 # ru 러시아어 # es 스페인어 # it 이탈리아어 # fr 프랑스어

    # Logging('===========> 파파고 설정(PapagoUSE): ' + str(Prefs['papago_use']),'Debug')
    # Logging('===========> 파파고 키값(PapagoKey): ' + str(Prefs['papagokey']), 'Debug')
    if (str(Prefs['papago_use']) == 'False'):
        Logging('### 파파고 사용 안함 체크됨(Papago Not use checked) ###','Debug')
        return txt
    if (str(Prefs['papagokey']) == 'None' ):
        Logging('### 파파고 키가 빈 값임(Papago key empty) ###','Debug')
        return txt
    if (txt == ''): 
        Logging('### 파파고 번역 요청 텍스트 없음 ###','Debug')    
        return txt

    try:
        # 환경변수에 입력한 파파고 키를 랜덤으로 추출해 사용함
        # 환경변수에는 key,secret key2,secret2 .... 으로 입력되어야 함
        # Logging('### PapagoKEY : ' + str(Prefs['papagokey']), 'Info')
        client_key=str(Prefs['papagokey'])
        papagokey = client_key.split(' ')
        get_papagokey = random.choice(papagokey)
        client_key_array = get_papagokey.split(',')
        client_id = client_key_array[0]
        client_secret = client_key_array[1]
        # Logging('### ID: ' + str(client_id) + ' Secret: ' + str(client_secret),'Debug')

        source_lang =  lang
        target_lang = "ko"
        encText = txt
        # Logging('### Trans Original TXT: ' + encText, 'Debug')
        data = "source=" + source_lang + "&target=" + target_lang + "&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib2.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib2.urlopen(request, data=data.encode("utf-8"), timeout=int(Prefs['timeout']))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            nResult = String_slice(response_body, 'translatedText":"', '","engineType')
            # Logging('#### Papago Trans Result : ' + str(response_body),'Debug')
            Logging('####  파파고 번역완료!   번역 전:' + encText + '  번역 후 :' + str(nResult),'Debug')
            return nResult
        elif (rescode == 400):
            Logging('HTTP 400 Bad Request 오류가 발생하였습니다. 요청 전문: ' + data,'Error')
            return txt
        else:
            # print("Error Code:" + rescode)
            return txt
    except:
        Logging('@@@ papago Exception 번역 요청: ' + txt + '언어: ' + lang,'Error')
        return txt

def String_slice(nStr,nStartstr,nEndstr):
    # 문자열 자르기(입력: 원본, 시작문자열, 끝 문자열)String slice. org: nStr  findString: nStartstr   Endstring: nEndstr
    nStr_find=''

    if (nStr == ''):
        return ''
    if (nStartstr == ''):
        nStartstr=0
    else:
        nStr_find = nStr.find(nStartstr)
        if(nStr_find == -1 ):
            return ''
    nStartstr = nStr_find + len(nStartstr)

    if (nEndstr == ''):
        nEndstr=len(nStr)
    nEndstr = nStr.find(nEndstr, nStartstr)
    nResult = nStr[nStartstr:nEndstr].strip() # .strip()하면 개행문자를 모두 제거해줌
    return nResult

def Extract_str(nStr,nStartstr,nEndstr):
    # nStr: 원본 문자열
    # nStartstr: 시작 문자열
    # nEndstr: 끝 문자열
    # 시작~끝 문자열로 자른 뒤 a href의 문자열을 추출해 배열로 리턴함
    # ex> ABC, DEF, GHI값을 배열로 반환
    # <span id = "performer" >
    # <a href = "/digital/videoa/-/list/=/article=actress/id=1047128/">ABC</a>
    # <a href = "/digital/videoa/-/list/=/article=actress/id=1042219/">DEF</a>
    # <a href = "/digital/videoa/-/list/=/article=actress/id=1051357/">GHI</a>
    # </td >

    nStr=String_slice(nStr,nStartstr,nEndstr)
    nNotfound=nStr.find('----')
    nFound=nStr.find('a href')
    nResult=[]

    if (nNotfound == -1 ):
        if (nFound <> -1):
            sTemp=nStr.split('a href')
            j = len(sTemp)
            for i in range(1, j):
                nCut=String_slice(sTemp[i],'>','<')
                nResult.append(nCut)
                Logging('Extract_str 자르기 전: ' + sTemp[i] + ' 자른 후: ' + nCut, 'Debug')

            return nResult
    return #Return 결과는 None

def Extract_str_title_pornav(nStr,nStartstr,nEndstr,nPoombun,ret_gubun):
    # nStr: 원본 문자열
    # nStartstr: 시작 문자열
    # nEndstr: 끝 문자열
    # nPoombun: 검색할 품번
    # ret_gubun: 리턴할 항목 지정('TITLE: 제목 리턴', 'URL: 상세주소 리턴')
    # 시작~끝 문자열로 자른 뒤 품번에 해당하는 타이틀명을 리턴함

    Logging('┌────── pornav 제목 찾기 시작  ──────┐','Info')
    nStr=String_slice(nStr,nStartstr,nEndstr)
    nPoombun=nPoombun.upper()
    if 'FC2' in nPoombun: nPoombun = nPoombun.replace('-', ' ').replace('FC2PPV','FC2 PPV')
    if (('CARIBBEANCOM' in nPoombun) or ('CARIB' in nPoombun) or ('LESSHIN' in nPoombun) or ('NYOSHIN' in nPoombun) or
            ('REAL-DIVA' in nPoombun) or ('UNKOTARE' in nPoombun) or ('KIN8TENGOKU' in nPoombun) or ('C0930' in nPoombun) or
            ('HEYDOUGA' in nPoombun) or ('H0930' in nPoombun) or ('GACHINCO' in nPoombun) or ('1PONDO' in nPoombun) or
            ('10MUSUME-DIVA' in nPoombun) or ('HEYZO' in nPoombun) or ('MD ' in nPoombun) or ('PACOPACOMAMA' in nPoombun) or
            ('H4610' in nPoombun) ):
        nPoombun = nPoombun.replace('-', ' ')

    index = 0
    while index > -1:
      try:
        index = nStr.index('<a itemprop="url"', index)
        searchstr = nStr[index:]
        rTITLE = String_slice(searchstr,'>','<')
        rURL = String_slice(searchstr,'href="','"')
        Logging('Slice Result  > title: ' + rTITLE + ' > URL: ' + rURL, 'debug')
        if nPoombun in rTITLE.replace('FC2-PPV','FC2 PPV').replace('FC2PPV','FC2 PPV'): #품번 텍스트가 rTITLE 문자열에 있는지 체크크
            rTITLE = rTITLE.replace('（','').replace('）','').replace(nPoombun,'').replace('[','').replace(']','')
            Logging('찾은 품번 제목: ' + rTITLE,'Debug')
            Logging('└────── pornav 제목 찾기 종료(찾음)  ──────┘', 'Info')
            if ret_gubun == 'TITLE':
                return rTITLE
            else:
                return rURL
        index += len('<a itemprop="url"')
      except ValueError:
        break
    Logging('└────── pornav 제목 찾기 종료(못찾음)  ──────┘', 'Info')
    return #Return 결과는 None

def Extract_str_title_javdb(nStr,nStartstr,nEndstr,nPoombun):
    # nStr: 원본 문자열
    # nStartstr: 시작 문자열
    # nEndstr: 끝 문자열
    # nPoombun: 검색할 품번
    # 리턴은 title, url 두개를 리턴함

    Logging('┌────── javdb 제목 찾기 시작  ──────┐','Info')
    nStr=String_slice(nStr,nStartstr,nEndstr)
    nPoombun=nPoombun.upper()
    if 'FC2' in nPoombun: nPoombun = nPoombun.replace('-', ' ').replace('FC2PPV','FC2').replace('FC2-PPV','FC2')

    # Logging('전체 문자열: ' + nStr,'Debug')

    index = 0
    while index > -1:
      try:
        index = nStr.index('grid-item column', index) #문자열 위치값
        searchstr = nStr[index:] #문자열 위치 이후부터 값에 넣음
        rTITLE = String_slice(searchstr,'title="','"').replace('「','"').replace('」','"').replace('！','!')
        rUID =  String_slice(searchstr,'"uid">','</div>') #검색결과의 품번
        rURL = String_slice(searchstr,'href="','"')
        Logging('Slice Result  > title: ' + rTITLE + ' > URL: ' + rURL + ' UID: ' + rUID + ' nPoombuh: ' + nPoombun, 'debug')
        if nPoombun in rUID: #품번 텍스트가 rUID 문자열에 있는지 체크
            Logging('찾은 품번 제목: ' + rTITLE + ' 주소: ' + rURL,'Debug')
            ret=[]
            ret.append(rTITLE)
            ret.append(rURL)
            Logging('└────── javdb 제목 찾기 종료(찾음)  ──────┘', 'Info')
            return ret
        index += len('grid-item column')
      except ValueError:
        break
    Logging('└────── javdb 제목 찾기 종료(못찾음)  ──────┘', 'Info')
    return #Return 결과는 None

def Extract_imgurl(nStr,nStartstr,nEndstr,hreforsrc='src'):
    # nStr: 원본 문자열
    # nStartstr: 시작 문자열
    # nEndstr: 끝 문자열
    # 시작~끝 문자열로 자른 뒤 이미지 URL을 모두 반환함
    # Logging('Original  Str: ' + nStr)
    FindSplittxt=''

    nStr=String_slice(nStr,nStartstr,nEndstr)
    nNotfound=nStr.find('----')
    if (hreforsrc == 'src'):
        FindSplittxt='img src'
        Logging('Extract from "img src"','Debug')
    elif(hreforsrc == 'href'):
        FindSplittxt = 'href'
        Logging('Extract from "href"','Debug')
    elif(hreforsrc == 'data-original'):
        FindSplittxt = 'data-original'
        Logging('Extract from "data-original"','Debug')
    nFound = nStr.find(FindSplittxt)
    nResult=[]
    if (nNotfound == -1 ):
        if (nFound <> -1):
            sTemp=nStr.split(FindSplittxt)
            j = len(sTemp)
            Logging('Length: ','Debug')
            Logging(int(j),'Debug')
            for i in range(1, j):
                # Logging('Before Cut: ' + sTemp[i],'Debug')
                nCut=String_slice(sTemp[i],'="','"')
                if (nCut.find('preview-video') == -1 ):
                    nResult.append(nCut)
                Logging('Extract_url  After Cut: ' + nCut,'Info')
            return nResult
    return #Return 결과는 None

def Search_Category(txt):

    if (str(Prefs['papago_use']) == 'False'):
        Logging('### 파파고 사용 안함 체크됨(Papago Not use checked) ###','Debug')
        return txt

    ## 미리 정의한 카테고리를 검색해 해당 한글을 리턴
    category = {u'アイドル':u'우상',u'芸能人':u'연예인',u'アクメ・オーガズム':u'아크메・오르가즘',u'アスリート':u'운동선수',u'アニメキャラクター':u'애니 캐릭터',
                u'姉・妹':u'누나・동생',u'イタズラ':u'장난',u'インストラクター':u'강사',u'ウェイトレス':u'웨이트리스',u'受付嬢':u'접수원',u'エステ':u'에스테 살롱',
                u'M男':u'마조히스트 남',u'M女':u'마조히스트 여',u'OL':u'오피스 레이디',u'お母さん':u'밀프',u'女将・女主人':u'마담, 여주인',u'幼なじみ':u'소꿉친구',
                u'お爺ちゃん':u'할아버지',u'お嬢様・令嬢':u'아가씨, 영애',u'オタク':u'오타쿠',u'オナサポ':u'자위 도우미',u'お姉さん':u'누나',u'お婆ちゃん':u'할머니',
                u'叔母さん':u'이모',u'お姫様':u'공주님',u'お風呂':u'목욕',u'温泉':u'온천',u'女教師':u'여교사',u'女上司':u'여상사',u'女戦士':u'여전사',u'女捜査官':u'여수사관',
                u'カーセックス':u'카섹스',u'格闘家':u'무도가',u'カップル':u'커플',u'家庭教師':u'가정교사',u'看護婦・ナース':u'간호사',u'キャバ嬢・風俗嬢':u'업소녀',
                u'キャンギャル':u'캠패인 걸',u'近親相姦':u'근친상간',u'義母':u'시어머니',u'逆ナン':u'역헌팅',u'ギャル':u'갸루',u'くノ一':u'여닌자',u'コンパニオン':u'동반자',
                u'極道・任侠':u'야쿠자',u'シスター':u'자매',u'主観':u'주관',u'職業色々':u'다양한 직업',u'ショタ':u'쇼타',u'白目・失神':u'백안, 실신',u'時間停止':u'시간정지',
                u'熟女':u'숙녀',u'女医':u'여의사',u'女王様':u'여왕님',u'女子アナ':u'여아나운서',u'女子校生':u'여학생',u'女子大生':u'여대생',u'スチュワーデス':u'스튜어디스',
                u'スワッピング・夫婦交換':u'부부교환',u'性転換・女体化':u'성전환, 여체화',u'セレブ':u'연예인',u'チアガール':u'치어리더',u'痴女':u'치녀',u'ツンデレ':u'쓴데레',
                u'デート':u'데이트',u'盗撮・のぞき':u'도/촬, 엿보기',u'ドール':u'인형',u'寝取り':u'네토리',u'寝取られ':u'네토라레',u'NTR':u'NTR',u'ノーパン':u'노팬티',
                u'ノーブラ':u'노브라',u'飲み会・合コン':u'회식, 미팅',u'ハーレム':u'하렘',u'花嫁':u'신부',u'バスガイド':u'버스 투어 가이드',u'秘書':u'비서',u'人妻':u'유부녀',
                u'主婦':u'주부',u'ビッチ':u'빗치',u'病院':u'병원',u'クリニック':u'클리닉',u'ファン感謝':u'팬감사',u'訪問':u'방문',u'不倫':u'불륜',u'部活':u'동아리활동',
                u'マネージャー':u'매니저',u'部下':u'부하',u'同僚':u'동료',u'ヘルス・ソープ':u'건강비누',u'変身ヒロイン':u'변신',u'ホテル':u'호텔',u'マッサージ':u'마사지',
                u'魔法少女':u'마법소녀',u'ママ友':u'엄마친구',u'未亡人':u'미망인',u'娘・養女':u'딸, 양녀',u'胸チラ':u'은근슬젖',u'メイド':u'메이드',u'面接':u'면접',
                u'モデル':u'모델',u'野外・露出':u'야외, 노출',u'ヨガ':u'요가',u'乱交':u'난교',u'旅行':u'여행',u'レースクィーン':u'레이스 여왕',u'若妻・幼妻':u'앳된 아내',
                u'アジア女優':u'아시아 배우',u'AV女優':u'AV 여배우',u'巨尻':u'큰 엉덩이',u'巨乳':u'거유',u'筋肉':u'근육',u'小柄':u'작은 몸집',u'黒人男優':u'흑인',
                u'処女':u'처녀',u'女装':u'여장남자',u'男の娘':u'낭자애',u'スレンダー':u'슬렌더',u'早漏':u'조루',u'そっくりさん':u'닮은꼴',u'長身':u'장신',u'超乳':u'초유',
                u'デカチン':u'거근',u'巨根':u'거근',u'童貞':u'동정',u'軟体':u'연체',u'ニューハーフ':u'뉴-하프',u'妊婦':u'임신부',u'白人女優':u'백인',u'パイパン':u'백보지',
                u'日焼け':u'태닝',u'貧乳':u'빈유',u'微乳':u'빈유',u'美少女':u'미소녀',u'美乳':u'미유',u'ふたなり':u'후타나리',u'ぽっちゃり':u'토실토실',u'ミニ系':u'미니계열',
                u'学生服':u'학생복',u'競泳':u'학교수영복',u'スクール水着':u'학교 수영복',u'コスプレ':u'코스프레',u'ゴスロリ':u'고슬로리',u'セーラー服':u'세라복',u'制服':u'유니폼',
                u'体操着':u'체육복',u'ブルマ':u'체육복',u'チャイナドレス':u'차이나 드레스',u'ニーソックス':u'니하이 삭스',u'ネコミミ':u'고양이 귀',u'獣系':u'동물계',
                u'裸エプロン':u'알몸 앞치마',u'バニーガール':u'버니걸',u'パンスト・タイツ':u'타이즈 스타킹',u'ビジネススーツ':u'정장',u'覆面・マスク':u'복면',u'ボディコン':u'바디콘',
                u'ボンテージ':u'본디지',u'巫女':u'무녀',u'水着':u'수영복',u'ミニスカ':u'미니스커트',u'ミニスカポリス':u'경찰 미니스커트',u'めがね':u'안경',u'ランジェリー':u'란제리',
                u'ルーズソックス':u'헐렁한 양말',u'レオタード':u'레오타드',u'和服・浴衣':u'일본옷・유카타',u'アクション':u'액션',u'アクション・格闘':u'격투',u'脚フェチ':u'다리',u'アニメ':u'애니',
                u'イメージビデオ':u'이미지 비디오',u'イメージビデオ(男性)':u'이미지 비디오 남자',u'淫乱・ハード系':u'음란・Hard계',u'学園もの':u'학원물',u'企画':u'기획물',
                u'局部アップ':u'국부/음부 확대',u'巨乳フェチ':u'거유 패티시',u'ギャグ・コメディ':u'게이・코미디',u'クラシック':u'클래식',u'ゲイ':u'게이',u'原作コラボ':u'오리지널 콜라보레이션',
                u'コラボ作品':u'콜라보레이션',u'サイコ・スリラー':u'싸이코',u'残虐表現':u'잔혹성',u'尻フェチ':u'엉덩이',u'素人':u'일반인',u'時代劇':u'사극',u'女性向け':u'여성향',
                u'女優ベスト・総集編':u'여배우 BSET, 총집편',u'スポーツ':u'스포츠',u'セクシー':u'섹시',u'その他フェチ':u'기타 페티시',u'体験告白':u'체험고백',u'単体作品':u'단체작품',
                u'ダーク系':u'다크 계',u'ダンス':u'춤',u'着エロ':u'착에로',u'デビュー作品':u'데뷔작',u'特撮':u'특수촬영',u'ドキュメンタリー':u'다큐멘터리',u'ドラマ':u'드라마',u'ナンパ':u'헌팅',
                u'パンチラ':u'팬티',u'ファンタジー':u'판타지',u'復刻':u'복각',u'Vシネマ':u'V 시네마',u'ベスト・総集編':u'BEST, 총집편',u'ホラー':u'호러',u'ボーイズラブ':u'BL',u'妄想':u'망상',
                u'洋ピン・海外輸入':u'서양 에로물',u'レズ':u'레즈비언',u'恋愛':u'연애',u'足コキ':u'풋 잡',u'汗だく':u'땀투성이',u'アナル':u'아날',u'アナルセックス':u'아날 섹스',
                u'異物挿入':u'이물삽입',u'イラマチオ':u'딥 쓰롯',u'淫語':u'음담',u'飲尿':u'인뇨',u'男の潮吹き':u'남자 분수',u'オナニー':u'자위',u'おもちゃ':u'장난감',u'監禁':u'감금',
                u'浣腸':u'관장',u'顔射':u'얼싸',u'顔面騎乗':u'안면승마',u'騎乗位':u'기승위',u'キス・接吻':u'키스',u'鬼畜':u'귀축',u'くすぐり':u'간지럼',u'クスコ':u'질경',
                u'クンニ':u'커널링구스',u'ゲロ':u'구토',u'拘束':u'구속',u'拷問':u'고문',u'ごっくん':u'정액',u'潮吹き':u'시오후키',u'シックスナイン':u'69',u'縛り・緊縛':u'긴박',
                u'羞恥':u'수치',u'触手':u'촉수',u'食糞':u'식분-스캇물',u'スカトロ':u'스캇',u'スパンキング':u'스팽킹',u'即ハメ':u'바로 섹스',u'脱糞':u'탈분 스캇물',u'手コキ':u'핸드잡',
                u'ディルド':u'딜도',u'電マ':u'전동 마사지기',u'ドラッグ':u'약',u'中出し':u'질내사정',u'辱め':u'치욕',u'鼻フック':u'코 후크',u'ハメ撮り':u'셀프 촬영',u'孕ませ':u'임신섹스',
                u'バイブ':u'바이브레터',u'バック':u'뒤',u'罵倒':u'매도',u'パイズリ':u'파이즈리',u'フィスト':u'주먹',u'フェラ':u'펠라치오',u'ぶっかけ':u'붓카케',u'放置':u'방치',
                u'放尿・お漏らし':u'방뇨',u'母乳':u'모유',u'ポルチオ':u'포루치오(P-Spot)',u'指マン':u'유비만(Fingering)',u'ラブコメ':u'러브 코미디',u'レズキス':u'레즈비언 키스',
                u'ローション・オイル':u'로션・오일',u'ローター':u'로터',u'蝋燭':u'양초',u'ギリモザ':u'기리모자',u'スマホ推奨縦動画':u'세로영상',u'3D':u'3D',u'4K':u'4K',u'4P':u'4P',u'3P':u'3P',
                u'R-15': u'R-15', u'お笑い・コント・漫才': u'코미디, 콘토, 만재', u'キャンペーンガール': u'캠페인 소녀', u'競泳・スクール水着': u'수영・학교 수영복',
                u'クッキング': u'쿠킹', u'グラビア': u'그라비아', u'声優': u'성우', u'セクシー女優': u'섹시 여배우', u'トーク': u'토크',u'ドキュメンタリー': u'다큐멘터리',
                u'独占配信': u'독점 배달', u'ネコミミ・獣系': u'고양이 미미・짐승시스템',u'ハイクオリティVR': u'고품질 VR', u'ハイビジョン': u'고화질', u'韓流': u'한류',
                u'バラエティ': u'버라이어티', u'ヒーロー・ヒロイン': u'영웅 히로인',u'美尻': u'예쁜 힙', u'VR専用': u'VR 전용',u'4時間以上作品': u'4시간 이상 작품',
                u'デジタル最新作': u'디지털 최신작', u'成人作品': u'성인 작품',u'期間限定50％OFF☆':u'기간한정50％세일☆',u'イメージビデオ':u'이미지 비디오',u'着エロ':u'착용',
                u'アイドル・芸能人':u'아이돌・연예인',u'双葉社30％OFF第1弾':u'후타바사30%세일 제1탄',u'デジモ':u'디지털 모자이크(약모)',u'野外・露出':u'야외・노출',
                u'寝取り・寝取られ・NTR':u'빼앗고・뺏기기・NTR',u'3P・4P':u'3P・4P',u'高畫質':u'고화질',u'バック':u'뒷치기(체위)',u'吊り橋':u'현수교(체위)', u'正常位': u'정상위(체위)',
                u'深山': u'깊은 산(체위)', u'開脚正常位': u'발 정상 위치 열기(체위)', u'反り正常位': u'변형 정상위(체위)', u'密着正常位': u'정상 위치에 가까움(체위)', u'手繋ぎ正常位': u'손 종합 정상위(체위)',
                u'抱きつき正常位': u'달라 붙어 정상위(체위)', u'脚閉じ正常位': u'다리 닫 정상위(체위)', u'自分で動く正常位': u'스스로 움직이는 정상위(체위)', u'背面騎乗位': u'후면 카우걸(체위)',
                u'四つん這い背面騎乗位': u'네발 후면 카우걸(체위)', u'エロい腰振り騎乗位': u'야한 허리 모습 기승 정도(체위)',u'撞木反り': u'당목 휘어짐(체위)',u'腰振り背面騎乗位': u'허리 모습 후면 카우걸(체위)',
                u'腰振り騎乗位': u'허리 모습 기승 정도(체위)',u'騎乗位': u'카우걸(체위)',u'またがり騎乗位': u'또한 공부 카우걸(체위)',u'エロい背面騎乗位': u'야한 후면 카우걸(체위)',
                u'エロい騎乗位': u'야한 카우걸(체위)', u'グラインド騎乗位': u'그라인드 카우걸(체위)',u'反り背面騎乗位': u'변형 후면 카우걸(체위)',u'反り騎乗位': u'변형 카우걸(체위)',
                u'密着騎乗位': u'밀착 카우걸(체위)',u'手繋ぎ騎乗位': u'손 종합 카우걸(체위)', u'杭打ち背面騎乗位': u'말뚝 박기 후면 카우걸(체위)'
                }

    if txt <> '':
        nret = txt.replace(' ', '').upper().decode('utf8')  # 문자열 공백 제거
        Logging('로컬에서 찾을 카테고리명: ' + nret, 'Info')
        if nret in category:
            nret = category[nret]
            Logging('로컬에서 찾았습니다! : ' + nret,'Info')
            return nret
    Logging(' @@@ 로컬에서 카테고리 못찾음 검색어: '+ txt, 'Debug')
    return txt

def Search_Label(txt):

    if (str(Prefs['papago_use']) == 'False'):
        Logging('### 파파고 사용 안함 체크됨(Papago Not use checked) ###','Debug')
        return txt
    
    ## 미리 정의한 레이블명을 검색해 레이블에 해당하는 한글을 리턴함
    label = {u'Aircontrol': u'에어컨트롤', u'アリスJAPAN': u'엘리스 재팬', u'ALICEJAPAN': u'엘리스 재팬', u'ATTACKERS': u'어택커즈', u'アタッカーズ': u'어택커즈',
             'BabyEntertainment': u'베이비 엔터테인먼트', u'BeFree': u'비프리', u'ビーフリー': u'비프리', u'痴女ヘブン': u'색녀천국',
             'ChijyoHEAVEN': u'색녀천국', u'DANDY&COSMOS': u'댄디&코스모스', u'ダスッ!': u'다스', u'DAS': u'다스', "DEEP'S": '딥스',
             'DOC(DIGITALOPTICALCREATE)': u'독', u'DIGITALOPTICALCREATE': u'독', u'E-BODY': u'이-바디', u'FALENO': u'팔레노',
             'FAプロ': u'FA프로', u'Fitch': u'피치', u'フィッチ': u'피치', u'G-AREA&PERFECT-G': u'G-애리어&퍼펙트-G', u'GIGA': u'기가',
             'GLORYQUEST': u'글로리 퀘스트', u'グローリークエスト': u'글로리 퀘스트', u'H.M.P': u'H.M.P', u'変態紳士倶楽部': u'헨타이 신사 클럽',
             'HENTAISHINSHICLUB': u'헨타이 신사 클럽', u'HHHGroup': u'HHH그룹', u'Hunter': u'HHH그룹', u'HunterBlack': u'HHH그룹',
             'ROYAL': u'HHH그룹', u'お夜食カンパニー': u'HHH그룹', u'Apache': u'HHH그룹', u'AtoM': u'HHH그룹', u'ゴールデンタイム': u'HHH그룹',
             'GOLDENTIME': u'HHH그룹', u'HIBINO': u'히비노', u'ヒビノ': u'히비노', u'HimeMix': u'히메믹스', u'ひよこ': u'히요코', u'hiyoko': u'히요코',
             '本中': u'혼나카', u'HONNAKA': u'혼나카', u'IENERGY': u'아이에너지', u'アイエナジー': u'아이에너지', u'IDEAPOCKET': u'아이디어포켓',
             u'アイデアポケット': u'아이디어 포켓', u'kawaii*': u'카와이', u'kawaii': u'카와이', u'kingdom': u'킹덤', u'KMP': u'KM프로듀스',
             'ケイ・エム・プロデュース': u'KM프로듀스', u'Aver': u'KM프로듀스', u'KMPPREMIUM': u'KM프로듀스', u'Million': u'KM프로듀스',
             'Millionミント(mint)': u'KM프로듀스', u'宇宙企画': u'KM프로듀스', u'REAL': u'KM프로듀스', u'SCOOP': u'KM프로듀스', u'BAZOOKA': u'KM프로듀스',
             'S級素人': u'KM프로듀스', u'エロガチャ(EROGACHA)': u'KM프로듀스', u'ヒメゴト': u'KM프로듀스', u'サロメ(SALOME)': u'KM프로듀스', u'300': u'KM프로듀스',
             '3000': u'KM프로듀스', u'俺の素人': u'KM프로듀스', u'僕たち男': u'KM프로듀스', u'EDGE': u'KM프로듀스', u'ナンパHEAVEN': u'KM프로듀스',
             'おかず。': u'KM프로듀스', u'UMANAMI': u'KM프로듀스', u'Nadeshiko': u'KM프로듀스', u'100人': u'KM프로듀스', u'マダムス': u'마담스',
             'Madames': u'마담스', u'FS.KnightsVisual': u'FS나이트비주얼', u'Madonna': u'마돈나', u'マドンナ': u'마돈나', u'MAXING': u'맥싱',
             '未満': u'미만', u'MIMAN': u'미만', u'MOODYZ': u'무디즈', u'ムーディーズ': u'무디즈', u'妄想族': u'망상족', u'Mousouzoku': u'망상족',
             'ANNEX(無言)/妄想族': u'망상족', u'ABC/妄想族': u'망상족', u'AVScollector’s': u'망상족', u'かぐや姫Pt/妄想族': u'망상족',
             'ティーチャー/妄想族': u'망상족', u'ブロッコリー/妄想族': u'망상족', u'山と空/妄想族': u'망상족', u'Mr.Michiru': u'미스터 미칠', u'ミスターミチル': u'미스터 미칠',
             'MUTEKI': u'무테키', u'舞ワイフ': u'마이 와이프', u'mywife': u'마이 와이프', u'AROUND': u'마이 와이프', u'ながえSTYLE': u'나가에 스타일',
             'NAGAE STYLE': u'나가에 스타일', u'ナンパJAPAN': u'남파 재팬', u'NANPA-JAPAN': u'남파 재팬', u'NATURALHIGH': u'내추럴 하이',
             'ナチュラルハイ': u'내추럴 하이', u'OPPAI': u'오파이', u'おっぱい': u'오파이', u'ORGA': u'올가', u'オルガ': u'올가', u'素人onlyプラム': u'플럼',
             'Plum': u'플럼', u'pornograph.tv': u'포르노그래피.TV', u'PREMIUM': u'프리미엄', u'プレミアム': u'프리미엄', u'PRESTIGE': u'프래스티지',
             'プレステージ': u'프래스티지', u'RADIX': u'래딕스', u'REbecca': u'레베카', u'ROCKET': u'로켓', u'ルビー': u'루비', u'Ruby': u'루비',
             'S1(S1NumberOneStyle)': u'S1 넘버원 스타일', u'エスワン ナンバーワンスタイル': u'S1 넘버원 스타일', u'S1': u'S1 넘버원 스타일',
             'SADISTICVILLAGE': u'사디스틱 빌리지', u'サディスティックヴィレッジ': u'사디스틱 빌리지', u'S-Cute': u'S-큐트', u'SILKLABO': u'실크라보',
             'SOD(SOFTONDEMAND)': u'소프트 온 디멘드', u'ソフトオンデマンド': u'소프트 온 디멘드', u'SOD': u'소프트 온 디멘드', u'SODクリエイト':u'소프트 온 디멘드', u'SOSORU×GARCON': u'소소루x가르콘',
             '溜池ゴロー': u'다마이케 고로', u'tameikegoro': u'다마이케 고로', u'タカラ映像': u'타카라 비주얼', u'TAKARA VISUAL': u'타카라 비주얼', u'鉄板': u'철판',
             'TEPPAN': u'철판', u'TMA(TotalMediaAgency)': u'토탈 미디어 에이전시', u'TMA': u'토탈 미디어 에이전시', u'I.B.WORKS': u'토탈 미디어 에이전시',
             'TOKYO247': u'도쿄247', u'VENUS': u'비너스', u'WAAPGROUP': u'WAAP그룹', u'WAAP': u'WAAP그룹', u'DREAMTICKET': u'WAAP그룹',
             'NON': u'WAAP그룹', u'光夜蝶': u'WAAP그룹', u'WANZFACTORY': u'완즈 팩토리', u'ワンズファクトリー': u'완즈 팩토리', u'天然むすめ': u'천연 무스메',
             '10musume': u'천연 무스메', u'1pondo': u'1폰도', u'一本道': u'1폰도', u'Caribbeancom': u'캐리비안컴', u'カリビアンコム': u'캐리비안컴',
             'エッチな4610': u'음란한4610', u'エッチな4610(H4610)': u'음란한4610', u'エッチな0930(H0930)': u'음란한4610',
             '人妻斬り(C0930)': u'음란한4610', u'HEYZO': u'헤이조', u'FellatioJapan': u'펠라치오 재팬', u'HandjobJapan': u'핸드잡 재팬',
             'LegsJapan': u'다리 재팬', u'金8天国': u'김8천국', u'kin8tengoku': u'김8천국', u'ムラムラ': u'무라무라', u'muramura': u'무라무라',
             'パコパコママ': u'파코파코마마', u'pacopacomama': u'파코파코마마', u'しろハメ': u'시로-하메', u'SIRO-HAME': u'시로-하메', u'Heydouga': u'시로-하메',
             'Heydouga4017': u'시로-하메', u'Tokyo-Hot': u'도쿄핫', u'東京熱': u'도쿄핫'}

    if txt <> '':
        nret = txt.replace(' ', '').upper().decode('utf8')  # 문자열 공백 제거
        Logging('로컬에서 찾을 레이블명: ' + nret, 'Info')
        if nret in label:
            nret = label[nret]
            Logging('레이블명을 찾았습니다! : ' + nret,'Info')
            return nret
    Logging('@@@ 로컬에서 레이블 못찾음 검색레이블:' + txt, 'Debug')
    return txt

def Start():
    HTTP.CacheTime = 0

def detailItem(root,selector):
    elements = root.xpath(selector)
    if len(elements) > 0:
        text = elements[0].text_content().strip()
        Logging(' DetailItem Function Text: ' + text,'Debug')
        if "----" in text:
            return None
        return elements[0].text_content().strip()
    return None

def Get_actor_info(nEntity):
    # hentaku 없어져서 avdbs.com 으로 변경 2021.12.31
    try:
        if (nEntity == ''):
            return
        Logging('############# Actor Info from avdbs ##############', 'Info')
        nEntity = nEntity.decode('utf8')
        Logging('검색할 배우명 : ' + nEntity,'Debug')
        Search_URL = 'https://www.avdbs.com/w2017/page/search/search_actor.php?kwd=' + nEntity#urllib2.quote(nEntity) #한글, 일어등은 quote 해줘야 함
        Logging('### search URL: =>' + Search_URL + '<=', 'Debug')
        searchResults = HTTP.Request(Search_URL,headers=HDR_AVDBS,timeout=int(Prefs['timeout'])).content
        # Logging('### searchResults: ' + searchResults,'Debug')
        nResult=[]
        if (searchResults == '' or searchResults.find('검색된 배우가 없습니다') <> -1):
            # 검색결과 없을때
            nResult.append('') #image url
            nResult.append(Papago_Trans(nEntity,'ja')) # kor name
            nResult.append(Papago_Trans(nEntity,'en')) # eng name
            Logging('### 검색된 배우가 없습니다. Actor Return is Null 저장할 배우명: ' + nEntity, 'Info')
        else:
            # 검색결과 존재시
            # Logging('### 배우 정보를 검색했습니다. Actor Return Found', 'Info')
            nStr = String_slice(searchResults, '<ul class="lst"', '</ul>')
            # Logging('### 배우 검색됨. 배우 정보: ' + nStr, 'Debug')
            nimgurl = String_slice(nStr, 'img src="', '"')
            Logging('### 배우 이미지 주소 Actor image: ' + nimgurl,'Debug')
            nResult.append(nimgurl)
            rKorName = Extract_str(nStr, '<p class="k_name">', '</p>') # 한국어 이름 리턴
            nResult.append(rKorName[0])   #String_slice(nStr, '<p class="k_name">', '<').strip()) # 한국어 이름
            nResult.append(Papago_Trans(nEntity, 'en'))  # eng name
            # nResult.append(String_slice(nStr, 'e_name ovf-hide"><br/>', '(<span')) # 영어 이름
            Logging('### 배우 이미지 정보 Actor info  img:' + nResult[0] + ' 한국어 Name_kor: ' + nResult[1] + ' 외국어 Name_eng: '+nResult[2] ,'Debug')
            return nResult
    except:
        return

def Get_search_url(SEARCH_URL, txt, reqMode='GET'):
    con = ''
    # try:
    if (reqMode == 'POST'):
        Logging('Request is POST','Info')
        data = {'search_str': txt}
        Logging('POST SearchURL: ' + SEARCH_URL + ' data: ' + txt, 'Debug')
        req = urllib2.Request(SEARCH_URL, data)
    else:
        Logging('Request is GET','Info')
        encodedId = urllib2.quote(txt)
        Logging('encodedID: ' + encodedId, 'Info')
        url = SEARCH_URL + encodedId
        Logging('SearchURL: ' + url, 'Info')
        req = urllib2.Request(url)
        # req.add_header =('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36')
        req.add_header('Cookie','age_check_done=1') #DMM의 성인인증
        # req.add_header('Cookie', 'over18=1') #JavDB의 성인인증
        # req.add_header('age_check_done', '1')
        # req.add_header('Referer', SEARCH_URL)
        Logging('Cookie added(Age_check_done=1, to Cookie)', 'Info')
    try:
        con = urllib2.urlopen(req, timeout=int(Prefs['timeout']))
        Logging('URL Open Success', 'Info')
    except urllib2.URLError as e:
        Logging(e.reason,'Debug')

    web_byte = con.read()
    Logging('webbyte completed','Info')
    webpage = web_byte.decode('utf-8')
    # Logging('webpage : ' + str(webpage), 'Debug')
    Logging("검색결과 가져옴(Got search result)", 'Info')
    return webpage
    # except:
    #     Logging("검색결과 Search Result: exception", 'Error')
    # return ''

def poombun_check(txt,filename):
    # 입력 문자에서 품번만 추출해 리턴함
    # (?i) 대소문자포함
    #  \w{2,}-[0-9]{3,}  xxx-yyy 품번 구분
    #  \w{2,} [0-9]{3,}  xxx yyy 품번 구분
    #  (?i)(FC2).*(PPV)-[0-9]{3,}   fc2ppv-0000 / fc2-ppv-00000 (단, scanner에서 하이픈 두개일때 뒤는 자르므로 파일명을 FC2PPV-0000으로 해야함
    # (?i)(carib.*)-[0-9]{3,} carib-9999 / caribbeancom-9999-9999 (carib는 하이픈 두개도 됨)

    # (?i)(tokyo.*)-n[0-9]{3,} / tokyohot-n000
    # (?i)((carib.*)|(1pondo.*)|\w{2,}|((FC2).*(PPV)))-[0-9]{3,}
    # (?i)(tokyo.*)-n[0-9]{3,}|((carib.*)|(1pondo.*)|\w{2,}|((FC2).*(PPV)))-[0-9]{3,} 위 두개를 합친 표현식

    Logging('### Poombun input: ' + txt,'Debug')
    if (txt <> ''):
        txt = txt.replace(' ', '-')
        # Logging('txt: ' + txt)
        pattern = '(?i)(TOKYO.*)-n[0-9]{3,}|((CARIB.*)|(1PONDO.*)|\w{2,}|((FC2).*(PPV)))-[0-9]{3,}'
        nMatch = re.search(pattern, txt)
        # Logging(nMatch)
        if (nMatch is not None):
            Logging('### Poombun output: ' + nMatch.group(0), 'Debug')
            return nMatch.group(0)
        elif (filename != ''):
            Logging('품번 파일명은 있으나 형식이 안맞음. 파일명: ' + txt, 'Debug')
            txt = urllib.unquote(filename).decode('utf8')
            Logging('입력받은 파일명 주소: ' + txt, 'Debug')
            # if(txt.find('DV-') > -1):
            nMatch = re.search(pattern, txt)
            if (nMatch is not None):
                Logging('### Poombun output: ' + nMatch.group(0), 'Debug')
                return nMatch.group(0)

    Logging('@@@ Poombun is wrong','Error')
    return txt

def poombun_split_num(txt):
    # 품번에서 숫자만 남겨서 리턴(아마추어 품번 검색때문)
    nMediaName = txt
    if (nMediaName.find('FC2PPV-') > -1):
        txt = nMediaName.replace('FC2PPV-', '')  # 검색을 위해 FC2 품번만 발췌함
    elif (nMediaName.find('TOKYOHOT-') > -1):
        txt = nMediaName.replace('TOKYOHOT-', '')  # 검색을 위해 품번만 발췌함
    elif (nMediaName.find('CARIB-') > -1):
        txt = nMediaName.replace('CARIB-', '')  # 검색을 위해 품번만 발췌함
    elif (nMediaName.find('CARIBBEANCOM-') > -1):
        txt = nMediaName.replace('CARIBBEANCOM-', '')  # 검색을 위해 품번만 발췌함
    else:
        txt = poombun_check(txt,'')  # .replace('[','').replace(']','')

    Logging('poombunSplitResult: ' + txt,'Debug')
    return txt

def uncensored_check(txt):
    # 파일명에 노모 포함인지 여부 확인

    if (txt is None): return 0
    txt=txt.upper()
    txt=urllib.unquote(txt).decode('utf8')
    Logging('Uncensored check txt: ' + txt	,'Debug')

    if (str(Prefs['uncensored_class']) == 'True'):
        if ((txt.find('UNC') > -1) or (txt.find('노모') > -1) ):
            Logging('Uncensored Detect', 'Info')
            return 1
    return 0

def Logging(txt, Level='Info'):
    # 에이전트 로그 남기기
    if (str(Prefs['loglevel']) == 'Error'):
        if (Level == 'Error'):
            Log(txt)
    elif (str(Prefs['loglevel']) == 'Info'):
        if (Level == 'Error') or (Level == 'Info'):
            Log(txt)
    elif (str(Prefs['loglevel']) == 'Debug'):
        Log(txt)

class redstar_javscraper(Agent.Movies):
    name = 'redstar_javscraper'
    languages = [Locale.Language.English,]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        Logging("####### Start search #########", 'Info')
        #https://www.javlibrary.com/
        #https://javdb.com/
        # https://pornav.co/  fc2등 노모 검색
        # https://www.jav321.com/
        # https://aa9969.com/ko/ #7mmtv
        nResult=0
        Logging('option Check dmm: ' + str(Prefs['dmm_use']),'Info')
        Logging('option check r18: ' + str(Prefs['r18_use']),'Info')
        Logging('option check javbus: ' + str(Prefs['javbus_use']),'Info')
        Logging('option check pornav: ' + str(Prefs['pornav_use']),'Info')
        Logging('option check javlibrary: ' + str(Prefs['javlibrary_use']), 'Info')
        Logging('option check javdb: ' + str(Prefs['javdb_use']),'Info')

        amateur = True
        media.name = media.name.upper().replace('HHD800 COM@','')
        nSearchstr = media.name
        Logging('### 분석할 파일명: ' + nSearchstr,'Info')
        if (nSearchstr.find('CARIB') == -1):
            if (nSearchstr.find('FC2PPV') == -1):
                if( nSearchstr.find('TOKYOHOT') == -1):
                    amateur=False
                    Logging('Amateur option is False','Debug')

        if (str(Prefs['dmm_use']) == 'True' and amateur == False):
            nResult=self.dmm_search(results, media, lang)
            Logging('dmm result: ' + str(nResult), 'Debug')
        if (str(Prefs['r18_use']) == 'True' and nResult == 0 and amateur == False):
            nResult=self.r18_search(results, media, lang)
            Logging('r18 result: ' + str(nResult), 'Debug')
        if (str(Prefs['javbus_use']) == 'True' and nResult == 0 and amateur == False):
            nResult=self.javbus_search(results, media, lang)
            Logging('jabus result: '  + str(nResult), 'Debug')
        if (str(Prefs['pornav_use']) == 'True' and nResult == 0):
            nResult=self.pornav_search(results, media, lang)
            Logging('pornav result: '  + str(nResult), 'Debug')
        if (str(Prefs['javdb_use']) == 'True' and nResult == 0):
            nResult=self.javdb_search(results, media, lang)
        if (str(Prefs['javlibrary_use']) == 'True' and nResult == 0):
            nResult=self.javlibrary_search(results, media, lang)
            Logging('javdb result: '  + str(nResult),'Debug')
        if (nResult == 0):
            Logging('@@@ Search failed on all sites.', 'Error')
        Logging('####### End search #########', 'Info')

    def update(self, metadata, media, lang):
        Logging("####### Start Update #########", 'Info')

        nTitle=media.title
        Logging('MediaTitle: ' + nTitle, 'Debug')

        # name = '[' + id + '] ' + title + ' §' + 'DMM' + '§' + uncResult + '§' + id+ '§'+Y/N/C
        # 0: ID, 타이틀 [OAE-101] PerfectBody..  /  1: 검색사이트 구분자   /  2: 노모유모확인 / 3: 오리지널 타이틀 /
        # #4 Y:파일명에서, 타이틀있음, N: 파일명에서, 타이틀 없음 C: 웹크롤링 타이틀
        if (nTitle.find('§') <> -1):
            nIDs = nTitle.split('§')
            metadata.title = nIDs[0]
            nSite = nIDs[1]
            nUncensored = nIDs[2]
            nOrgID = nIDs[3]
            ncroling = nIDs[4]
            Logging('### Uncensored: ' + nUncensored + ' Update site : ' + nSite, 'Debug')
            if (nUncensored == 'U'):
                metadata.content_rating = '노모'
                Logging('ContentRating: 노모', 'Debug')
            if (nUncensored == 'C'):
                metadata.content_rating = '유모'
                Logging('ContentRating: 유모', 'Debug')
        else:
            nSite=' '
            nOrgID=nTitle
            ncroling='C'

        if (str(Prefs['dmm_use']) == 'True' and ((nSite == 'DMMa') or (nSite == 'DMMc') or(nSite == 'DMMd') or(nSite == 'DMMr') or(nSite == ' '))):
            nResult=self.dmm_update(metadata, media, lang, nOrgID,ncroling,nSite)
            # Logging('dmm result: ' + str(nResult),'Debug')
        elif (str(Prefs['r18_use']) == 'True' and ((nSite == 'r18v') or (nSite == 'r18a') or (nSite == ' '))):
            nResult=self.r18_update(metadata, media, lang, nOrgID, ncroling, nSite)
            # Logging('r18 result: ' + str(nResult),'Debug')
        elif (str(Prefs['javbus_use']) == 'True' and ((nSite == 'javbus')or (nSite == ' '))):
            nResult=self.javbus_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('jabus result: ' + str(nResult), 'Debug')
        elif (str(Prefs['pornav_use']) == 'True' and ((nSite == 'pornav')or (nSite == ' '))):
            nResult=self.pornav_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('pornav result: ' + str(nResult), 'Debug')
        elif (str(Prefs['javdb_use']) == 'True' and ((nSite == 'javdb')or (nSite == ' '))):
            nResult=self.javdb_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('pornav result: ' + str(nResult), 'Debug')
        elif (str(Prefs['javlibrary_use']) == 'True' and ((nSite == 'javlibrary')or (nSite == ' '))):
            nResult=self.javlibrary_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('javdb result: ' + str(nResult), 'Debug')

        Logging("####### End update #########", 'Info')

    def get_fileinfo(self,media):
        # 파일에서 정보를 읽어 품번, 제목을 리턴함
        Logging('### 파일에서 정보읽기 시작 ###', 'Debug')
        n_ret=[]
        filename = urllib.unquote(media.filename).decode('utf8')
        filename = os.path.splitext(filename)[0]
        filename = os.path.basename(filename).strip().replace('hhd800.com@','')
        Logging('입력 파일명: ' + filename,'Debug')
        pattern = '(?i)(TOKYO.*)-n[0-9]{3,}|((CARIB.*)|(1PONDO.*)|\w{2,}|((FC2).*(PPV)))-[0-9]{3,}'
        nMatch = re.search(pattern, filename)
        if (nMatch is not None):
            poombun=nMatch.group(0).upper()
            pattern = '(?i)(TOKYO.*)-[A-Z]{1,}[0-9]{3,}|((CARIB.*)|(1PONDO.*)_[0-9]{1,}|\w{2,}|((FC2).*(PPV)))-[0-9]{3,}'
            title = re.sub(pattern,'', filename)  # 품번 제거
            pattern = '\([^)]*\)|\[[^)]*\]'
            title = re.sub(pattern, '', title)  # 괄호와 대괄호 사이 글자 제거
            if title == ' ': title=''
            Logging('### Poombun output: ' + poombun , 'Debug')
            Logging(title, 'Debug')
            n_ret.append(poombun)
            n_ret.append(title)
        else:
            n_ret.append(filename)
            n_ret.append('')
            # return None
        return n_ret

    def func_update_title(self,metadata,media,id,title,ncroling,Trans):
        # title: 크롤링에서 가져온 제목, ncroling: Y일때 파일명을 타이틀로, N일때 웹크롤링을 타이틀로
        Logging('func_update_title 함수 시작','Debug')
        firststring = metadata.title[0]
        # Logging('First string: ' + firststring, 'Debug')
        try:
            if (ncroling == 'Y'):
                Logging('파일명 => 제목', 'Debug')
                rTitle = '▶' + metadata.title.strip()
                metadata.title = rTitle
                metadata.title_sort = rTitle.replace('[','').replace(']','').replace('▶','')
            elif (ncroling == 'N'):
                Logging('웹크롤링 => 제목', 'Debug')
                nTitle_Trans = Papago_Trans(title, Trans)
                rTitle = '[' + id + "] " + nTitle_Trans
                metadata.title_sort = id + ' ' + nTitle_Trans
                metadata.title = rTitle.strip()
            elif (firststring == '▶'):
                Logging('첫번째 문자열에 ▶ 발견. 제목행은 업데이트 하지 않습니다','Info')

            Logging('## Title: ' + metadata.title, 'Debug')
        except:
            Logging('@@@ 제목 오류 @@@', 'Error')
            pass

        # Logging('### 제목 종료 ###', 'info')
        # Logging('func_update_title 함수 종료','Debug')

##### SEARCH Define #####

    def dmm_search(self,results,media,lang):
        ##############################
        ###### dmm video 검색  ########
        ##############################

        Logging('##### Start dmm video search #####','Info')
        SEARCH_URL = 'https://www.dmm.co.jp/search/=/searchstr='

        Logging('Media input title: ' + media.name,'Debug')

        getfileinfo=self.get_fileinfo(media)
        # if getfileinfo is None:
        #     # Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
        #     getfineinfo[0]=media
            # return
        Logging('품번: ' + getfileinfo[0],'Info')
        Logging('타이틀: <' + getfileinfo[1] + '>','Info')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()

        # org_id = poombun_check(media.name,media.filename).replace(' ','-').upper() #파일명에서 품번 가져옴
        # 품번이 공백이면 종료, dmm은 검색시 하이픈 대신 00을 사용함. DV품번은 0 하나만 들어감
        if (org_id == ''): return 0
        if (org_id.find('DV-') > -1): release_id = org_id.replace('-', '0')
        else: release_id=org_id.replace('-','00')

        Logging('******* DMM Video 검색 시작(Media search start) ****** ','Info')
        Logging("### Release ID:    " + str(release_id) + ' org_id: ' + str(org_id),'Debug')  # Release ID: IPZ00929 org_id: IPZ-929
        searchResults = Get_search_url(SEARCH_URL, release_id)

        if (searchResults <> ''):
            nResult = searchResults.find('<ul id="list">') #검색결과 없음
            if (nResult <> -1):
                Logging('##### dmm Video Result Found #####','Error')
                if (uncensored_check(media.filename) == 1):
                    uncResult = 'U'
                else:
                    uncResult = 'C'
                Logging('### UNC:' + uncResult,'Debug')

                # try:
                # 검색된 타이틀 개수 확인
                searchCNTtxt = String_slice(searchResults, 'list-boxcaptside list-boxpagenation', '</p>')
                searchCNTtxt = String_slice(searchCNTtxt,'<p>','タイトル中')
                searchCNT = int(searchCNTtxt)
                Logging('### 검색된 타이틀 개수: ' + searchCNTtxt, 'Info')

                searchResults = String_slice(searchResults, '<ul id="list">', '</ul>')
                searchArray = searchResults.split('</li>')
                nResult_url = ''
                nResult_title = ''

                for i in range(0, searchCNT): # 검색된 항목들의 값에서 실제 호출 주소와 타이틀명만 발라냄
                    nResult_url=String_slice(searchArray[i],'<a href="','?')
                    nResult_title= String_slice(searchArray[i],'alt="','"')
                    Logging('1 ### nResult_url: ' + nResult_url + ' nResult_title: ' + nResult_title)
                    if (nResult_url.find('digital/videoa') <> -1):
                        searchtype = 'DMMa'
                        # Logging('dmma','Info')
                        break
                    elif (nResult_url.find('digital/videoc') <> -1):
                        searchtype = 'DMMc'
                        # Logging('dmmc', 'Info')
                        break
                    elif (nResult_url.find('mono/dvd') <> -1):
                        searchtype = 'DMMd'
                        # Logging('dmmd', 'Info')
                        break
                    elif (nResult_url.find('rental/ppr') <> -1):
                        searchtype = 'DMMr'
                        # Logging('dmmr', 'Info')
                        break
                    else:
                        nResult_url=''
                        # Logging('else', 'Info')

                Logging('2 ### SearchType: ' + searchtype + ' nResult_url: ' + nResult_url + ' nResult_title: ' + nResult_title)

                if (nResult_url == ''): #
                    Logging('### Cannot find title !!', 'Info')
                    return 1

                content_id = String_slice(nResult_url,'cid=','/')
                Logging(' Content_id: ' + content_id, 'Debug')
                id = org_id
                title = Papago_Trans(nResult_title,'ja')
                if (Prefs['filenametotitle'] == False or title_fromfile == ''):
                    titletype = 'N'
                else:
                    title=title_fromfile.strip()
                    titletype='Y'
                name = '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id + '§' + titletype
                score=100
                results.Append(MetadataSearchResult(id=content_id, name=name, score=score, lang=lang))
                Logging('### Search Update Result ==> id: ' + content_id + ' name: ' + name + ' score : ' + str(score), 'Debug')
                return 1
            else:
                Logging('DMM Video result Not found', 'Error')
        else:
            Logging('DMM Video result not found1', 'Error')

        return 0

    def r18_search(self,results,media,lang):
        ##############################
        ######### r18 검색  ##########
        ##############################
        Logging('##### Start r18 video search #####', 'Info')
        SEARCH_URL = 'https://www.r18.com/common/search/searchword='

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return 0
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()
        release_id = org_id
        
        Logging('******* r18 미디어 검색 시작(r18 Media search start) ****** ','Info')
        Logging("Release ID:    " + str(release_id) + ' org_id: ' + org_id,'Debug')
        try:
            encodedId = urllib2.quote(release_id)
            url = SEARCH_URL + encodedId.replace('-','00')
            Logging('다음의 주소로 검색합니다: ' + url , 'Debug')
            searchResults = HTML.ElementFromURL(url, timeout=int(Prefs['timeout']))
            Logging("검색결과 가져옴(Got search result)",'Info')
        except:
            Logging('@@@ r18 검색 실패','Error')
            return 0
        if (searchResults <> None):
            Logging('##### r18 검색된 문장 파싱 시작 #####', 'Info')
            findcontent=0
            for searchResult in searchResults.xpath('//li[contains(@class, "item-list")]'):
                if (uncensored_check(media.filename) == 1):
                    uncResult = 'U'
                else:
                    uncResult = 'C'
                Logging('### UNC:' + uncResult,'Debug')
                findcontent=1 #xpath에 내용이 검색되면 값을 1로
                # Logging(searchResult.text_content())
                content_id = searchResult.get("data-content_id")
                id = searchResult.xpath('a//p//img')[0].get("alt")
                id = id.upper()
                title = searchResult.xpath('a//dl//dt')[0].text_content()
                if title.startswith("SALE"): title = title[4:] # SALE 텍스트 이후부터 저장

                videotype = searchResults.xpath('//*[@id="contents"]/div[2]/section/ul[2]/li/a')[0].get("href")
                # Logging('### VideoType: ' + videotype,'Info')
                if (videotype.find('amateur') == -1 ):
                    searchtype='r18v' #비디오 경로가 일반 비디오
                else:
                    searchtype='r18a' #비디오 경로가 아마추어 비디오
                Logging('### VideoType: ' + searchtype, 'Info')
                
                if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                    title=title_fromfile
                    titletype='Y'
                else:
                    titletype = 'N'

                title = Papago_Trans(title, 'en')
                name= '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id +'§' + titletype
                score = 100 - Util.LevenshteinDistance(id.lower(), release_id.lower())
                results.Append(MetadataSearchResult(id=content_id, name=name, score=score, lang=lang))
                Logging('ID: ' + content_id + ' name: ' + "[" + id + "] " + title, 'Debug')
            if (findcontent==0):
                Logging('@@@ r18 검색결과 없음(Result not found)', 'Error')
                return 0
            else:
                results.Sort('score', descending=True)
                Logging('******* r18 검색 완료(Search Completed) ****** ', 'Info')
                return 1
        else:
            Logging('@@@ r18 검색결과 없음(Result not found)', 'Error')
            return 0

    def javbus_search(self, results, media, lang):
        ###############################
        ##### javbus video 검색  #######
        ###############################
        Logging('##### Start javbus video search #####','Info')
        SEARCH_URL = 'https://www.javbus.com/search/'

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()
        release_id = org_id

        Logging('******* javbus Video 검색 시작(Media search start) ****** ','Info')
        Logging("Release ID:    " + str(release_id),'Debug')
        try: searchResults=HTTP.Request(SEARCH_URL + release_id, timeout=int(Prefs['timeout'])).content # post로 보낼경우 value={'aaa' : 내용} 으로 보냄
        except:	return 0
        # Logging(searchResults,'Debug')
        if (searchResults <> ''):
            nResult = searchResults.find('<div id="waterfall">')  # 검색결과 확인
            # Logging(searchResults)
            # Logging(nResult)
            if (nResult <> -1):
                Logging('##### javbus Video Result Found #####','Info')
                if (uncensored_check(media.filename) == 1):
                    uncResult = 'U'
                else:
                    uncResult = 'C'
                Logging('### UNC:' + uncResult,'Debug')
                searchResults = String_slice(searchResults, '<div id="waterfall">', '<script')
                content_id = String_slice(searchResults, '<date>', '</date>')
                id = org_id
                title = String_slice(searchResults, 'title="', '">').replace('\"','"')

                searchtype='javbus'
                if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                    title=title_fromfile
                    titletype='Y'
                else:
                    titletype = 'N'

                title = Papago_Trans(title, 'ja')
                name= '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id +'§' + titletype
                score = 100
                results.Append(MetadataSearchResult(id=content_id, name=name , score=score, lang=lang))# id는 내부적사용, name은 미리보기 타이틀명
                Logging('ContentID: ' + content_id + ' org_id: ' + org_id,'Debug')
                # Logging('Title: ' + title)
                return 1
            else:
                Logging('javbus Video result Not found','Error')
                return 0
        else:
            Logging('javbus result Not found','Error')
            return 0

    def pornav_search(self, results, media, lang):
        ###############################
        ##### pornav video 검색  #######
        ###############################
        Logging('##### Start pornav video search #####','Info')
        SEARCH_URL = 'https://pornav.co/jp/search?q='

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Logging('품번 정보: ' + getfileinfo[0],'Info')
        Logging('파일에서 읽은 타이틀: <' + getfileinfo[1] + '>','Info')
        org_id = getfileinfo[0]
        title_fromfile = getfileinfo[1].strip()
        release_id = poombun_split_num(org_id) #아마추어 작품의 경우 품번 숫자만 필요해서 숫자만 추리는 함수 호출

        Logging("### Release ID:    " + str(release_id) + ' ### org_id: ' + org_id,'Debug')
        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id).content  # post로 보낼경우 value={'aaa' : 내용} 으로 보냄
        except:
            Logging( 'pornav search exception','Error')
            return 0
        # Logging(searchResults)
        if (searchResults <> ''):
            title = ''
            if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                title = title_fromfile
                titletype = 'Y'
            else:
                titletype = 'N'
                nResult = '<div class="product-description">'  # 검색결과 확인 이 텍스트가 있으면 일단 오류페이지는 아님
                if nResult in searchResults: # nResult 문자열이 searchResults 문자열안에 있을 경우
                    nTitle = Extract_str_title_pornav(searchResults, '<div id="grid-container"', '<div class="footer">', release_id,'TITLE')
                    if nTitle is not None:
                        Logging('##### pornav Video Result Found #####','Info')
                        title = Papago_Trans(nTitle,'ja')
                    else:
                        Logging('@@@ Pornav 검색 실패', 'Error')
                        return 0

            if (uncensored_check(media.filename) == 1):
                uncResult = 'U'
            else:
                uncResult = 'C'
            Logging('### UNC:' + uncResult,'Debug')
            content_id=org_id
            id = org_id
            searchtype = 'pornav'
            name = '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id + '§' + titletype
            score = 100
            results.Append(MetadataSearchResult(id=content_id, name=name , score=score, lang=lang))  # id는 내부적사용, name은 미리보기 타이틀명
            Logging('ContentID: ' + content_id + ' org_id: ' + org_id,'Debug')
            return 1

        Logging('pornav result Not found','Error')
        return 0

    def javdb_search(self,results,media,lang):
        ##############################
        ###### javdb video 검색  ######
        ##############################
        Logging('##### Start javdb video search #####','Info')
        SEARCH_URL = 'https://javdb.com/search?q=' #https://javdb.com/search?q=STARS-466&f=all
        SEARCH_URL_R18 = 'https://javdb.com/over18?respond=1&rurl='

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id = getfileinfo[0]
        title_fromfile = getfileinfo[1].strip()
        release_id = poombun_split_num(org_id) #아마추어 작품의 경우 품번 숫자만 필요해서 숫자만 추리는 함수 호출

        Logging('******* javdb Video 검색 시작(Media search start) ****** ','Info')
        Logging("### Release ID:    " + str(release_id) + ' org_id: ' + str(org_id),'Info')  # Release ID: IPZ00929 org_id: IPZ-929

        # try:
        searchResults = HTTP.Request(SEARCH_URL + release_id + '&f=all' , headers = HDR_javdb).content
        Log(searchResults)
        # except:
        #     Logging( 'javdb search exception','Error')
        #     return 0

        if (searchResults <> ''):
            if 'rurl' in searchResults: # 18over 체킹 시도시.
                rurl = String_slice(searchResults,'=','"')
                Logging('성인 인증을 위한 rurl 정보: ' + rurl,'Info')
                try:
                    searchResults = HTTP.Request(SEARCH_URL_R18 + rurl).content
                except:
                    Logging('javdb R18over search exception', 'Error')
                    return 0
                # Logging(searchResults,'Debug')
            nResult = 'videos video-container'  # 검색결과 있음
            if nResult in searchResults:
                Logging('##### javdb Video Result Found1 #####','Info')
                if (uncensored_check(media.filename) == 1):
                    uncResult = 'U'
                else:
                    uncResult = 'C'
                Logging('### UNC:' + uncResult,'Debug')
                nTitle = []
                nTitle = Extract_str_title_javdb(searchResults, 'videos video-container', '</section>', release_id)
                if nTitle is not None:
                    Logging('##### javdb Video Result Found2 #####','Info')
                    title = Papago_Trans(nTitle[0],'ja')
                    content_id = nTitle[1].replace('/v/','')
                    id = org_id
                    searchtype = 'javdb'
                    if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                        title = title_fromfile
                        titletype = 'Y'
                    else:
                        titletype = 'N'
                    name = '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id + '§' + titletype
                    score = 100
                    results.Append(MetadataSearchResult(id=content_id, name=name, score=score, lang=lang))
                    Logging(
                        '##Search Update Result ==> id: ' + id + ' name: ' + name + ' score : ' + str(score) + ' Contents_id: ' + content_id,
                        'Debug')
                    return 1
                else:
                    Logging('@@@ javdb 검색 실패', 'Error')
                    return 0
            else:
                Logging('javdb Video result Not found','Error')
        else:
            Logging('javdb Video result not found1','Error')
        return 0

    def javlibrary_search(self,results,media,lang):
        #############################
        ##### javlibrary video 검색  ######
        #############################
        Logging('##### Start javlibrary video search #####','Info')
        SEARCH_URL = 'http://www.javlibrary.com/ja/vl_searchbyid.php?keyword='

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()
        release_id=poombun_split_num(org_id) #아마추어 작품의 경우 품번 숫자만 필요해서 숫자만 추리는 함수 호출

        Logging('******* javlibrary Video 검색 시작(Media search start) ****** ','Info')
        Logging("### Release ID:    " + str(release_id) + ' org_id: ' + str(org_id),'Info')  # Release ID: IPZ00929 org_id: IPZ-929

        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id).content
        except:
            Logging( 'javlibrary search exception','Error')
            return 0

        if ((searchResults <> '') and ('ご指定の検索条件に合う項目がありませんでした' not in searchResults)):#'상세 검색 조건에 맞는 항목이 없습니다' 메시지임
            # Logging("javlibrary 호출 본문: " + searchResults,'Debug')

            Logging('##### javlibrary Video Result Found #####','Info')
            if (uncensored_check(media.filename) == 1):
                uncResult = 'U'
            else:
                uncResult = 'C'
            Logging('### 파일명에 노모 글자 포함인지 확인 UNC:' + uncResult,'Debug')

            # 검색결과가 바로 나올 경우
            if ('<div id="video_title">' in searchResults): #검색 결과가 바로 나올경우
                searchResults=String_slice(searchResults,'<div id="video_title">','</table>')
                if (searchResults.find(release_id) == -1): return 0
                content_id = String_slice(searchResults, '/ja/?v=','"')
                Logging(' Content_id: ' + content_id,'Debug')
                title = String_slice(searchResults, "rel='bookmark' >", '</a>').replace(org_id,'').strip()
            elif ('<div class="videothumblist">' in searchResults): #검색 항목이 여러개일때
                searchResults=String_slice(searchResults,'<div class="videothumblist">','</div>')
                if (searchResults.find(release_id) == -1): return 0
                content_id = String_slice(searchResults, '"./?v=','"')
                Logging(' Content_id: ' + content_id,'Debug')
                title = String_slice(searchResults, 'title="', '"').replace(org_id,'').strip()
            else:
                Logging('javlibrary Video result not found', 'Error')
                return 0

            id = org_id
            Logging(' Title: ' + title, 'Debug')
            title = Papago_Trans(title,'ja')
            searchtype = 'javlibrary'
            if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                title = title_fromfile
                titletype = 'Y'
            else:
                titletype = 'N'
            name = '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id + '§' + titletype
            score = 100
            results.Append(MetadataSearchResult(id=content_id, name=name, score=score, lang=lang))
            Logging('##Search Update Result ==> id: ' + content_id + ' name: ' + name + ' score : ' + str(score),'Debug')
            return 1
        else:
            Logging('javlibrary Video result not found1','Error')
        return 0

##### UPDATE Define #####

    def dmm_update(self, metadata, media, lang, nOrgID,ncroling,nSite):
        ################################################
        ################## DMM update ##################
        ################################################
        DETAIL_URL=''

        if (nOrgID.find('[') <> -1):
            org_id = poombun_check(nOrgID, '')
        else:
            org_id = nOrgID

        if (nSite == 'DMMa'):
            DETAIL_URL = 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid='
        elif (nSite == 'DMMc'):
            DETAIL_URL = 'https://www.dmm.co.jp/digital/videoc/-/detail/=/cid='
        elif (nSite == 'DMMd'):
            DETAIL_URL = 'https://www.dmm.co.jp/mono/dvd/-/detail/=/cid='
        elif (nSite == 'DMMr'):
            DETAIL_URL = 'https://www.dmm.co.jp/rental/ppr/-/detail/=/cid='

        Logging('### 검색 사이트: DMM 일반 영상 / UpdateSite: DMM Video ###', 'Info')
        bgimgURL = 'https://pics.dmm.co.jp/digital/video/'
        bgimgExt = 'jp-'

        Logging('ORG_ID: ' + org_id + ' metadataID: ' + str(metadata.id), 'Debug')

        searchResults = Get_search_url(DETAIL_URL, metadata.id, 'GET')
        searchResults = String_slice(searchResults, 'area-headline group', 'div id="recommend"')

        # 제목
        Logging('┌────── dmm 제목 시작 ──────┐', 'Info')
        id = org_id.upper()

        nTitle = String_slice(searchResults, 'item fn">', '<')
        Logging('### 추출한 제목 : ' + nTitle + '  Search 단계에서의 제목:' + metadata.title, 'Debug')
        if  ((nTitle == '') and (metadata.title <> '')): nTitle = metadata.title
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('└──────  dmm 제목 시작 ──────┘', 'Info')

        # 스튜디오
        Logging('┌────── dmm 스튜디오 시작 ──────┐', 'Info')
        sTemp = String_slice(searchResults, 'メーカー：', '</tr>').replace('width="100%">','')  # 스튜디오 정보
        Logging('자를원본:'+ sTemp,'Debug')
        sTemp = re.sub('<.+?>', '', sTemp, 0, re.I|re.S)
        nStudio = Search_Label(sTemp)
        if (sTemp == nStudio): nStudio = Papago_Trans(sTemp, 'ja')
        metadata.studio = nStudio
        Logging(" dmm 스튜디오 정보: " + nStudio,'Info')
        Logging('└────── dmm 스튜디오 종료 ──────┘', 'Info')

        # 감독
        Logging('┌────── dmm 감독 시작 ──────┐', 'Info')
        try:
            sTemp = String_slice(searchResults, '監督：', '</tr>')
            director_info = re.sub('<.+?>', '', sTemp, 0, re.I|re.S)
            # sTemp = ExtractFromHtml('監督：', '</tr>',searchResults)
            Logging('감독 이름: ' + director_info,'Debug')
            if (director_info <> '----'):
                director_info_ko = Papago_Trans(director_info, 'ja')
                metadata.directors.clear()
                try:
                    meta_director = metadata.directors.new()
                    meta_director.name = director_info_ko
                    Logging("저장할 감독 정보: " + director_info_ko,'Info')
                except:
                    try:
                        metadata.directors.add(director_info_ko)
                    except:
                        pass
        except:
            pass
        Logging('└────── dmm 감독 종료 ──────┘', 'Info')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        Logging('┌────── dmm 일자 시작 ──────┐', 'Info')
        # try:
        if (searchResults.find('発売日') <> -1):
            sTemp = String_slice(searchResults, '>配信', '</tr>')
        elif (searchResults.find('商品発売日') <> -1):
            sTemp = String_slice(searchResults, '>商品', '</tr>')
        elif (searchResults.find('配信開始日') <> -1):
            sTemp = String_slice(searchResults, '>配信', '</tr>')
        else:
            sTemp = ''
        if (sTemp <> ''):
            Log(sTemp)
            nYear = String_slice(sTemp, '<td>', '</td>')
            Log(nYear)
            nYearArray = nYear.split('/')
            # 미리보기 항목의 이미지 아래 표시되는 년도
            metadata.year = int(nYearArray[0])
            # 상세항목의 '원출처' 일자
            nYear = nYear.replace('/', '-')
            metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
            Logging('## 저장할 일자: ' + nYear)
        # except:
        #     pass
        Logging('└────── dmm 일자 종료 ──────┘', 'Info')

        # 국가
        metadata.countries.clear()
        metadata.countries.add('일본')

        # 줄거리
        Logging('┌────── dmm 줄거리 시작 ──────┐', 'Info')
        try:
            sTemp = String_slice(searchResults, '<div class="mg-b20 lh4">', '</div')
            # sTemp = ExtractFromHtml('<div class="mg-b20 lh4">', '</div',searchResults)
            sTemp = re.sub('<.+?>', '', sTemp, 0, re.I|re.S)
            sTemp = re.sub('&nbsp;| |\t|\r|\n', '', sTemp) # 모든 HTML 태그 제거
            Logging(' 테그 제거 결과: ' + sTemp ,'Debug')
            if (sTemp <> ''):
                Logging('#### 줄거리 (Summary): ' + sTemp, 'Debug')
                metadata.summary = Papago_Trans(sTemp, 'ja')
                if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[DMM] ' + metadata.summary
        except:
            pass
        Logging('└────── dmm 줄거리 종료 ──────┘', 'Info')

        # 장르
        Logging('┌────── dmm 장르 시작 ──────┐', 'Info')
        try:
            metadata.genres.clear()
            nGenreName = Extract_str(searchResults, 'ジャンル：', '</tr>')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                nGenreName_ko = Search_Category(nGenreName[i])
                if (nGenreName[i] == nGenreName_ko): nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.', '')
                metadata.genres.add(nGenreName_ko)
        except:
            pass
        Logging('└────── dmm 장르 종료 ──────┘', 'Info')

        # 배우정보
        Logging('┌────── dmm 배우정보 시작 ──────┐', 'Info')
        try:
            metadata.roles.clear()
            nActorName = Extract_str(searchResults, '出演者：', '</tr>')

            if (nActorName is not None):
                j = len(nActorName)
                Logging('### 배우 수: ' + str(len(nActorName)), 'Debug')
                for i in range(0, j):
                    role = metadata.roles.new()
                    if ('すべて表示する' in nActorName[i]):break # すべて表示する 모두보기 버튼임
                    if ('（' in nActorName[i]): nActorName[i] = nActorName[i][0:nActorName[i].find('（')] # '（' 이전까지만 저장
                    nActorInfo = Get_actor_info(nActorName[i])
                    if (nActorInfo is not None):
                        role.photo = nActorInfo[0]
                        role.name = nActorInfo[1]
                        # Logging('배우이미지주소: ' + nActorInfo[0] + ' 배우이름: ' + nActorInfo[1], 'Debug')
                    else:
                        role.name = nActorName
                        # Logging('배우이미지주소: 검색실패' + ' 배우이름: ' + nActorName[i], 'Debug')
            else:
                Logging('배우정보 없음','Info')
        except:
            Logging('Actor Info Failed','Info')
            pass
        Logging('└────── dmm 배우정보 종료 ──────┘', 'Info')

        # 포스터
        Logging('┌────── dmm 포스터 시작 ──────┐', 'Info')
        nposterMain = String_slice(searchResults, 'id="sample-video"', '</div>')
        posterURL_Small = String_slice(nposterMain, 'img src="', '"')  # 큰이미지가 없을수도 있음(아마추어의 경우)
        posterURL_Large = String_slice(nposterMain, 'a href="', '"')
        Logging("small Poster URL / 포스터 주소 : " + posterURL_Small, 'Debug')
        Logging("Large Poster URL / 포스터 주소 : " + posterURL_Large, 'Debug')
        try:
            if (posterURL_Small <> ''):
                metadata.posters[posterURL_Small] = Proxy.Preview(
                    HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
        except:
            Logging('@@@ Can not load Small Poster', 'Error')

        try:
            if (posterURL_Large <> ''):
                metadata.posters[posterURL_Large] = Proxy.Preview(
                    HTTP.Request(posterURL_Large, timeout=int(Prefs['timeout'])), sort_order=2)
        except:
            Logging('@@@ Can not load Large Poster', 'Error')
        Logging('└────── dmm 포스터 종료 ──────┘', 'Info')

        # 배경 이미지
        Logging('┌────── dmm 배경이미지 시작 ──────┐', 'Info')
        sTemp = String_slice(searchResults, 'div id="sample-image-block"', '<div class')
        Logging('배경이미지:' + sTemp, 'Debug')
        j = sTemp.count('img src') # 검색된 이미지 개수 카운트
        imgcnt = int(Prefs['img_cnt']) # 설정에 등록한 최대 다운로드 이미지 개수
        if (imgcnt <= j): j = imgcnt
        Logging('Image count: ' + str(j),'Debug')
        extimg = Extract_imgurl(sTemp, 'class', '<br', hreforsrc='src')
        Logging('추출된 이미지 개수: ' + str(j),'Info')
        for i in range(0,j):
            # 경로에서 파일명 및 확장자만 추출
            originNames = extimg[i].split("/")
            renameFile = originNames[len(originNames) - 1]
            Logging('### 파일명 추출: ' + renameFile, 'Info')

            # 이미지 파일이 aaajs-1.jpg => aaajp-1.jpg 로 해야 큰 이미지
            # 가끔 aaa-1.jpg 같이 나올경우 강제로 jp를 붙여야 큰 이미지로 나옴
            if (renameFile.find('js-') <> -1):
                ReplaceFile = renameFile.replace('js-','jp-')
            else:
                ReplaceFile = renameFile.replace('-', 'jp-')
            extimg_Large=extimg[i].replace(renameFile,ReplaceFile)

            Logging(str(i)+ '### 이미지 경로: ' + extimg[i] + ' 큰이미지 경로: ' + extimg_Large ,'Debug')
            try:
                if (extimg_Large <> ''):
                    metadata.art[extimg_Large] = Proxy.Preview(HTTP.Request(extimg_Large, headers=HDR_javdb,
                                                                         timeout=int(Prefs['timeout'])).content, sort_order=i + 1) #{'Referer': 'http://www.google.com'}
            except:
                Logging('###' + extimg[i] + ' Can not load', 'Error')
        Logging('└────── dmm 배경이미지 종료 ──────┘', 'Info')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        # try:
        Logging('######## series info ########', 'Info')
        sTemp = String_slice(searchResults, 'シリー', '</tr>')
        # Logging(sTemp)
        series_info = Extract_str(sTemp, '<td>', '</td>')
        # Logging(series_info)
        # Logging('SeriesInfo: ' + series_info)
        if (series_info is not None):
            if (series_info[0] <> '----'):
                series_info_ko = Papago_Trans(series_info[0], 'ja')
                Logging(series_info_ko, 'Info')
                metadata.tagline = series_info_ko
        else:
            Logging('Series info not found', 'Error')
        # except:
        #     pass

        # studio 컬렉션 생성
        if (str(Prefs['create_collection_studio']) == 'True'):
            if metadata.studio != None:
                metadata.collections.add(metadata.studio)
                Logging(' metadata.collections studio: ' + str(metadata.studio), 'Debug')
        else:
            Logging('### Studio 컬렉션 생성 안함(설정 미체크) / Studio connection not create(prefrence not check ###', 'Info')

        # series 컬렉션 생성
        if (str(Prefs['create_collection_series']) == 'True'):
            if metadata.tagline != None:
                metadata.collections.add(metadata.tagline)
                Logging(' metadata.collections series: ' + str(metadata.tagline), 'Debug')
        else:
            Logging('### series 컬렉션 생성 안함(설정 미체크) Series connection not create(prefrence not check ###', 'Info')

        Logging('******* DMM 미디어 업데이트 완료/Media Update completed ****** ', 'Info')
        return 1

    def r18_update(self, metadata, media, lang, nOrgID,ncroling, nSite):
        ################################################
        ################## r18 update ##################
        ################################################
        Logging('****** 미디어 업데이트(상세항목) 시작 / r18 Media Update Start *******', 'Info')

        DETAIL_URL = 'https://www.r18.com/api/v4f/contents/'
        org_id = poombun_check(nOrgID, '')
        Logging('orgid: ' + org_id + ' metadataid: ' + metadata.id, 'Info')

        try:
            json_data = JSON.ObjectFromURL(url=DETAIL_URL + metadata.id)
            Logging(json_data,'Debug')
        except:
            Logging('@@@ Update content load failed', 'Error')
            return 0

        Logging('┌────── r18 제목 시작 ──────┐', 'Info')
        try:
            id = org_id.upper()
            nTitle = json_data['data']['title']
            metadata.original_title = nTitle
            self.func_update_title(metadata, media, id, nTitle, ncroling, 'en')
        except:
            pass
        Logging('└────── r18 제목 종료 ──────┘', 'Info')

        # 스튜디오
        # Logging('--------------------------------')
        # Logging(json_data['data']['maker'],'Info')
        # Logging('--------------------------------')
        Logging('┌────── r18 스튜디오 시작 ──────┐', 'Info')
        try:
            for key, value in json_data['data']['maker'].items():
                if (key == 'name'):
                    # Logging(value,'Info')
                    # nStudio = value
                    nStudio = Search_Label(value)
                    if (value == nStudio): nStudio = Papago_Trans(value, 'en')
                    # nStudioTr = Papago_Trans(nStudio, 'en')
                    metadata.studio = nStudio  # 스튜디오 정보
                    Logging('### 스튜디오 정보(ORG): ' + nStudio + ' 번역: ' + nStudioTr, 'Info')
        except:
            pass
        Logging('└────── r18 스튜디오 종료 ──────┘', 'Info')

        # 줄거리 요약정보
        Logging('┌────── r18 줄거리 시작 ──────┐', 'Info')
        try:
            if (json_data['data']['comment'] is not None):
                nSummary = json_data['data']['comment']
                nSummaryTR = Papago_Trans(nSummary, 'en')
                metadata.summary = '[R18] ' + nSummaryTR  # 줄거리 요약정보
                Logging('### 줄거리 정보(ORG): ' + nSummary + ' 번역: ' + nSummaryTr, 'Info')
            else:
                Logging('@@@ 줄거리 정보 없음 @@@', 'Info')
        except:
            pass
        Logging('└────── r18 줄거리 종료 ──────┘', 'Info')

        # 감독정보
        Logging('┌────── r18 감독정보 시작 ──────┐', 'Info')
        try:
            if (json_data['data']['director'] is not None):
                nDirector = json_data['data']['director']
                nDirectorTR = Papago_Trans(nDirector, 'en')
                metadata.directors.clear()
                meta_director = metadata.directors.new()
                meta_director.name = director_info
                metadata.directors.add(director_info)
                Logging('### 감독 정보(ORG): ' + nDirector + ' 번역: ' + nDirectorTR, 'Info')
            else:
                Logging('@@@ 감독 정보 없음 @@@', 'Info')
        except:
            pass
        Logging('└────── r18 감독정보 종료 ──────┘', 'Info')

        # 릴리즈 날짜
        Logging('┌────── r18 릴리즈 날짜 시작 ──────┐', 'Info')
        try:
            if (json_data['data']['release_date'] is not None):
                nDate = json_data['data']['release_date']
                nYear = nDate.split(' ')
                nYearArray = nYear[0].split('-')
                metadata.year = int(nYearArray[0]) # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.originally_available_at = datetime.strptime(nYear[0], '%Y-%m-%d')# 상세항목의 '원출처' 일자
                Logging('### 릴리즈 날짜 : ' + str(metadata.originally_available_at), 'Info')
            else:
                Logging('@@@ 릴리즈 날짜 없음 @@@', 'Info')
        except:
            pass
        Logging('└────── r18 릴리즈 날짜 종료 ──────┘', 'Info')

        # 장르
        Logging('┌──────  장르 정보 시작 Genre Info start ──────┐', 'Info')
        try:
            nCategories=json_data['data']['categories']
            if (nCategories is not None):
                for categories in nCategories:
                    nGenre = categories['name']
                    nGenreName_ko = Search_Category(nGenre)
                    if (nGenre == nGenreName_ko): nGenreName_ko = Papago_Trans(nGenre, 'en').replace('.','')
                    # nGenreTr = Papago_Trans(nGenre, 'en')
                    metadata.genres.add(nGenreName_ko)  # 스튜디오 정보
                    Logging('### 장르 정보(ORG): ' + nGenre + ' 번역: ' + nGenreName_ko, 'Info')
            else:
                Logging('@@@ 장르 정보 없음 @@@', 'Info')
        except:
            Logging('@@@ Genre failed', 'Error')
            pass
        Logging('└──────  장르 정보 종료 Genre Info end ──────┘', 'Info')

        # 국가
        metadata.countries.clear()
        metadata.countries.add('일본')

        # 배우정보
        Logging('┌──────  배우 정보 시작 Actor Info start ──────┐', 'Info')
        try:
            metadata.roles.clear()
            nActor = json_data['data']['actresses']
            if (nActor is not None):
                for actor in nActor:
                    role = metadata.roles.new()
                    nActresses = actor['name']
                    nActorInfo = Get_actor_info(nActresses) #영문 배우명으로 AVDBS에서 먼저 찾는다
                    if (nActorInfo is not None):
                        Logging('### AVDBS에서 배우 정보 찾음  배우명: ' + nActorInfo[1] + ' 이미지 경로: ' + nActorInfo[0] ,'Info')
                        role.photo = nActorInfo[0]
                        role.name = nActorInfo[1]
                    else:
                        Logging('@@@ AVDBS에서 배우 정보 검색 실패. @@@')
                        nActressesTr = Papago_Trans(nActresses, 'en')
                        nActresses_url = actor['image_url']
                        if (nActresses_url.find('printing')==-1): ## 이미지 없을 경우 경로에 printing이 들어감. 이때는 이미지를 빼줌
                            role.photo = nActresses_url
                        else:
                            role.photo = ''
                        role.name = nActressesTr
                        Logging('R18 배우 정보로 저장합니다. 배우 이미지 주소: ' + nActresses_url + ' 배우 이름: ' + nActressesTr, 'Debug')
            else:
                Logging('@@@ 배우 정보 없음 @@@', 'Info')
        except:
            Logging('@@@ Actor failed','Error')
            pass
        Logging('└──────  배우 정보 끝 Actor Info end ──────┘', 'Info')

        # 포스터
        try:
            Logging('┌──────  포스터 시작 Poster Info start ──────┐', 'Info')
            nPoster = json_data['data']['images']['jacket_image']
            if (nPoster is not None):
                for key, value in nPoster.items():
                    if (key == 'large'): nPosterlarge = value
                    if (key == 'medium'): nPostermedium = value
                Logging('### 포스터 큰사이즈: ' + nPosterlarge + ' 작은사이즈: ' + nPostermedium)
                try:
                        metadata.posters[nPostermedium] = Proxy.Preview(
                            HTTP.Request(nPostermedium, timeout=int(Prefs['timeout'])), sort_order=1)
                        metadata.posters[nPosterlarge] = Proxy.Preview(
                            HTTP.Request(nPosterlarge, timeout=int(Prefs['timeout'])), sort_order=2)
                except:
                    Logging('@@@ Can not load Small Poster', 'Error')
        except:
            Logging('@@@ Poster failed', 'Error')
        pass
        Logging('└──────  포스터 정보 끝 Actor Info end ──────┘', 'Info')

        #배경이미지(갤러리)
        Logging('┌──────  배경이미지 background Info start ──────┐', 'Info')
        # try:
        nBackground = json_data['data']['gallery']
        nBackgroundcnt = len(nBackground)
        imgcnt = int(Prefs['img_cnt'])  # 설정에 등록한 최대 다운로드 이미지 개수
        if (imgcnt <= nBackgroundcnt): nBackgroundcnt = imgcnt
        Logging('### 전체 배경 이미지 수: ' + str(nBackgroundcnt) + ' 가져올 이미지 최대 수 : ' + str(nBackgroundcnt), 'Debug')
        if (nBackground is not None):
            i=1
            for Background in nBackground:
                nBackgroundLarge = Background['large']
                try:
                    metadata.art[nBackgroundLarge] = Proxy.Preview(
                        HTTP.Request(nBackgroundLarge, headers=HDR_R18, timeout=int(Prefs['timeout'])).content,
                        sort_order=i)
                except:
                    Logging('@@@ 배경 이미지 파일을 가져올 수 없습니다.', 'Error')
                if (i == nBackgroundcnt):break
                i = i + 1
        # except:
        #     Logging('@@@ 배경이미지 실패 Background failed', 'Error')
        # pass
        Logging('└──────  배경이미지 background end ──────┘', 'Info')

        # studio 컬렉션 생성
        if (str(Prefs['create_collection_studio']) == 'True'):
            if metadata.studio != None:
                metadata.collections.add(metadata.studio)
                Logging(' metadata.collections studio: ' + str(metadata.studio), 'Debug')
        else:
            Logging('### Studio 컬렉션 생성 안함(설정 미체크) / Studio connection not create(prefrence not check ###', 'Info')

        # series 컬렉션 생성
        if (str(Prefs['create_collection_series']) == 'True'):
            if metadata.tagline != None:
                metadata.collections.add(metadata.tagline)
                Logging(' metadata.collections series: ' + str(metadata.tagline), 'Debug')
        else:
            Logging('### series 컬렉션 생성 안함(설정 미체크) Series connection not create(prefrence not check ###', 'Info')

        Logging('******* r18 미디어 업데이트 완료/Media Update completed ****** ', 'Info')

        return 1

    def javbus_update(self, metadata, media, lang, nOrgID,ncroling):
        # nIDs[0]: 검색용 품번  nIDs[1]: 검색된 사이트(DMM, R18)   nIDs[2]: 아마추어(C)or일반(A)  nIDs[3]: 오리지널 품번(OAE-101)
        Logging('****** 미디어 업데이트(상세항목) 시작 / Javbus Media Update Start *******','Info')

        ################################################
        ################# javbus update #################
        ################################################
        Logging('### 검색 사이트: javbus 일반 영상 / UpdateSite: javbus Video ###','Info')
        DETAIL_URL = 'https://www.javbus.com/'
        org_id=poombun_check(nOrgID,'')

        try:
            searchResults=HTTP.Request(DETAIL_URL + metadata.id, timeout=int(Prefs['timeout'])).content
        except:
            Logging('@@@ Update content load failed','Error')
            return 0

        nResult = searchResults.find('<div class="container">')  # 검색결과 확인
        if (nResult == -1):
            Logging('@@@ Update content search result failed1', 'Error')
            return 0
        searchResults = String_slice(searchResults, '<div class="container">', '<div class="clearfix">')
        if (searchResults == ''):
            Logging('@@@ Update content search result failed2', 'Error')
            return 0

        Logging('┌────── javbus 제목 시작 ──────┐', 'Info')
        id = org_id.upper()
        nTitle = String_slice(searchResults, 'title="', '"')
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('└────── javbus 제목 종료 ──────┘', 'Info')

        # 스튜디오=> 제조사
        Logging('┌──────  Studio Info start ──────┐', 'Info')
        try:
            sTemp = String_slice(searchResults, '製作商', '</p>')
            sTemp = String_slice(sTemp, '">', '</a')
            nStudio = Search_Label(sTemp)
            if (sTemp == nStudio): nStudio = Papago_Trans(sTemp, 'ja')
            metadata.studio = nStudio #Papago_Trans(str(metadata.studio), 'ja')
            Logging('Studio: ' + str(metadata.studio),'Info')
        except:
            Logging('@@@ Studio failed','Error')
        Logging('└──────  Studio Info end ──────┘', 'Info')

        # 감독
        Logging('┌──────  Director Info start ──────┐','Info')
        try:
            # sTemp = String_slice(searchResults, '導演', '<p>')
            director_info = Extract_str(searchResults, '導演', '</p>')
            if (director_info is not None):
                director_info_ko = Papago_Trans(director_info[0], 'ja')
                metadata.directors.clear()
                try:
                    meta_director = metadata.directors.new()
                    meta_director.name = director_info_ko
                except:
                    try:
                        metadata.directors.add(director_info_ko)
                    except:
                        pass
        except:
            Logging('@@@ Director failed','Error')
        Logging('└──────  Director Info end ──────┘', 'Info')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        Logging('┌──────  Date Info start ──────┐', 'Info')
        try:
            if '日期:' in searchResults:
                nYear = String_slice(searchResults, '日期:', '</p>')
                Logging('nYear1:'+ nYear,'Debug')
                nYear = re.sub('<.+?>', '', nYear, 0, re.I | re.S).strip()
                Logging('nYear2:' + nYear, 'Debug')
                # nYear = String_slice(nYear, 'value">', '</')
                # Logging('nYear3:' + nYear, 'Debug')
                nYearArray = nYear.split('-')
                metadata.year = int(nYearArray[0])# 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')# 상세항목의 '원출처' 일자
                Logging('검색된 출시일자: ' + nYear,'Info')
        except:
            Logging('@@@ Date Failed','Error')
        Logging('└──────  Date Info start ──────┘', 'Info')

        # 줄거리(javbus는 줄거리 없음)
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[javbus]'

        # 국가
        metadata.countries.clear()
        metadata.countries.add('일본')

        # 장르
        Logging('┌──────  Genre Info start ──────┐', 'Info')
        try:
            metadata.roles.clear()
            nGenreName = Extract_str(searchResults, '類別:<span', '><butto')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                nGenreName_ko = Search_Category(nGenreName[i])
                if (nGenreName[i] == nGenreName_ko): nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.', '')
                # nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.','')
                # Logging(nGenreName[i])
                Logging(nGenreName_ko, 'Debug')
                metadata.genres.add(nGenreName_ko)
        except:
            Logging('@@@ Genre failed','Error')
        Logging('└──────  Genre Info end ──────┘', 'Info')

        # 배우정보
        Logging('┌──────  Actor Info start ──────┐', 'Info')
        metadata.roles.clear()
        nFound = '<div id="star-div">'
        try:
            if nFound in searchResults:
                nStr = String_slice(searchResults, '<div id="star-div">', '<h4 id="mag-submit-show')
                nActorURL = []
                nActorName= []
                linksList = re.findall('<img src="(.*)" ', nStr)
                for link in linksList: nActorURL.append(link)
                linksList = re.findall('title="(.*)"', nStr)
                for link in linksList: nActorName.append(link)
                j=len(nActorURL)
                for i in range(j):
                    role = metadata.roles.new()
                    rolename_kr = Papago_Trans(nActorName[i],'ja')
                    role.photo = str('https://www.javbus.com' + nActorURL[i])
                    role.name = rolename_kr
                    Logging('nURL: ' + str(nActorURL[i]) + ' nName: ' + rolename_kr,'Debug')
        except:
            Logging('@@@ Get actor info exception','Error')

        Logging('└──────  Actor Info end ──────┘','Info')

        # 포스터
        Logging('┌──────  Poster Info start ──────┐','Info')
        try:
            nposterMain = String_slice(searchResults, 'col-md-9 screencap', '</div>')
            posterURL_Large = 'https://www.javbus.com' + String_slice(nposterMain, 'href="', '"')
            posterURL_Small = posterURL_Large.replace('_b.jpg','.jpg').replace('cover', 'thumb')
            Logging("small Poster URL / 포스터 주소 : " + posterURL_Small,'Debug')
            Logging("Large Poster URL / 포스터 주소 : " + posterURL_Large,'Debug')
            try:
                if(posterURL_Small <>''):
                    metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:	Logging(' Can not load Small Poster','Error')
            try:
                if(posterURL_Large <>''):
                    metadata.posters[posterURL_Large] = Proxy.Preview(HTTP.Request(posterURL_Large, timeout=int(Prefs['timeout'])), sort_order=2)
            except:	Logging(' Can not load Large Poster', 'Error')
        except:
            Logging('@@@ Poster Failed','Error')
        Logging('└──────  Poster Info end ──────┘', 'Info')

        # 배경 이미지
        Logging('┌──────  Background Info start ──────┐', 'Info')
        # try:
        nBackgroundimg = Extract_imgurl(searchResults, '<div id="sample-waterfall">', '<div class="clearfix','href')
        j = len(nBackgroundimg)
        Logging('찾은 이미지 개수: ' + str(j),'Debug')
        imgcnt = int(Prefs['img_cnt'])
        if (imgcnt <= j): j = imgcnt
        if (j <> -1):
            for i in range(0, j):
                if (nBackgroundimg[i].find('pics.dmm.co.jp') <> -1):
                    bgimg = nBackgroundimg[i]
                    Logging('경로 있음 ' + nBackgroundimg[i],'Debug')
                else:
                    bgimg = 'https://www.javbus.com' + nBackgroundimg[i]
                    Logging('경로 없음 ' + nBackgroundimg[i],'Debug')
                # try:
                if(bgimg <>''):
                    metadata.art[bgimg] = Proxy.Preview(
                    HTTP.Request(bgimg, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order=i + 1)
                # except:
                #     Logging('@@@' + bgimg + ' Can not load','Error')
        # except:
        #     Logging('@@@ Background Image failed','Error')
        Logging('└──────  Background Info end ──────┘', 'Info')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        Logging('┌──────  Series Info start ──────┐', 'Info')
        try:
            # Logging('######## series info')
            # Logging(sTemp)
            series_info = Extract_str(searchResults, '系列', '</p>')
            # Logging(series_info)
            # Logging('SeriesInfo: ' + series_info)
            if (series_info is not None):
                if (series_info[0] <> '----'):
                    series_info_ko = Papago_Trans(series_info[0], 'ja')
                    Logging(series_info_ko,'Debug')
                    metadata.tagline = series_info_ko
            else:
                Logging('Series info not found','Error')
        except:
            Logging('@@@ Series failed','Error')
        Logging('└──────  Series Info end ──────┘', 'Info')

        # studio 컬렉션 생성
        try:
            if (str(Prefs['create_collection_studio']) == 'True'):
                if metadata.studio != None:
                    metadata.collections.add(metadata.studio)
                    Logging(' metadata.collections studio: ' + str(metadata.studio),'Debug')
            else:
                Logging('### Studio 컬렉션 생성 안함(설정 미체크) / Studio connection not create(prefrence not check ###','Info')
        except:
            Logging('@@@ Studio collection failed','Error')

        # series 컬렉션 생성
        try:
            if (str(Prefs['create_collection_series']) == 'True'):
                if metadata.tagline != None:
                    metadata.collections.add(metadata.tagline)
                    Logging(' metadata.collections series: ' + str(metadata.tagline),'Debug')
            else:
                Logging('### series 컬렉션 생성 안함(설정 미체크) Series connection not create(prefrence not check ###','Info')

            Logging('******* javbus 미디어 업데이트 완료/Media Update completed ****** ','Info')
            return
        except:
            Logging('@@@ Series collection failed','Error')

        return 1

    def pornav_update(self, metadata, media, lang, nOrgID,ncroling):

        # nIDs[0]: 검색용 품번  nIDs[1]: 검색된 사이트(DMM, R18)   nIDs[2]: 아마추어(C)or일반(A)  nIDs[3]: 오리지널 품번(OAE-101)
        Logging('****** 미디어 업데이트(상세항목) 시작 / pornav Media Update Start *******','Info')

        ################################################
        ################# pornav update #################
        ################################################
        Logging('### 검색 사이트: pornav 일반 영상 / UpdateSite: pornav Video ###','Info')
        DETAIL_URL = 'https://pornav.co/'
        SEARCH_URL = 'https://pornav.co/jp/search?q='

        org_id = metadata.id
        release_id = poombun_split_num(org_id)

        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id).content  # post로 보낼경우 value={'aaa' : 내용} 으로 보냄
        except:
            Logging( 'pornav search exception','Error')
            return 0

        nResult = '<div class="product-description">'  # 검색결과 확인 이 텍스트가 있으면 일단 오류페이지는 아님
        if nResult in searchResults:  # nResult 문자열이 searchResults 문자열안에 있을 경우
            nURL = Extract_str_title_pornav(searchResults, '<div id="grid-container"', '<div class="footer">',
                                              release_id, 'URL')
            if nURL is None:
                Logging('@@@ Pornav 업데이트를 위한 검색 실패', 'Error')
                return 0

        try:
            searchResults = HTTP.Request(DETAIL_URL + nURL , headers = {'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content
            nResult = searchResults.find('<div class="container content"')  # 검색결과 확인
            if (nResult == -1):
                Logging('@@@ Update content search result failed1','Error')
                return 0
        except:
            Logging('@@@ Update content load failed','Error')
        # Logging(searchResults)

        searchResults = String_slice(searchResults, '<div class="container content"', '</ul>')
        if (searchResults == ''):
            Logging('@@@ Update content search result failed2','Error')
            return 0
        # Logging(searchResults)

        Logging('┌────── pornav 제목 시작 ──────┐', 'Info')
        try:
            id= String_slice(media.title,'[',']').upper()
            nTitle = String_slice(searchResults, 'alt="', '"').replace(id,'').upper()
            nTitle = nTitle.replace('FC2 PPV ', '')
            nTitle = nTitle.replace(release_id.upper(), '')
            nTitle = nTitle.replace('TOKYO HOT','')
            metadata.original_title = nTitle
            self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        except:
            pass
        Logging('└────── pornav 제목 종료 ──────┘', 'Info')

        # 스튜디오=> 제조사
        Logging('┌──────  Studio Info start ──────┐','Info')
        try:
            sTemp = String_slice(searchResults, 'itemprop="author">', '<')
            nStudio = Search_Label(sTemp)
            if (sTemp == nStudio): nStudio = Papago_Trans(sTemp, 'ja')
            metadata.studio = nStudio #Papago_Trans(str(sTemp), 'ja')
            Logging('Studio: ' + nStudio,'Debug')
        except:
            Logging('@@@ Studio failed','Error')
        Logging('└──────  Studio Info end ──────┘','Info')

        # 감독
        Logging('┌──────  Director Info start ──────┐','Info')
        try:            
            # sTemp = String_slice(searchResults, '導演', '<p>')
            director_info = String_slice(searchResults, 'itemprop="director">', '<')
            Logging(director_info,'Debug')
            if (director_info <> ''):
                director_info_ko = Papago_Trans(director_info, 'ja')
                metadata.directors.clear()
                try:
                    meta_director = metadata.directors.new()
                    meta_director.name = director_info_ko
                except:
                    try:
                        metadata.directors.add(director_info_ko)
                        Logging(' Director: ' + director_info_ko,'Debug')
                    except:
                        pass
        except:
            Logging('@@@ Director failed','Error')
            pass
        Logging('└────── Director Info end ──────┘','Info')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        Logging('┌──────  Date Info start ──────┐','Info')
        try:
            if (searchResults.find('発売日') <> -1):
                nYear = String_slice(searchResults, 'time datetime="', '"')
                nYear = nYear.replace('/','-')
                nYearArray = nYear.split('-')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
                Logging(' Year: ' + nYear,'Debug')
        except:
            Logging('@@@ Date Failed','Error')
            pass
        Logging('└──────  Date Info end ──────┘','Info')

        # 줄거리
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[pornav]'
        Logging('┌──────  summary Info start ──────┐','Info')
        try:
            sTemp = String_slice(searchResults, 'class="tag-box tag-box-v2">', '</div>').replace('<p>','').replace('</p>','').replace('<br/>','').replace('\"','"')
            metadata.summary = metadata.summary + Papago_Trans(sTemp, 'ja')
            Logging('summary: ' + str(metadata.summary),'Debug')
        except:
            Logging('@@@ summary failed','Error')
        Logging('└────── summary Info end ──────┘','Info')

        # 국가
        metadata.countries.clear()
        metadata.countries.add('일본')

        # 장르
        Logging('┌──────  Genre Info start ──────┐','Info')
        try:            
            metadata.roles.clear()
            nGenreName = String_slice(searchResults, 'itemprop="keywords">', '<')
            Logging('########## Genre str: ' + nGenreName,'Debug')
            nGenreName_arr=nGenreName.split(',')
            j = len(nGenreName_arr)
            for i in range(0, j):
                role = metadata.roles.new()
                if (nGenreName_arr[i] == '' or nGenreName_arr[i] <> ' '):
                    nGenreName_ko = Search_Category(nGenreName_arr[i])
                    if (nGenreName_arr[i] == nGenreName_ko): nGenreName_ko = Papago_Trans(nGenreName_arr[i], 'ja').replace('.','')
                    metadata.genres.add(nGenreName_ko)
                    Logging(' Genre add: ' + nGenreName_ko,'Debug')            
        except:
            Logging('@@@ Genre failed','Error')
        Logging('└──────  Genre Info end ──────┘','Info')
		
        # 배우정보 => 이시키들이 배우 구분자가 스페이스인데 이름이 2글자면 이것도 스페이스로 나눠서 이름을 당췌 알 수 없음.. 통짜로 넣어야할듯
        Logging('┌──────  Actor Info start ──────┐','Info')
        metadata.roles.clear()
        # try:
        nFound = 'itemprop="actor">'
        if nFound in searchResults: # searchResults안에서 nFound 문자열 찾기. 찾으면 다음으로
            nStr = String_slice(searchResults, 'itemprop="actor">', '<')
            Logging(' 찾은 배우 정보: ' + nStr,'Debug')
            nActor = nStr.split(' ')
            for i in range(0, len(nActor)):
                if (nActor[i] == '' or nActor[i] <> ' '):
                    role = metadata.roles.new()
                    nActorInfo = Get_actor_info(nActor[i])  # 영문 배우명으로 AVDBS에서 먼저 찾는다
                    if (nActorInfo is not None):
                        Logging('### AVDBS에서 배우 정보 찾음  배우명: ' + nActorInfo[1] + ' 이미지 경로: ' + nActorInfo[0], 'Info')
                        role.photo = nActorInfo[0]
                        role.name = nActorInfo[1]
                    else:
                        Logging('@@@ AVDBS에서 배우 정보 검색 실패. @@@')
                        nActressesTr = Papago_Trans(nActor[i], 'ja')
                        role.photo = ''
                        role.name = nActressesTr
                        Logging('pornav 배우 정보로 저장합니다. 배우 이름: ' + nActressesTr, 'Debug')
        else:
            Logging('@@@ Actor info not found', 'Error')
        # except:
        #     Logging('@@@ Get actor info exception','Error')
        Logging('└──────  Actor Info end ──────┘','Info')

        # Posters
        Logging('┌──────  Poster Info start ──────┐','Info')
        try:
            posterURL_Small = String_slice(searchResults, '<img itemprop="image" src="', '"')
            Logging("small Poster URL / 포스터 주소 : " + posterURL_Small,'Debug')
            try:
                if(posterURL_Small <>''):
                    metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:	Logging(' Can not load Small Poster','Error')
        except:
            Logging('@@@ Poster Failed','Error')
        Logging('└──────  Poster Info end ──────┘','Info')
		
        #background images
        Logging('┌──────  Background Info start ──────┐','Info')
        try:
            nBgackgroundimg=Extract_imgurl(searchResults, 'preview-images">', '<div class','data-original')
            j = len(nBgackgroundimg)
            imgcnt = int(Prefs['img_cnt'])
            if (imgcnt <= j): j = imgcnt
            if (j <> -1):
                for i in range(0, j):
                    bgimg = nBgackgroundimg[i]
                    try:
                        if(bgimg <>''):
                            metadata.art[bgimg] = Proxy.Preview(
                            HTTP.Request(bgimg, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order=i + 1)
                    except:
                        Logging('@@@' + bgimg + ' Can not load','Error')
        except:
            Logging('@@@ Background Image failed','Error')
        Logging('└──────  Background Info end ──────┘','Info')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        Logging('┌──────  Series Info start ──────┐','Info')
        try:
            # Logging('######## series info')
            # Logging(sTemp)
            series_info = String_slice(searchResults, 'シリーズ： ', '<')
            # Logging(series_info)
            # Logging('SeriesInfo: ' + series_info)
            if (series_info <> ''):
                series_info_ko = Papago_Trans(series_info, 'ja')
                Logging(series_info_ko,'Debug')
                metadata.tagline = series_info_ko
            else:
                Logging('Series info not found','Error')
        except:
            Logging('@@@ Series failed','Error')
        Logging('└──────  Series Info end ──────┘','Info')
		
        # studio 컬렉션 생성
        try:
            if (str(Prefs['create_collection_studio']) == 'True'):
                if metadata.studio != None:
                    metadata.collections.add(metadata.studio)
                    Logging(' metadata.collections studio: ' + str(metadata.studio),'Debug')
            else:
                Logging('### Studio 컬렉션 생성 안함(설정 미체크) / Studio connection not create(prefrence not check ###','Info')
        except:
            Logging('@@@ Studio collection failed','Error')

        # series 컬렉션 생성
        try:
            if (str(Prefs['create_collection_series']) == 'True'):
                if metadata.tagline != None:
                    metadata.collections.add(metadata.tagline)
                    Logging(' metadata.collections series: ' + str(metadata.tagline),'Debug')
            else:
                Logging('### series 컬렉션 생성 안함(설정 미체크) Series connection not create(prefrence not check ###','Info')

            Logging('******* pornav 미디어 업데이트 완료/Media Update completed ****** ','Info')
        except:
            Logging('@@@ Series collection failed','Error')

        return 1

    def javdb_update(self, metadata, media, lang, nOrgID, ncroling):
        ################################################
        ################# javdb update #################
        ################################################
        Logging('****** 미디어 업데이트(상세항목) 시작 / javdb Media Update Start *******', 'Info')

        Logging('### 검색 사이트: javdb 일반 영상 / UpdateSite: javdb Video ###', 'Info')
        DETAIL_URL = 'https://javdb.com/v/'
        org_id = poombun_check(nOrgID, '')
        # release_id=poombun_split_num(org_id)

        try:
            searchResults = HTTP.Request(DETAIL_URL + metadata.id, headers={'Referer': 'http://www.google.com'},
                                         timeout=int(Prefs['timeout'])).content
        except:
            Logging('@@@ Update content load failed', 'Error')
            return 0

        # Logging(searchResults)
        nResult = searchResults.find('頁面未找到 (404)')  # 검색결과 확인
        if (nResult <> -1):
            Logging('@@@ Update content search result failed1', 'Error')
            return 0
        searchResults = String_slice(searchResults, 'title is-4', '</article>')
        if (searchResults == ''):
            Logging('@@@ Update content search result failed2', 'Error')
            return 0
        # Logging(searchResults)

        Logging('┌────── javdb 제목 시작 ──────┐', 'Info')
        id = String_slice(media.title, '[', ']').upper()
        nTitle = String_slice(searchResults, '<strong>', '<').replace(id, '').replace('\"','"')
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('└────── javdb 제목 종료 ──────┘', 'Info')

        # 스튜디오=> 제조사
        Logging('┌──────  javdb Studio Info start ──────┐', 'Info')
        try:
            sTemp = String_slice(searchResults, '片商', '</div>')
            sTemp = String_slice(sTemp, 'a href', '</span>')
            sTemp = String_slice(sTemp, '">', '</a')
            nStudio = Search_Label(sTemp)
            if (sTemp == nStudio): nStudio = Papago_Trans(sTemp, 'ja')
            metadata.studio = nStudio #Papago_Trans(str(metadata.studio), 'ja')
            Logging('Studio: ' + str(metadata.studio), 'Debug')
        except:
            Logging('@@@ Studio failed', 'Error')
            pass
        Logging('└──────  javdb Studio Info end ──────┘', 'Info')

        # 감독
        Logging('┌──────  javdb Director Info start ──────┐', 'Info')
        try:
            director_info = Extract_str(searchResults, '導演', '</div>')
            if (director_info is not None):
                director_info_ko = Papago_Trans(director_info[0], 'ja')
                Logging('Director: ' + director_info_ko, 'Debug')
                metadata.directors.clear()
                try:
                    meta_director = metadata.directors.new()
                    meta_director.name = director_info_ko
                except:
                    try:
                        metadata.directors.add(director_info_ko)
                    except:
                        pass
        except:
            Logging('@@@ Director failed', 'Error')
            pass
        Logging('└──────  javdb Director Info end ──────┘', 'Info')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        Logging('┌──────  javdb Date Info start ──────┐', 'Info')
        try:
            if '日期' in searchResults:
                nYear = String_slice(searchResults, '日期', '</div>')
                nYear = String_slice(nYear, 'value">', '<')
                nYearArray = nYear.split('-')
                metadata.year = int(nYearArray[0])# 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')# 상세항목의 '원출처' 일자
                Logging('nYear: ' + nYear,'Debug')
        except:
            Logging('@@@ Date Failed', 'Error')
            pass
        Logging('└──────  javdb Date Info start ──────┘', 'Info')

        # 줄거리(javdb는 줄거리 없음)
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[javdb]'

        # 국가
        metadata.countries.clear()
        metadata.countries.add('일본')

        # 장르
        Logging('┌──────  javdb Genre Info start ──────┐', 'Info')
        try:
            metadata.roles.clear()
            nGenreName = Extract_str(searchResults, '類別', '</div>')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                nGenreName_ko = Search_Category(nGenreName[i])
                if (nGenreName[i] == nGenreName_ko): nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.', '')
                metadata.genres.add(nGenreName_ko)
        except:
            Logging('@@@ Genre failed', 'Error')
            pass
        Logging('└──────  javdb Genre Info end ──────┘', 'Info')

        # 배우정보
        Logging('┌──────  javdb Actor Info start ──────┐', 'Info')
        metadata.roles.clear()
        nActorName = Extract_str(searchResults, '演員', '</div>')
        Logging(nActorName, 'Debug')
        if (nActorName is not None):
            j = len(nActorName)
            for i in range(0, j):
                Logging('배열 0: ' + nActorName[0], 'Debug')
                role = metadata.roles.new()
                nTemp = nActorName[i]
                if (nTemp.find('(') <> -1): nTemp = nTemp[0:nTemp.find('(')]
                nActorInfo = Get_actor_info(nTemp)
                if (nActorInfo is not None):
                    role.photo = nActorInfo[0]
                    role.name = Papago_Trans(nActorInfo[1],'ja')
                    Logging('배우 이미지 주소: ' + nActorInfo[0] + ' 배우이름: ' + nActorInfo[1], 'Debug')
                else:
                    role.name = nActorName
                    Logging('배우 이미지 주소: 검색실패' + ' 배우이름: ' + nActorName[i], 'Debug')
        Logging('└────── javdb Actor Info end ──────┘', 'Info')

        # Posters
        Logging('┌──────  javdb Poster Info start ──────┐', 'Info')
        try:
            nmid = metadata.id[0:2].lower()
            posterURL_Small = 'https://jdbimgs.com/thumbs/' + nmid + '/' +  metadata.id + '.jpg'
            # posterURL_Large = 'https://jdbimgs.com/covers/' + nmid + '/' +  metadata.id.replace('/v/','') + '.jpg'
            # Logging("small Poster URL / 포스터 주소 : " + posterURL_Small, 'Debug')
            try:
                if (posterURL_Small <> '' or posterURL_Small <> '#preview-video'):
                    metadata.posters[posterURL_Small] = Proxy.Preview(
                        HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:
                Logging(' Can not load Small Poster', 'Error')
        except:
            Logging('@@@ Poster Failed', 'Error')
            pass
        Logging('└──────  javdb Poster Info end ──────┘', 'Info')

        # background images
        Logging('┌──────  javdb Background Info start ──────┐', 'Info')
        try:
            nBgackgroundimg = Extract_imgurl(searchResults, 'tile-images preview-images', '</article>', 'href')
            j = len(nBgackgroundimg)
            imgcnt = int(Prefs['img_cnt'])
            if (imgcnt <= j): j = imgcnt
            if (j <> -1):
                for i in range(0, j):
                    bgimg = nBgackgroundimg[i]
                    try:
                        if (bgimg <> ''):
                            metadata.art[bgimg] = Proxy.Preview(
                                HTTP.Request(bgimg, headers={'Referer': 'http://www.google.com'},
                                             timeout=int(Prefs['timeout'])).content, sort_order=i + 1)
                    except:
                        Logging('@@@' + bgimg + ' Can not load', 'Error')
        except:
            Logging('@@@ Background Image failed', 'Error')
            pass
        Logging('└──────  javdb Background Info end ──────┘', 'Info')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        Logging('┌──────  javdb Series Info start ──────┐', 'Info')
        try:
            series_info = Extract_str(searchResults, '系列', '</div>')
            # Logging(series_info,'Debug')
            # Logging('SeriesInfo: ' + series_info)
            if (series_info is not None):
                if (series_info[0] <> '----'):
                    series_info_ko = Papago_Trans(series_info[0], 'ja')
                    Logging(series_info_ko, 'Debug')
                    metadata.tagline = series_info_ko
            else:
                Logging('Series info not found', 'Error')
        except:
            Logging('@@@ Series failed', 'Error')
            pass
        Logging('└──────  javdb Series Info end ──────┘', 'Info')

        # studio 컬렉션 생성
        try:
            if (str(Prefs['create_collection_studio']) == 'True'):
                if metadata.studio != None:
                    metadata.collections.add(metadata.studio)
                    Logging(' metadata.collections studio: ' + str(metadata.studio), 'Debug')
            else:
                Logging('### Studio 컬렉션 생성 안함(설정 미체크) / Studio connection not create(prefrence not check ###', 'Info')
        except:
            Logging('@@@ Studio collection failed', 'Error')

        # series 컬렉션 생성
        try:
            if (str(Prefs['create_collection_series']) == 'True'):
                if metadata.tagline != None:
                    metadata.collections.add(metadata.tagline)
                    Logging(' metadata.collections series: ' + str(metadata.tagline), 'Debug')
            else:
                Logging('### series 컬렉션 생성 안함(설정 미체크) Series connection not create(prefrence not check ###', 'Info')

            Logging('******* javdb 미디어 업데이트 완료/Media Update completed ****** ', 'Info')

        except:
            Logging('@@@ Series collection failed', 'Error')

        return 1

    def javlibrary_update(self, metadata, media, lang, nOrgID,ncroling):

        # nIDs[0]: 검색용 품번  nIDs[1]: 검색된 사이트(DMM, R18)   nIDs[2]: 아마추어(C)or일반(A)  nIDs[3]: 오리지널 품번(OAE-101)
        Logging('****** 미디어 업데이트(상세항목) 시작 / javlibrary Media Update Start *******','Info')
        # Logging("Update ID:   " + str(metadata.id) +  ' Original ID: ' + org_id)

        #####################################################
        ################# javlibrary update #################
        #####################################################
        Logging('### 검색 사이트: javlibrary 일반 영상 / UpdateSite: javlibrary Video ###','Info')
        DETAIL_URL = 'http://www.javlibrary.com/ja/?v='
        org_id=poombun_check(nOrgID,'')
        # release_id=poombun_split_num(org_id)

        try:
            searchResults = HTTP.Request(DETAIL_URL + metadata.id , headers = {'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content
        except:
            Logging('@@@ Update content load failed','Error')
            return 0

        # Logging(searchResults)
        nResult = searchResults.find('404 Not Found')  # 검색결과 확인
        if (nResult <> -1):
            Logging('@@@ Update content search result failed1','Error')
            return 0
        # searchResults = String_slice(searchResults, 'title is-4', '</article>')
        # if (searchResults == ''):
        #     Logging('@@@ Update content search result failed2','Error')
        #     return 0
        # Logging(searchResults)

        Logging('┌────── javlibrary 제목 시작 ──────┐', 'Info')
        id= String_slice(media.title,'[',']').upper()
        nTitle = String_slice(searchResults, "rel='bookmark' >", '</a>').replace(id,'')
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('└────── javlibrary 제목 종료 ──────┘', 'Info')

        # 스튜디오=> 제조사
        try:
            Logging('┌──────  javlibrary Maker Info start ──────┐','Info')
            sTemp = String_slice(searchResults, 'メーカー', '</tr>')
            sTemp = String_slice(sTemp, 'rel="tag">', '</a>')
            nStudio = Search_Label(sTemp)
            if (sTemp == nStudio): nStudio = Papago_Trans(sTemp, 'ja')
            metadata.studio = nStudio
            # metadata.studio = Papago_Trans(str(metadata.studio), 'ja')
            Logging('Maker: ' + str(metadata.studio),'Debug')
            Logging('└──────  javlibrary Maker Info end ──────┘','Info')
        except:
            Logging('@@@ Studio failed','Error')

        # 감독
        try:
            Logging('┌──────  javlibrary Director Info start ──────┐','Info')
            # sTemp = String_slice(searchResults, '導演', '<p>')
            sTemp = Extract_str(searchResults, '監督', '</tr>')
            director_info = sTemp
            Logging('Director: ','Info')
            Logging(director_info,'Info')
            if (director_info != ''):
                director_info_ko = Papago_Trans(director_info[0], 'ja')
                Logging('Director: ' + director_info_ko,'Debug')
                metadata.directors.clear()
                try:
                    meta_director = metadata.directors.new()
                    meta_director.name = director_info_ko
                except:
                    try:
                        metadata.directors.add(director_info_ko)
                    except:
                        pass
            Logging('└──────  javlibrary Director Info end ──────┘','Info')
        except:
            Logging('@@@ Director failed','Error')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        try:
            Logging('┌──────  javlibrary Date Info start ──────┐','Info')
            if (searchResults.find('発売日') <> -1):
                nYear = String_slice(searchResults, '発売日', '</tr>')
                nYear = String_slice(nYear, '<td class="text">', '</td>')
                Logging(nYear,'Debug')
                nYearArray = nYear.split('-')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
            Logging('└──────  javlibrary Date Info end ──────┘','Info')
        except:
            Logging('@@@ Date Failed','Error')

        # 줄거리(javlibrary는 줄거리 없음)
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[javlibrary]'

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 장르
        try:
            Logging('┌──────  javlibrary Genre Info start ──────┐','Info')
            metadata.roles.clear()
            nGenreName = Extract_str(searchResults, 'ジャンル', '</tr>')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                nGenreName_ko = Search_Category(nGenreName[i])
                if (nGenreName[i] == nGenreName_ko): nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.', '')
                # nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.','')
                # Logging(nGenreName[i],'Debug')
                # Logging(nGenreName_ko,'Debug')
                metadata.genres.add(nGenreName_ko)
            Logging('└──────  javlibrary Genre Info end ──────┘','Info')
        except:
            Logging('@@@ Genre failed','Error')

        # 배우정보
        Logging('┌──────  javlibrary Actor Info start ──────┐','Info')
        metadata.roles.clear()
        nActorName = Extract_str(searchResults,'出演者', '</tr>')
        if (nActorName is not None):
            j=len(nActorName)
            for i in range(0,j):
                role = metadata.roles.new()
                nTemp = nActorName[i]
                if (nTemp.find('(') <> -1) : nTemp=nTemp[0:nTemp.find('(')]
                nActorInfo = Get_actor_info(nTemp)
                if (nActorInfo is not None):
                    role.photo = nActorInfo[0]
                    role.name = nActorInfo[1]
                    Logging('배우 이미지 주소: ' + nActorInfo[0] + ' 배우이름: ' + nActorInfo[1], 'Debug')
                else:
                    role.name = nActorName
                    Logging('배우 이미지 주소: 검색실패' + ' 배우이름: ' + nActorName[i], 'Debug')
        Logging('└──────  javlibrary Actor Info end ──────┘','Info')

        # Posters
        Logging('┌──────  javlibrary Poster Info start ──────┐','Info')
        try:
            posterURL_Small = String_slice(searchResults, 'video_jacket_img" src="', '"').replace("pl.","ps.")
            if (posterURL_Small.find('http:') <> -1): posterURL_Small = 'http:' + posterURL_Small
            # posterURL_Small = Extract_imgurl(searchResults, '<div class="previewthumbs"', '</div>', 'src')
            Logging("small Poster URL / 포스터 주소 : " + posterURL_Small,'Debug')
            try:
                if(posterURL_Small <>'' or posterURL_Small <> '#preview-video'):
                    metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:	Logging(' Can not load Small Poster','Error')
            Logging('└──────  javlibrary Poster Info end ──────┘','Info')
        except:
            Logging('@@@ Poster Failed','Error')

        #background images
        try:
            Logging('┌──────  javlibrary Background Info start ──────┐','Info')
            nBgackgroundimg=Extract_imgurl(searchResults, '<div class="previewthumbs"', '</div>','src')
            j = len(nBgackgroundimg)
            if (j <> -1):
                imgcnt = int(Prefs['img_cnt'])
                Logging('설정파일에 설정된 배경파일 받을 이미지 개수: ','Debug')
                Logging(imgcnt,'Debug')
                if (imgcnt <= j):
                    j = imgcnt
                    if (nBgackgroundimg[0] == '../img/player.gif'): j = imgcnt+1 #첫 이미지가 불필요한 이미지면 두번째 부터 받기위해 1 추가
                Logging(j, 'Debug')
                for i in range(0, j):
                    bgimg = nBgackgroundimg[i]
                    Logging('배경화면 이미지 주소: ','Debug')
                    Logging(bgimg,'Debug')
                    try:
                        if(bgimg <>''):
                            metadata.art[bgimg] = Proxy.Preview(
                            HTTP.Request(bgimg, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order=i + 1)
                    except:
                        Logging('@@@' + bgimg + ' Can not load','Error')

            Logging('└──────  javlibrary Background Info end ──────┘','Info')
        except:
            Logging('@@@ Background Image failed','Error')

        # studio 컬렉션 생성
        try:
            if (str(Prefs['create_collection_studio']) == 'True'):
                if metadata.studio != None:
                    metadata.collections.add(metadata.studio)
                    Logging(' metadata.collections studio: ' + str(metadata.studio), 'Debug')
            else:
                Logging('### Studio 컬렉션 생성 안함(설정 미체크) / Studio connection not create(prefrence not check ###','Info')
        except:
            Logging('@@@ Studio collection failed','Error')

        # series 컬렉션 생성
        try:
            if (str(Prefs['create_collection_series']) == 'True'):
                if metadata.tagline != None:
                    metadata.collections.add(metadata.tagline)
                    Logging(' metadata.collections series: ' + str(metadata.tagline),'Debug')
            else:
                Logging('### series 컬렉션 생성 안함(설정 미체크) Series connection not create(prefrence not check ###','Info')

            Logging('******* javlibrary 미디어 업데이트 완료/Media Update completed ****** ','Info')

        except:
            Logging('@@@ Series collection failed','Error')

        return 1
