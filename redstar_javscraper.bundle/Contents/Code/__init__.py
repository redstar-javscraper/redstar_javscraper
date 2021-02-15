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

def Papago_Trans(txt,lang='en'):
    # 번역언어:	# ko	한국어	# en	영어	# ja	일본어	# zh-CN	중국어 간체	# zh-TW	중국어 번체	# vi	베트남어
    # id	인도네시아어	# th	태국어	# de	독일어	# ru	러시아어	# es	스페인어	# it	이탈리아어	# fr	프랑스어

    Logging('===========> 파파고 설정(PapagoUSE): ' + str(Prefs['papago_use']),'Info')
    Logging('===========> 파파고 키값(PapagoKey): ' + str(Prefs['papagokey']), 'Info')
    if (str(Prefs['papago_use']) == 'False'):
        Logging('### 파파고 사용 안함 체크됨(Papago Not use checked) ###','Debug')
        return txt
    if (str(Prefs['papagokey']) == 'None' ):
        Logging('### 파파고 키가 빈 값임(Papago key empty) ###','Debug')
        return txt

    try:
        # 환경변수에 입력한 파파고 키를 랜덤으로 추출해 사용함
        # 환경변수에는 key,secret key2,secret2 .... 으로 입력되어야 함
        Logging('### PapagoKEY : ' + str(Prefs['papagokey']), 'Info')
        client_key=str(Prefs['papagokey'])
        papagokey = client_key.split(' ')
        get_papagokey = random.choice(papagokey)
        client_key_array = get_papagokey.split(',')
        client_id = client_key_array[0]
        client_secret = client_key_array[1]
        Logging('### ID: ' + str(client_id) + ' Secret: ' + str(client_secret),'Debug')

        source_lang =  lang
        target_lang = "ko"
        encText = txt
        Logging('### Trans Original TXT: ' + encText, 'Debug')
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
            Logging('#### Papago Trans Result : ' + str(response_body),'Debug')
            Logging('####  Trans Result Cut : ' + str(nResult),'Debug')
            return nResult
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
                # Logging('Before Cut: ' + sTemp[i],'Debug')
                nCut=String_slice(sTemp[i],'>','<')
                nResult.append(nCut)
                Logging('After Cut: ' + nCut, 'Debug')

            return nResult
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
    # hentaku	홈페이지에서	배우정보를	가져옴(DMM의	경우만.r18은	페이지에	배우	정보	나옴)
    if (nEntity == ''):
        return
    Logging('nEntity(Search Actor String) : ' + nEntity,'Debug')
    Search_URL = 'https://hentaku.co/search/'
    post_values = {'search_str': nEntity}
    searchResults = HTTP.Request(Search_URL, values=post_values, timeout=int(Prefs['timeout'])).content
    Logging('############# Actor Info from Hentaku ##############','Info')
    # Logging(searchResults)
    nResult=[]
    if (searchResults == '' or searchResults.find('class="avstar_wrap"') == -1):
        # 리턴값이 없을 경우
        nResult.append('') #image url
        nResult.append(Papago_Trans(nEntity,'ja')) # kor name
        nResult.append(Papago_Trans(nEntity,'en')) # eng name
        Logging('Actor Return not found','Error')
    else:
        # 검색결과 존재시
        nStr = String_slice(searchResults, '<s_article_rep>', '</s_article_rep>')
        # Logging(nStr)
        nimgurl = Extract_imgurl(nStr, 'avstar_wrap', '</div>')
        Logging('Actor image: ' + nimgurl[0],'Debug')
        if (nimgurl is None):
            nResult[0]=''
        else:
            nResult.append(nimgurl[0])
        nResult.append(String_slice(nStr, 'px;">', ' /'))
        nResult.append(String_slice(nStr, ' / ', ' /'))
        Logging('Actor info  #img:' + nResult[0] + '  Name_kor: ' + nResult[1] + '  Name_eng: '+nResult[2] ,'Debug')
    return nResult

def Get_search_url(SEARCH_URL, txt, reqMode='GET'):
    con = ''
    try:
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
            req.add_header('age_check_done', '1')
            Logging('Header adding', 'Info')
        try:
            con = urllib2.urlopen(req,timeout=int(Prefs['timeout']))
            Logging('URL Open Success', 'Info')
        except urllib2.URLError as e:
            Logging(e.reason,'Debug')
        web_byte = con.read()
        # Logging('webbyte completed')
        webpage = web_byte.decode('utf-8')
        # Logging('webpage : ' + str(webpage), 'Debug')
        Logging("검색결과 가져옴(Got search result)", 'Info')
        return webpage
    except:
        Logging("검색결과 Search Result: exception", 'Error')
    return ''

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

