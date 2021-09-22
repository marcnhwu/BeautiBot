#!/user/bin/env python
# -*- coding: utf-8 -*-

import logging
import discord
import json
import re
from datetime import datetime
from pprint import pprint

from Loki import result as beautiBot
from botREF import handleBodypartDICT
from botREF import userDefinedDICT
from botREF import doctorNameLIST

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

        if re.search("(hi|hello|hey|yo|哈囉|嗨|嗨嗨|[你您]好|在嗎|早安|午安|晚安|早上好|晚上好|欸|誒|ㄟ)", msgSTR.lower()):
            replySTR = "嗨嗨，你需要什麼醫美服務呢？\n可以跟我說「我想除毛」或是「我的手毛好長，好煩惱」喔^_^"
            await message.reply(replySTR)
            return
    except Exception as e:
        logging.error("[MSG greetings ERROR] {}".format(str(e)))
    
    
    lokiResultDICT = beautiBot(msgSTR)    # 取得 Loki 回傳結果
    logging.info(lokiResultDICT)  
    
    # 多輪對話
    try:
        if lokiResultDICT:
            if client.user.id not in mscDICT:    # 判斷 User 是否為第一輪對話
                mscDICT[client.user.id] = {"bodypart": None,
                                           "request": "",
                                           "confirm": "",
                                           "queryIntentSTR": "",
                                           "bodyQuestionSTR": "",
                                           "appointmentQuestionSTR": "",
                                           "appointmentClinic": "",
                                           "appointmentDoctor": "",
                                           "appointmentDay": "",
                                           "appointmentTime": "",
                                           "medicalHistory": "",
                                           "updatetime": datetime.now(),
                                           "finish": ""
                                           } 
                #logging.info(mscDICT)
            else: 
                # 處理時間差
                datetimeNow = datetime.now()  # 取得當下時間
                timeDIFF = datetimeNow - mscDICT[client.user.id]["updatetime"]
                if timeDIFF.total_seconds() <= 300:    # 以秒為單位，5分鐘以內都算是舊對話
                    mscDICT[client.user.id]["updatetime"] = datetimeNow
                    
                # 先處理「簡答題」
                    #醫療史
                    if mscDICT[client.user.id]["appointmentQuestionSTR"] == "medicalHistory":
                        if msgSTR in ["沒","沒有"]:
                            mscDICT[client.user.id]["medicalHistory"] = False
                        else:
                            QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["appointmentQuestionSTR"]])
                            logging.info(QlokiResultDICT) 
                            #for v in userDefinedDICT["medicalCondition"]:
                            if QlokiResultDICT["medicalHistory"] in userDefinedDICT["medicalCondition"]:
                                mscDICT[client.user.id]["medicalHistory"] = True
                            else:
                                mscDICT[client.user.id]["medicalHistory"] = False #ideal
                    #醫師
                    elif mscDICT[client.user.id]["appointmentQuestionSTR"] == "appointmentDoctor":
                        QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["appointmentQuestionSTR"]])
                        logging.info(QlokiResultDICT) 
                        if QlokiResultDICT["appointmentDoctor"] in doctorNameLIST:
                            mscDICT[client.user.id]["appointmentDoctor"] = QlokiResultDICT["appointmentDoctor"] 
                            logging.info(mscDICT[client.user.id])
                        else:
                            mscDICT[client.user.id]["appointmentDoctor"] = ""
                            logging.info(mscDICT[client.user.id])
                            replySTR = "請重新選擇醫師～\n【王經凱醫師(男)｜程昭瑞醫師(男)｜謝羽翔醫師(男)｜薛博駿醫師(男)｜陳棨揮醫師(男)｜劉宇婷醫師(女)】"
                    #診所位置
                    elif mscDICT[client.user.id]["appointmentQuestionSTR"] == "appointmentClinic":
                        QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["appointmentQuestionSTR"]])
                        logging.info(QlokiResultDICT) 
                        if QlokiResultDICT["appointmentClinic"] in userDefinedDICT["location"]:
                            mscDICT[client.user.id]["appointmentClinic"] = QlokiResultDICT["appointmentClinic"]                         
                        else:
                            mscDICT[client.user.id]["appointmentClinic"] = ""
                            replySTR = "請重新選擇診所～\ｎ【忠孝敦化門診｜中山門診】"
                    #預約時間
                    elif mscDICT[client.user.id]["appointmentQuestionSTR"] == "appointmentTime": 
                        QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["appointmentQuestionSTR"]])
                        logging.info(QlokiResultDICT) 
                        if QlokiResultDICT["appointmentDay"] != False and QlokiResultDICT["appointmentTime"] != False:
                            mscDICT[client.user.id]["appointmentDay"] = QlokiResultDICT["appointmentDay"]
                            mscDICT[client.user.id]["appointmentTime"] = QlokiResultDICT["appointmentTime"]    
                        elif QlokiResultDICT["appointmentDay"] == False and QlokiResultDICT["appointmentTime"] != False:
                            mscDICT[client.user.id]["appointmentDay"] = ""
                            mscDICT[client.user.id]["appointmentTime"] = QlokiResultDICT["appointmentTime"] 
                        elif QlokiResultDICT["appointmentDay"] != False and QlokiResultDICT["appointmentTime"] == False:
                            mscDICT[client.user.id]["appointmentDay"] = QlokiResultDICT["appointmentDay"] 
                            mscDICT[client.user.id]["appointmentTime"] = ""
                        else:
                            mscDICT[client.user.id]["appointmentDay"] = ""
                            mscDICT[client.user.id]["appointmentTime"] = ""                            
                            replySTR = "請重新選擇看診時間～\n【星期一12:30~17:00、18:00~20:30\n星期二 12:30~17:00、18:00~20:30\n星期三 14:00~17:00、18:00~20:30\n星期四 12:30~17:00、18:00~20:30\n星期五 12:30~17:00、18:00~20:30\n星期六 12:30~17:00、18:00~20:30\n(星期日為診所休息日)】"                         
                     

                    elif mscDICT[client.user.id]["bodyQuestionSTR"]:
                        if mscDICT[client.user.id]["bodyQuestionSTR"] in list(["".join(value) for value in handleBodypartDICT.values()]):
                        #if mscDICT[client.user.id]["bodyQuestionSTR"] in ["請問是大腿還是小腿呢？","大腿還是小腿呢？","請問想處理哪個部位呢？"]:
                            for v in userDefinedDICT["bodypart"]:
                                if v in msgSTR:
                                    mscDICT[client.user.id]["bodypart"] = v
                                    mscDICT[client.user.id]["request"] = True # 因為會問「請問是大腿還是小腿呢？」，代表前提request要成立
                                    mscDICT[client.user.id]["bodyQuestionSTR"] = None # 處理完簡答題後，清除問題

                # 再處理「是非題」      
                    else:
                        QlokiResultDICT = beautiBot(msgSTR, [mscDICT[client.user.id]["queryIntentSTR"]])
                        logging.info(QlokiResultDICT) 
                        
                        # inputSTR是「沒有」
                        if QlokiResultDICT["confirm"] == False:
                            # 問題是「有沒有其他與療程相關的疑問呢？」
                            if mscDICT[client.user.id]["confirm"] == True and mscDICT[client.user.id]["finish"] == None:
                                mscDICT[client.user.id]["finish"] = True   # 回應要是「謝謝你使用BeautiBot！」
                                # once finish=TRUE, save the current appointment into appointmentLIST
                                appointmentLIST.append(mscDICT[client.user.id]) 
                                logging.info(appointmentLIST)
                            
                            # 問題是「你是不是有其他疑問呢？」
                            elif mscDICT[client.user.id]["confirm"] == False and mscDICT[client.user.id]["finish"] == "":
                                mscDICT[client.user.id]["finish"] = "END"  # 回應要是「謝謝你使用BeautiBot！」
                                logging.info(mscDICT[client.user.id])                            
                            
                            # 問題是確定部位或是療程
                            elif mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["finish"] == "":
                                mscDICT[client.user.id]["confirm"] = False
                                logging.info(mscDICT[client.user.id])
                        
                        # inputSTR是「有」 
                        elif QlokiResultDICT["confirm"] == True:
                            # 問題是「確認預約單」
                            if mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] != None:
                                if mscDICT[client.user.id]["confirm"] == True:
                                    mscDICT[client.user.id]["finish"] = QlokiResultDICT["confirm"]
                                        
                                elif mscDICT[client.user.id]["confirm"] == "":
                                    mscDICT[client.user.id]["confirm"] = QlokiResultDICT["confirm"]
                                # 問題是「有沒有其他與療程相關的疑問呢？」
                                #if mscDICT[client.user.id]["finish"] == None:
                                    #mscDICT[client.user.id]["confirm"] = QlokiResultDICT["confirm"]

                                # 問題是確定部位或是療程
                                #elif mscDICT[client.user.id]["finish"] == "":
                                    #mscDICT[client.user.id]["finish"] = None 
                            #elif mscDICT[client.user.id]["confirm"] == "":
                                #mscDICT[client.user.id]["confirm"] = QlokiResultDICT["confirm"]
                                
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
                if k == "appointmentDoctor":
                    mscDICT[client.user.id]["appointmentDoctor"] = lokiResultDICT["appointmentDoctor"]
                if k == "appointmentClinic":
                    mscDICT[client.user.id]["appointmentClinic"] = lokiResultDICT["appointmentClinic"]   
                if k == "appointmentDay":
                    mscDICT[client.user.id]["appointmentDay"] = lokiResultDICT["appointmentDay"]                    
                if k == "appointmentTime":
                    mscDICT[client.user.id]["appointmentTime"] = lokiResultDICT["appointmentTime"]                    
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
            if mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] != "": #!= none
                if mscDICT[client.user.id]["confirm"] == True:
                    if mscDICT[client.user.id]["finish"] == None:
                #把預約資訊存到 appointmentLIST
                        appointmentLIST.append(mscDICT[client.user.id]) 
                        replySTR = "謝謝你使用BeautiBot！如果有療程相關問題，可以繼續問我們的醫美小幫手BeautiQuestion喔！\n期待再為你服務～"
                #清空 mscDICT
                        mscDICT[client.user.id] = {"bodypart": None,
                                                   "request": "",
                                                   "confirm": "",
                                                   "queryIntentSTR": "",
                                                   "bodyQuestionSTR": "",
                                                   "appointmentQuestionSTR": "",
                                                   "appointmentClinic": "",
                                                   "appointmentDoctor": "",
                                                   "appointmentDay": "",
                                                   "appointmentTime": "",
                                                   "medicalHistory": "",
                                                   "updatetime": datetime.now(),
                                                   "finish": ""
                                                   }                                        
                    #else:
                        #replySTR = "請問哪些資訊不正確呢？"                
                
                #確認療程後，詢問病史
                    elif mscDICT[client.user.id]["finish"] == "":
                        if mscDICT[client.user.id]["medicalHistory"] == "":
                            replySTR = "請問你有沒有以下病史或情況呢？\n【藥物過敏、凝血功能障礙、蟹足腫、免疫疾病、糖尿病、癲癇、懷孕、哺乳中、抗生素】"
                            mscDICT[client.user.id]["appointmentQuestionSTR"] = "medicalHistory"
                    #病史不適合做療程
                        elif mscDICT[client.user.id]["medicalHistory"] == True:
                            replySTR = "這樣你可能不適合做這個療程耶，建議請先詢問你的醫生喔～"
                            #mscDICT[client.user.id]["appointmentQuestionSTR"] = "medicalHistory" 
                    #確認沒有病史後，詢問醫師
                        elif mscDICT[client.user.id]["medicalHistory"] == False:
                            replySTR = "你要預約哪位醫師呢？\n請選擇【王經凱醫師(男)、程昭瑞醫師(男)、謝羽翔醫師(男)、薛博駿醫師(男)、陳棨揮醫師(男)、劉宇婷醫師(女)】"
                            mscDICT[client.user.id]["appointmentQuestionSTR"] = "appointmentDoctor"
                            #確認醫師後，詢問預約哪間診所
                            if mscDICT[client.user.id]["appointmentDoctor"] != "":
                                replySTR = "你要預約哪間診所呢？請選擇\n【忠孝敦化門診】或是【中山門診】"
                                mscDICT[client.user.id]["appointmentQuestionSTR"] = "appointmentClinic" 
                            #確認診所後，詢問預約時段
                                if mscDICT[client.user.id]["appointmentClinic"] != "":
                                    replySTR = "你要預約哪個時段呢？請選擇\n【星期一 12:30~17:00、18:00~20:30\n星期二 12:30~17:00、18:00~20:30\n星期三 14:00~17:00、18:00~20:30\n星期四 12:30~17:00、18:00~20:30\n星期五 12:30~17:00、18:00~20:30\n星期六 12:30~17:00、18:00~20:30\n(星期日為診所休息日)】"
                                    mscDICT[client.user.id]["appointmentQuestionSTR"] = "appointmentTime" 
                            #確認時段後，收尾        
                                    if mscDICT[client.user.id]["appointmentDay"] != "" and mscDICT[client.user.id]["appointmentTime"] != "":
                                        replySTR = """你預約的是：\n
                                        {} {}\n
                                        {}門診 的 {}除毛療程
                                        由{}醫師看診
                                        
                                        請問這樣正確嗎？""".format(mscDICT[client.user.id]["appointmentDay"],
                                                                           mscDICT[client.user.id]["appointmentTime"],
                                                                           mscDICT[client.user.id]["appointmentClinic"],
                                                                           mscDICT[client.user.id]["bodypart"],
                                                                           mscDICT[client.user.id]["appointmentDoctor"]
                                                                           )
                                        mscDICT[client.user.id]["queryIntentSTR"] = "confirm"
                                        mscDICT[client.user.id]["finish"] = None
    
                                    elif mscDICT[client.user.id]["appointmentDay"] == "" and mscDICT[client.user.id]["appointmentTime"] != "":
                                        replySTR = "請重新選擇日期！\n【星期一12:30~17:00、18:00~20:30\n星期二 12:30~17:00、18:00~20:30\n星期三 14:00~17:00、18:00~20:30\n星期四 12:30~17:00、18:00~20:30\n星期五 12:30~17:00、18:00~20:30\n星期六 12:30~17:00、18:00~20:30\n(星期日為診所休息日)】"
                                        mscDICT[client.user.id]["appointmentQuestionSTR"] = "appointmentTime" 
                                    elif mscDICT[client.user.id]["appointmentDay"] != "" and mscDICT[client.user.id]["appointmentTime"] == "":
                                        replySTR = "請重新選擇看診時間！\n【星期一12:30~17:00、18:00~20:30\n星期二 12:30~17:00、18:00~20:30\n星期三 14:00~17:00、18:00~20:30\n星期四 12:30~17:00、18:00~20:30\n星期五 12:30~17:00、18:00~20:30\n星期六 12:30~17:00、18:00~20:30\n(星期日為診所休息日)】"   
                                        mscDICT[client.user.id]["appointmentQuestionSTR"] = "appointmentTime" 
                    
                    
                elif mscDICT[client.user.id]["confirm"] == False and mscDICT[client.user.id]["finish"] == "END":
                    replySTR = "謝謝你使用BeautiBot！" 
                    mscDICT[client.user.id] = {"bodypart": None,
                                               "request": "",
                                               "confirm": "",
                                               "queryIntentSTR": "",
                                               "bodyQuestionSTR": "",
                                               "appointmentQuestionSTR": "",
                                               "appointmentClinic": "",
                                               "appointmentDoctor": "",
                                               "appointmentDay": "",
                                               "appointmentTime": "",
                                               "medicalHistory": "",
                                               "updatetime": datetime.now(),
                                               "finish": ""
                                               }                  
                elif mscDICT[client.user.id]["confirm"] == False and mscDICT[client.user.id]["finish"] == "":
                    replySTR = "那你有什麼「毛」病？^_^"

            # 第一輪的回覆
                elif mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == None:   # input == "我想要除腿的毛"
                    replySTR = "OK～請問你要詢問{}的除毛療程，是嗎？".format(mscDICT[client.user.id]["bodypart"])
                    mscDICT[client.user.id]["queryIntentSTR"] = "confirm"
                
                elif mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] != "":   # 我想除毛-->請問想處理哪個部位呢？-->[部位]-->
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
                
                elif mscDICT[client.user.id]["confirm"] == "" and mscDICT[client.user.id]["bodyQuestionSTR"] == "":   # input == "我想要除胸毛"
                    if mscDICT[client.user.id]["bodypart"] not in [key for key in handleBodypartDICT.keys()]:         # 需要釐清的部位
                        replySTR = "了解～請問你要詢問{}的除毛療程，是嗎？".format(mscDICT[client.user.id]["bodypart"])
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
                            replySTR = "請問你要詢問{}的除毛療程，是嗎？".format(mscDICT[client.user.id]["bodypart"])
                            mscDICT[client.user.id]["queryIntentSTR"] = "confirm"  
                        else:
                            for e in handleBodypartDICT.keys():
                                if mscDICT[client.user.id]["bodypart"] == e:
                                    replySTR = "".join(handleBodypartDICT[e])   # handleBodypartDICT 回傳的value是一個LIST，因此用join()把它變成STR
                                    mscDICT[client.user.id]["queryIntentSTR"] = "bodypart" 
                                    mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                            else:
                                pass                        

            elif mscDICT[client.user.id]["request"] == True and mscDICT[client.user.id]["bodypart"] == "":   # input == "我想除毛" or "我想預約星期一下午四點在南西診所給程昭瑞醫生除毛" 
                if mscDICT[client.user.id]["appointmentDoctor"] != "" or mscDICT[client.user.id]["appointmentClinic"] != "" or mscDICT[client.user.id]["appointmentDay"] != "" or mscDICT[client.user.id]["appointmentTime"] != "":
                    replySTR = "想除毛嗎？請問想處理哪個部位呢？"
                else: 
                    replySTR = "請問想處理哪個部位呢？"
                    mscDICT[client.user.id]["queryIntentSTR"] = "bodypart"
                    mscDICT[client.user.id]["bodyQuestionSTR"] = replySTR
                    
            elif mscDICT[client.user.id]["request"] == "" and mscDICT[client.user.id]["bodypart"] == None and mscDICT[client.user.id]["confirm"] == "":
                replySTR = "我只能回答醫美相關問題喔～有沒有相關問題想問我呀？\n可以跟我說「我想除毛」或是「我的手毛好長，好煩惱」喔！"
                mscDICT[client.user.id] = {"bodypart": None,
                                           "request": "",
                                           "confirm": "",
                                           "queryIntentSTR": "",
                                           "bodyQuestionSTR": "",
                                           "appointmentQuestionSTR": "",
                                           "appointmentClinic": "",
                                           "appointmentDoctor": "",
                                           "appointmentDay": "",
                                           "appointmentTime": "",
                                           "medicalHistory": "",
                                           "updatetime": datetime.now(),
                                           "finish": ""
                                           }              
        else:
            replySTR = "我只能回答醫美相關問題喔～有沒有相關問題想問我呀？\n可以跟我說「我想除毛」或是「我的手毛好長，好煩惱」喔！"
            mscDICT[client.user.id] = {"bodypart": None,
                                       "request": "",
                                       "confirm": "",
                                       "queryIntentSTR": "",
                                       "bodyQuestionSTR": "",
                                       "appointmentQuestionSTR": "",
                                       "appointmentClinic": "",
                                       "appointmentDoctor": "",
                                       "appointmentDay": "",
                                       "appointmentTime": "",
                                       "medicalHistory": "",
                                       "updatetime": datetime.now(),
                                       "finish": ""
                                       }           
                                 
    except Exception as e:
        logging.error("[MSG scene ERROR] {}".format(str(e)))


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
    