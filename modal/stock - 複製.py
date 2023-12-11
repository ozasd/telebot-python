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
import seaborn as sns
jieba.set_dictionary('./modal/big/dict.txt.big') 
jieba.load_userdict('./modal/big/stock.txt.big')
font1 = font(fname="./modal/font/NotoSansTC-VariableFont_wght.ttf",size=18)
plt.figure(dpi=1000)



class stock:
    def __init__(self,stock = None ,message = None,bot = None):
        self.stock =  stock
        self.news_href = []
        self.months = 6
        self.yahool_news = {}
        self.count_dict = {}
        self.bot = bot
        self.message = message
        
        
    def get_yahool_link(self):

        yahoo_news = f'https://tw.stock.yahoo.com/quote/{self.stock}/news'
        page = requests.get(yahoo_news)
        soup = BeautifulSoup(page.text, 'lxml')
        news_list = soup.find_all("li", class_="js-stream-content Pos(r)")
        # 抓版面的新聞 link
        news_href = []
        for news in news_list:
            href = news.find('a',class_="Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled")
            news_href.append(href['href'])
            
        self.news_href = news_href
        return news_href
    
    def get_wordcloud(self):
        # 格式設定
         print(self.count_dict)
         font_path = './font/NotoSansTC-VariableFont_wght.ttf' # 設定字體格式
         wc = wordcloud.WordCloud(background_color='white',
                                  margin=2, # 文字間距
                                  max_words=200, # 取多少文字在裡面
                                  font_path=font_path, # 設定字體
                                  width=1080, height=720, # 長寬解析度
                                  relative_scaling=0.5 # 詞頻與詞大小關聯性
                                  )
         # 生成文字雲
         wc.generate_from_frequencies(self.count_dict) # 吃入次數字典資料
         wc.to_file(f'./img/W{self.stock}.png')
         plt.imshow(wc)
         plt.show()
         sorted_data = sorted(self.count_dict.items(), key=lambda x: x[1], reverse=True)
         labels, values = zip(*sorted_data[:20])
        
        # 製作長條圖
         colors = sns.color_palette("pastel")

         plt.bar(range(len(labels)), values, tick_label=labels,color=colors)
         plt.xticks(rotation=90,fontproperties=font1)  # 如果標籤太多，可以旋轉標籤以避免重疊
         plt.xlabel('詞彙',fontproperties=font1)
         plt.ylabel('出現次數',fontproperties=font1)
         plt.title('詞彙出現次數長條圖',fontproperties=font1)
         
         plt.savefig(f'./img/C{self.stock}.png',bbox_inches = 'tight')
         plt.show()
                 
         
         
    def get_jieba(self):
        count_dict = {}
        
        stopword = [
            '會','報導','前','元','營收','占','是','已','更','但','且','仍','讓','將','次','月','然','有','月','年','日','的', '也', '及', '與', '和', '或', '而', '乃', '之', '乎', '所', '以', '於', '為', '爲', '在', '對', '由', '被', '自',',',' ','，','(',')','。','※','!','•','-',':','＋','：', '；','/','.','「','】', '」', '！','？','【', '1','、','（', '）','％', '／','～'
        ]
        for j,text in enumerate(self.yahool_news['values']):
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
        
    
    def get_yahool_news (self):
        labels = []
        values = []
        print(self.news_href)
        for url in self.news_href:
            self.bot.send_message(self.message.chat.id, url)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            time = soup.find('div',class_="caas-attr-time-style")
            time = time.find('time')['datetime']
            time = datetime.strptime(time ,'%Y-%m-%dT%H:%M:%S.%fZ')
            current_datetime = datetime.now()
            new_datetime = current_datetime - relativedelta(months=self.months)
            if time  >  new_datetime:
                content = soup.find('div',class_="caas-body")
                content = content.find_all('p')
                text = ''
                for p in content:
                    text += p.text + ','
                # time = f"{time.year}/{time.month}/{time.day}"
                labels.append(time)
                values.append(text)
            else:
                break
            
            
        yahool_news = {
            'labels':labels,
            'values':values
            }

        # Combine 'labels' and 'values' into a list of tuples
        combined_data = list(zip(yahool_news['labels'], yahool_news['values']))
        
        # Sort the list of tuples based on the date values
        sorted_data = sorted(combined_data, key=lambda x: x[0])
        
        # Extract sorted 'labels' and 'values' lists
        sorted_labels, sorted_values = zip(*sorted_data)
        
        yahool_news = {
            'labels':sorted_labels,
            'values':sorted_values
            }
        
        return yahool_news
    
    def get_sentiment(self):
            
        
        # # 設定目標 URL
        url = "http://120.125.73.101/~asisweb/textcloud/sentiment.php"
        
        x1 = []
        y1 = []
        y2 = []
        for j,k in enumerate(self.yahool_news['values']):
            time = self.yahool_news['labels'][j]
            content = self.yahool_news['values'][j]
            # 準備標頭，指定 Content-Type 為 application/x-www-form-urlencoded
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
    
            # 將內容轉為字典，以符合 requests.post 的要求
            data = {"content": content}
            # 發送 POST 請求
            response = requests.post(url, data=data, headers=headers)
            # 顯示伺服器回應
        
            text = [round(float(i)*100,2) for i in response.text.split(',')]
            x1.append(time)
            y1.append(text[0])
            y2.append(text[1])

        
        

        plt.plot(x1, y1, color='blue', linestyle="-", linewidth="2", markersize="16", marker=".", label="Postive")
        plt.plot(x1, y2, color='red', linestyle="-", linewidth="2", markersize="16", marker=".", label="Negative")
        plt.tight_layout()
        plt.xticks(rotation=90,fontproperties=font1)  # 如果標籤太多，可以旋轉標籤以避免重疊
        plt.xlabel('日期',fontproperties=font1)
        plt.ylabel('情緒',fontproperties=font1)
        plt.title('情緒折線圖',fontproperties=font1)
        plt.savefig(f'./img/S{self.stock}.png',bbox_inches = 'tight')

        # # 顯示圖形
        plt.show()
        
        
        
        # return sentiments
    def main(self):
        chat_id = self.message.chat.id
        bot =  self.bot
        bot.send_message(chat_id, "正在抓取新聞...")
        self.news_href = self.get_yahool_link()
        self.yahool_news = self.get_yahool_news()
        bot.send_message(chat_id, "正在資料分析...")
        self.count_dict = self.get_jieba()
        bot.send_message(chat_id, "正在製圖...")
        self.get_wordcloud()
        photo = open("modal/img/W{self.stock}.png",'rb')
        self.bot.send_photo(chat_id,photo)
        photo = open("modal/img/{self.stock}.png",'rb')
        self.bot.send_photo(chat_id,photo)
        bot.send_message(chat_id, "正在製圖...")
        self.get_sentiment()
        photo = open("modal/img/{self.stock}.png",'rb')
        self.bot.send_photo(chat_id,photo)
        bot.send_message(chat_id, "結束 ...")

            
        
        
        
if __name__ == '__main__':
    # stock('3008.TW').main()
    pass