def Logging(txt, Level):
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
        Logging('option check javdb: ' + str(Prefs['javdb_use']),'Info')

        amateur = True
        nSearchstr=media.name.upper()
        if (nSearchstr.find('CARIB') == -1):
            if (nSearchstr.find('FC2PPV') == -1):
                if( nSearchstr.find('TOKYOHOT') == -1):
                    amateur=False
                    Logging('Amateur option is False','Debug')

        if (str(Prefs['dmm_use']) == 'True' and amateur == False):
            nResult=self.dmm_search(results, media, lang)
            # Logging('dmm result: ' + str(nResult), 'Debug')
        if (str(Prefs['r18_use']) == 'True' and nResult == 0 and amateur == False):
            nResult=self.r18_search(results, media, lang)
            # Logging('r18 result: ' + str(nResult), 'Debug')
        if (str(Prefs['javbus_use']) == 'True' and nResult == 0 and amateur == False):
            nResult=self.javbus_search(results, media, lang)
            # Logging('jabus result: '  + str(nResult), 'Debug')
        if (str(Prefs['pornav_use']) == 'True' and nResult == 0):
            nResult=self.pornav_search(results, media, lang)
            # Logging('pornav result: '  + str(nResult), 'Debug')
        if (str(Prefs['javdb_use']) == 'True' and nResult == 0):
            nResult=self.javdb_search(results, media, lang)
            # Logging('javdb result: '  + str(nResult),'Debug')
        if (nResult == 0):
            Logging('@@@ Search failed on all sites.', 'Error')
        Logging('####### End search #########', 'Info')

    def update(self, metadata, media, lang):
        Logging("####### Start Update #########", 'Info')

        nTitle=media.title
        Logging('MediaTitle: ' + nTitle, 'Debug')

        # name = '[' + id + '] ' + title + ' §' + 'DMMa' + '§' + uncResult + '§' + id+ '§'+Y/N/C
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

        if (str(Prefs['dmm_use']) == 'True' and ((nSite == 'DMMa') or (nSite == 'DMMo') or (nSite == ' '))):
            nResult=self.dmm_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('dmm result: ' + str(nResult),'Debug')
        elif (str(Prefs['r18_use']) == 'True' and ((nSite == 'r18')or (nSite == ' '))):
            nResult=self.r18_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('r18 result: ' + str(nResult),'Debug')
        elif (str(Prefs['javbus_use']) == 'True' and ((nSite == 'javbus')or (nSite == ' '))):
            nResult=self.javbus_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('jabus result: ' + str(nResult), 'Debug')
        elif (str(Prefs['pornav_use']) == 'True' and ((nSite == 'pornav')or (nSite == ' '))):
            nResult=self.pornav_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('pornav result: ' + str(nResult), 'Debug')
        elif (str(Prefs['javdb_use']) == 'True' and ((nSite == 'javdb')or (nSite == ' '))):
            nResult=self.javdb_update(metadata, media, lang, nOrgID,ncroling)
            # Logging('javdb result: ' + str(nResult), 'Debug')
        Logging("####### End update #########", 'Info')

    def get_fileinfo(self,media):
        # 파일에서 정보를 읽어 품번, 제목을 리턴함
        Logging('### 파일에서 정보읽기 시작 ###', 'Debug')
        n_ret=[]
        filename = urllib.unquote(media.filename).decode('utf8')
        filename = os.path.splitext(filename)[0]
        filename = os.path.basename(filename).strip()
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
            return n_ret
        else:
            return None

    def dmm_search(self,results,media,lang):
        ##############################
        ###### dmm video 검색  ########
        ##############################

        Logging('##### Start dmm video search #####','Info')
        # SEARCH_URL = 'https://www.dmm.co.jp/age_check/=/declared=yes/?rurl='
        # SEARCH_URL = SEARCH_URL + 'http%3A%2F%2Fwww.dmm.co.jp%2Fdigital%2Fvideoa%2F-%2Flist%2Fsearch%2F%3D%2F%3Fsearchstr%3D'
        SEARCH_URL = 'https://www.dmm.co.jp/digital/videoa/-/list/search/=/?searchstr='
        Logging('Media input title: ' + media.name,'Debug')

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
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
                searchResults=String_slice(searchResults,'<ul id="list">','(function()')
                content_id = String_slice(searchResults,'content_id":"','"')
                Logging(' Content_id: ' + content_id, 'Debug')
                id = org_id
                searchtype='DMMo'
                title = String_slice(searchResults, 'alt="', '"')
                if (Prefs['filenametotitle'] == False or title_fromfile == ''):
                    titletype = 'N'
                else:
                    title=title_fromfile.strip()
                    titletype='Y'
                name= '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id +'§' + titletype
                score=100
                results.Append(MetadataSearchResult(id=content_id, name=name, score=score, lang=lang))
                Logging('##Search Update Result ==> id: ' + content_id + ' name: ' + name + ' score : ' + str(score), 'Debug')
                return 1
            else:
                Logging('DMM Video result Not found', 'Error')
        else:
            Logging('DMM Video result not found1', 'Error')

        ###### dmm Amateur 검색  ########
        SEARCH_URL = 'https://www.dmm.co.jp/digital/videoc/-/list/search/=/?searchstr='
        release_id = org_id.replace('-','')
        Logging("org_id ID:    " + str(org_id) + " release_id: " + str(release_id), 'Debug')
        Logging('******* DMM Amateur 검색 시작(Media search start) ****** ', 'Info')
        searchResults = Get_search_url(SEARCH_URL, release_id)
        # Logging(searchResults)
        if (searchResults <> ''):
            nResult = searchResults.find('id="list"') #검색 결과 있을때 이 텍스트가 있음
            Logging(nResult,'Debug')
            if (nResult <> -1):
                Logging('##### dmm Amateur Result Found #####', 'Info')
                if (uncensored_check(media.filename) == 1):
                    uncResult = 'U'
                else:
                    uncResult = 'C'
                Logging('### UNC:' + uncResult, 'Debug')
                searchResults=String_slice(searchResults,'<ul id="list">','(function()')
                content_id = String_slice(searchResults,'content_id":"','"')
                Logging('amature ContentID: ' + content_id, 'Debug')
                id= org_id
                searchtype='DMMa'
                title = String_slice(searchResults, 'class="txt">', '<')
                if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                    title=title_fromfile
                    titletype='Y'
                else:
                    titletype = 'N'
                name= '[' + id + '] ' + title + ' §' + searchtype + '§' + uncResult + '§' + id +'§' + titletype
                score=100
                results.Append(MetadataSearchResult(id=content_id, name=name, score=score, lang=lang))
                return 1
        else:
            Logging('DMM Amateur result Not found', 'Error')
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
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()
        release_id = org_id
        
        Logging('******* r18 미디어 검색 시작(r18 Media search start) ****** ','Info')
        Logging("Release ID:    " + str(release_id) + ' org_id: ' + org_id,'Debug')
        try:
            encodedId = urllib2.quote(release_id)
            url = SEARCH_URL + encodedId
            Logging('다음의 주소로 검색합니다: ' + url , 'Debug')
            searchResults = HTML.ElementFromURL(url, timeout=int(Prefs['timeout']))
            Logging("검색결과 가져옴(Got search result)",'Info')
        except:
            Logging('@@@ r18 검색 실패','Error')
            return 0
        if (searchResults <> None):
            Logging('##### r18 Result Found #####', 'Info')
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
                if title.startswith("SALE"): title = title[4:]
                searchtype='r18'
                if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                    title=title_fromfile
                    titletype='Y'
                else:
                    titletype = 'N'
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
        # Logging(searchResults)
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
                title = String_slice(searchResults, 'title="', '">')
                searchtype='javbus'
                if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                    title=title_fromfile
                    titletype='Y'
                else:
                    titletype = 'N'
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
        SEARCH_URL = 'http://pornav.co/jp/search?q='

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()
        release_id=poombun_split_num(org_id) #아마추어 작품의 경우 품번 숫자만 필요해서 숫자만 추리는 함수 호출

        Logging("Release ID:    " + str(release_id) + ' # org_id: ' + org_id,'Debug')
        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id).content  # post로 보낼경우 value={'aaa' : 내용} 으로 보냄
        except:
            Logging( 'pornav search exception','Error')
            return 0
        # Logging(searchResults)
        if (searchResults <> ''):
            nResult = searchResults.find('<div id="grid-container')  # 검색결과 확인
            # Logging(searchResults)
            # Logging(nResult)
            if (nResult <> -1):
                searchResults = String_slice(searchResults, '<div id="grid-container', '</ul>')
                nResult = searchResults.find(release_id)  # 2차 검색결과 확인
                if (nResult <> -1):
                    Logging('##### pornav Video Result Found #####','Info')
                    if (uncensored_check(media.filename) == 1):
                        uncResult = 'U'
                    else:
                        uncResult = 'C'
                    Logging('### UNC:' + uncResult,'Debug')
                    searchResults = String_slice(searchResults, '<li class="cbp-item', '</li>')
                    # content_id = String_slice(searchResults, '<a itemprop="url" href="', '"')
                    content_id=org_id
                    id = org_id
                    title = String_slice(searchResults, 'data-title="' + release_id + ' ', '"')
                    searchtype = 'pornav'
                    if (Prefs['filenametotitle'] == True and title_fromfile != ''):
                        title = title_fromfile
                        titletype = 'Y'
                    else:
                        titletype = 'N'
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

        getfileinfo=self.get_fileinfo(media)
        if getfileinfo is None:
            Logging('파일 정보를 분석할 수 없어 검색을 종료합니다', 'Debug')
            return
        Log('품번: ' + getfileinfo[0])
        Log('타이틀: <' + getfileinfo[1] + '>')
        org_id=getfileinfo[0]
        title_fromfile=getfileinfo[1].strip()
        release_id=poombun_split_num(org_id) #아마추어 작품의 경우 품번 숫자만 필요해서 숫자만 추리는 함수 호출

        Logging('******* javdb Video 검색 시작(Media search start) ****** ','Info')
        Logging("### Release ID:    " + str(release_id) + ' org_id: ' + str(org_id),'Info')  # Release ID: IPZ00929 org_id: IPZ-929
        # searchResults = Get_search_url(SEARCH_URL + '&f=all', release_id)

        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id + '&f=all').content
        except:
            Logging( 'javdb search exception','Error')
            return 0
        if (searchResults <> ''):
            nResult = searchResults.find('div class="empty-message"') #검색결과 없음
            # Logging(searchResults)
            # Logging(nResult)
            if (nResult == -1):
                Logging('##### javdb Video Result Found #####','Info')
                if (uncensored_check(media.filename) == 1):
                    uncResult = 'U'
                else:
                    uncResult = 'C'
                Logging('### UNC:' + uncResult,'Debug')
                searchResults=String_slice(searchResults,'videos video-container','</section>')
                if (searchResults.find(release_id) == -1): return 0
                content_id = String_slice(searchResults, 'a href="','"').replace('/v/','')
                Logging(' Content_id: ' + content_id,'Debug')
                id = org_id
                title = String_slice(searchResults, 'video-title">', '<')
                searchtype = 'javdb'
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
                Logging('javdb Video result Not found','Error')
        else:
            Logging('javdb Video result not found1','Error')
        return 0

    def func_update_title(self,metadata,media,id,title,ncroling,Trans):
        # title: 크롤링에서 가져온 제목, ncroling: Y일때 파일명을 타이틀로, N일때 웹크롤링을 타이틀로
        Logging('func_update_title 함수 시작','Debug')
        firststring = metadata.title[0]
        Logging('First string: ' + firststring, 'Debug')
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

        Logging('### 제목 종료 ###', 'info')
        Logging('func_update_title 함수 종료','Debug')

    def dmm_update(self, metadata, media, lang, nOrgID,ncroling):
        ################################################
        ################## DMM update ##################
        ################################################
        if (nOrgID.find('[') <> -1 ):
            org_id=poombun_check(nOrgID,'')
        else:
            org_id=nOrgID

        Logging('### 검색 사이트: DMM 일반 영상 / UpdateSite: DMM Video ###','Info')
        DETAIL_URL = 'https://www.dmm.co.jp/digital/videoa/-/detail/=/cid='
        bgimgURL='https://pics.dmm.co.jp/digital/video/'
        bgimgExt='jp-'

        Logging('ORG_ID: ' + org_id + ' metadataID: ' + str(metadata.id),'Debug')

        searchResults = Get_search_url(DETAIL_URL, metadata.id + '/?i3_ref=list&i3_ord=1')
        searchResults = String_slice(searchResults, 'area-headline group', 'div id="recommend"')
        if (searchResults == ''):
            Logging('### 검색 사이트: DMM 아마추어 영상 / UpdateSite: DMM Amateur ###','Info')
            DETAIL_URL = 'https://www.dmm.co.jp/digital/videoc/-/detail/=/cid='
            bgimgURL = 'https://pics.dmm.co.jp/digital/amateur/'
            bgimgExt = 'jp-00'
            searchResults = Get_search_url(DETAIL_URL, metadata.id)
            searchResults = String_slice(searchResults, 'area-headline group', 'div id="recommend"')
            if (searchResults == ''):
                return 0
        # Logging(searchResults)

        # 제목
        id =org_id.upper()
        nTitle=String_slice(searchResults, 'item fn">', '<')
        Logging(' title : ' + nTitle + ' OrgTitle:' + metadata.title ,'Debug')
        metadata.original_title=nTitle
        self.func_update_title(metadata,media,id,nTitle,ncroling,'ja')

        # 스튜디오
        sTemp = String_slice(searchResults, 'メーカー：', '</tr>') # 스튜디오 정보
        metadata.studio = String_slice(sTemp, '/">', '</a')
        metadata.studio = Papago_Trans(str(metadata.studio),'ja')

        # 감독
        try:
            sTemp=String_slice(searchResults, '監督：', '</tr>')
            director_info = Extract_str(sTemp, '<td>', '</td>')
            # Logging('### Director info / 감독 정보 ###')
            # Logging(director_info)
            if (director_info is not None):
                if (director_info[0] <> '----'):
                    director_info_ko = Papago_Trans(director_info[0],'ja')
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
            pass

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        try:
            if (searchResults.find('商品発売日') <> -1):
                sTemp = String_slice(searchResults, '>商品', '</tr>')
            elif (searchResults.find('配信開始日') <> -1):
                sTemp = String_slice(searchResults, '>配信', '</tr>')
            else:
                sTemp=''
            if (sTemp<>''):
                nYear = String_slice(sTemp, '<td>', '</td>')
                nYearArray=nYear.split('/')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                nYear = nYear.replace('/', '-')
                metadata.originally_available_at = datetime.strptime(nYear,'%Y-%m-%d')
        except:
            pass

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 줄거리
        try:
            sTemp = String_slice(searchResults, 'mg-b20 lh4">', '</div')
            # sTemp=sTemp.strip()
            if (sTemp <> ''):
                sTemp=re.sub('<.+?>', '', sTemp, 0, re.I|re.S)
                Logging('#################### SUMMARY' + sTemp, 'Debug')
                metadata.summary = Papago_Trans(sTemp,'ja')
                if (str(Prefs['searchsiteinfo']) == 'True'):metadata.summary='[DMM] ' + metadata.summary
        except:
            pass

        # 장르
        try:
            metadata.genres.clear()
            nGenreName=Extract_str(searchResults,'ジャンル：', '</tr>')
            j=len(nGenreName)
            for i in range(0,j):
                role = metadata.roles.new()
                # nGenreName[i]=nGenreName[i].replace('.','')
                nGenreName_ko=Papago_Trans(nGenreName[i],'ja').replace('.','')
                # Logging(nGenreName[i])
                # Logging(nGenreName_ko)
                metadata.genres.add(nGenreName_ko)
        except:
            pass

        # 배우정보
        try:
            metadata.roles.clear()
            nActorName=Extract_str(searchResults,'出演者：', '</tr>')
            # Logging('===================')
            # Logging(nActorName)
            if (nActorName is not None):
                j=len(nActorName)
                for i in range(0,j):
                    role = metadata.roles.new()
                    nActorInfo = Get_actor_info(nActorName[i])
                    role.photo = nActorInfo[0]
                    role.name = nActorInfo[1]
        except:
            pass

        # Posters/Background
        nposterMain=String_slice(searchResults,'id="sample-video"', '</div>')
        posterURL_Small = String_slice(nposterMain, 'img src="', '"') # 큰이미지가 없을수도 있음(아마추어의 경우)
        posterURL_Large = String_slice(nposterMain, 'a href="', '"')
        Logging("small Poster URL / 포스터 주소 : " + posterURL_Small, 'Debug')
        Logging("Large Poster URL / 포스터 주소 : " + posterURL_Large, 'Debug')
        try:
            if(posterURL_Small<>''):
                metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
        except:
            Logging(' Can not load Small Poster','Error')

        try:
            if(posterURL_Large<>''):
                metadata.posters[posterURL_Large] = Proxy.Preview(HTTP.Request(posterURL_Large, timeout=int(Prefs['timeout'])), sort_order=2)
        except:	Logging(' Can not load Large Poster', 'Error')
        sTemp = String_slice(searchResults, 'div id="sample-image-block"', '<div class')
        # Logging(sTemp)
        j=sTemp.count('img src')
        imgcnt=int(Prefs['img_cnt'])
        if(imgcnt <= j): j=imgcnt
        # Logging('Image count: ','Debug')
        # Logging(j,'Debug')
        if (j <> -1):
            for i in range(0,j):
                bgimg=bgimgURL + metadata.id + '/' + metadata.id + bgimgExt + str(i+1) + '.jpg'
                try:
                    if (bgimg <> ''):
                        metadata.art[bgimg] = Proxy.Preview(HTTP.Request(bgimg, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order=i+1)
                except:
                    Logging('###' + bgimg + ' Can not load','Error')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        try:
            Logging('######## series info','Info')
            sTemp=String_slice(searchResults, 'シリー', '</tr>')
            # Logging(sTemp)
            series_info = Extract_str(sTemp, '<td>', '</td>')
            # Logging(series_info)
            # Logging('SeriesInfo: ' + series_info)
            if (series_info is not None):
                if (series_info[0] <> '----'):
                    series_info_ko = Papago_Trans(series_info[0],'ja')
                    Logging(series_info_ko,'Info')
                    metadata.tagline=series_info_ko
            else:
                Logging('Series info not found', 'Error')
        except:
            pass

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

        Logging('******* DMM 미디어 업데이트 완료/Media Update completed ****** ','Info')
        return 1

    def r18_update(self, metadata, media, lang, nOrgID,ncroling):

        Logging('****** 미디어 업데이트(상세항목) 시작 / r18 Media Update Start *******','Info')
        # Logging("Update ID:   " + str(metadata.id) +  ' Original ID: ' + org_id)

        ################################################
        ################## r18 update ##################
        ################################################
        # r18 사이트 검색
        DETAIL_URL = 'https://www.r18.com/videos/vod/movies/detail/-/id='
        DETAIL_URL2 = 'https://www.r18.com/videos/vod/amateur/detail/-/id='

        org_id = poombun_check(nOrgID,'')

        #일반 검색에서 안나올 경우 아마추어 URL로 다시 확인함
        try:
            url = DETAIL_URL + metadata.id
            root = HTML.ElementFromURL(url,timeout=int(Prefs['timeout']))
        except:
            try:
                url = DETAIL_URL2 + metadata.id
                root = HTML.ElementFromURL(url, timeout=int(Prefs['timeout']))
            except:
                return 0

        # id = detailItem(root, '//dt[contains(text(), "DVD ID")]/following-sibling::dd[1]')  # 작품 ID
        # 제목
        Logging('##### r18 제목 시작 ####','Info')
        id = org_id.upper()
        nTitle=detailItem(root,'//cite[@itemprop="name"]')
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling,'en')
        Logging('#### r18 제목 종료 ####', 'Info')

        # 스튜디오
        metadata.studio = detailItem(root,'//dd[@itemprop="productionCompany"]//a') # 스튜디오 정보
        metadata.studio = Papago_Trans(str(metadata.studio))

        #줄거리 요약정보(r18은 요약정보가 없으므로 검색된 사이트 이름만 표기
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[r18]'

        #Logging('### 감독정보 가져오기 ###')
        director_info = detailItem(root,'//dd[@itemprop="director"]') # 감독 정보
        director_info = Papago_Trans(director_info)
        metadata.directors.clear()
        try:
            meta_director = metadata.directors.new()
            meta_director.name = director_info
        except:
            try:
                metadata.directors.add(director_info)
            except:
                pass

        date = detailItem(root,'//dd[@itemprop="dateCreated"]') # 릴리즈 날짜
        date_object = datetime.strptime(date.replace(".", "").replace("Sept", "Sep").replace("July", "Jul").replace("June", "Jun"), '%b %d, %Y')
        metadata.originally_available_at = date_object
        metadata.year = metadata.originally_available_at.year

        metadata.genres.clear()
        categories = root.xpath('//div[contains(@class, "product-categories-list")]//div//a')
        for category in categories:
            genreName = category.text_content().strip()
            if "Featured" in genreName or "Sale" in genreName:
                continue
            genreName=genreName.replace('.','')
            nTrans=Papago_Trans(genreName)
            metadata.genres.add(nTrans)
            Logging('metadata.genre : ' + nTrans,'Info')

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 배우정보
        metadata.roles.clear()
        actors = root.xpath('//div[contains(@class, "js-tab-contents")]//ul[contains(@class, "cmn-list-product03")]//a')
        if len(actors) > 0:
            for actorLink in actors:
                role = metadata.roles.new()
                actorName = actorLink.text_content().strip()
                nTrans=Papago_Trans(actorName)

                role.name = nTrans
                actorPage = actorLink.xpath("p/img")[0].get("src")
                role.photo = actorPage
                Logging("Actor: " + nTrans,'Info')
        else:
            Logging("배우 정보를 찾을 수 없음",'Error')

        # Posters/Background
        posterURL = root.xpath('//img[@itemprop="image"]')[0].get("src")
        Logging("Poster URL / 포스터 주소 : " + posterURL,'Debug')
        try:
            if(posterURL<>''):
                metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order = 1)
        except: Logging(posterURL + ' Not Load','Error')
        posterURL=posterURL.replace('ps.jpg','pl.jpg')
        try:
            if (posterURL <> ''):
                metadata.posters[posterURL] = Proxy.Preview(HTTP.Request(posterURL, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order=2)
        except: Logging(posterURL + ' Not Load','Error')
        scenes = root.xpath('//ul[contains(@class, "product-gallery")]//img')
        i=1
        imgcnt=int(Prefs['img_cnt'])

        for scene in scenes:
            background = scene.get("data-original").replace("js-", "jp-")
            Logging("백그라운드 URL BackgroundURL: " + background, 'Debug')
            try:
                if(background <>''):
                    metadata.art[background] = Proxy.Preview(HTTP.Request(background, headers={'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content, sort_order = i)
            except:Logging(background + ' Not Load', 'Error')
            if (imgcnt <= i): break
            i=i+1

        Logging('******* 미디어 업데이트 완료 ****** ','Info')

        # studio 컬렉션 생성
        if (str(Prefs['create_collection_studio']) == 'True'):
            if metadata.studio != None:
                metadata.collections.add(metadata.studio)
                Logging(' metadata.collections studio: ' + str(metadata.studio), 'Info')
        else:
            Logging('### Studio 컬렉션 생성 안함(설정 미체크)' ,'Info')
        # series 컬렉션 생성
        if (str(Prefs['create_collection_series']) == 'True'):
            series = detailItem(root,'//div[contains(@class, "product-details")]//a[contains(@href, "type=series")]')
            if series != None:
                nTrans=Papago_Trans(series)
                metadata.collections.add(nTrans)
                Logging(' metadata.collections series: ' + str(nTrans),'Info')
        else:
            Logging('### series 컬렉션 생성 안함(설정 미체크)','Info')

        return 1

    def javbus_update(self, metadata, media, lang, nOrgID,ncroling):

        # nIDs[0]: 검색용 품번  nIDs[1]: 검색된 사이트(DMM, R18)   nIDs[2]: 아마추어(C)or일반(A)  nIDs[3]: 오리지널 품번(OAE-101)
        Logging('****** 미디어 업데이트(상세항목) 시작 / Javbus Media Update Start *******','Info')
        # Logging("Update ID:   " + str(metadata.id) +  ' Original ID: ' + org_id)

        ################################################
        ################# javbus update #################
        ################################################
        Logging('### 검색 사이트: javbus 일반 영상 / UpdateSite: javbus Video ###','Info')
        DETAIL_URL = 'https://www.javbus.com/'

        org_id=poombun_check(nOrgID,'')

        try:
            searchResults = HTTP.Request(DETAIL_URL + metadata.id , headers = {'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content
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

        Logging('#### javbus 제목 시작####', 'Info')
        id = org_id.upper()
        nTitle = String_slice(searchResults, 'title="', '"')
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('#### javbus 제목 종료 ####', 'Info')

        # 스튜디오=> 제조사
        try:
            Logging('=======  Studio Info start =========','Info')
            sTemp = String_slice(searchResults, '製作商', '</p>')
            metadata.studio = String_slice(sTemp, '">', '</a')
            metadata.studio = Papago_Trans(str(metadata.studio), 'ja')
            Logging('Studio: ' + str(metadata.studio),'Info')
            Logging('=======  Studio Info end =========','Info')
        except:
            Logging('@@@ Studio failed','Error')

        # 감독
        try:
            Logging('=======  Director Info start =========','Info')
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
            Logging('=======  Director Info end =========','Info')
        except:
            Logging('@@@ Director failed','Error')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        try:
            Logging('=======  Date Info start =========','Info')
            if (searchResults.find('發行日') <> -1):
                nYear = String_slice(searchResults, '發行日期:</span>', '</p>')
                nYearArray = nYear.split('-')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
            Logging('=======  Date Info start =========','Info')
        except:
            Logging('@@@ Date Failed','Error')

        # 줄거리(javbus는 줄거리 없음)
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[javbus]'

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 장르
        try:
            Logging('=======  Genre Info start =========','Info')
            metadata.roles.clear()
            nGenreName = Extract_str(searchResults, '類別:</p>', '</p>')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                # nGenreName[i] = nGenreName[i].replace('.', '')
                nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.','')
                # Logging(nGenreName[i])
                Logging(nGenreName_ko, 'Debug')
                metadata.genres.add(nGenreName_ko)
            Logging('=======  Genre Info end =========','Info')
        except:
            Logging('@@@ Genre failed','Error')

        # 배우정보
        metadata.roles.clear()
        Logging('=======  Actor Info start =========','Info')
        nFound = searchResults.find('<div id="star-div">')
        try:
            if (nFound <> -1):
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
                    role.photo = str(nActorURL[i])
                    role.name = rolename_kr
                    Logging('nURL: ' + str(nActorURL[i]) + ' nName: ' + rolename_kr,'Debug')
        except:
            Logging('@@@ Get actor info exception','Error')

        Logging('=======  Actor Info end =========','Info')

        # Posters
        Logging('=======  Poster Info start =========','Info')
        try:
            nposterMain = String_slice(searchResults, 'col-md-9 screencap', '</div>')
            posterURL_Large = String_slice(nposterMain, 'href="', '"')
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
            Logging('=======  Poster Info end =========','Info')
        except:
            Logging('@@@ Poster Failed','Error')

        #background images
        try:
            Logging('=======  Background Info start =========','Info')
            nBgackgroundimg=Extract_imgurl(searchResults, '<div id="sample-waterfall">', '<div class="clearfix','href')
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
            Logging('=======  Background Info end =========','Info')
        except:
            Logging('@@@ Background Image failed','Error')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        try:
            Logging('=======  Series Info start =========','Info')
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
            Logging('=======  Series Info end =========','Info')
        except:
            Logging('@@@ Series failed','Error')

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
        # Logging("Update ID:   " + str(metadata.id) +  ' Original ID: ' + org_id)
        # id: /jp/article-179279/N0836-Saionji-Reo-vs-TOKYO-HOT-Devil-Kang

        ################################################
        ################# pornav update #################
        ################################################
        Logging('### 검색 사이트: pornav 일반 영상 / UpdateSite: pornav Video ###','Info')
        DETAIL_URL = 'http://pornav.co/'
        SEARCH_URL = 'http://pornav.co/jp/search?q='

        org_id=metadata.id
        release_id=poombun_split_num(org_id)
        try:
            searchResults = HTTP.Request(SEARCH_URL + release_id, timeout=int(Prefs['timeout'])).content  # post로 보낼경우 value={'aaa' : 내용} 으로 보냄
        except:
            return 0
        content_id = String_slice(searchResults, '<a itemprop="url" href="', '"')
        try:
            searchResults = HTTP.Request(DETAIL_URL + content_id , headers = {'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content
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

        Logging('#### pornav 제목 시작####', 'Info')
        id= String_slice(media.title,'[',']').upper()
        nTitle = String_slice(searchResults, 'alt="', '"').replace(id,'').upper()
        nTitle = nTitle.replace('FC2 PPV ', '')
        nTitle = nTitle.replace(release_id.upper(), '')
        nTitle = nTitle.replace('TOKYO HOT','')
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('#### pornav 제목 종료 ####', 'Info')

        # 스튜디오=> 제조사
        try:
            Logging('=======  Studio Info start =========','Info')
            sTemp = String_slice(searchResults, 'メーカー： ', '<')
            metadata.studio = Papago_Trans(str(sTemp), 'ja')
            Logging('Studio: ' + str(metadata.studio),'Debug')
            Logging('=======  Studio Info end =========','Info')
        except:
            Logging('@@@ Studio failed','Error')

        # 감독
        try:
            Logging('=======  Director Info start =========','Info')
            # sTemp = String_slice(searchResults, '導演', '<p>')
            director_info = String_slice(searchResults, '監督： ', '<')
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
            Logging('=======  Director Info end =========','Info')
        except:
            Logging('@@@ Director failed','Error')

            # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        try:
            Logging('=======  Date Info start =========','Info')
            if (searchResults.find('発売日') <> -1):
                nYear = String_slice(searchResults, '発売日： ', '<')
                nYear = nYear.replace('/','-')
                nYearArray = nYear.split('-')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
                Logging(' Year: ' + nYear,'Debug')
            Logging('=======  Date Info end =========','Info')
        except:
            Logging('@@@ Date Failed','Error')

            # 줄거리
            if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[pornav]'
        try:
            Logging('=======  summary Info start =========','Info')
            sTemp = String_slice(searchResults, 'class="tag-box tag-box-v2">', '</div>')
            metadata.summary = metadata.summary + Papago_Trans(sTemp, 'ja')
            Logging('summary: ' + str(metadata.summary),'Debug')
            Logging('=======  summary Info end =========','Info')
        except:
            Logging('@@@ summary failed','Error')

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 장르
        try:
            Logging('=======  Genre Info start =========','Info')
            metadata.roles.clear()
            nGenreName = String_slice(searchResults, 'ジャンル：', '<')
            Logging('########## Genre str: ' + nGenreName,'Debug')
            nGenreName_arr=nGenreName.split(' ')
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
            Logging('=======  Genre Info end =========','Info')
        except:
            Logging('@@@ Genre failed','Error')

        # 배우정보 => 이시키들이 배우 구분자가 스페이스인데 이름이 2글자면 이것도 스페이스로 나눠서 이름을 당췌 알 수 없음.. 통짜로 넣어야할듯
        metadata.roles.clear()
        Logging('=======  Actor Info start =========','Info')
        nFound = searchResults.find('出演者： ')
        try:
            if (nFound <> -1):
                nStr = String_slice(searchResults, '出演者： ', '<')
                nActor=nStr.split(' ')
                j = len(nActor)
                for i in range(0, j):
                    if (nActor[i] == '' or nActor[i] <> ' '):
                        role = metadata.roles.new()
                        rolename_kr = Papago_Trans(nActor[i], 'ja')
                        role.photo = str(nActor[i])
                        role.name = rolename_kr
                        Logging('nURL: ' + str(nActor[i]) + ' nName: ' + rolename_kr,'Debug')
                Logging('=======  Genre Info end =========','Info')
        except:
            Logging('@@@ Get actor info exception','Error')

        # Posters
        Logging('=======  Poster Info start =========','Info')
        try:
            posterURL_Small = String_slice(searchResults, '<img itemprop="image" src="', '"')
            Logging("small Poster URL / 포스터 주소 : " + posterURL_Small,'Debug')
            try:
                if(posterURL_Small <>''):
                    metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:	Logging(' Can not load Small Poster','Error')
            Logging('=======  Poster Info end =========','Info')
        except:
            Logging('@@@ Poster Failed','Error')

        #background images
        try:
            Logging('=======  Background Info start =========','Info')
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
            Logging('=======  Background Info end =========','Info')
        except:
            Logging('@@@ Background Image failed','Error')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        try:
            Logging('=======  Series Info start =========','Info')
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
            Logging('=======  Series Info end =========','Info')
        except:
            Logging('@@@ Series failed','Error')

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

    def javdb_update(self, metadata, media, lang, nOrgID,ncroling):

        # nIDs[0]: 검색용 품번  nIDs[1]: 검색된 사이트(DMM, R18)   nIDs[2]: 아마추어(C)or일반(A)  nIDs[3]: 오리지널 품번(OAE-101)
        Logging('****** 미디어 업데이트(상세항목) 시작 / javdb Media Update Start *******','Info')
        # Logging("Update ID:   " + str(metadata.id) +  ' Original ID: ' + org_id)

        ################################################
        ################# javdb update #################
        ################################################
        Logging('### 검색 사이트: javdb 일반 영상 / UpdateSite: javdb Video ###','Info')
        DETAIL_URL = 'https://javdb.com/v/'
        org_id=poombun_check(nOrgID,'')
        # release_id=poombun_split_num(org_id)

        try:
            searchResults = HTTP.Request(DETAIL_URL + metadata.id , headers = {'Referer': 'http://www.google.com'}, timeout=int(Prefs['timeout'])).content
        except:
            Logging('@@@ Update content load failed','Error')
            return 0

        # Logging(searchResults)
        nResult = searchResults.find('頁面未找到 (404)')  # 검색결과 확인
        if (nResult <> -1):
            Logging('@@@ Update content search result failed1','Error')
            return 0
        searchResults = String_slice(searchResults, 'title is-4', '</article>')
        if (searchResults == ''):
            Logging('@@@ Update content search result failed2','Error')
            return 0
        # Logging(searchResults)

        Logging('#### javdb 제목 시작####', 'Info')
        id= String_slice(media.title,'[',']').upper()
        nTitle = String_slice(searchResults, '<strong>', '<').replace(id,'')
        metadata.original_title = nTitle
        self.func_update_title(metadata, media, id, nTitle, ncroling, 'ja')
        Logging('#### javdb 제목 종료 ####', 'Info')

        # 스튜디오=> 제조사
        try:
            Logging('=======  Studio Info start =========','Info')
            sTemp = String_slice(searchResults, '片商', '</div>')
            sTemp = String_slice(sTemp, 'a href', '</span>')
            metadata.studio = String_slice(sTemp, '">', '</a')
            metadata.studio = Papago_Trans(str(metadata.studio), 'ja')
            Logging('Studio: ' + str(metadata.studio),'Debug')
            Logging('=======  Studio Info end =========','Info')
        except:
            Logging('@@@ Studio failed','Error')

        # 감독
        try:
            Logging('=======  Director Info start =========','Info')
            # sTemp = String_slice(searchResults, '導演', '<p>')
            director_info = Extract_str(searchResults, '導演', '</div>')
            if (director_info is not None):
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
            Logging('=======  Director Info end =========','Info')
        except:
            Logging('@@@ Director failed','Error')

        # 일자 표시(미리보기, 원출처) 제품발매일:商品発売日 전달개시일:配信開始日
        try:
            Logging('=======  Date Info start =========','Info')
            if (searchResults.find('日期') <> -1):
                nYear = String_slice(searchResults, '日期', '</div>')
                nYear = String_slice(nYear, 'value">', '<')
                nYearArray = nYear.split('-')
                # 미리보기 항목의 이미지 아래 표시되는 년도
                metadata.year = int(nYearArray[0])
                # 상세항목의 '원출처' 일자
                metadata.originally_available_at = datetime.strptime(nYear, '%Y-%m-%d')
            Logging('=======  Date Info start =========','Info')
        except:
            Logging('@@@ Date Failed','Error')

        # 줄거리(javdb는 줄거리 없음)
        if (str(Prefs['searchsiteinfo']) == 'True'): metadata.summary = '[javdb]'

        # 국가
        metadata.countries.clear()
        metadata.countries.add(Papago_Trans('Japan').replace('.',''))

        # 장르
        try:
            Logging('=======  Genre Info start =========','Info')
            metadata.roles.clear()
            nGenreName = Extract_str(searchResults, '類別', '</div>')
            j = len(nGenreName)
            for i in range(0, j):
                role = metadata.roles.new()
                # nGenreName[i] = nGenreName[i].replace('.', '')
                nGenreName_ko = Papago_Trans(nGenreName[i], 'ja').replace('.','')
                Logging(nGenreName[i],'Debug')
                Logging(nGenreName_ko,'Debug')
                metadata.genres.add(nGenreName_ko)
            Logging('=======  Genre Info end =========','Info')
        except:
            Logging('@@@ Genre failed','Error')

        # 배우정보
        Logging('=======  Actor Info end =========','Info')
        metadata.roles.clear()
        nActorName=Extract_str(searchResults,'演員', '</div>')
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
                role.photo = nActorInfo[0]
                role.name = nActorInfo[1]
        Logging('=======  Actor Info end =========','Info')

        # Posters
        Logging('=======  Poster Info start =========','Info')
        try:
            posterURL_Small = String_slice(searchResults, 'gallery" href="', '"')
            Logging("small Poster URL / 포스터 주소 : " + posterURL_Small,'Debug')
            try:
                if(posterURL_Small <>'' or posterURL_Small <> '#preview-video'):
                    metadata.posters[posterURL_Small] = Proxy.Preview(HTTP.Request(posterURL_Small, timeout=int(Prefs['timeout'])), sort_order=1)
            except:	Logging(' Can not load Small Poster','Error')
            Logging('=======  Poster Info end =========','Info')
        except:
            Logging('@@@ Poster Failed','Error')

        #background images
        try:
            Logging('=======  Background Info start =========','Info')
            nBgackgroundimg=Extract_imgurl(searchResults, 'tile-images preview-images', '</article>','href')
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
            Logging('=======  Background Info end =========','Info')
        except:
            Logging('@@@ Background Image failed','Error')

        # Series 정보(plex에는 seires 항목이 없으므로 '주제' 항목에 이 값을 넣음)
        try:
            Logging('=======  Series Info start =========','Info')
            # Logging('######## series info')
            # Logging(sTemp)
            series_info = Extract_str(searchResults, '系列', '</div>')
            # Logging(series_info,'Debug')
            # Logging('SeriesInfo: ' + series_info)
            if (series_info is not None):
                if (series_info[0] <> '----'):
                    series_info_ko = Papago_Trans(series_info[0], 'ja')
                    Logging(series_info_ko,'Debug')
                    metadata.tagline = series_info_ko
            else:
                Logging('Series info not found','Error')
            Logging('=======  Series Info end =========','Info')
        except:
            Logging('@@@ Series failed','Error')

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

            Logging('******* javdb 미디어 업데이트 완료/Media Update completed ****** ','Info')

        except:
            Logging('@@@ Series collection failed','Error')

        return 1
