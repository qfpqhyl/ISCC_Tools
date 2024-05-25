import requests
from bs4 import BeautifulSoup
import json
import re

# training_page_url = "你的练武主页链接"
# arena_page_url = "你的擂台主页链接"
# macaron_session = 'wp页面下的macaron_session'
# page_count = wp页面下的总页数

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

def get_uploaded_filenames(headers):
    url3 = "https://information.isclab.org.cn/wpupload/getdata"
    uploaded_filenames = set()
    duplicates = set()
    
    for i in range(1, page_count+1):
        payload = {"pageindex": str(i)}
        response = requests.post(url3, headers=headers, json=payload)
        data = json.loads(response.content)
        for item in data["data"]:
            filename = item["Filename"]
            match = re.search(r'-([\w\W]+)_', filename)
            if match:
                title = match.group(1)
                if title in uploaded_filenames:
                    duplicates.add(title)
                else:
                    uploaded_filenames.add(title)
    return uploaded_filenames, duplicates

def main():

    training_data = get_data_from_url(training_page_url)
    arena_data = get_data_from_url(arena_page_url)
    print('*********************************')
    print("练武共有"+str(len(training_data)-2))
    print("打擂共有"+str(len(arena_data)))
    training_names = get_name_set(training_data)
    arena_names = get_name_set(arena_data)
    all_names = training_names.union(arena_names)
    all_names.remove('Choice')
    all_names.remove('实战题')
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "17",
    "Content-Type": "application/json",
    "Cookie": "MacaronSession="+macaron_session,
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
    
    uploaded_filenames = get_uploaded_filenames(headers)[0]
    print('有效wp有'+str(len(uploaded_filenames))+'个,共有'+str(len(all_names))+'道题')
    print('*********************************')
    
    if len(all_names - uploaded_filenames) == 0:
        print('\n')
        print('*********************************')
        print('恭喜你已经完成所有WriteUp的上传')
        print('*********************************')
    else:
        print('\n')
        print('*********************************')
        print('未提交wp的有以下题目：')
        for i in all_names - uploaded_filenames:
            print(i)
        print('*********************************')
    if get_uploaded_filenames(headers)[1]!=0:
        print('\n')
        print('*********************************')
        print('重复提交的有以下题目：')
        for i in get_uploaded_filenames(headers)[1]:
            print(i)
        print('*********************************')

if __name__ == "__main__":
    main()
