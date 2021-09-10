#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint

from beautiBot_for_loki import result as beautiBot
from botREF import handleBodypartDICT
from botREF import userDefinedDICT

logging.basicConfig(level=logging.INFO) 

# <取得多輪對話資訊>
client = discord.Client()

mscDICT = {# "userID": {Template}
           }

appointmentLIST = []
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
                                           "confirm": "",
                                           "queryIntentSTR": "",
                                           "bodyQuestionSTR": "",
                                           "therapyQuestionSTR": "",
                                           "updatetime": datetime.now(),
                                           "finish": ""
                                           } 
                #logging.info(mscDICT)
            else: 
                # 處理時間差
                datetimeNow = datetime.now()  # 取得當下時間
                timeDIFF = datetimeNow - mscDICT[client.user.id]["updatetime"]
                if timeDIFF.total_seconds() <= 30:    # 以秒為單位，5分鐘以內都算是舊對話
                    mscDICT[client.user.id]["updatetime"] = datetimeNow
                    
                # 先處理「簡答題」
                    if mscDICT[client.user.id]["bodyQuestionSTR"]:
                        if mscDICT[client.user.id]["bodyQuestionSTR"] in list(["".join(value) for value in handleBodypartDICT.values()]):
                        #if mscDICT[client.user.id]["bodyQuestionSTR"] in ["請問是大腿還是小腿呢？","大腿還是小腿呢？","請問想處理哪個部位呢？"]:
                            for v in userDefinedDICT["bodyparts"]:
                                if v in msgSTR:
                                    mscDICT[client.user.id]["bodypart"] = v
                                    mscDICT[client.user.id]["request"] = True # 因為會問「請問是大腿還是小腿呢？」，代表前提request要成立
                                    mscDICT[client.user.id]["bodyQuestionSTR"] = None # 清除問題

                # 再處理「是非題」      
                    else:
                        QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["queryIntentSTR"]])
                        logging.info(QlokiResultDICT) 
                        
                        if QlokiResultDICT["confirm"] != True:                                   # inputSTR：沒有
                            if mscDICT[client.user.id]["finish"] == None:                        # 已確認療程
                                mscDICT[client.user.id]["confirm"] = True                        # Q:「你有其他跟療程相關的疑問嗎？」
                                appointmentLIST.append(mscDICT[client.user.id])
                                mscDICT[client.user.id] = {"bodypart": "",
                                                           "request": "",
                                                           "confirm": "",
                                                           "queryIntentSTR": "",
                                                           "bodyQuestionSTR": "",
                                                           "therapyQuestionSTR": "",
                                                           "updatetime": datetime.now(),
                                                           "finish": True
                                                           } 
                                logging.info(appointmentLIST)
                                logging.info(QlokiResultDICT)  
                            elif mscDICT[client.user.id]["finish"] == "":
                                if mscDICT[client.user.id]["confirm"] == None:                     # Q:「你是不是有其他疑問呢？」
                                    appointmentLIST.append(mscDICT[client.user.id])
                                    mscDICT[client.user.id] = {"bodypart": "",
                                                               "request": "",
                                                               "confirm": None,
                                                               "queryIntentSTR": "",
                                                               "bodyQuestionSTR": "",
                                                               "therapyQuestionSTR": "",
                                                               "updatetime": datetime.now(),
                                                               "finish": "END"
                                                               } 
                                    logging.info(appointmentLIST)
                                    logging.info(QlokiResultDICT)                              
                                
                                elif mscDICT[client.user.id]["confirm"] == "":
                                    mscDICT[client.user.id]["confirm"] = QlokiResultDICT["confirm"]   # 如果確認問題得到相反的回答，清掉mscDICT重新開始
                                    appointmentLIST.append(mscDICT[client.user.id])
                                    mscDICT[client.user.id] = {"bodypart": "",
                                                               "request": "",
                                                               "confirm": None,
                                                               "queryIntentSTR": "",
                                                               "bodyQuestionSTR": "",
                                                               "therapyQuestionSTR": "",
                                                               "updatetime": datetime.now(),
                                                               "finish": ""
                                                               } 
                                    logging.info(appointmentLIST)
                                    logging.info(QlokiResultDICT)
                            
                        elif QlokiResultDICT["confirm"] == True:
                            mscDICT[client.user.id]["confirm"] = QlokiResultDICT["confirm"]
                            # once confirm, save the current appointment into appointmentLIST
                            appointmentLIST.append(mscDICT[client.user.id])
                            mscDICT[client.user.id] = {"bodypart": "",
                                                       "request": "",
                                                       "confirm": True,
                                                       "queryIntentSTR": "",
                                                       "bodyQuestionSTR": "",
                                                       "therapyQuestionSTR": "",
                                                       "updatetime": datetime.now(),
                                                       "finish": None
                                                       } 
                            logging.info(appointmentLIST)
                            logging.info(QlokiResultDICT)
                        else:
                            pass
                        
                        
            # 將第一輪對話 Loki Intent 的結果，存進 Global mscDICT 變數，可替換成 Database。
            for k in lokiResultDICT.keys():
                if k == "bodypart":
                    mscDICT[client.user.id]["bodypart"] = lokiResultDICT["bodypart"]
                if k == "request" and mscDICT[client.user.id][k] != True:
                    mscDICT[client.user.id]["request"] = lokiResultDICT["request"]
                if k == "confirm" and lokiResultDICT["confirm"] == "":
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
            # 多輪的回覆
            if mscDICT[client.user.id]["request"] == "" and mscDICT[client.user.id]["bodypart"] == "":
                if mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["finish"] == True and mscDICT[client.user.id]["bodyQuestionSTR"] == "":
                    replySTR = "謝謝你使用BeautiBot！"
                elif mscDICT[client.user.id]["confirm"] == True and mscDICT[client.user.id]["finish"] == None and mscDICT[client.user.id]["bodyQuestionSTR"] == "":
                    replySTR = "有沒有其他與療程相關的疑問呢？"
                    mscDICT[client.user.id]["queryIntentSTR"] = "confirm"   
                    
                elif mscDICT[client.user.id]["confirm"] == None and mscDICT[client.user.id]["finish"] == "END" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":
                    replySTR = "謝謝你使用BeautiBot！"                
                elif mscDICT[client.user.id]["confirm"] == None and mscDICT[client.user.id]["finish"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":
                    replySTR = "你有什麼其他的疑問呢？"

            # 第一輪的回覆
            elif mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] != "":          # input == "我想要除腿的毛"
                if mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == None:
                    replySTR = "OK啊，我就幫您安排{}的除毛療程囉，好不好？".format(mscDICT[client.user.id]["bodypart"])
                    mscDICT[client.user.id]["queryIntentSTR"] = "confirm"
                
                elif mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":
                    if mscDICT[client.user.id]["bodypart"] not in [key for key in handleBodypartDICT.keys()]:         # 需要釐清的部位
                        replySTR = "沒問題呀，我就幫您安排{}的除毛療程囉，好不好？".format(mscDICT[client.user.id]["bodypart"])
                        mscDICT[client.user.id]["queryIntentSTR"] = "confirm"  
                    else:
                        for e in handleBodypartDICT.keys():
                            if mscDICT[client.user.id]["bodypart"] == e:
                                replySTR = "".join(handleBodypartDICT[e])   # handleBodypartDICT 回傳的value是一個LIST，因此用join()把它變成STR
                                mscDICT[client.user.id]["queryIntentSTR"] = "bodypart" 
                                mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                        else:
                            pass

            elif mscDICT[client.user.id]["request"] == "" and mscDICT[client.user.id]["bodypart"] != "":           # input == "我腿毛好長"
                if mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":  
                    if mscDICT[client.user.id]["bodypart"] != "毛":
                        if mscDICT[client.user.id]["bodypart"] not in [key for key in handleBodypartDICT.keys()]:
                            replySTR = "那我就幫您安排{}的除毛療程囉，好不好？".format(mscDICT[client.user.id]["bodypart"])
                            mscDICT[client.user.id]["queryIntentSTR"] = "confirm"  
                        else:
                            for e in handleBodypartDICT.keys():
                                if mscDICT[client.user.id]["bodypart"] == e:
                                    replySTR = "".join(handleBodypartDICT[e])   # handleBodypartDICT 回傳的value是一個LIST，因此用join()把它變成STR
                                    mscDICT[client.user.id]["queryIntentSTR"] = "bodypart" 
                                    mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                            else:
                                pass                        

            elif mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] == "":          # input == "我想除毛" 
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
    