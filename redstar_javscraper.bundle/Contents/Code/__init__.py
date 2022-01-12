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

HDR_javdb = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8',
        'referer': 'www.google.com',
       'Connection': 'keep-alive'}

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
        Logging('papago Exception','Error')
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

# def ExtractFromHtml(startstr,endstr,txt):
#  # startstr ~ endstr 사이의 문자열 추출
#  # <tr><b>가나다</b></tr> 일때 문자열만 추출함
#  # 값이 없으면 공백 리턴 ''
#   try:
#     extractstr = re.search(startstr + '(.+?)' + endstr, txt).group(1)
#     sTemp = re.sub('<.+?>', '', extractstr, 0, re.I|re.S)
#     return sTemp
#   except AttributeError:
#     return ''

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
        SEARCH_URL = 'https://javdb.com/search?q='
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

        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id).content
        except:
            Logging( 'javdb search exception','Error')
            return 0

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
        sTemp = Papago_Trans(sTemp, 'ja')
        metadata.studio = sTemp
        Logging(" dmm 스튜디오 정보: " + sTemp,'Info')
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
        # Logging('┌────── dmm 일자 시작 ──────┐', 'Info')
        # try:
        #     if (searchResults.find('発売日') <> -1):
        #         sTemp = String_slice(searchResults, '>配信', '</tr>')
        #         # sTemp = ExtractFromHtml('発売日：', '</tr>',searchResults)
        #     elif (searchResults.find('商品発売日') <> -1):
        #         sTemp = String_slice(searchResults, '>商品', '</tr>')
        #         # sTemp = ExtractFromHtml('>商品', '</tr>',searchResults)
        #     elif (searchResults.find('配信開始日') <> -1):
        #         sTemp = String_slice(searchResults, '>配信', '</tr>')
        #         # sTemp = ExtractFromHtml('>配信', '</tr>',searchResults)
        #     else:
        #         sTemp = ''
        #     if (sTemp <> ''):
        #         nYear = String_slice(sTemp, '<td>', '</td>')
        #         nYear=sTemp
        #         nYearArray = nYear.split('/')
        #         # 미리보기 항목의 이미지 아래 표시되는 년도
        #         metadata.year = int(nYearArray[0])
        #         # 상세항목의 '원출처' 일자
        #         nYear = nYear.replace('/', '-')
        #         metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
        #         Logging('## 저장할 일자: ' + nYear)
        # except:
        #     pass
        # Logging('└────── dmm 일자 종료 ──────┘', 'Info')

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
            # nGenreName = ExtractFromHtml('ジャンル：', '</tr>',searchResults)
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                # nGenreName[i]=nGenreName[i].replace('.','')
                nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.', '')
                # Logging(nGenreName[i])
                # Logging(nGenreName_ko)
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
                    Logging(value,'Info')
                    nStudio = value
                    nStudioTr = Papago_Trans(nStudio, 'en')
                    metadata.studio = nStudioTr  # 스튜디오 정보
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
                    nGenreTr = Papago_Trans(nGenre, 'en')
                    metadata.genres.add(nGenreTr)  # 스튜디오 정보
                    Logging('### 장르 정보(ORG): ' + nGenre + ' 번역: ' + nGenreTr, 'Info')
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
            metadata.studio = String_slice(sTemp, '">', '</a')
            metadata.studio = Papago_Trans(str(metadata.studio), 'ja')
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
                # nGenreName[i] = nGenreName[i].replace('.', '')
                nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.','')
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
            metadata.studio = Papago_Trans(str(sTemp), 'ja')
            Logging('Studio: ' + str(metadata.studio),'Debug')
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
                    # nGenreName_arr[i] = nGenreName_arr[i].replace('.', '')
                    nGenreName_ko = Papago_Trans(nGenreName_arr[i], 'ja').replace('.','')
                    # Logging(nGenreName[i])
                    # Logging(nGenreName_ko)
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
            metadata.studio = String_slice(sTemp, '">', '</a')
            metadata.studio = Papago_Trans(str(metadata.studio), 'ja')
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
                # nGenreName[i] = nGenreName[i].replace('.', '')
                nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.', '')
                # Logging(nGenreName[i], 'Debug')
                # Logging(nGenreName_ko, 'Debug')
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
            Logging('┌──────  Maker Info start ──────┐','Info')
            sTemp = String_slice(searchResults, 'メーカー', '</tr>')
            sTemp = String_slice(sTemp, 'rel="tag">', '</a>')
            metadata.studio = sTemp
            metadata.studio = Papago_Trans(str(metadata.studio), 'ja')
            Logging('Maker: ' + str(metadata.studio),'Debug')
            Logging('└──────  Maker Info end ──────┘','Info')
        except:
            Logging('@@@ Studio failed','Error')

        # 감독
        try:
            Logging('┌──────  Director Info start ──────┐','Info')
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
            Logging('└──────  Director Info end ──────┘','Info')
        except:
            Logging('@@@ Director failed','Error')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        try:
            Logging('┌──────  Date Info start ──────┐','Info')
            if (searchResults.find('発売日') <> -1):
                nYear = String_slice(searchResults, '発売日', '</tr>')
                nYear = String_slice(nYear, '<td class="text">', '</td>')
                Logging(nYear,'Debug')
                nYearArray = nYear.split('-')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
            Logging('└──────  Date Info end ──────┘','Info')
        except:
            Logging('@@@ Date Failed','Error')

        # 줄거리(javlibrary는 줄거리 없음)
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[javlibrary]'

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 장르
        try:
            Logging('┌──────  Genre Info start ──────┐','Info')
            metadata.roles.clear()
            nGenreName = Extract_str(searchResults, 'ジャンル', '</tr>')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                # nGenreName[i] = nGenreName[i].replace('.', '')
                nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.','')
                Logging(nGenreName[i],'Debug')
                Logging(nGenreName_ko,'Debug')
                metadata.genres.add(nGenreName_ko)
            Logging('└──────  Genre Info end ──────┘','Info')
        except:
            Logging('@@@ Genre failed','Error')

        # 배우정보
        Logging('┌──────  Actor Info end ──────┐','Info')
        metadata.roles.clear()
        nActorName=Extract_str(searchResults,'出演者', '</tr>')
        # Logging('===================')
        Logging(nActorName,'Debug')
        if (nActorName is not None):
            j=len(nActorName)
            for i in range(0,j):
                role = metadata.roles.new()
                # if (nActorName[i].find('(') > -1): nActorName = nActorName[i][0:nActorName[i].find('(')]
                nTemp=nActorName[i]
                if (nTemp.find('(') <> -1) : nTemp=nTemp[0:nTemp.find('(')]
                nActorInfo = Get_actor_info(nTemp)
                if (nActorInfo is not None):
                    role.photo = nActorInfo[0]
                    role.name = nActorInfo[1]
                    Logging('배우이미지주소: ' + nActorInfo[0] + ' 배우이름: ' + nActorInfo[1], 'Debug')
                else:
                    role.name = nActorName
                    Logging('배우이미지주소: 검색실패' + ' 배우이름: ' + nActorName[i], 'Debug')
        Logging('└──────  Actor Info end ──────┘','Info')

        # Posters
        Logging('┌──────  Poster Info start ──────┐','Info')
        try:
            posterURL_Small = String_slice(searchResults, 'video_jacket_img" src="', '"').replace("pl.","ps.")
            posterURL_Small = 'http:' + posterURL_Small
            # posterURL_Small = Extract_imgurl(searchResults, '<div class="previewthumbs"', '</div>', 'src')
            Logging("small Poster URL / 포스터 주소 : " + posterURL_Small,'Debug')
            try:
                if(posterURL_Small <>'' or posterURL_Small <> '#preview-video'):
                    metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:	Logging(' Can not load Small Poster','Error')
            Logging('└──────  Poster Info end ──────┘','Info')
        except:
            Logging('@@@ Poster Failed','Error')

        #background images
        try:
            Logging('┌──────  Background Info start ──────┐','Info')
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

            Logging('└──────  Background Info end ──────┘','Info')
        except:
            Logging('@@@ Background Image failed','Error')

        # # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        # try:
        #     Logging('=======  Series Info start =========','Info')
        #     # Logging('######## series info')
        #     # Logging(sTemp)
        #     series_info = Extract_str(searchResults, '系列', '</div>')
        #     # Logging(series_info,'Debug')
        #     # Logging('SeriesInfo: ' + series_info)
        #     if (series_info is not None):
        #         if (series_info[0] <> '----'):
        #             series_info_ko = Papago_Trans(series_info[0], 'ja')
        #             Logging(series_info_ko,'Debug')
        #             metadata.tagline = series_info_ko
        #     else:
        #         Logging('Series info not found','Error')
        #     Logging('=======  Series Info end =========','Info')
        # except:
        #     Logging('@@@ Series failed','Error')

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
