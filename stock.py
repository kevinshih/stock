'''
Created on 2019年9月10日
This program can tell me the average yield in Taiwan stock.
@author: kevin.shih
'''
import time
import datetime
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup
import lineTool
import os

showBrowser = True

def main():
	doCrawl()
	

def doCrawl():

	if showBrowser:
		driver = webdriver.Chrome("D:/chromedriver.exe")
	else:
		option = webdriver.ChromeOptions()
		option.add_argument('headless')
		driver = webdriver.Chrome("D:/chromedriver.exe", chrome_options=option) # in crontab, i need to tell the chromedriver where it is
	
	lineTokensList = []
	
	allstock =  "D:/github/stock/allstock2.txt"
	for line in list(open(allstock, "r",encoding="utf-8")):
		lineTokens = line.strip().split("　")
		if len(lineTokens) != 2:
			logging.info("格式有誤，資料: {}".format(line))
			errorList.append("格式有誤，資料: {}<br/><br/>".format(line))
			continue
			#raise Exception("格式有誤，資料: {}".format(line))
		
		url = 'https://goodinfo.tw/StockInfo/StockDividendSchedule.asp?STOCK_ID='+lineTokens[0]
		driver.get(url) 
		time.sleep(1)
		# # 取得 html 解析
		#time.sleep(20)
		soup = BeautifulSoup(driver.page_source, "html.parser")
		tmp = soup.find(id="divDetail") 
		if tmp==None: 
			continue
		trs = soup.find(id="divDetail").findAll("tr")
		trlength = len(trs)
		
		yearNumber = 3
		yeardata=[]
		dolor=[]
		profit=[]
		while(True):
			if  25==yearNumber:
				break
			if  yearNumber==trlength:
				break
			tds = trs[yearNumber].findAll("td")
			pay = tds[5].text.strip()
			bonus = tds[9].text.strip()
			if "除息"  in  pay:
				break
			if pay=="" or bonus==""  :
				break
			payF = float(pay)
			bonusF = float(bonus)
			answer = bonusF/payF
			msg = str(answer)
			yeardata.append(answer)
			dolor.append(payF)
			profit.append(bonusF)
			yearNumber+=1
			
		total=0.0
		for data in yeardata:
			total = total +data
			
		totaldolor=0.0
		for data in dolor:
			totaldolor = totaldolor +data
			
		totalprofit=0.0
		for data in profit:
			totalprofit = totalprofit +data
			
		average = 0
		avergedolor = 0
		avergeprofit = 0
		yearNumber = yearNumber-3
		if yearNumber!=0:
			average = total/yearNumber
			avergedolor = totaldolor/yearNumber
			avergeprofit = totalprofit/yearNumber
			average = average*100
			yearNumber = str(yearNumber)
			average = str(round(average, 3))
			avergedolor = str(round(avergedolor, 3))
			avergeprofit = str(round(avergeprofit, 3))
		else:
			yearNumber = str(yearNumber)
			average = str(average)
			avergedolor = str(avergedolor)
			avergeprofit = str(avergeprofit)
			
		data = lineTokens[0]+","+ lineTokens[1]+","+yearNumber+"年,平均值利率是："+average+"%,平均股價是："+avergedolor+"千,平均盈餘是："+avergeprofit+"千"
		lineTokensList.append(data)
		print(data)
		
	with open("D:\allstock.csv", "w", encoding="utf-8") as f:
		for line in lineTokensList:
			f.write(line+"\n")
		
	driver.close()	

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
