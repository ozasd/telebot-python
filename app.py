# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 15:49:35 2023

@author: ozasd
"""

import telebot
import controllers.botcontrollers as botcontrollers
from telebot.util import quick_markup

class telegram_bot:
    def __init__ (self):
        self.token = '5986646521:AAG5lQ8x_FlMDEMNuD316xuJsJri27jcqmI' # 正式機
        # self.token = '6884590924:AAG1EKkecO9ByDLTXze9A_1bDHI0Ws2fS0s' # 測試機
        self.username = ['youSheng']
        self.bot = None

    def create_bot(self):
        self.bot = telebot.TeleBot(self.token)

        
    def run(self):
        @self.bot.message_handler(commands=['start', 'hello'])
        def handle_start(message):
            controllers = botcontrollers.botcontrollers(self.bot,message)
            if controllers.comfirm(self.username) == True:
                self.bot.send_message(message.chat.id, "登入成功")

        @self.bot.message_handler(commands=['img'])
        def handle_message(message):
            controllers = botcontrollers.botcontrollers(self.bot,message)
            if controllers.comfirm(self.username) == True:
                controllers = controllers.handle_img()

        @self.bot.message_handler()
        def handle_message(message):
            controllers = botcontrollers.botcontrollers(self.bot,message)
            if controllers.comfirm(self.username) == True:
                controllers = controllers.handle_message()

               
                

                
        self.bot.infinity_polling()


        
        

if __name__ == '__main__':
    app = telegram_bot()
    app.create_bot()
    app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    