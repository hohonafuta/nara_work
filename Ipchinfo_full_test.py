 # -*- coding: utf-8 -*-

import csv
import json
from urllib.request import urlopen
from urllib import parse
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import re

today = dt.date.today().strftime('%Y%m%d')
today = today + "0000"
month_before = (dt.datetime.now() - relativedelta(months=1) ).strftime('%Y%m%d') + "0000"
print("Today's date : " + today)
inqryBgnDt = month_before
inqryEndDt = today

# 나라장터검색조건에 의한 입찰공고용역조회
'''
> parameter(조회조건)
- inqryDiv :조회구분(접수일시)
- inqryBgnDt : 조회시작일시
- inqryEndDt : 조회종료일시
- intrntnlDivCd : 1(국내)
- bidClseExcpYn : Y(입찰마감건 제외)
'''
url = 'https://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwkPPSSrch'
#url = 'http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwkPPSSrch'
queryParams = '?' + parse.urlencode({ parse.quote_plus('serviceKey') : '2574fa14b823f9e42dcab8e6709dc21742dba10ba13040d4ba046518ff5c2bb9', 
                                     parse.quote_plus('pageNo') : '1', 
                                     parse.quote_plus('numOfRows') : 900, 
                                     parse.quote_plus('type') : 'json' ,
                                     parse.quote_plus('inqryDiv') : '1', 
                                     parse.quote_plus('inqryBgnDt') : inqryBgnDt, 
                                     parse.quote_plus('inqryEndDt') : inqryEndDt,
                                     parse.quote_plus('intrntnlDivCd') : '1',
                                     parse.quote_plus('bidClseExcpYn') : 'Y',
                                     parse.quote_plus('indstrytyCd') : '0037',
                                     parse.quote_plus('prtcptLmtRgnNm') : '서울특별시'
                                    })


# print(url + queryParams)
# set_API & get_data -> openAPI & parameters
response = urlopen(url + queryParams)
data = response.read()
print(data)
JSON_object = json.loads(data.decode('utf-8'))


for object in JSON_object["response"]["body"]["items"]:
    print(object)
    print("\n")


# Total Count
print("total Count : " + str(JSON_object["response"]["body"]["totalCount"]))

# 정렬(내림차순) -> 등록일시(rgstDt)
def sortFunction(value):
	return value["bidNtceDt"]

sortedList = sorted(JSON_object["response"]["body"]["items"], key=sortFunction, reverse=True)
for value in sortedList:
   print(value)
   print("\n")

'''
> Columns
- 공고일시 : bidNtceDt
- 공고번호 : bidNtceNo
- 공고명 : bidNtceNm
- 수요기관 : dminsttNm
- 계약체결방법명 : cntrctCnclsMthdNm
- 입찰방식명 : bidMethdNm
- 낙찰방법명 : sucsfbidMthdNm
- 입찰마감일시 : bidClseDt
- 개찰일시 : opengDt
- 입찰공고 상세(URL) : bidNtceUrl
- 예가방법 : prearngPrceDcsnMthdNm
- 총예가건수 : totPrdprcNum
- 추첨예가건수 : drwtPrdprcNum
- 배정예산 : asignBdgtAmt
- 추정가격 : presmptPrce
'''

