# cargurus-web-scraper

import requests
import pandas as pd
import json
import os 

baseDir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/'
os.chdir(baseDir)
#create excel
writer = pd.ExcelWriter('RawData.xlsx',options={'strings_to_urls': False})
session = requests.Session()



#Mercedes-Benz C-Class 2005-2009 52240 Nationwide###########################
sheetName = 'Mercedes-Benz C-Class'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=forSaleTab_false_0&newSearchFromOverviewPage=true&inventorySearchWidgetType=AUTO&entitySelectingHelper.selectedEntity=c6079&entitySelectingHelper.selectedEntity2=c21239&zip=52240&distance=50000&searchChanged=true&modelChanged=true&filtersModified=true&sortType=undefined&sortDirection=undefined',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    }

post = {
    'zip':'52240',
    'address':'Iowa+City,+IA',
    'latitude':'41.642601013183594',
    'longitude':'-91.5416030883789',
    'distance':'50000',
    'selectedEntity':'c6079',
    'entitySelectingHelper.selectedEntity2':'c21239',
    'transmission':'ANY',
    'page':'1',
    'displayFeaturedListings':'true',
    'inventorySearchWidgetType':'AUTO',
    'allYearsForTrimName':'false',
    'vatOnly':'false',
    'startYear':'2005',
    'endYear':'2009',
    'isRecentSearchView':'false',
    }

ajaxUrl = 'https://www.cargurus.com/Cars/inventorylisting/ajaxFetchSubsetInventoryListing.action?sourceContext=forSaleTab_false_0'

cars = session.post(ajaxUrl,headers=headers,data=post).text
cars = json.loads(cars)['listings']
columns = cars[0].keys()
rows = {column:[] for column in columns}
# exclude AMG
for car in cars:
    if 'amg' in car['trimName'].lower():
        continue
    for column in columns:
        try:
            rows[column].append(car[column])
        except:
            rows[column].append('')
rows = pd.DataFrame(rows)
rows.to_excel(writer,sheet_name=sheetName,index=False,columns=columns)
###########################################################################


#Mercedes-Benz E-Class 2005-2009 52240 Nationwide###########################
sheetName = 'Mercedes-Benz E-Class'

post['selectedEntity'] = 'c6086'
post['entitySelectingHelper.selectedEntity2'] = 'c21242'

cars = session.post(ajaxUrl,headers=headers,data=post).text
cars = json.loads(cars)['listings']
rows = {column:[] for column in columns}
#exclude AMG
for car in cars:
    if 'amg' in car['trimName'].lower():
        continue
    for column in columns:
        try:
            rows[column].append(car[column])
        except:
            rows[column].append('')
rows = pd.DataFrame(rows)
rows.to_excel(writer,sheet_name=sheetName,index=False,columns=columns)
##########################################################################



#BWM 3-series 2005-2009 52240 Nationwide###########################
sheetName = 'BWM 3-Series'

post['selectedEntity'] = 'c23512'
post['entitySelectingHelper.selectedEntity2'] = 'c23970'
post['startYear']='2013'
post['endYear']='2014'
ajaxUrl = ajaxUrl

cars = session.post(ajaxUrl,headers=headers,data=post).text
cars = json.loads(cars)['listings']
rows = {column:[] for column in columns}
#exclude m series
for car in cars:
    if 'm' in car['trimName'].lower():
        continue
    for column in columns:
        try:
            rows[column].append(car[column])
        except:
            rows[column].append('')
rows = pd.DataFrame(rows)
rows.to_excel(writer,sheet_name=sheetName,index=False,columns=columns)
##########################################################################

writer.save()
