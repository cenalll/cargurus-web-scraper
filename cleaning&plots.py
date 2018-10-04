#cargurus-web-scraper
#data cleaning and manipulation


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os

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
    section = pd.DataFrame({'%sfreq'%column:colState,'dealScoreMean':dealScore,'%sMean'%column:colMean})
    section = section.dropna()
    section['%sfreq'%column] = section['%sfreq'%column]/section['%sfreq'%column].sum()
    section.to_excel(writer,sheet_name='%sInterval'%column,columns=['%sfreq'%column,'%sfreq'%column,'%sMean'%column,'dealScoreMean'])
    return section

def scatter(column):
    #grouping data into intervals
    global writer,data
    colState = data[column].groupby(data[column]).count().sort_index()
    dealScore = data['dealScore'].groupby(data[column]).mean().sort_index()
    section = pd.DataFrame({'%sfreq'%column:colState,'dealScoreMean':dealScore})
    section['%sfreq'%column] = section['%sfreq'%column]/section['%sfreq'%column].sum()
    section.to_excel(writer,sheet_name='%sInterval'%column,columns=['%sfreq'%column,'%sfreq'%column,'dealScoreMean'])
    return section

sheetNames = pd.ExcelFile('RawData.xlsx').sheet_names
for sheetName in sheetNames:
    if not os.path.exists(sheetName):
        os.mkdir(sheetName)
    writer = pd.ExcelWriter('%s/NewData.xlsx'%sheetName,options={'strings_to_urls': False})
 
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