df = pd.DataFrame(sortedList, columns = ["resultCode",
                                        "resultMsg",
                                        "numOfRows",
                                        "pageNo",
                                        "totalCount",
                                        "bidNtceNo",
                                        "bidNtceOrd",
                                        "reNtceYn",
                                        "rgstTyNm",
                                        "ntceKindNm",
                                        "intrbidYn",
                                        "bidNtceDt",
                                        "refNo",
                                        "bidNtceNm",
                                        "ntceInsttCd",
                                        "ntceInsttNm",
                                        "dminsttCd",
                                        "dminsttNm",
                                        "bidMethdNm",
                                        "cntrctCnclsMthdNm",
                                        "ntceInsttOfclNm",
                                        "ntceInsttOfclTelNo",
                                        "ntceInsttOfclEmailAdrs",
                                        "exctvNm",
                                        "bidQlfctRgstDt",
                                        "cmmnSpldmdAgrmntRcptdocMethd",
                                        "cmmnSpldmdAgrmntClseDt",
                                        "cmmnSpldmdCorpRgnLmtYn",
                                        "bidBeginDt",
                                        "bidClseDt",
                                        "opengDt",
                                        "ntceSpecDocUrl1",
                                        "ntceSpecDocUrl2",
                                        "ntceSpecDocUrl3",
                                        "ntceSpecDocUrl4",
                                        "ntceSpecDocUrl5",
                                        "ntceSpecDocUrl6",
                                        "ntceSpecDocUrl7",
                                        "ntceSpecDocUrl8",
                                        "ntceSpecDocUrl9",
                                        "ntceSpecDocUrl10",
                                        "ntceSpecFileNm1",
                                        "ntceSpecFileNm2",
                                        "ntceSpecFileNm3",
                                        "ntceSpecFileNm4",
                                        "ntceSpecFileNm5",
                                        "ntceSpecFileNm6",
                                        "ntceSpecFileNm7",
                                        "ntceSpecFileNm8",
                                        "ntceSpecFileNm9",
                                        "ntceSpecFileNm10",
                                        "rbidPermsnYn",
                                        "pqApplDocRcptMthdNm",
                                        "pqApplDocRcptDt",
                                        "arsltApplDocRcptMthdNm",
                                        "arsltApplDocRcptDt",
                                        "jntcontrctDutyRgnNm1",
                                        "jntcontrctDutyRgnNm2",
                                        "jntcontrctDutyRgnNm3",
                                        "rgnDutyJntcontrctRt",
                                        "dtlsBidYn",
                                        "bidPrtcptLmtYn",
                                        "prearngPrceDcsnMthdNm",
                                        "totPrdprcNum",
                                        "drwtPrdprcNum",
                                        "bdgtAmt",
                                        "presmptPrce",
                                        "govsplyAmt",
                                        "aplBssCntnts",
                                        "indstrytyEvlRt",
                                        "mainCnsttyNm",
                                        "mainCnsttyCnstwkPrearngAmt",
                                        "incntvRgnNm1",
                                        "incntvRgnNm2",
                                        "incntvRgnNm3",
                                        "incntvRgnNm4",
                                        "opengPlce",
                                        "dcmtgOprtnDt",
                                        "dcmtgOprtnPlce",
                                        "contrctrcnstrtnGovsplyMtrlAmt",
                                        "govcnstrtnGovsplyMtrlAmt",
                                        "bidNtceDtlUrl",
                                        "bidNtceUrl",
                                        "bidPrtcptFeePaymntYn",
                                        "bidPrtcptFee",
                                        "bidGrntymnyPaymntYn",
                                        "crdtrNm",
                                        "cmmnSpldmdCnum",
                                        "untyNtceNo",
                                        "sptDscrptDocUrl1",
                                        "sptDscrptDocUrl2",
                                        "sptDscrptDocUrl3",
                                        "sptDscrptDocUrl4",
                                        "sptDscrptDocUrl5",
                                        "subsiCnsttyNm1",
                                        "subsiCnsttyNm2",
                                        "subsiCnsttyNm3",
                                        "subsiCnsttyNm4",
                                        "subsiCnsttyNm5",
                                        "subsiCnsttyNm6",
                                        "subsiCnsttyNm7",
                                        "subsiCnsttyNm8",
                                        "subsiCnsttyNm9",
                                        "subsiCnsttyIndstrytyEvlRt1",
                                        "subsiCnsttyIndstrytyEvlRt2",
                                        "subsiCnsttyIndstrytyEvlRt3",
                                        "subsiCnsttyIndstrytyEvlRt4",
                                        "subsiCnsttyIndstrytyEvlRt5",
                                        "subsiCnsttyIndstrytyEvlRt6",
                                        "subsiCnsttyIndstrytyEvlRt7",
                                        "subsiCnsttyIndstrytyEvlRt8",
                                        "subsiCnsttyIndstrytyEvlRt9",
                                        "cmmnSpldmdMethdCd",
                                        "cmmnSpldmdMethdNm",
                                        "stdNtceDocUrl",
                                        "brffcBidprcPermsnYn",
                                        "cnsttyAccotShreRateList",
                                        "cnstrtnAbltyEvlAmtList",
                                        "dsgntCmptYn",
                                        "arsltCmptYn",
                                        "pqEvalYn",
                                        "ntceDscrptYn",
                                        "rsrvtnPrceReMkngMthdNm",
                                        "mainCnsttyPresmptPrce",
                                        "orderPlanUntyNo",
                                        "sucsfbidLwltRate",
                                        "rgstDt",
                                        "bfSpecRgstNo",
                                        "sucsfbidMthdCd",
                                        "sucsfbidMthdNm",
                                        "chgDt",
                                        "dminsttOfclEmailAdrs",
                                        "indstrytyLmtYn",
                                        "cnstrtsiteRgnNm",
                                        "rgnDutyJntcontrctYn",
                                        "chgNtceRsn",
                                        "rbidOpengDt",
                                        "ciblAplYn",
                                        "mtltyAdvcPsblYn",
                                        "mtltyAdvcPsblYnCnstwkNm",
                                        "VAT",
                                        "indutyVAT",
                                        "indstrytyMfrcFldEvlYn",
                                        "bidWgrnteeRcptClseDt",
                                        "rgnLmtBidLocplcJdgmBssCd",
                                        "rgnLmtBidLocplcJdgmBssNm"
                                        ])

