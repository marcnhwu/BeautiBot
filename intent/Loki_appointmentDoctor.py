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
userDefinedDICT = {"bodypart": ["毛", "腋", "腋下", "腿", "小腿", "大腿", "膝蓋", "腳", "腳趾", "腳背", "比基尼線", "私密處", "手", "手臂", "上手臂", "下手臂", "全手", "手指", "手背", "臉", "全臉", "鬍子", "眉心", "唇周", "下巴", "頸", "前頸", "後頸", "胸", "胸部", "腹", "腹部", "子母線", "背", "上背", "下背", "臀", "臀部", "乳暈", "胳肢窩"], "location": ["忠孝敦化", "中山"], "doctorName": ["王經凱", "程昭瑞", "劉宇婷", "謝羽翔", "薛博駿", "陳棨揮"], "medicalCondition": ["藥物過敏", "凝血功能障礙", "蟹足腫", "免疫疾病", "糖尿病", "癲癇", "懷孕", "哺乳中", "抗生素"]}
#doctorNameLIST = ["王經凱","程昭瑞","劉宇婷","謝羽翔","薛博駿","陳棨揮","王經凱醫師","程昭瑞醫師","劉宇婷醫師","謝羽翔醫師","薛博駿醫師","陳棨揮醫師"]

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_appointmentDoctor:
        print("[appointmentDoctor] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    
    if utterance == "[我]想約[程昭瑞]":
        if "約" in inputSTR:
            resultDICT["appointmentDoctor"] = args[0]
        pass

    if utterance == "[我]想約[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想要[程昭瑞]":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想要[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想要約[程昭瑞]":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想要約[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想預約[程昭瑞]":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]想預約[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]要[程昭瑞]":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]要[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]要約[程昭瑞]":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]要約[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]要預約[程昭瑞]":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[我]要預約[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[星期一][程昭瑞]有看診嗎":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[星期一][程昭瑞]醫師有看診嗎":
        resultDICT["appointmentDoctor"] = args[1]
        pass

    if utterance == "[程昭瑞]":
        if args[0] not in userDefinedDICT["doctorName"]:
            pass
        else:
            resultDICT["appointmentDoctor"] = args[0]
        pass

    if utterance == "[程昭瑞][星期一]有看診嗎":
        resultDICT["appointmentDoctor"] = args[0]
        pass

    if utterance == "[程昭瑞]醫師":
        resultDICT["appointmentDoctor"] = args[0]
        pass

    if utterance == "[程昭瑞]醫師[星期一]有看診嗎":
        resultDICT["appointmentDoctor"] = args[0]
        pass

    return resultDICT