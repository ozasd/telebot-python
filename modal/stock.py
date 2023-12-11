#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 16:04:06 2023

@author: ot
"""
import wordcloud # 文字雲
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties as font
import requests
from cnsenti import Sentiment
import seaborn as sns
import pandas as pd
import numpy as np
font1 = font(fname="./modal/font/NotoSansTC-VariableFont_wght.ttf",size=18)
plt.figure(dpi=1000)
jieba.set_dictionary('./modal/big/dict.txt.big') # 
jieba.load_userdict('./modal/big/stock.txt.big')


class stock:
    def get_yahool_link(
            stock = '3008.TW'
        ):
        yahoo_news = f'https://tw.stock.yahoo.com/quote/{stock}/news'
        page = requests.get(yahoo_news)
        soup = BeautifulSoup(page.text, 'lxml')
        news_list = soup.find_all("li", class_="js-stream-content Pos(r)")
        # 抓版面的新聞 link
        news_href = []
        for news in news_list:
            href = news.find('a',class_="Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled")
            news_href.append(href['href'])
        return news_href
    
    def get_wordcloud(
            data = {},
            title = 'wordcloud'
        ):
        # 格式設定
        
         font_path = './modal/font/NotoSansTC-VariableFont_wght.ttf' # 設定字體格式
         wc = wordcloud.WordCloud(background_color='white',
                                  margin=2, # 文字間距
                                  max_words=200, # 取多少文字在裡面
                                  font_path=font_path, # 設定字體
                                  width=1080, height=720, # 長寬解析度
                                  relative_scaling=0.5 # 詞頻與詞大小關聯性
                                  )
         # 生成文字雲
         wc.generate_from_frequencies(data) # 吃入次數字典資料
         wc.to_file(f'./modal/img/W{title}.png')
         plt.imshow(wc)
         plt.show()
         sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
         labels, values = zip(*sorted_data[:20])
        
        # 製作長條圖
         colors = sns.color_palette("pastel")

         plt.bar(range(len(labels)), values, tick_label=labels,color=colors)
         plt.xticks(rotation=90,fontproperties=font1)  # 如果標籤太多，可以旋轉標籤以避免重疊
         plt.xlabel('詞彙',fontproperties=font1)
         plt.ylabel('出現次數',fontproperties=font1)
         plt.title('詞彙出現次數長條圖',fontproperties=font1)
         
         plt.savefig(f'./modal/img/C{title}.png',bbox_inches = 'tight')
         plt.show()
                 
         
         
    def get_jieba(
            yahool_news = {
                'labels':[], 
                'values':[]
                }
        ):
        count_dict = {}
        
        stopword = [
            '會','報導','前','元','營收','占','是','已','更','但','且','仍','讓','將','次','月','然','有','月','年','日','的', '也', '及', '與', '和', '或', '而', '乃', '之', '乎', '所', '以', '於', '為', '爲', '在', '對', '由', '被', '自',',',' ','，','(',')','。','※','!','•','-',':','＋','：', '；','/','.','「','】', '」', '！','？','【', '1','、','（', '）','％', '／','～'
        ]
        for j,text in enumerate(yahool_news['values']):
            text = jieba.lcut(text)
            text = [i for i in text if i not in stopword]
            for word in text:
                
                try:
                    int(word)
                except Exception:
                    word =str(word)
                    if word in count_dict:
                        count_dict[word] += 1
                    else:
                        count_dict[word] = 1
        return count_dict
        
    
    def get_yahool_news (
            news_href = [],
            months = 6
        ):
        
        labels = []
        values = []
        for url in news_href:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            time = soup.find('div',class_="caas-attr-time-style")
            time = time.find('time')['datetime']
            time = datetime.strptime(time ,'%Y-%m-%dT%H:%M:%S.%fZ')
            current_datetime = datetime.now()
            new_datetime = current_datetime - relativedelta(months=months)
            if time  >  new_datetime:
                content = soup.find('div',class_="caas-body")
                content = content.find_all('p')
                text = ''
                for p in content:
                    text += p.text + ','
                time = f"{time.year}/{time.month}/{time.day}"
                labels.append(time)
                values.append(text)
            else:
                break
            
            
        yahool_news = pd.DataFrame({})
        yahool_news['labels'] = pd.to_datetime(labels)        
        yahool_news['values'] = values
        yahool_news = yahool_news.sort_values(by="labels",ascending=True)
        yahool_news.reset_index(drop=True, inplace=True)
        return yahool_news
    
    def get_sentiment(
            yahool_news = {
                'labels':[],
                'values':[]
                },
            title = 'sentiment' 
        ):
        
        y1 = []
        y2 = []
        positive = './modal/big/positive.txt'
        negative = './modal/big/negative.txt'
        senti = Sentiment(pos=positive,  #正面词典txt文件相对路径
                          neg=negative,  #负面词典txt文件相对路径
                          merge=True,             #融合cnsenti自带词典和用户导入的自定义词典
                          encoding='utf-8')      #两txt均为utf-8编码


        for i,text in enumerate(yahool_news['values']):
            result2 = senti.sentiment_calculate(text)
            positive = result2['pos'] 
            negative = result2['neg']
            sum = positive+negative
            positive = round((positive / sum)*100)
            negative = round((negative / sum)*100)
            y1.append(positive)
            y2.append(negative)





        yahool_news['postive'] = y1
        yahool_news['negative'] = y2
        yahool_news = yahool_news.groupby(by=['labels']).agg({'values': ','.join,'postive':np.mean,'negative':np.mean})
        yahool_news.reset_index(inplace=True)
        plt.plot(yahool_news['labels'], yahool_news['postive'], color='blue', linestyle="-", linewidth="2", markersize="16", marker=".", label="Postive")
        plt.plot(yahool_news['labels'], yahool_news['negative'], color='red', linestyle="-", linewidth="2", markersize="16", marker=".", label="Negative")
        plt.tight_layout()
        plt.xticks(rotation=90,fontproperties=font1)  # 如果標籤太多，可以旋轉標籤以避免重疊
        plt.xlabel('日期',fontproperties=font1)
        plt.ylabel('情緒',fontproperties=font1)
        plt.title('情緒折線圖',fontproperties=font1)
        plt.savefig(f'./modal/img/S{title}.png',bbox_inches = 'tight')

        # # 顯示圖形
        plt.show()
        
        
        
        # return sentiments
    

        
        
        
            
        
        
        
if __name__ == '__main__':
    hrefs = stock.get_yahool_link("00878.TW")
    yahool_news = stock.get_yahool_news(hrefs)
    text_count = stock.get_jieba(yahool_news)
    stock.get_wordcloud(text_count,'00878.TW')
    stock.get_sentiment(yahool_news,'00878.TW')