# filter_1 : 입찰참여 가능한 공고 ("입찰마감일시" > 현재시간 )
valid = df['bidClseDt'] > str(dt.datetime.now().strftime('%Y-%m-%d %H:%m:%S'))
valid_bid = df[valid]

# filter_2 : 공고명 특정 문자 포함 여부
#filter_2 = df['bidNtceNm'].str.contains('음식|생물|녹색|청소|하수처리')
#~filter_2
#valid_bid = valid_bid[~filter_2]

# 구분 컬럼 추가 -> 운영/구축
valid_bid['class'] = np.where(valid_bid['bidNtceNm'].str.contains('유지관리|유지보수|위탁운영|통합운영|운영관리'), '운영(ITO)', '구축(SI)')

valid_bid.rename(columns = {"resultCode": "결과코드",
                            "resultMsg": "결과메세지",
                            "numOfRows": "한 페이지 결과 수",
                            "pageNo": "페이지 번호",
                            "totalCount": "전체 결과 수",
                            "bidNtceNo": "입찰공고번호",
                            "bidNtceOrd": "입찰공고차수",
                            "reNtceYn": "재공고여부",
                            "rgstTyNm": "등록유형명",
                            "ntceKindNm": "공고종류명",
                            "intrbidYn": "국제입찰여부",
                            "bidNtceDt": "입찰공고일시",
                            "refNo": "참조번호",
                            "bidNtceNm": "입찰공고명",
                            "ntceInsttCd": "공고기관코드",
                            "ntceInsttNm": "공고기관명",
                            "dminsttCd": "수요기관코드",
                            "dminsttNm": "수요기관명",
                            "bidMethdNm": "입찰방식명",
                            "cntrctCnclsMthdNm": "계약체결방법명",
                            "ntceInsttOfclNm": "공고기관담당자명",
                            "ntceInsttOfclTelNo": "공고기관담당자전화번호",
                            "ntceInsttOfclEmailAdrs": "공고기관담당자이메일주소",
                            "exctvNm": "집행관명",
                            "bidQlfctRgstDt": "입찰참가자격등록마감일시",
                            "cmmnSpldmdAgrmntRcptdocMethd": "공동수급협정서접수방식",
                            "cmmnSpldmdAgrmntClseDt": "공동수급협정마감일시",
                            "cmmnSpldmdCorpRgnLmtYn": "공동수급업체지역제한여부",
                            "bidBeginDt": "입찰개시일시",
                            "bidClseDt": "입찰마감일시",
                            "opengDt": "개찰일시",
                            "ntceSpecDocUrl1": "공고규격서URL1",
                            "ntceSpecDocUrl2": "공고규격서URL2",
                            "ntceSpecDocUrl3": "공고규격서URL3",
                            "ntceSpecDocUrl4": "공고규격서URL4",
                            "ntceSpecDocUrl5": "공고규격서URL5",
                            "ntceSpecDocUrl6": "공고규격서URL6",
                            "ntceSpecDocUrl7": "공고규격서URL7",
                            "ntceSpecDocUrl8": "공고규격서URL8",
                            "ntceSpecDocUrl9": "공고규격서URL9",
                            "ntceSpecDocUrl10": "공고규격서URL10",
                            "ntceSpecFileNm1": "공고규격파일명1",
                            "ntceSpecFileNm2": "공고규격파일명2",
                            "ntceSpecFileNm3": "공고규격파일명3",
                            "ntceSpecFileNm4": "공고규격파일명4",
                            "ntceSpecFileNm5": "공고규격파일명5",
                            "ntceSpecFileNm6": "공고규격파일명6",
                            "ntceSpecFileNm7": "공고규격파일명7",
                            "ntceSpecFileNm8": "공고규격파일명8",
                            "ntceSpecFileNm9": "공고규격파일명9",
                            "ntceSpecFileNm10": "공고규격파일명10",
                            "rbidPermsnYn": "재입찰허용여부",
                            "pqApplDocRcptMthdNm": "PQ신청서접수방법명",
                            "pqApplDocRcptDt": "PQ신청서접수일시",
                            "arsltApplDocRcptMthdNm": "실적신청서접수방법명",
                            "arsltApplDocRcptDt": "실적신청서접수일시",
                            "jntcontrctDutyRgnNm1": "공동도급의무지역명1",
                            "jntcontrctDutyRgnNm2": "공동도급의무지역명2",
                            "jntcontrctDutyRgnNm3": "공동도급의무지역명3",
                            "rgnDutyJntcontrctRt": "지역의무공동도급비율",
                            "dtlsBidYn": "내역입찰여부",
                            "bidPrtcptLmtYn": "입찰참가제한여부",
                            "prearngPrceDcsnMthdNm": "예정가격결정방법명",
                            "totPrdprcNum": "총예가건수",
                            "drwtPrdprcNum": "추첨예가건수",
                            "bdgtAmt": "예산금액",
                            "presmptPrce": "추정가격",
                            "govsplyAmt": "관급금액",
                            "aplBssCntnts": "적용기준내용",
                            "indstrytyEvlRt": "업종평가비율",
                            "mainCnsttyNm": "주공종명",
                            "mainCnsttyCnstwkPrearngAmt": "주공종공사예정금액",
                            "incntvRgnNm1": "가산지역명1",
                            "incntvRgnNm2": "가산지역명2",
                            "incntvRgnNm3": "가산지역명3",
                            "incntvRgnNm4": "가산지역명4",
                            "opengPlce": "개찰장소",
                            "dcmtgOprtnDt": "설명회실시일시",
                            "dcmtgOprtnPlce": "설명회실시장소",
                            "contrctrcnstrtnGovsplyMtrlAmt": "도급자설치관급자재금액",
                            "govcnstrtnGovsplyMtrlAmt": "관급자설치관급자재금액",
                            "bidNtceDtlUrl": "입찰공고상세URL",
                            "bidNtceUrl": "입찰공고URL",
                            "bidPrtcptFeePaymntYn": "입찰참가수수료납부여부",
                            "bidPrtcptFee": "입찰참가수수료",
                            "bidGrntymnyPaymntYn": "입찰보증금납부여부",
                            "crdtrNm": "채권자명",
                            "cmmnSpldmdCnum": "공동수급업체수",
                            "untyNtceNo": "통합공고번호",
                            "sptDscrptDocUrl1": "현장설명서URL1",
                            "sptDscrptDocUrl2": "현장설명서URL2",
                            "sptDscrptDocUrl3": "현장설명서URL3",
                            "sptDscrptDocUrl4": "현장설명서URL4",
                            "sptDscrptDocUrl5": "현장설명서URL5",
                            "subsiCnsttyNm1": "부대공종명1",
                            "subsiCnsttyNm2": "부대공종명2",
                            "subsiCnsttyNm3": "부대공종명3",
                            "subsiCnsttyNm4": "부대공종명4",
                            "subsiCnsttyNm5": "부대공종명5",
                            "subsiCnsttyNm6": "부대공종명6",
                            "subsiCnsttyNm7": "부대공종명7",
                            "subsiCnsttyNm8": "부대공종명8",
                            "subsiCnsttyNm9": "부대공종명9",
                            "subsiCnsttyIndstrytyEvlRt1": "부공종업종평가비율1",
                            "subsiCnsttyIndstrytyEvlRt2": "부공종업종평가비율2",
                            "subsiCnsttyIndstrytyEvlRt3": "부공종업종평가비율3",
                            "subsiCnsttyIndstrytyEvlRt4": "부공종업종평가비율4",
                            "subsiCnsttyIndstrytyEvlRt5": "부공종업종평가비율5",
                            "subsiCnsttyIndstrytyEvlRt6": "부공종업종평가비율6",
                            "subsiCnsttyIndstrytyEvlRt7": "부공종업종평가비율7",
                            "subsiCnsttyIndstrytyEvlRt8": "부공종업종평가비율8",
                            "subsiCnsttyIndstrytyEvlRt9": "부공종업종평가비율9",
                            "cmmnSpldmdMethdCd": "공동수급방식코드",
                            "cmmnSpldmdMethdNm": "공동수급방식명",
                            "stdNtceDocUrl": "표준공고서URL",
                            "brffcBidprcPermsnYn": "지사투찰허용여부",
                            "cnsttyAccotShreRateList": "공종별지분율목록",
                            "cnstrtnAbltyEvlAmtList": "시공능력평가금액목록",
                            "dsgntCmptYn": "지명경쟁여부",
                            "arsltCmptYn": "실적경쟁여부",
                            "pqEvalYn": "PQ심사여부",
                            "ntceDscrptYn": "공고설명여부",
                            "rsrvtnPrceReMkngMthdNm": "예비가격재작성방법명",
                            "mainCnsttyPresmptPrce": "주공종추정가격",
                            "orderPlanUntyNo": "발주계획통합번호",
                            "sucsfbidLwltRate": "낙찰하한율",
                            "rgstDt": "등록일시",
                            "bfSpecRgstNo": "사전규격등록번호",
                            "sucsfbidMthdCd": "낙찰방법코드",
                            "sucsfbidMthdNm": "낙찰방법명",
                            "chgDt": "변경일시",
                            "dminsttOfclEmailAdrs": "수요기관담당자이메일주소",
                            "indstrytyLmtYn": "업종제한여부",
                            "cnstrtsiteRgnNm": "공사현장지역명",
                            "rgnDutyJntcontrctYn": "지역의무공동도급여부",
                            "chgNtceRsn": "변경공고사유",
                            "rbidOpengDt": "재입찰개찰일시",
                            "ciblAplYn": "건설산업법적용대상여부",
                            "mtltyAdvcPsblYn": "상호시장진출허용여부",
                            "mtltyAdvcPsblYnCnstwkNm": "건설산업법적용대상공사명",
                            "VAT": "부가가치세",
                            "indutyVAT": "주공종부가가치세",
                            "indstrytyMfrcFldEvlYn": "주력분야평가여부",
                            "bidWgrnteeRcptClseDt": "입찰보증서접수마감일시",
                            "rgnLmtBidLocplcJdgmBssCd": "지역제한입찰소재지판단기준코드",
                            "rgnLmtBidLocplcJdgmBssNm": "지역제한입찰소재지판단기준명",
                            "class": "구분"
                            }
                 ,inplace=True)

