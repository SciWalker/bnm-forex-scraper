import requests
from bs4 import BeautifulSoup
import json
import datetime
import csv
import pandas
import threading
import time
import numpy as np
def BNMFunction(timenow):
    time_bnm=""
    time_9am=timenow.replace(hour=9, minute=10, second=0, microsecond=0)
    time_12pm=time_9am.replace(hour=12, minute =20, second = 0, microsecond=0)
    time_5pm=time_9am.replace(hour=17, minute =20, second = 0, microsecond=0)
    print(timenow)
    if timenow>time_9am:
        time_bnm="0900"
    if timenow>time_12pm:
        time_bnm="1200"
    if timenow>time_5pm:
        time_bnm="1700"
    if timenow<=time_9am:
        time_bnm="1700"
    print(time_bnm)
    response = requests.get("https://api.bnm.gov.my/public/exchange-rate", params= {"quote":"fx","session":"0900"}, headers={'Accept': 'application/vnd.BNM.API.v1+json'})
    json_response = response.json()
    print("BNM data")
    print(json_response)
    currency_exchange_rate=json_response['data']
    bnm_data=[]
    currency_list_bnm = ['AED','AUD','BND','CAD','CHF','CNY','EGP','EUR','GBP','HKD','IDR','JPY','KHR','KRW','MMK','NPR','NZD','PHP','PKR','SAR','SDR','SGD','THB','TWD','USD','VND']
    for i in range(len(currency_exchange_rate)):
        if currency_exchange_rate[i]['currency_code']=='USD':
            bnm_data.append([currency_exchange_rate[i]['currency_code'],currency_exchange_rate[i]['rate']['middle_rate']])
    for i in range(len(currency_exchange_rate)):
        if currency_exchange_rate[i]['currency_code']=='CNY':
            bnm_data.append([currency_exchange_rate[i]['currency_code'],currency_exchange_rate[i]['rate']['middle_rate']*100])
    for i in range(len(currency_exchange_rate)):
        if currency_exchange_rate[i]['currency_code']=='EUR':
            bnm_data.append([currency_exchange_rate[i]['currency_code'],currency_exchange_rate[i]['rate']['middle_rate']])
    for i in range(len(currency_exchange_rate)):
        if currency_exchange_rate[i]['currency_code']=='SGD':
            bnm_data.append([currency_exchange_rate[i]['currency_code'],currency_exchange_rate[i]['rate']['middle_rate']])
    for i in range(len(currency_exchange_rate)):
        if currency_exchange_rate[i]['currency_code']=='IDR':
            bnm_data.append([currency_exchange_rate[i]['currency_code'],currency_exchange_rate[i]['rate']['middle_rate']])
    for i in range(len(currency_exchange_rate)):
        if currency_exchange_rate[i]['currency_code']=='JPY':
            bnm_data.append([currency_exchange_rate[i]['currency_code'],currency_exchange_rate[i]['rate']['middle_rate']])
    return(bnm_data)



