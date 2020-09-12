import pandas as pd
import requests
from requests import get
from openpyxl.workbook import Workbook
my_api_key = "7b223972a523c778b978119f006377298a78e966"

#### blog.naver.com/dh3508/221798911085
# 1단계 고유번호 XML 파일을 zip 파일로 다운로드
def download(url, file_name):
  with open(file_name, "wb") as file:
    response = get(url)
    file.write(response.content)

if __name__ == '__main__':
  url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={0}".format(my_api_key)
  download(url, "codes.zip")

#### 2단계 xml 파일 읽고 엑셀로 저장
from xml.etree.ElementTree import parse
tree = parse('./codes/CORPCODE.xml')
root = tree.getroot()
kids = root.getchildren()

data = []
for child in kids:
  if child.tag == "list":
    temp = []
    for i in child:
      temp.append(i.text)
    data.append(temp)

고유번호 = []
회사이름 = []
종목코드 = []
변경일 = []

for i in data:
    고유번호.append(i[0])
    회사이름.append(i[1])
    종목코드.append(i[2])
    변경일.append(i[3])
df = pd.DataFrame({"고유번호":고유번호, "회사이름":회사이름, "종목코드":종목코드, "변경일":변경일})
df.to_excel("회사고유번호.xlsx")

# # print (df. head())

##################################################

df2 = df.loc[df["회사이름"]=="삼성전자"]
print(df2["고유번호"].values)
print(df2["회사이름"].values)


# # 특정단어 포함한 회사찾기
# df2 = df.loc[df["회사이름"].str.contains('현대중공업')]
# print(df2)

# 딕셔너리 어펜드 테스트

# dict1 = {"회사명":"삼성전자", "매출액": 100}
# dict2 = {"회사명":"한국조선해양", "매출액": 200}

# print(dict1.values())
# print(dict1.values(0))

# df1 = dict1.DataFrame({"회사명":dcit.values()}

# df1 =  dict1.DataFrame("회사명", "매출액")
# print(df1)
