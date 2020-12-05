from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import math
import datetime
import csv
from collections import defaultdict

required_show_dict = []
default = defaultdict(lambda: defaultdict(list))
final_lookup_dict = {}

col_list = ["Title", "Series number", "Episode number"]
df = pd.read_excel("/Users/hritikraj/Desktop/UIUC Job/BBC_Three_episodes_consumed_on_iplayer_after_channel_reinvented_itself_online_-_with_genres_1.xlsx", usecols = col_list)
df["Title"] = df["Title"].fillna("")
df["Episode number"] = df["Episode number"].fillna(0)
df["Series number"] = df["Series number"].fillna(0)
result = df.to_dict(orient='records')
for entries in result:
	
	default[entries["Title"]]["Series number"].append(str(int(entries["Series number"])))
	default[entries["Title"]]["Episode number"].append(str(int(entries["Episode number"])))

required_show_dict = [
    {'Title': name.rstrip(), **{inner_titles: ' '.join(inner_values) for inner_titles, inner_values in values.items()}}
    for name, values in default.items()
]


for dicts in required_show_dict:
	title = dicts["Title"]
	list_store = []
	season = (dicts["Series number"]).split()
	episode = (dicts["Episode number"]).split()
	for i in range(len(season)):
		list_store.append("Series " + season[i] + ": Episode " + episode[i])
	final_lookup_dict[title] = list_store
del final_lookup_dict[""]


dates_list = []
url_list = []
hero = []
titles = []
date_to_url_dict = {}
date_to_title_dict_featured = {}
date_to_title_dict_bbcthree = {}
date_to_title_dict_bestofbbcthree = {}
date_to_title_dict_popular = {}
date_to_title_dict_binge = {}
date_to_title_dict_documentary = {}
date_to_title_dict_drama = {}
date_to_title_dict_films = {}
date_to_title_dict_entertainment = {}
date_to_title_dict_sport = {}
date_to_title_dict_box = {}



response = requests.get("http://web.archive.org/cdx/search/cdx?url=bbc.co.uk/iplayer&output=json&filter=statuscode:200&from=201811&to=201910&fl=timestamp&collapse=timestamp:8")
dates = response.json()
for elements in dates:
	for inner in elements:
		url_val = "http://web.archive.org/web/" + inner + "/http://www.bbc.co.uk/iplayer"
		dates_list.append(inner)
		url_list.append(url_val)
		date_to_url_dict[inner] = url_val
del url_list[0]
del dates_list[0]
del date_to_url_dict["timestamp"]