valid_bid

for idx, row in valid_bid.iterrows():
    s_word=row["입찰공고명"]
    
    s_word = re.sub('\d{4}년~\d{4}년', '', s_word)
    s_word = re.sub('\d{4}~\d{4}년도', '', s_word)
    s_word = re.sub('\d{4}-\d{4}년도', '', s_word)
    s_word = re.sub('\d{4}-\d{4}', '', s_word)
    s_word = re.sub('\d{4}~\d{4}년', '', s_word)
    s_word = re.sub('\d{4}~\d{2}년', '', s_word)
    s_word = re.sub('\d{4}년도', '', s_word)
    s_word = re.sub('(\d{4}년)', '', s_word)
    s_word = re.sub('\d{4}년', '', s_word)
    s_word = re.sub('\d{4}', '', s_word)
    s_word = re.sub('\d{2}~\d{2}년', '', s_word)
    s_word = re.sub('\d{4}~\d{2}년', '', s_word)
    s_word = re.sub('\d{4}-\d{2}년', '', s_word)
    s_word = re.sub('\d{2} ~ \d{2}년도', '', s_word)
    s_word = re.sub('\d{2}년-\d{2}년', '', s_word)
    s_word = re.sub('\'\d{2}년도', '', s_word)
    s_word = re.sub('\d{2}년', '', s_word)
    #print(idx, s_word, "||", row["공고명"])
    
    if row["구분"] == '운영(ITO)':
        '''
        # 직전 3년 이력 조회(운영) ----- begin
        for i in range(3):
            hstrYear = str(dt.date.today().year -i -1)
            schDateFr = hstrYear + "01010000"
            schDateTo = hstrYear + "12312359"
            
            url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusServcPPSSrch'
            queryParams = '?' + parse.urlencode({ parse.quote_plus('serviceKey') : 'B1CsUiO26Y56VDOKIParM6z394FXvTQC0rafsREBzSnOl8Cc1PUFY98LOcqKq5OahD5s2AhvszA2AIIYj0KXvg==', 
                                         parse.quote_plus('pageNo') : '1', 
                                         parse.quote_plus('numOfRows') : 10, 
                                         parse.quote_plus('type') : 'json' ,
                                         parse.quote_plus('inqryDiv') : '1', 
                                         parse.quote_plus('inqryBgnDt') : schDateFr, 
                                         parse.quote_plus('inqryEndDt') : schDateTo, 
                                         parse.quote_plus('intrntnlDivCd') : '1',
                                         parse.quote_plus('bidNtceNm') : s_word
                                    })
            response = urlopen(url + queryParams)
            data = response.read()
            JSON_object = json.loads(data.decode('utf-8'))
            #print(JSON_object)
            searchedCnt = JSON_object["response"]["body"]["totalCount"]
            
            # 이력이 있으면
            if searchedCnt > 0:
                history = pd.DataFrame(JSON_object["response"]["body"]["items"], columns = ["bidNtceNo",
                                         "bidNtceNm",
                                         "bidwinnrNm",
                                         "bidwinnrBizno",
                                         "bidwinnrCeoNm",
                                         "sucsfbidAmt"])
                # 이력 추가
                for index, item in history.iterrows():
                    valid_bid.loc[idx, hstrYear + "(공고번호/공고명/낙찰업체/사업자번호/대표자명/입찰금액)"] = str(item['bidNtceNo']) + " / " + item['bidNtceNm'] + " / " + item['bidwinnrNm'] + " / " + str(item['bidwinnrBizno']) + " / " + item['bidwinnrCeoNm'] + " / " + str(item['sucsfbidAmt']) + " / "
        
        # 직전 3년 이력 조회 ----- end
        '''
    else:
        '''
        # 구축 또는 개발 사업
        
        # 직전 3년 이력 조회(구축) ----- begin
        for i in range(3):
            hstrYear = str(dt.date.today().year -i -1)
            schDateFr = hstrYear + "01010000"
            schDateTo = hstrYear + "12312359"
            
            url = 'http://apis.data.go.kr/1230000/BidPublicInfoService/getBidPblancListInfoServcPPSSrch'
            queryParams = '?' + parse.urlencode({ parse.quote_plus('serviceKey') : 'B1CsUiO26Y56VDOKIParM6z394FXvTQC0rafsREBzSnOl8Cc1PUFY98LOcqKq5OahD5s2AhvszA2AIIYj0KXvg==', 
                                                 parse.quote_plus('pageNo') : '1', 
                                                 parse.quote_plus('numOfRows') : 10, 
                                                 parse.quote_plus('type') : 'json' ,
                                                 parse.quote_plus('inqryDiv') : '1', 
                                                 parse.quote_plus('inqryBgnDt') : schDateFr, 
                                                 parse.quote_plus('inqryEndDt') : schDateTo, 
                                                 parse.quote_plus('intrntnlDivCd') : '1',
                                                 parse.quote_plus('bidNtceNm') : '구축',
                                                 parse.quote_plus('dminsttNm') : row["수요기관"]
                                    })
            response = urlopen(url + queryParams)
            data = response.read()
            JSON_object = json.loads(data.decode('utf-8'))
            #print(JSON_object)
            searchedCnt = JSON_object["response"]["body"]["totalCount"]
            
            # 이력이 있으면
            if searchedCnt > 0:
                historyBid = pd.DataFrame(JSON_object["response"]["body"]["items"], columns = ["bidNtceNo"])
                
                # 이력 추가
                for index, item in historyBid.iterrows():
                    historyBidNo = item['bidNtceNo']
                    
                    url = 'http://apis.data.go.kr/1230000/ScsbidInfoService/getScsbidListSttusServcPPSSrch'
                    queryParams = '?' + parse.urlencode({ parse.quote_p
                    lus('serviceKey') : 'B1CsUiO26Y56VDOKIParM6z394FXvTQC0rafsREBzSnOl8Cc1PUFY98LOcqKq5OahD5s2AhvszA2AIIYj0KXvg==', 
                                                 parse.quote_plus('pageNo') : '1', 
                                                 parse.quote_plus('numOfRows') : 10, 
                                                 parse.quote_plus('type') : 'json' ,
                                                 parse.quote_plus('inqryDiv') : '1', 
                                                 parse.quote_plus('inqryBgnDt') : schDateFr, 
                                                 parse.quote_plus('inqryEndDt') : schDateTo, 
                                                 parse.quote_plus('intrntnlDivCd') : '1',
                                                 parse.quote_plus('bidNtceNo') : historyBidNo
                                    })
                    response = urlopen(url + queryParams)
                    data = response.read()
                    JSON_object = json.loads(data.decode('utf-8'))
                    #print(JSON_object)
                    searchedCnt = JSON_object["response"]["body"]["totalCount"]
                    
                    # 이력이 있으면
                    if searchedCnt > 0:
                        history = pd.DataFrame(JSON_object["response"]["body"]["items"], columns = ["bidNtceNo",
                                         "bidNtceNm",
                                         "bidwinnrNm",
                                         "bidwinnrBizno",
                                         "bidwinnrCeoNm",
                                         "sucsfbidAmt"])
                        
                        # 이력 추가
                        for index, item in history.iterrows():
                            valid_bid.loc[idx, hstrYear + "winnr"] = str(item['bidNtceNo']) + " / " + item['bidNtceNm'] + " / " + item['bidwinnrNm'] + " / " + str(item['bidwinnrBizno']) + " / " + item['bidwinnrCeoNm'] + " / " + str(item['sucsfbidAmt']) + " EoL "
        
        # 직전 3년 이력 조회 ----- end
    '''
    
#valid_bid   

# export to csv file
#df.to_csv("/home/jonghyun/workspace/open_api/g2b_bid_plan.csv", header=True, index=True)
#valid_bid.to_csv("./g2b_bid_plan_software("+ str(dt.date.today()) +").csv", header=True, index=True)
#valid_bid.to_csv("./g2b_bid_plan_software("+ str(dt.date.today()) +").csv", header=True, index=True)
valid_bid.to_excel("./g2b_bid_plan_software("+ str(dt.date.today()) +").xlsx", header=True, index=True)