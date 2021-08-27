#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint

from beautiBot_for_loki import Result as beautiBot

logging.basicConfig(level=logging.CRITICAL)

# <取得多輪對話資訊>
client = discord.Client()

mscDICT = {
    # "userID": {Template}
}
# </取得多輪對話資訊>

with open("account.info.py", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
# 另一個寫法是：accountDICT = json.load(open("account.info", encoding="utf-8"))


#punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")

#def getLokiResult(inputSTR, intentSTR=None):
    #punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    #inputLIST = punctuationPat.sub("\n", inputSTR).split("\n") #斷句："一杯特級綠茶，不要糖，不要冰塊" > ["一杯特級綠茶", "不要糖", "不要冰塊"]
    #if intentSTR != None:
        #filterLIST = [intentSTR]
    #else:
        #filterLIST = []
    #resultDICT = runLoki(inputLIST, filterLIST) #resultDICT["confirmation"] = True/False
    #print("Loki Result => {}".format(resultDICT))
    #return resultDICT



@client.event
async def on_ready():
    logging.info("[READY INFO] {} has connected to Discord!".format(client.user))
    print("[READY INFO] {} has connected to Discord!".format(client.user))


@client.event
async def on_message(message):
    #if message.channel.name != "dt_intern":
        #return

    if not re.search("<@[!&]{}> ?".format(client.user.id), message.content):    # 只有 @Bot 才會回應
        return

    if message.author == client.user:
        return

    try:
        print("client.user.id =", client.user.id, "\nmessage.content =", message.content)
        msgSTR = re.sub("<@[!&]{}> ?".format(client.user.id), "", message.content)    # 收到 User 的訊息，將 id 取代成 ""
        print("msgSTR =", msgSTR)
        replySTR = ""    # Bot 回應訊息

        if msgSTR in ["哈囉", "嗨", "你好", "您好"]:
            replySTR = "Hi 您好，今天想辦什麼業務呢？"
            await message.reply(replySTR)
            return

        lokiResultDICT = beautiBot(msgSTR)    # 取得 Loki 回傳結果
        print(lokiResultDICT)

        if lokiResultDICT:
            if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
                mscDICT[client.user.id] = {"bodypart": "",
                                           "request": "",
                                           "confirm": "",
                                           "queryIntentSTR": "<request/bodypart/confirm>"
                                           }  #"updatetime": datetime.now()
                print(mscDICT)
              
            else: 
                pass
            for k in lokiResultDICT.keys():    # 將 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
                if k == "bodypart":
                    mscDICT[client.user.id]["bodypart"] = lokiResultDICT["bodypart"]
                if k == "request":
                    mscDICT[client.user.id]["request"] = lokiResultDICT["request"]
                #elif k == "msg":
                    #replySTR = lokiResultDICT[k]
                    #if "loan_type" in lokiResultDICT:
                        #mscDICT[client.user.id]["loan_type"] = lokiResultDICT["loan_type"]
                    #if mscDICT[client.user.id]["credit"] == {} and mscDICT[client.user.id]["mortgage"] == {}:
                        #replySTR += "\n請問您從事什麼工作呢？"
                    #print("Loki msg:", replySTR, "\n")
                if "confirm" in lokiResultDICT.keys() and lokiResultDICT["confirm"] == True:
                    replySTR = "好的，謝謝。"
                else:
                    replySTR = "你是要詢問療程相關的事情嗎？"

                #now = datetime.now() #取得當下時間
                #if now - mscDICT[client.user.id]["updatetime"] <= 5min:
                    #mscDICT[client.user.id]["updatetime"] = now

            QlokiResultDICT = beautiBot(msgSTR, mscDICT[client.user.id]["queryIntentSTR"])
            #QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id], "yesORno"])

            #if QlokiResultDICT["queryIntentSTR"] == None: #回覆的答案，和 bot 的提問無關
                ##if lokiResultDICT["type"] == "question":
                #if "療程" in msgSTR: #療程多少錢？
                    #replySTR = "您說的是哪一個療程？"
                #else:
                    #replySTR = "請問您的意思是？"
                    ##lokiResultDICT["answer"] = "<從 Loki_question intent 中取得的回覆>"


            # Scenario 1
            # input == "我[腿]毛好長"
            if mscDICT[client.user.id]["bodypart"] != "" and mscDICT[client.user.id]["request"] == None:
                if "腿" in mscDICT[client.user.id]["bodypart"]:
                    replySTR = "你是指大腿還是小腿呢？"
                    mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                elif "手臂" in mscDICT[client.user.id]["bodypart"]:
                    replySTR = "你是指上手臂還是下手臂呢？"
                    mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                else:
                    replySTR = "請問您是要 {} 的除毛療程嗎？".format(mscDICT[client.user.id]["bodypart"])
                    mscDICT[client.user.id]["queryIntentSTR"] = "confirm"
            
            
            # Scenario 2
            # input == "我]想[除毛]"                    
            if mscDICT[client.user.id]["bodypart"] == None and mscDICT[client.user.id]["request"] == True:
                replySTR = "請問您要處理哪個部位呢？"
                mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
            else:
                replySTR = "不好意思，我們沒有處理這個部位耶！"
            
            
            # Scenario 3
            # input == "[我]想要除[腿]的毛"                     
            if mscDICT[client.user.id]["bodypart"] != "" and mscDICT[client.user.id]["request"] == True:
                replySTR = "我就幫您安排 {} 的療程囉，好不好？".format(mscDICT[client.user.id]["bodypart"])
                mscDICT[client.user.id]["queryIntentSTR"] = "confirm"
            else:
                replySTR = "請重新描述你的需求！"

        else:
            replySTR = "不好意思，你想詢問什麼服務呢？"


        print("mscDICT =")
        pprint(mscDICT)

        if mscDICT[client.user.id]["completed"]:    # 清空 User Dict
            del mscDICT[client.user.id]

        #if replySTR:    # 回應 User 訊息
            #await message.reply(replySTR)
        #return

    except Exception as e:
        logging.error("[MSG ERROR] {}".format(str(e)))
        print("[MSG ERROR] {}".format(str(e)))





if __name__ == "__main__":
    client.run(accountDICT["discord_token"])

    beautiBot("我腿毛好長")