for keys in date_to_url_dict.keys():
	title_priority_dict_featured = {}
	title_priority_dict_bbcthree = {}
	title_priority_dict_bestofbbcthree = {}
	title_priority_dict_popular = {}
	title_priority_dict_binge = {}
	title_priority_dict_documentary = {}
	title_priority_dict_drama = {}
	title_priority_dict_films = {}
	title_priority_dict_entertainment = {}
	title_priority_dict_sport = {}
	title_priority_dict_box = {}
	page = requests.get(date_to_url_dict[keys])
	soup = BeautifulSoup(page.text, features= "html.parser")
	# if soup.findAll('section', {"data-section-type": "editorial"}):
	# 	flag = False
	# 	for featured in soup.findAll('section', {"data-section-type": "editorial"}):
	# 		type(featured)
	# 		resultfeatured = featured.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
	# 		resultsubtitle = featured.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
	# 		type_val = featured.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
	# 		subtitle_url = resultsubtitle['href']
	# 		priority = featured['data-section-type'] 
	# 		if (resultfeatured):
	# 			if (resultfeatured.text in final_lookup_dict):
	# 				titles.append(resultfeatured.text)
	# 				string_val = "https://web.archive.org" + subtitle_url
	# 				page_new = requests.get(string_val)
	# 				soup_new = BeautifulSoup(page_new.text, features = "html.parser")
	# 				if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
	# 					subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
	# 					flag = True
	# 				elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
	# 					subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
	# 					flag = True
	# 				if (flag == True):
	# 					title_priority_dict_featured[resultfeatured.text] = (subtitle_val.text, " Genre ", type_val.text)
	# 				else:
	# 					title_priority_dict_featured[resultfeatured.text] = ("No episode ", " Genre ", type_val.text)
	# 			else:
	# 				titles.append("")
	# 				title_priority_dict_featured[""] = ("")

	# 		date_to_title_dict_featured[int(keys)] = title_priority_dict_featured

	if soup.findAll('section', {"data-section-type": "high-priority"}):
		flag = False
		for bbcthree in soup.findAll('section', {"data-section-type": "high-priority"}):
			type(bbcthree)
			resultbbcthree = bbcthree.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = bbcthree.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = bbcthree.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = bbcthree['data-section-type']
			if (resultbbcthree):
				if (resultbbcthree.text in final_lookup_dict):
					titles.append(resultbbcthree.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_bbcthree[resultbbcthree.text] = (subtitle_val.text, " Genre ", type_val.text)
					else:
						title_priority_dict_bbcthree[resultbbcthree.text] = ("No episode", " Genre ", type_val.text)
				else:
					titles.append("")
					title_priority_dict_bbcthree[""] = ("")
			date_to_title_dict_bbcthree[int(keys)] = title_priority_dict_bbcthree
			print(date_to_title_dict_bbcthree)
				
	# if soup.findAll('section', {"data-section-type": "popular"}):
	# 	flag = False
	# 	for bestofbbcthree in soup.findAll('section', {"data-section-type": "popular"}):
	# 		type(bestofbbcthree)
	# 		resultbestofbbcthree = bestofbbcthree.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
	# 		resultsubtitle = bestofbbcthree.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
	# 		type_val = bestofbbcthree.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
	# 		subtitle_url = resultsubtitle['href']
	# 		priority = bestofbbcthree['data-section-type']
	# 		if (resultbestofbbcthree):
	# 			if (resultbestofbbcthree.text in final_lookup_dict):
	# 				titles.append(resultbestofbbcthree.text)
	# 				page_new = requests.get("https://web.archive.org" + subtitle_url)
	# 				soup_new = BeautifulSoup(page_new.text, features = "html.parser")
	# 				if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
	# 					subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
	# 					flag = True
	# 				elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
	# 					subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
	# 					flag = True
	# 				if (flag == True):
	# 					title_priority_dict_bestofbbcthree[resultbestofbbcthree.text] = (subtitle_val.text, " Genre ", type_val.text)
	# 				else:
	# 					title_priority_dict_bestofbbcthree[resultbestofbbcthree.text] = ("No episode", " Genre ", type_val.text)
	# 			else:
	# 				titles.append("")
	# 				title_priority_dict_bestofbbcthree[""] = ("")
	# 		date_to_title_dict_bestofbbcthree[int(keys)] = title_priority_dict_bestofbbcthree
				
	# if soup.findAll('section', {"data-section-type": "normal-priority"}):
	# 	flag = False
	# 	for popular in soup.findAll('section', {"data-section-type": "normal-priority"}):
	# 		type(popular)
	# 		resultpopular = popular.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
	# 		resultsubtitle = popular.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
	# 		type_val = popular.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
	# 		subtitle_url = resultsubtitle['href']
	# 		priority = popular['data-section-type']
	# 		if (resultpopular):
	# 			if (resultpopular.text in final_lookup_dict):
	# 				titles.append(resultpopular.text)
	# 				page_new = requests.get("https://web.archive.org" + subtitle_url)
	# 				soup_new = BeautifulSoup(page_new.text, features = "html.parser")
	# 				if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
	# 					subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
	# 					flag = True
	# 				elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
	# 					subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
	# 					flag = True
	# 				if (flag == True):
	# 					title_priority_dict_popular[resultpopular.text] = (subtitle_val.text, " Genre ", type_val.text)
	# 				else:
	# 					title_priority_dict_popular[resultpopular.text] = ("No episode", " Genre ", type_val.text)
	# 			else:
	# 				titles.append("")
	# 				title_priority_dict_popular[""] = ("")
	# 		date_to_title_dict_popular[int(keys)] = title_priority_dict_popular
	# 		print(date_to_title_dict_popular)
			
	
	# elif soup.findAll('section', {"class": "section"}):
	# 	# if soup.findAll('section', {"data-bbc-container": "Bundle"}):
	# 	flag = False
	# 	for box in soup.findAll('section', {"class": "section"}):
	# 		type(box)
	# 		resultbox = box.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
	# 		resultsubtitle = box.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
	# 		type_val = box.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
	# 		subtitle_url = resultsubtitle['href']
	# 		page_new = requests.get("https://web.archive.org" + subtitle_url)
	# 		soup_new = BeautifulSoup(page_new.text, features = "html.parser")
	# 		if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
	# 			subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
	# 			flag = True
	# 		elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
	# 			subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
	# 			flag = True
	# 		if (resultbox):
	# 			if (resultbox.text in final_lookup_dict):
	# 				titles.append(resultbox.text)
	# 				if (flag == True):
	# 					title_priority_dict_box[resultbox.text] = (subtitle_val.text, " Genre ", type_val.text)
	# 				else:
	# 					title_priority_dict_box[resultbox.text] = ("No episode", " Genre ", type_val.text)
	# 			else:
	# 				titles.append("")
	# 				title_priority_dict_box[""] = ("")
	# 		date_to_title_dict_box[int(keys)] = title_priority_dict_box
			


# df_featured = pd.DataFrame.from_dict(date_to_title_dict_featured, orient="index")
df_bbcthree = pd.DataFrame.from_dict(date_to_title_dict_bbcthree, orient="index")
# df_bestofbbcthree = pd.DataFrame.from_dict(date_to_title_dict_bestofbbcthree, orient="index")
# df_popular = pd.DataFrame.from_dict(date_to_title_dict_popular, orient="index")
# df_box = pd.DataFrame.from_dict(date_to_title_dict_box, orient="index")

# df_featured.to_csv('iplayer_priority1.csv')
df_bbcthree.to_csv('iplayer_priority2.csv')
# df_bestofbbcthree.to_csv('iplayer_priority3.csv')
# df_popular.to_csv('iplayer_priority4.csv')
# df_box.to_csv('iplayer_priority5.csv')
