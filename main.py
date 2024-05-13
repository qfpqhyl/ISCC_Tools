import requests
from bs4 import BeautifulSoup
import json
import re

url1 = "写你自己的练武题主页"
url2 = "写你自己的擂台赛主页"
MacaronSession = '你自己的token'

def get_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 4:  # 确保有足够的<td>标签
            row = {
                'name': tds[0].get_text(strip=True),
                'type': tds[1].get_text(strip=True),
                'score': tds[2].get_text(strip=True),
                'time': tds[3].get_text(strip=True),
            }
            data.append(row)
    return data

def get_name_set(data):
    name_set = set()
    for row in data:
        name_set.add(row['name'])
    return name_set

def get_name1(headers):
    url3 = "https://information.isclab.org.cn/wpupload/getdata"
    name1 = set()

    for i in range(1, 4):
        payload = {"pageindex": str(i)}
        response = requests.post(url3, headers=headers, json=payload)
        data = json.loads(response.content)
        for item in data["data"]:
            filename = item["Filename"]
            match = re.search(r'-([\w\W]+)_', filename)
            if match:
                title = match.group(1)
                name1.add(title)
    return name1

def main():

    data1 = get_data_from_url(url1)
    data2 = get_data_from_url(url2)

    print("练武共有"+str(len(data1)-1))
    print("打擂共有"+str(len(data2)))

    name_set1 = get_name_set(data1)
    name_set2 = get_name_set(data2)
    name_set = name_set1.union(name_set2)
    name_set.remove('Choice')
    name_set.remove('实战题')
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "17",
    "Content-Type": "application/json",
    "Cookie": "MacaronSession="+MacaronSession,
    "Host": "information.isclab.org.cn",
    "Origin": "https://information.isclab.org.cn",
    "Referer": "https://information.isclab.org.cn/wpupload",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    name1 = get_name1(headers)
    print('未提交wp的有以下题目：')
    for i in name_set-name1:
        print(i)

if __name__ == "__main__":
    main()