#cargurus-web-scraper
#data cleaning and some plots


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os

#I use Chinese characters so
plt.rcParams['font.sans-serif']=['SimHei'] 
#ignore the error of negative sign
plt.rcParams['axes.unicode_minus']=False
#extract the column I'm interested in
columns = ['carYear','price','exteriorColorName',
           'hasAccidents','distance','fuelType',
           'sellerRating','mileage','wheelSystemDisplay',
           'dealScore'] 
#current path
baseDir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/'
os.chdir(baseDir)
def continuous(column):
    #grouping data into intervals
    global writer,data
    width = data[column].max()/10
    section = np.arange(0,width*11,width)
    section = pd.cut(data[column],section,right=False)
    section = pd.DataFrame({column:section,'dealScore':data['dealScore'],'originCol':data[column]})
    dealScore = section['dealScore'].groupby(section[column]).mean().sort_index()
    colState = section['dealScore'].groupby(section[column]).count().sort_index()
    colMean = section['originCol'].groupby(section[column]).mean().sort_index()
    section = pd.DataFrame({'%s频数'%column:colState,'dealScore均值':dealScore,'%s均值'%column:colMean})
    section = section.dropna()
    section['%s频率'%column] = section['%s频数'%column]/section['%s频数'%column].sum()
    section.to_excel(writer,sheet_name='%s区间统计'%column,columns=['%s频数'%column,'%s频率'%column,'%s均值'%column,'dealScore均值'])
   
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.barh(range(section.shape[0]),section['%s频率'%column],color='#8EE5EE')
    plt.yticks([num+0.5 for num in range(section.shape[0])],section.index,fontsize=9,rotation=30)
    ax.set_xlabel('频率')
    fig.savefig('%s/%s频率直方图.jpg'%(sheetName,column))
   
    corr = section['dealScore均值'].corr(section['%s均值'%column])
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(section['%s均值'%column],section['dealScore均值'],color='#FF3030')
    ax.set_title('dealScore与%s的相关系数:%.2f'%(column,corr),fontsize=10)
    ax.set_xlabel('%s'%column,fontsize=15)
    ax.set_ylabel('dealScore',fontsize=15)
    fig.savefig('%s/%s相关系数折线图.jpg'%(sheetName,column))
    return section

def scatter(column):
    #grouping data into intervals
    global writer,data
    colState = data[column].groupby(data[column]).count().sort_index()
    dealScore = data['dealScore'].groupby(data[column]).mean().sort_index()
    section = pd.DataFrame({'%s频数'%column:colState,'dealScore均值':dealScore})
    section['%s频率'%column] = section['%s频数'%column]/section['%s频数'%column].sum()
    section.to_excel(writer,sheet_name='%s统计'%column,columns=['%s频数'%column,'%s频率'%column,'dealScore均值'])
   
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.barh(range(section.shape[0]),section['%s频率'%column],color='#8EE5EE')
    plt.yticks([num+0.5 for num in range(section.shape[0])],section.index,fontsize=8)
    ax.set_xlabel('频率')
    fig.savefig('%s/%s频率直方图.jpg'%(sheetName,column))
    return section
    

sheetNames = pd.ExcelFile('RawData.xlsx').sheet_names
for sheetName in sheetNames:
    if not os.path.exists(sheetName):
        os.mkdir(sheetName)
    writer = pd.ExcelWriter('%s/统计分析.xlsx'%sheetName,options={'strings_to_urls': False})
 
    origin = pd.read_excel('RawData.xlsx',sheetname=sheetName,header=0)
    origin = origin.set_index(['id',])
    #########################################################
    data = origin.loc[:,columns]
    data = data.dropna()
    data = data[data['price']>100]
    data = data[data['exteriorColorName']!='Unknown']
    data.to_excel(writer,columns=columns,sheet_name='CleanedData')
    ############################################################
    
    price = continuous('price')
    distance = continuous('distance')
    sellerRating = continuous('sellerRating')
    mileage = continuous('mileage')
    
    exteriorColorName = scatter('exteriorColorName')
    hasAccidents = scatter('hasAccidents')
    exteriorColorName = scatter('exteriorColorName')
    fuelType = scatter('fuelType')
    wheelSystemDisplay = scatter('wheelSystemDisplay')
    writer.save()
del baseDir,sheetName,sheetNames,origin
