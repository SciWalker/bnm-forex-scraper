import requests
from bs4 import BeautifulSoup
import datetime
import csv
import sys
import pandas as pd
import io
import numpy as np
import time
import os
class scraper:
    def __init__(self):
        self.currency_list = ['USD','100CNY','EUR','SGD','100IDR','100JPY']

def BNMFunction(timenow):
    time_bnm=""
    time_9am=timenow.replace(hour=9, minute=10, second=0, microsecond=0)
    time_12pm=time_9am.replace(hour=12, minute =20, second = 0, microsecond=0)
    time_5pm=time_9am.replace(hour=17, minute =20, second = 0, microsecond=0)
    if timenow>time_9am:
        time_bnm="0900"
    if timenow>time_12pm:
        time_bnm="1200"
    if timenow>time_5pm:
        time_bnm="1700"
    if timenow<=time_9am:
        time_bnm="1700"
    response = requests.get("https://api.bnm.gov.my/public/exchange-rate", params= {"quote":"fx","session":"0900"}, headers={'Accept': 'application/vnd.BNM.API.v1+json'})
    json_response = response.json()
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



def periodic_function(scraper_obj):

    link="https://transfer.moneymatch.co/business" 
    response = requests.get(link)
    html_page=response.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(class_='text-right pr-4')
    output=[]
    for i in range(len(text)):
        output.append(text[i].get_text())
    timenow=datetime.datetime.now()
    
    combined_array=[]
    perc_diff=[]
    perc_diff_BNM=[]
    for i in range(len(scraper_obj.currency_list)):
        combined_array.append([BNM_value[i][0],BNM_value[i][1],RHB_values[i][0],RHB_values[i][1],scraper_obj.currency_list[i],output[i]])
        perc_diff.append(round(100*(float(combined_array[i][5])/float(combined_array[i][3])-1),3))
        combined_array[i].append(perc_diff[i])
        perc_diff_BNM.append(round(100*(float(combined_array[i][5])/float(combined_array[i][1])-1),3))
        combined_array[i].append(perc_diff_BNM[i])
    header=["BNM","","RHB","","MoneyMatch","","Markup vs RHB(%)","Markup vs BNM (%)"]
    if not os.path.exists("./data"):
        os.makedirs("./data")
    with open('data/currency_exchange_data.csv', 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        string_time=[(str(timenow.year)+'-'+str(timenow.month)+'-'+str(timenow.day)),(str(timenow.hour)+':'+str(timenow.minute)+':'+str(timenow.second))]
        writer.writerow('')
        writer.writerow(string_time)
        writer.writerow(header)
        for i in range(len(combined_array)):
            writer.writerow(combined_array[i])
    csvFile.close()

def RHBFunction(scraper_obj):
    link="https://www.rhbgroup.com/treasury-rates/foreign-exchange/fx.csv"

    ##TODO: read from the csv and get currency results, need to first remove spaces
    data = requests.get('https://www.rhbgroup.com/treasury-rates/foreign-exchange/fx.csv').content
    data=data.strip()
    data_str=data.decode('utf-8')
    #df_data = requests.get(r'C:\Users\WenWei\Downloads\fx.csv')
    
    data_str="".join(data_str.split(" ")[2:])
    data_str=io.StringIO(data_str)

    rawData = pd.read_csv(data_str,delimiter=',',names=["shortform","currency", "unit", "sell", "buy","OOD"])
    ul_list=[]
    for i in scraper_obj.currency_list:
        if "100" in i:
            i=(i.replace("100",""))
        sublist=[i,(rawData.loc[rawData['shortform']==i]['buy'].values[0]+rawData.loc[rawData['shortform']==i]['sell'].values[0])/2]
        ul_list.append(sublist)
    
    return ul_list

scraper_obj=scraper()
iterations = 900
tstep = datetime.timedelta(seconds=10)
for i in np.arange(iterations):
    timenow = datetime.datetime.now()
    try:
        BNM_value=BNMFunction(timenow)
        RHB_values=RHBFunction(scraper_obj)
        periodic_function(scraper_obj)
        
        while datetime.datetime.now() < timenow + tstep:
            1==1
    except Exception as e:
        print("error:"+str(e)+", retry in a while.")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        time.sleep(50)
        pass