def myPeriodicFunction():
    #response_bnm = requests.get("https://api.bnm.gov.my/public/exchange-rate", params= {"quote":"fx","session":"1200"}, headers={'Accept': 'application/vnd.BNM.API.v1+json'})
    #response = requests.get("https://api.bnm.gov.my/public/exchange-rate/USD/year/2019/month/5",headers={'Accept': 'application/vnd.BNM.API.v1+json'})
    #print(response)
    #json_response_bnm = response_bnm.json()

    link="https://transfer.moneymatch.co/business" 
    response = requests.get(link)
    html_page=response.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(class_='text-right pr-4')
    #text = soup.find_all(class_="tombstone-container")
    output=[]
    for i in range(len(text)):
        output.append(text[i].get_text())
    currency_list=['USD','100CNY','EUR','SGD','100IDR','100JPY']
    #currency_list=['USD','100CNY','EUR','SGD','100IDR','100JPY','MYR', 'CND','INR']
    timenow=datetime.datetime.now()
    combined_array=[]
    perc_diff=[]
    perc_diff_BNM=[]
    print(BNM_value)
    for i in range(len(currency_list)):
        combined_array.append([BNM_value[i][0],BNM_value[i][1],RHB_values[i][0],RHB_values[i][1],currency_list[i],output[i]])
        perc_diff.append(round(100*(float(combined_array[i][5])/float(combined_array[i][3])-1),3))
        combined_array[i].append(perc_diff[i])
        perc_diff_BNM.append(round(100*(float(combined_array[i][5])/float(combined_array[i][1])-1),3))
        combined_array[i].append(perc_diff_BNM[i])
    print(combined_array)
    header=["BNM","","RHB","","MoneyMatch","","Markup vs RHB(%)","Markup vs BNM (%)"]
    with open('MoneyMatch data.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        string_time=[(str(timenow.year)+'-'+str(timenow.month)+'-'+str(timenow.day)),(str(timenow.hour)+':'+str(timenow.minute)+':'+str(timenow.second))]
        print(string_time)
        writer.writerow('')
        writer.writerow(string_time)
        writer.writerow(header)
        for i in range(len(combined_array)):
            writer.writerow(combined_array[i])
#            print(currency_list[i])
#            print(output[i])
    csvFile.close()

def RHBFunction():
    link="https://www.rhbgroup.com/malaysia/products-and-services/rates-and-charges/treasury-rates/foreign-exchange"
    response = requests.get(link)
    html_page=response.content
    #soup = BeautifulSoup(html_page, 'html.parser')
    #text = soup.find_all(class_=('text-right','text-center'),id_="rhbcontentplaceholder_0_rhbsection1_0_tabplaceholder_0_lvForeignExchangeRates_codeLabel_8")
    soup = BeautifulSoup(html_page, features="lxml")
    text = soup.findAll("td")
    output_rhb=[]
    filtered_rhb_rate=[]
    for i in range(len(text)):
        text_raw=text[i].get_text()
        output_rhb.append(text_raw)
    num_row=int(len(output_rhb)/7)
    #currency_list=['USD','100CNY','EUR','SGD','100IDR','100JPY','MYR', 'CND','INR']
    timenow=datetime.datetime.now()
    for i in range(0,len(output_rhb)-num_row,6):
        del output_rhb[i]
    for i in range(1,len(output_rhb)-num_row,5):
        del output_rhb[i]
    for i in range(4,len(output_rhb)-num_row,4):
        del output_rhb[i]
    for i in range(2,len(output_rhb),4):
        if output_rhb[i]=='-':
            output_rhb[i]='-10000'
        if output_rhb[i+1]=='-':
            output_rhb[i+1]='-10000'
    for i in range(2,len(output_rhb)-(num_row*2),2):
        output_rhb[i+1]=(float(output_rhb[i])+float(output_rhb[i+1]))/2
        output_rhb[i-2]=output_rhb[i-1]+output_rhb[i-2]
        del output_rhb[i]
        del output_rhb[i-1]
    #for i in range(1,)
    for i in range(len(output_rhb)):
        if output_rhb[i]=="1USD":
            filtered_rhb_rate.append(output_rhb[i:i+2])
    for i in range(len(output_rhb)):
        if output_rhb[i]=="100CNY":
            filtered_rhb_rate.append(output_rhb[i:i+2])
    for i in range(len(output_rhb)):
        if output_rhb[i]=="1EUR":
            filtered_rhb_rate.append(output_rhb[i:i+2])
    for i in range(len(output_rhb)):
        if output_rhb[i]=="1SGD":
            filtered_rhb_rate.append(output_rhb[i:i+2])
    for i in range(len(output_rhb)):
        if output_rhb[i]=="100IDR":
            filtered_rhb_rate.append(output_rhb[i:i+2])
    for i in range(len(output_rhb)):
        if output_rhb[i]=="100JPY":
            filtered_rhb_rate.append(output_rhb[i:i+2])
    return filtered_rhb_rate

iterations = 900
tstep = datetime.timedelta(seconds=10)
for i in np.arange(iterations):
    timenow = datetime.datetime.now()
    try:
        BNM_value=BNMFunction(timenow)
        RHB_values=RHBFunction()
        myPeriodicFunction()
        
        while datetime.datetime.now() < timenow + tstep:
            1==1
        print("===================================")
    except Exception as e:
        print("error:"+str(e)+", rest for a while.")
        time.sleep(50)
        pass

