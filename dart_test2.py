import requests
import pandas as pd
from openpyxl.workbook import Workbook
 
'''
주요 기업 고유번호 
현대중공업지주 01205709
한국조선해양  00164830
현대중공업  01390344
현대미포조선  00164609
현대삼호중공업 00332468
대우조선해양  00111704
삼성중공업 00126478
삼성전자 00126380

'''

my_api_key = "7b223972a523c778b978119f006377298a78e966"
corp_codes = ["00164830","00164609","00111704","00126478"]
corp_codes_dict = {"00164830":"한국조선해양", "00164609":"현대미포조선", "00111704":"대우조선해양", "00126478":"삼성중공업"}
target_year = "2020"
target_report = "11012"
reports_dict = {"11013" : "1분기보고서", "11012" : "반기보고서", "11014" : "3분기보고서", "11011" : "사업보고서"}
report_type = "OFS"               #CFS:연결재무제표, OFS:재무제표

# print(corp_codes_dict["00111704"])


##============공시정보/보고서 검색=========================================
# corp_code = "00126478"
# resp=requests.get("https://opendart.fss.or.kr/api/list.json?crtfc_key={0}&corp_code={1}&bgn_de=20190117&end_de=20200117&corp_cls=Y&page_no=1&page_count=10"\
#     .format(my_api_key, corp_code))
# dict=resp.json()
# df2=pd.DataFrame(dict['list'])
# print(df2)

##======공시 임원 정보=====================================================

# corp_code = "00126478"
# resp=requests.get("https://opendart.fss.or.kr/api/exctvSttus.json?crtfc_key={0}&corp_code={1}&bsns_year=2019&reprt_code=11011".format(my_api_key, corp_code))
# dict=resp.json()
# print(dict)
# df2=pd.DataFrame(dict['list'])
# # print(df2)
# df2.to_excel("executives_{0}.xlsx".format(corp_code))

##=======직원 정보==========================================================================

# for corp_code in corp_codes:
#   resp=requests.get("https://opendart.fss.or.kr/api/empSttus.json?crtfc_key={0}&corp_code={1}&bsns_year=2018&reprt_code=11011".format(my_api_key, corp_code))
#   dict=resp.json()
#   print(dict)
#   df2=pd.DataFrame(dict['list'])
#   print(df2)
#   df2.to_excel("employee_num_{0}_{1}.xlsx".format(corp_codes_dict[corp_code], target_year))

##========단위회사 전체 재무정보(연결이 아닌 개별재무재표임)=================================

for corp_code in corp_codes:
  resp=requests.get("https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={0}&corp_code={1}&bsns_year={2}&reprt_code={3}&fs_div={4}".format(my_api_key, corp_code, target_year, target_report, report_type))
  dict=resp.json()
  # print(dict)
  df2=pd.DataFrame(dict['list'])
  # print(df2)
  df2.to_excel("financial_report/fin_Statement_{0}_{1}_{2}_{3}.xlsx".format(report_type, target_year, reports_dict[target_report], corp_codes_dict[corp_code]))

