# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 16:07:11 2023

@author: ozasd
"""
import sys
import os
import requests
sys.path.append('..')
# print(os.path.dirname(os.path.abspath(__file__)))
from bs4 import BeautifulSoup
import modal.stock  as stock

class botcontrollers:
    def __init__(self,bot,message):
        self.bot = bot 
        self.message = message
    def comfirm (self,username = []):
        if self.message.chat.last_name in username:
            # self.bot.send_message(self.message.chat.id, f"你好 {self.message.chat.last_name} !")
            return True
        else:
            self.bot.send_message(self.message.chat.id, f"{ self.message.chat.last_name} 你沒有使用權限 !")
            return False
        
    def handle_message(self):
        message = self.message
        bot = self.bot
        stock_id = message.json['text']
        if '.' not in stock_id:
            stock_id+='.TW'
        chat_id = message.chat.id
        href = f'https://tw.stock.yahoo.com/quote/{stock_id}'
        bot.send_message(message.chat.id, f"正在搜尋股票 ...")
        response = requests.get(href)
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.find('h1',class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)') != None:
            bot.send_message(chat_id, href)
            bot.send_message(chat_id, "正在抓取新聞...")
            hrefs = stock.stock.get_yahool_link(stock_id)
            for href in hrefs[0:1]:
                bot.send_message(chat_id, href)
                yahool_news = stock.stock.get_yahool_news(hrefs)
                bot.send_message(chat_id, "正在分析新聞...")
                text_count = stock.stock.get_jieba(yahool_news)
                bot.send_message(chat_id, "正在製圖...")
                stock.stock.get_wordcloud(text_count,stock_id)
                bot.send_message(chat_id, "1. 最近新聞關鍵詞出現次數")
                photo = open(f"./modal/img/C{stock_id}.png",'rb')
                bot.send_photo(chat_id,photo)
                bot.send_message(chat_id, "2. 新聞關鍵字的文字雲")
                photo = open(f"./modal/img/W{stock_id}.png",'rb')
                bot.send_photo(chat_id,photo)
                stock.stock.get_sentiment(yahool_news,stock_id)
                bot.send_message(chat_id, "3. 近幾則新聞情續圖")
                photo = open(f"modal/img/S{stock_id}.png",'rb')
                bot.send_photo(chat_id,photo)
                bot.send_message(chat_id, "* 藍色正面 紅色負面")
            
        else:
            bot.send_message(chat_id, "請輸入正確股票")
            return False
    def handle_img(self):
        message = self.message
        bot = self.bot
        chat_id = message.chat.id
        stock_id = '3008.TW'
        print(f"./img/C{stock_id}.png")
        photo = open(f"./modal/img/C{stock_id}.png",'rb')
        bot.send_photo(chat_id,photo)
        photo = open(f"./modal/img/W{stock_id}.png",'rb')
        bot.send_photo(chat_id,photo)
        photo = open(f"./modal/img/S{stock_id}.png",'rb')
        bot.send_photo(chat_id,photo)


if __name__ == '__main__':
    stock.get_yahool_link("00878.TW")

    pass

        
        
      
        
        
                
        
   
        
        
        
        
        

