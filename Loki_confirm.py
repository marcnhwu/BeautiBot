#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for confirm

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_confirm = True
userDefinedDICT = {"bodyparts": ["毛", "腋", "腋下", "腿", "小腿", "大腿", "膝蓋", "腳", "腳趾", "腳背", "比基尼線", "私密處", "手", "手臂", "上手臂", "下手臂", "全手", "手指", "手背", "臉", "全臉", "鬍子", "眉心", "唇周", "下巴", "頸", "前頸", "後頸", "胸", "胸部", "腹", "腹部", "子母線", "背", "上背", "下背", "臀", "臀部", "乳暈", "胳肢窩"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_confirm:
        print("[confirm] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "不好":
        resultDICT["confirm"] = False
        pass

    if utterance == "不是":
        resultDICT["confirm"] = False
        pass

    if utterance == "不確定":
        resultDICT["confirm"] = False
        pass

    if utterance == "好":
        resultDICT["confirm"] = True
        pass

    if utterance == "好的":
        resultDICT["confirm"] = True
        pass

    if utterance == "恩恩":
        resultDICT["confirm"] = True
        pass

    if utterance == "摁":
        resultDICT["confirm"] = True
        pass

    if utterance == "摁摁":
        resultDICT["confirm"] = True
        pass

    if utterance == "是":
        resultDICT["confirm"] = True
        pass

    if utterance == "有":
        resultDICT["confirm"] = True
        pass

    if utterance == "沒有":
        resultDICT["confirm"] = False
        pass

    return resultDICT