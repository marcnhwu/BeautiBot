#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for appointmentTime

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_appointmentTime = True
userDefinedDICT = {"bodypart": ["毛", "腋", "腋下", "腿", "小腿", "大腿", "膝蓋", "腳", "腳趾", "腳背", "比基尼線", "私密處", "手", "手臂", "上手臂", "下手臂", "全手", "手指", "手背", "臉", "全臉", "鬍子", "眉心", "唇周", "下巴", "頸", "前頸", "後頸", "胸", "胸部", "腹", "腹部", "子母線", "背", "上背", "下背", "臀", "臀部", "乳暈", "胳肢窩"], "location": ["忠孝敦化", "中山"], "doctorName": ["王經凱", "程昭瑞", "劉宇婷", "謝羽翔", "薛博駿", "陳棨揮"], "medicalCondition": ["藥物過敏", "凝血功能障礙", "蟹足腫", "免疫疾病", "糖尿病", "癲癇", "懷孕", "哺乳中", "抗生素"]}


from ArticutAPI import ArticutAPI
articut = ArticutAPI.Articut()
import re
#articut = Articut(username="nienhengwu@gmail.com", apikey="X1#CfW!S^1z%ncCakreZ^ys%j42@6BX")

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_appointmentTime:
        print("[appointmentTime] {} ===> {}".format(inputSTR, utterance))

def timeSTRConvert(inputSTR):
    resultDICT = {}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT


from datetime import datetime
dt = datetime.now()

def format_identifier(time_STR):   #只有把時間格式轉成00:00，沒有處理日期格式
    if dt.strftime("%p") == "PM":
        time_STR = time_STR + "PM"
        #dt1 = dateparser.parse(time_STR)
        dt1 = datetime.strptime(str(time_STR),"%Y-%m-%d %H:%M:%S.%f")
        time_STR = datetime.strftime(dt1, '%H:%M')
        return time_STR   #16:00
    else:
        return time_STR

def time_check(hour, minute):
    if hour < 21 and hour > 11:
        if minute < 60 and minute >= 0:
            return True
    else:
        return False
    

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[我]想預約[星期一下午四點]":
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9] #抓articutAPI中time的日期 2021-09-13
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
        pass
    
    
    if utterance == "[星期一下午四點]":
        datetime = timeSTRConvert(args[0])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9] #抓articutAPI中time的日期 2021-09-13
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
        pass


    if utterance == "[星期一][16]:[00]":
        datetime = timeSTRConvert(args[0])["time"]
        
        #再處理數字時間
        timeLIST = re.findall(r'[0-9]+:[0-9]+', inputSTR)
        timeSTR = "".join(timeLIST) #16:00
        #判斷時間是否在營業時間內 
        hour = int(timeSTR.split(":")[0])
        minute = int(timeSTR.split(":")[1])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = timeSTR
        else:
            resultDICT ['appointmentTime'] = False        

        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9] #抓articutAPI中time的日期 2021-09-13
            resultDICT['appointmentDay'] = weekday

    return resultDICT
