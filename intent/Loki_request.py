#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for request

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_request = True
userDefinedDICT = {"bodypart": ["毛", "腋", "腋下", "腿", "小腿", "大腿", "膝蓋", "腳", "腳趾", "腳背", "比基尼線", "私密處", "手", "手臂", "上手臂", "下手臂", "全手", "手指", "手背", "臉", "全臉", "鬍子", "眉心", "唇周", "下巴", "頸", "前頸", "後頸", "胸", "胸部", "腹", "腹部", "子母線", "背", "上背", "下背", "臀", "臀部", "乳暈", "胳肢窩"], "location": ["忠孝敦化", "中山"], "doctorName": ["王經凱", "程昭瑞", "劉宇婷", "謝羽翔", "薛博駿", "陳棨揮"], "medicalCondition": ["藥物過敏", "凝血功能障礙", "蟹足腫", "免疫疾病", "糖尿病", "癲癇", "懷孕", "哺乳中", "抗生素"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_request:
        print("[request] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[我]想要除[腿]":
        if "毛" in inputSTR:
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True
            resultDICT["confirm"] = ""
        else:
            resultDICT["bodypart"] = args[1]
            resultDICT["request"] = True
            resultDICT["confirm"] = ""
        pass

    if utterance == "[我]想要除[腿][上]的毛":
        resultDICT["bodypart"] = args[1]
        resultDICT["request"] = True
        resultDICT["confirm"] = ""
        pass

    if utterance == "[我]想要除[腿]毛":
        resultDICT["bodypart"] = args[1]
        resultDICT["request"] = True    
        resultDICT["confirm"] = ""
        pass

    if utterance == "[我]想除[腿]":
        if "毛" in inputSTR:
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True
            resultDICT["confirm"] = ""
        else:
            resultDICT["bodypart"] = args[1]
            resultDICT["request"] = True
            resultDICT["confirm"] = ""

    if utterance == "[我]想除[腿][上]的毛":
        resultDICT["bodypart"] = args[1]
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        pass

    if utterance == "[我]想除[腿]毛":
        resultDICT["bodypart"] = args[1]
        resultDICT["request"] = True
        resultDICT["confirm"] = ""
        pass

    if utterance == "[我]想除毛":
        if "毛" in inputSTR:
            resultDICT["bodypart"] = ""
            resultDICT["request"] = True
            resultDICT["confirm"] = ""
        pass

    if utterance == "[腿]毛太長了想除[腿]毛":
        resultDICT["bodypart"] = args[0]
        resultDICT["request"] = True  
        resultDICT["confirm"] = ""
        pass

    if utterance == "[腿]毛太長了想除毛":
        resultDICT["bodypart"] = args[0]
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        pass

    if utterance == "[腿]毛好長想除[腿]毛":
        resultDICT["bodypart"] = args[0]
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        pass

    if utterance == "[腿]毛好長想除毛":
        resultDICT["bodypart"] = args[0]
        resultDICT["request"] = True  
        resultDICT["confirm"] = ""
        pass

    if utterance == "想除[腿]毛[我][腿]毛太長了":
        resultDICT["bodypart"] = args[0]
        resultDICT["request"] = True  
        resultDICT["confirm"] = ""
        pass

    if utterance == "想除[腿]毛[我][腿]毛好長":
        resultDICT["bodypart"] = args[0]
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        pass

    if utterance == "[我]想找[程昭瑞]醫師除[腿]毛":
        resultDICT["bodypart"] = args[2]
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想找[程昭瑞]醫師除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想找[程昭瑞]除[腿]毛":
        resultDICT["bodypart"] = args[2]
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想找[程昭瑞]除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentDoctor"] = args[1]
        pass

    return resultDICT