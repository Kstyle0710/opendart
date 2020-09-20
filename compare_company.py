import requests
import pandas as pd
import numpy as np
from openpyxl.workbook import Workbook
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager,rc

mpl.rcParams['axes.unicode_minus'] = False

font_path = "C:/my_develop/opendart/font/H2HDRM.TTF"
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

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

corp_codes = ["00111704"]   #"00164609", "00111704", "00126478"
target_year = "2020"
target_report = "11012"
report_type = "OFS"               #CFS:연결재무제표, OFS:재무제표

my_api_key = "7b223972a523c778b978119f006377298a78e966"
corp_codes_dict = {"00164830": "한국조선해양", "00164609": "현대미포조선", "00111704": "대우조선해양", "00126478": "삼성중공업", "00126380": "삼성전자"}
reports_dict = {"11013": "1분기보고서", "11012": "반기보고서", "11014": "3분기보고서", "11011": "사업보고서"}

for corp_code in corp_codes:
  resp=requests.get("https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={0}&corp_code={1}&bsns_year={2}&reprt_code={3}&fs_div={4}".format(my_api_key, corp_code, target_year, target_report, report_type))
  dict=resp.json()
  # print(dict)
  df1=pd.DataFrame(dict['list'])
  select_df1 = df1.loc[:,['account_nm', 'thstrm_amount']]
  select_df1 = select_df1[select_df1["account_nm"].isin(['유동자산','현금및현금성자산','재고자산', '자산총계', '유동부채', '부채총계', '매출액', '매출원가', '매출총이익', '영업이익', '영업이익(손실)', '총포괄이익', '총포괄이익(손실)'])]
  select_df1 = pd.DataFrame(select_df1).fillna(0)

  # print(select_df1)

for corp_code in corp_codes:
  resp=requests.get("https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={0}&corp_code={1}&bsns_year={2}&reprt_code={3}&fs_div={4}".format(my_api_key, corp_code, int(target_year)-1, target_report, report_type))
  dict=resp.json()
  df2=pd.DataFrame(dict['list'])
  select_df2 = df2.loc[:,['account_nm', 'thstrm_amount']]
  select_df2 = select_df2[select_df2["account_nm"].isin(['유동자산','현금및현금성자산','재고자산', '자산총계', '유동부채', '부채총계', '매출액', '매출원가', '매출총이익', '영업이익', '영업이익(손실)', '총포괄이익', '총포괄이익(손실)'])]
  select_df2 = pd.DataFrame(select_df2).fillna(0)


merged_df=pd.merge(select_df1, select_df2, how="outer", on="account_nm")
try:
  merged_df=merged_df.astype({"thstrm_amount_x":'int64', "thstrm_amount_y":'int64'})
  calculated = merged_df['thstrm_amount_x']-merged_df['thstrm_amount_y']
  merged_df["calculated"] = calculated
except:
  pass


merged_df = merged_df.rename(columns = {'thstrm_amount_x':'{}'.format(target_year), 'thstrm_amount_y':'{}'.format(int(target_year)-1)})
print(merged_df)
# merged_df[['2019', '2020']].plot(kind='bar')
merged_df.plot.barh()

plt.show()



# x_name = merged_df['account_nm'].values.tolist()
# y1_value = merged_df['{}'.format(target_year)].values.tolist()
# y2_value = merged_df['{}'.format(int(target_year)-1)].values.tolist()
# y3_value = merged_df['calculated'].values.tolist()


# plt.sublpot(2, 1, 1)
# plt.plot(x_name, y1_value, color='red')
# plt.ylabel("Money1")


# plt.sublpot(2, 1, 2)
# plt.plot(x_name, y2_value, color='blue')
# plt.ylabel("Money2")
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('title')
#
# plt.legend()
# plt.show()
#
#


# df2.to_excel("financial_report/fin_Statement_{0}_{1}_{2}_{3}.xlsx".format(report_type, target_year, reports_dict[target_report], corp_codes_dict[corp_code]))
# print("{0:+,}".format(10000000000000000))

