#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for appointmentDoctor

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_appointmentDoctor = True
userDefinedDICT = {"bodypart": ["毛", "腋", "腋下", "腿", "小腿", "大腿", "膝蓋", "腳", "腳趾", "腳背", "比基尼線", "私密處", "手", "手臂", "上手臂", "下手臂", "全手", "手指", "手背", "臉", "全臉", "鬍子", "眉心", "唇周", "下巴", "頸", "前頸", "後頸", "胸", "胸部", "腹", "腹部", "子母線", "背", "上背", "下背", "臀", "臀部", "乳暈", "胳肢窩"], "location": ["忠孝敦化", "南西"], "medicalCondition": ["藥物過敏", "凝血功能障礙", "蟹足腫", "免疫疾病", "糖尿病", "癲癇", "懷孕", "哺乳中", "抗生素"]}

import json
from ArticutAPI import Articut
with open("account.info.py", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
articut = Articut(username = accountDICT["username"], apikey = accountDICT["articut_api_key"])

def timeSTRConvert(inputSTR):
    resultDICT = {}
    resultDICT = articut.parse(inputSTR, level="lv3")
    return resultDICT

def getPersonSTR(inputSTR):
    resultDICT = {}
    resultDICT = articut.parse(inputSTR, level="lv3")
    personSTR = resultDICT["person"][0][0][2]
    return personSTR


# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_appointmentDoctor:
        print("[appointmentDoctor] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[我]想約[程昭瑞]":
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想要[程昭瑞]":
        #lv3resultDICT = articut.parse(inputSTR, level="lv3")
        #resultDICT['appointmentDoctor'] = lv3resultDICT["person"][0][0][2]
        resultDICT['appointmentDoctor'] = args[1]
        pass
    
    if utterance == "[我]想要約[程昭瑞]":
        resultDICT['appointmentDoctor'] = args[1]
        pass

    if utterance == "[我]想預約[程昭瑞]":
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]要[程昭瑞]":
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]要約[程昭瑞]":
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass
    
    if utterance == "[我]要預約[程昭瑞]":
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[星期一][程昭瑞]有看診嗎":
        if "看診" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            
            datetime = timeSTRConvert(args[0])["time"]
            #先處理中文日期
            if datetime[0][0]["time_span"]["weekday"][0] == 7:
                resultDICT['appointmentDay'] = False
            else:
                weekday = datetime[0][0]["datetime"][-19:-9]
                resultDICT['appointmentDay'] = weekday  
        pass

    if utterance == "[程昭瑞][星期一]有看診嗎":
        if "看診" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            
            datetime = timeSTRConvert(args[1])["time"]
            #先處理中文日期
            if datetime[0][0]["time_span"]["weekday"][0] == 7:
                resultDICT['appointmentDay'] = False
            else:
                weekday = datetime[0][0]["datetime"][-19:-9]
                resultDICT['appointmentDay'] = weekday  
        pass

    if utterance == "程昭瑞":
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想約[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想要[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想要約[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想預約[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]要[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]要約[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]要預約[程昭瑞]醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[星期一][程昭瑞]醫師有看診嗎":
        if "看診" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            
            datetime = timeSTRConvert(args[0])["time"]
            #先處理中文日期
            if datetime[0][0]["time_span"]["weekday"][0] == 7:
                resultDICT['appointmentDay'] = False
            else:
                weekday = datetime[0][0]["datetime"][-19:-9]
                resultDICT['appointmentDay'] = weekday  
        pass

    if utterance == "[程昭瑞]醫師[星期一]有看診嗎":
        if "看診" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            
            datetime = timeSTRConvert(args[1])["time"]
            #先處理中文日期
            if datetime[0][0]["time_span"]["weekday"][0] == 7:
                resultDICT['appointmentDay'] = False
            else:
                weekday = datetime[0][0]["datetime"][-19:-9]
                resultDICT['appointmentDay'] = weekday  
        pass

    if utterance == "程昭瑞醫師":
        if "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想預約[程昭瑞]醫生做除毛":
        if "醫生" in inputSTR or "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR) 
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True            
        pass

    if utterance == "[我]想預約[程昭瑞]醫生的除毛門診":
        if "醫生" in inputSTR or "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True            
        pass

    if utterance == "[我]想預約[程昭瑞]醫生除毛":
        if "醫生" in inputSTR or "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True            
        pass
    
    if utterance == "[我]想預約[程昭瑞]醫生的除毛療程":
        if "醫生" in inputSTR or "醫師" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True            
        pass

    if utterance == "[我]想改[程昭瑞]":
        if "改" in inputSTR:
            resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass

    if utterance == "[我]想改[程昭瑞]醫師":
        if "改" in inputSTR:
            if "醫生" in inputSTR or "醫師" in inputSTR:
                resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        pass
    
    return resultDICT