#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint

from beautiBot_for_loki import result as beautiBot

logging.basicConfig(level=logging.INFO) 

# <取得多輪對話資訊>
client = discord.Client()

mscDICT = {# "userID": {Template}
           }
# </取得多輪對話資訊>

with open("account.info.py", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
# 另一個寫法是：accountDICT = json.load(open("account.info", encoding="utf-8"))


#punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")

#def getLokiResult(inputSTR, intentSTR=""):
    #punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    #inputLIST = punctuationPat.sub("\n", inputSTR).split("\n") #斷句："一杯特級綠茶，不要糖，不要冰塊" > ["一杯特級綠茶", "不要糖", "不要冰塊"]
    #if intentSTR != "":
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
    
    # Greetings
    try:
        print("client.user.id =", client.user.id, "\nmessage.content =", message.content)
        msgSTR = re.sub("<@[!&]{}> ?".format(client.user.id), "", message.content)    # 收到 User 的訊息，將 id 取代成 ""
        logging.info(msgSTR)
        #print("msgSTR =", msgSTR)
        replySTR = ""    # Bot 回應訊息

        if msgSTR in ["哈囉","嗨","你好","您好","在嗎"]:
            replySTR = "嗨嗨，您需要什麼服務呢？"
            await message.reply(replySTR)
            return
        #else:
            #replySTR = "我是醫美bot喔！有沒有相關問題想問我呀？"

    except Exception as e:
        logging.error("[MSG greetings ERROR] {}".format(str(e)))
    
    
    lokiResultDICT = beautiBot(msgSTR)    # 取得 Loki 回傳結果
    logging.info(lokiResultDICT)  
    
    # 多輪對話
    try:
        if lokiResultDICT:
            if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
                mscDICT[client.user.id] = {"bodypart": "",
                                           "request": "",
                                           "confirm": None,
                                           "queryIntentSTR": "",
                                           "bodyQuestionSTR": "",
                                           "updatetime": datetime.now()
                                           } 
                #logging.info(mscDICT)
            else: 
                # 處理時間差
                timeNew = datetime.now() # 取得當下時間
                timeOld = mscDICT[client.user.id]["updatetime"] # 取得上一輪對話的時間
                timeNewSTR = datetime.strptime(str(timeNew),"%Y-%m-%d %H:%M:%S.%f")
                timeOldSTR = datetime.strptime(str(timeOld),"%Y-%m-%d %H:%M:%S.%f")
                timeDIFF = (timeNewSTR - timeOldSTR).seconds # 以秒為單位
                # 5 分鐘以內都算是舊對話
                if timeDIFF <= 300:
                    mscDICT[client.user.id]["updatetime"] = timeNew
                    
                    # 先處理「簡答題」
                    if mscDICT[client.user.id]["bodyQuestionSTR"] in ["請問是大腿還是小腿呢？","大腿還是小腿呢？","請問想處理哪個部位呢？"]:
                        if "大腿" in msgSTR:
                            mscDICT[client.user.id]["bodypart"] = "大腿"
                            mscDICT[client.user.id]["request"] == True # 因為會問「請問是大腿還是小腿呢？」，代表前提request要成立
                        if "小腿" in msgSTR:
                            mscDICT[client.user.id]["bodypart"] = "小腿"
                            mscDICT[client.user.id]["request"] == True 

                    # 再處理「是非題」      
                    else:
                        QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["queryIntentSTR"]])
                        if QlokiResultDICT["confirm"] != "":
                            mscDICT[client.user.id]["confirm"] = QlokiResultDICT["confirm"]
                            logging.info(QlokiResultDICT)

                    
            
            for k in lokiResultDICT.keys():    # 將 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
                if k == "bodypart":
                    mscDICT[client.user.id]["bodypart"] = lokiResultDICT["bodypart"]
                if k == "request":
                    mscDICT[client.user.id]["request"] = lokiResultDICT["request"]
                if k == "confirm":
                    mscDICT[client.user.id]["confirm"] = lokiResultDICT["confirm"]
                if k == "msg":
                    replySTR = lokiResultDICT[k]
                #else:
                    #replySTR = "你是要詢問療程相關的事情嗎？"
                    
    except Exception as e:
        logging.error("[MSG lokiResultDICT ERROR] {}".format(str(e)))


    # bot回覆
    try:
        if lokiResultDICT:
            # input == "我想要除腿的毛"
            # 第一輪和多輪的回覆
            if mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] != "":
                if mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] != "":
                    replySTR = "OK啊，我就幫您安排{}的除毛療程囉，好不好？".format(mscDICT[client.user.id]["bodypart"])
                    mscDICT[client.user.id]["queryIntentSTR"] = "confirm"

                elif mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":
                    if mscDICT[client.user.id]["bodypart"] == "腿":
                        replySTR = "請問是大腿還是小腿呢？"
                        mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                        mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                        
                    elif mscDICT[client.user.id]["bodypart"] == "手臂":
                        replySTR = "請問是上手臂還是下手臂呢？"
                        mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                        mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                        
                    elif mscDICT[client.user.id]["bodypart"] == "手":
                        replySTR = "請問是手指、手背還是全手呢？"
                        mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                        mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                        
                    elif mscDICT[client.user.id]["bodypart"] == "脖子" or mscDICT[client.user.id]["bodypart"] == "頸部":
                        replySTR = "請問是前頸還是後頸呢？"
                        mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                        mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                    else:
                        replySTR = "沒問題呀，我就幫您安排{}的除毛療程囉，好不好？".format(mscDICT[client.user.id]["bodypart"])
                        mscDICT[client.user.id]["queryIntentSTR"] = "confirm"

                    
                    
            # #############################################################################
            
            # input == "我腿毛好長"
            # 第一輪的回覆
            elif mscDICT[client.user.id]["request"] == "" and mscDICT[client.user.id]["bodypart"] != "":
                if mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] != "":  
                    if mscDICT[client.user.id]["bodypart"] != "毛":
                        if mscDICT[client.user.id]["bodypart"] == "腿":   
                            replySTR = "大腿還是小腿呢？"
                            mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                            mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                            
                        elif "手臂" in mscDICT[client.user.id]["bodypart"]:
                            replySTR = "上手臂還是下手臂呢？"
                            mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                            mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
    
                        elif "手" in mscDICT[client.user.id]["bodypart"]:
                            replySTR = "手指、手背還是全手呢？"
                            mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                            mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                            
                        elif "脖子" in mscDICT[client.user.id]["bodypart"] or "頸部" in mscDICT[client.user.id]["bodypart"]:
                            replySTR = "前頸還是後頸呢？"
                            mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                            mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                            
                        else:
                            replySTR = "那我就幫您安排{}的除毛療程囉，好嗎？".format(mscDICT[client.user.id]["bodypart"])
                            mscDICT[client.user.id]["queryIntentSTR"] = "confirm"                    


            # #############################################################################
        
            # input == "我想除毛" 
            # 第一輪的回覆
            elif mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] == "":
                if mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":  
                    replySTR = "請問想處理哪個部位呢？"
                    mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                    mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                
            else:
                replySTR = "？？？"
                                 
    except Exception as e:
        logging.error("[MSG scene3 ERROR] {}".format(str(e)))


    #print("mscDICT =")
    pprint(mscDICT)

    #if mscDICT[client.user.id]["completed"]:    # 清空 User Dict
        #del mscDICT[client.user.id]

    if replySTR:    # 回應 User 訊息
        await message.reply(replySTR)
    return

    #except Exception as e:
        #logging.error("[MSG ERROR] {}".format(str(e)))
        #print("[MSG ERROR] {}".format(str(e)))


if __name__ == "__main__":
    client.run(accountDICT["discord_token"])

    #print(beautiBot("我腿毛好長"))
    
    #臉可以嗎
    #想除腿毛
    