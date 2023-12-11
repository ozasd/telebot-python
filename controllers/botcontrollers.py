# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 16:07:11 2023

@author: ozasd
"""

import requests
from bs4 import BeautifulSoup
import sys

class botcontrollers:
    
    def comfirm (message,bot,username):
        if message.chat.last_name in username:
            # bot.send_message(message.chat.id, f"你好 {message.chat.last_name} !")
            return True
        else:
            bot.send_message(message.chat.id, f"{ message.chat.last_name} 你沒有使用權限 !")
            return False
        
    def handle_message(message,bot):
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
            return stock_id
        else:
            bot.send_message(chat_id, "請輸入正確股票")
            return False
        
        
      
        
        
                
        
   
        
        
        
        
        

