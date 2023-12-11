# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 15:49:35 2023

@author: ozasd
"""

import telebot
import controllers.botcontrollers as botcontrollers
import modal.stock as stock

class telegram_bot:
    def __init__ (self):
        self.token = '5986646521:AAG5lQ8x_FlMDEMNuD316xuJsJri27jcqmI'
        self.username = ['youSheng']
        self.bot = None
        self.botcontrollers = botcontrollers.botcontrollers
        self.stock = stock.stock

    def create_bot(self):
        self.bot = telebot.TeleBot(self.token)

        
    def run(self):
        
        @self.bot.message_handler(commands=['start', 'hello'])
        def handle_start(message):
            chat_id = message.chat.id
            if self.botcontrollers.comfirm(message=message,bot = self.bot,username = self.username) == True:
                self.bot.send_message(chat_id, "登入成功")
                     
        @self.bot.message_handler(commands=['img'])
        def handle_message(message):
            if self.botcontrollers.comfirm(message=message,bot=self.bot,username=self.username) == True:
                chat_id = message.chat.id
                stock_id = '3008.TW'
                print("./modal/img/C{stock_id}.png")
                photo = open("modal/img/{stock_id}.png",'rb')
                self.bot.send_photo(chat_id,photo)
                photo = open(f"modal/img/W{stock_id}.png",'rb')
                self.bot.send_photo(chat_id,photo)
                photo = open(f"modal/img/S{stock_id}.png",'rb')
                self.bot.send_photo(chat_id,photo)

                
                
                
                
                
        @self.bot.message_handler()
        def handle_message(message):
            chat_id = message.chat.id

            if self.botcontrollers.comfirm(message=message,bot=self.bot,username=self.username) == True:
                stock_id = self.botcontrollers.handle_message(message,self.bot)
                if  stock_id != False:
                    self.bot.send_message(chat_id, "正在抓取新聞...")
                    hrefs = self.stock.get_yahool_link(stock_id)
                    for href in hrefs[0:1]:
                        self.bot.send_message(chat_id, href)

                    yahool_news = self.stock.get_yahool_news(hrefs)
                    self.bot.send_message(chat_id, "正在分析新聞...")
                    text_count = self.stock.get_jieba(yahool_news)
                    self.bot.send_message(chat_id, "正在製圖...")
                    self.stock.get_wordcloud(text_count,stock_id)
                    photo = open(f"modal/img/C{stock_id}.png",'rb')
                    self.bot.send_message(chat_id, "1. 最近新聞關鍵詞出現次數")
                    self.bot.send_photo(chat_id,photo)
                    photo = open(f"modal/img/W{stock_id}.png",'rb')
                    self.bot.send_message(chat_id, "2. 新聞關鍵字的文字雲")
                    self.bot.send_photo(chat_id,photo)
                    self.stock.get_sentiment(yahool_news,stock_id)
                    self.bot.send_message(chat_id, "3. 近幾則新聞情續圖")
                    photo = open(f"modal/img/S{stock_id}.png",'rb')
                    self.bot.send_photo(chat_id,photo)
                    self.bot.send_message(chat_id, "* 藍色正面 紅色負面")

                    # self.stock(stock =stock_id , message=message,bot = self.bot).main()
        


                
        self.bot.infinity_polling()


        
        

if __name__ == '__main__':
    app = telegram_bot()
    app.create_bot()
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    