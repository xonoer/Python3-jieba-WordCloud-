import requests
import time

from urllib.parse import urlencode

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#https://api.bilibili.com/pgc/review/short/list?media_id=1586&ps=20&sort=0
#https://api.bilibili.com/pgc/review/short/list?media_id=1586&ps=20&sort=0&cursor=78997352071387

base_url = 'https://api.bilibili.com/pgc/review/short/list?'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

comments = []

words = []

cursor = '0'

check = True

key = set()

def get_page():
    params = {
        'media_id': '1586',
        'ps': '20',
        'sort': '0',
    }
    if cursor!='0':
        params['cursor'] = str(cursor)
    url = base_url + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)

def parse_page(json):
    global cursor,check,key
    if json:
        datas = json.get('data')
        items = datas.get('list',{})
        next = datas.get('next')

        if next is None:
            check = False
            return

        if next in key:
            check = False
            print('next visited!')
            return
        else:
            key.add(next)

        cursor = next

        for item in items:
            comment = item.get('content')
            print(comment)
            comments.append(comment)

def cut(sentence):
    words.extend(jieba.lcut(sentence,cut_all=False,HMM=True))# 精确模式
#     words.extend(jieba.lcut(sentence,cut_all=True,HMM=True))# 全模式
#     words.extend(jieba.lcut_for_search (sentence, HMM=True))# 搜索引擎模式

def display():
    wc = WordCloud(
                   font_path='/Users/gs/Downloads/simheittf/simhei.ttf',
                   background_color="white",  # 背景颜色
                   max_words=100,  # 词云显示的最大词数
                   max_font_size=500,  # 字体最大值
                   min_font_size=20, #字体最小值
                   random_state=42, #随机数
                   collocations=False, #避免重复单词
                   width=1300,height=900,margin=10, #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
                  )
    print(words)
    temp = ' '.join(words)
    wc.generate(temp)
    
    plt.figure(dpi=100) #通过这里可以放大或缩小
    plt.imshow(wc, interpolation='catrom',vmax=1000)
    plt.axis("off") #隐藏坐标
    plt.show()

if __name__ == '__main__':
    while check:
        json = get_page()
        parse_page(json)
        time.sleep(1)
    for temp in comments:
        cut(temp)
    display()
