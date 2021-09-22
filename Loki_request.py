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
userDefinedDICT = {"bodypart": ["毛", "腋", "腋下", "腿", "小腿", "大腿", "膝蓋", "腳", "腳趾", "腳背", "比基尼線", "私密處", "手", "手臂", "上手臂", "下手臂", "全手", "手指", "手背", "臉", "全臉", "鬍子", "眉心", "唇周", "下巴", "頸", "前頸", "後頸", "胸", "胸部", "腹", "腹部", "子母線", "背", "上背", "下背", "臀", "臀部", "乳暈", "胳肢窩"], "location": ["忠孝敦化", "南西"], "medicalCondition": ["藥物過敏", "凝血功能障礙", "蟹足腫", "免疫疾病", "糖尿病", "癲癇", "懷孕", "哺乳中", "抗生素"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_request:
        print("[request] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[我]想找[程昭瑞]除[腿]毛":
        # write your code here
        pass

    if utterance == "[我]想找[程昭瑞]除毛":
        # write your code here
        pass

    if utterance == "[我]想要除[腿]":
        # write your code here
        pass

    if utterance == "[我]想要除[腿][上]的毛":
        # write your code here
        pass

    if utterance == "[我]想要除[腿]毛":
        # write your code here
        pass

    if utterance == "[我]想除[腿]":
        # write your code here
        pass

    if utterance == "[我]想除[腿][上]的毛":
        # write your code here
        pass

    if utterance == "[我]想除[腿]毛":
        # write your code here
        pass

    if utterance == "[我]想除毛":
        # write your code here
        pass

    if utterance == "[我]想預約[星期一下午四點][南西]診所[程昭瑞]醫生的除毛療程":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = args[2]
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
            
        pass

    if utterance == "[我]想預約[星期一下午四點][南西]診所做除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = args[2]
        resultDICT['appointmentDoctor'] = ""        
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
        
        pass

    if utterance == "[我]想預約[星期一下午四點][南西]診所的[程昭瑞]醫生做除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = args[2]
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
        
        pass

    if utterance == "[我]想預約[星期一下午四點][南西]診所的除毛療程":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = args[2]
        resultDICT['appointmentDoctor'] = ""
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
        
        pass

    if utterance == "[我]想預約[星期一下午四點][南西]診所除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = args[2]
        resultDICT['appointmentDoctor'] = ""
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
          
        pass

    if utterance == "[我]想預約[星期一下午四點]找[程昭瑞]醫生做除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = ""
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)   
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
        
        pass

    if utterance == "[我]想預約[星期一下午四點]找[程昭瑞]醫生的除毛療程":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = ""
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
          
        pass

    if utterance == "[我]想預約[星期一下午四點]找[程昭瑞]醫生除毛":
        resultDICT["bodypart"] = ""
        resultDICT["request"] = True 
        resultDICT["confirm"] = ""
        resultDICT["appointmentClinic"] = ""
        resultDICT['appointmentDoctor'] = getPersonSTR(inputSTR)
        
        datetime = timeSTRConvert(args[1])["time"]
        #先處理中文日期
        if datetime[0][0]["time_span"]["weekday"][0] == 7:
            resultDICT['appointmentDay'] = False
        else:
            weekday = datetime[0][0]["datetime"][-19:-9]
            resultDICT['appointmentDay'] = weekday
        #再判斷時間是否在營業時間內
        hour = int(datetime[0][0]["datetime"][-8:-6])
        minute = int(datetime[0][0]["datetime"][-5:-3])
        if time_check(hour, minute):
            resultDICT ['appointmentTime'] = datetime[0][0]["datetime"][-8:-3]
        else:
            resultDICT ['appointmentTime'] = False
            
        pass

    if utterance == "[腿]毛太長了想除[腿]毛":
        # write your code here
        pass

    if utterance == "[腿]毛太長了想除毛":
        # write your code here
        pass

    if utterance == "[腿]毛好長想除[腿]毛":
        # write your code here
        pass

    if utterance == "[腿]毛好長想除毛":
        # write your code here
        pass

    if utterance == "想除[腿]毛[我][腿]毛太長了":
        # write your code here
        pass

    if utterance == "想除[腿]毛[我][腿]毛好長":
        # write your code here
        pass

    if utterance == "找[程昭瑞]醫生除[腿]毛":
        # write your code here
        pass

    if utterance == "找[程昭瑞]醫生除毛":
        # write your code here
        pass

    return resultDICT