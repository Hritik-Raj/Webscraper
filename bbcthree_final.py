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
# print(result)

# for entries in result:
# 	title = (entries["Title"]).rstrip()
# 	series_num = entries["Series number"]
# 	ep_num = entries["Episode number"]
# 	if math.isnan(series_num) or math.isnan(ep_num):
# 		required_show_dict[title] = "Singular"
# 	else:
# 		required_show_dict[title] = "Series " + str(int(series_num)) + ": Episode " + str(int(ep_num))
for entries in result:
	
	default[entries["Title"]]["Series number"].append(str(int(entries["Series number"])))
	default[entries["Title"]]["Episode number"].append(str(int(entries["Episode number"])))

required_show_dict = [
    {'Title': name.rstrip(), **{inner_titles: ' '.join(inner_values) for inner_titles, inner_values in values.items()}}
    for name, values in default.items()
]

# print(required_show_dict)

for dicts in required_show_dict:
	title = dicts["Title"]
	list_store = []
	season = (dicts["Series number"]).split()
	episode = (dicts["Episode number"]).split()
	for i in range(len(season)):
		list_store.append("Series " + season[i] + ": Episode " + episode[i])
	# print(list_store)

	final_lookup_dict[title] = list_store
	# if (len(final_lookup_dict[title]) > 0):
	# 	final_lookup_dict[title.append(list_store)]

del final_lookup_dict[""]

# print(final_lookup_dict)


dates_list = []
url_list = []
title1 = []
title2 = []
subtitle1 = []
subtitle2 = []


date_to_url_dict = {}
date_to_title_dict1 = {}
date_to_title_dict2 = {}
date_to_title_dict3 = {}



response = requests.get("http://web.archive.org/cdx/search/cdx?url=bbc.co.uk/bbcthree&output=json&filter=statuscode:200&from=201811&to=201910&fl=timestamp&collapse=timestamp:8")
dates = response.json()
for elements in dates:
	for inner in elements:
		url_val = "http://web.archive.org/web/" + inner + "/http://www.bbc.co.uk/bbcthree"
		dates_list.append(inner)
		url_list.append(url_val)
		date_to_url_dict[inner] = url_val
del url_list[0]
del dates_list[0]
del date_to_url_dict["timestamp"]
print(final_lookup_dict)
for keys in date_to_url_dict.keys():
	title_episode_dict1 = {}
	title_episode_dict2 = {}
	title_episode_dict3 = {}
	page = requests.get(date_to_url_dict[keys])
	soup = BeautifulSoup(page.text, features="html.parser")
	for a in soup.findAll("li", {"class": "HeroGroup-item"}):
		type(a)

		print(keys)
		resa = a.find('a', {"class": "Hero Hero--primary"})
		resb = a.find('a', {"class": "Hero"})
		if (resa):
			url_val_main = resa['href']
		if (resb):
			url_val_remaining = resb['href']
		page_main = requests.get(url_val_main)
		soup_main = BeautifulSoup(page_main.text, features="html.parser")
		if soup_main.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"}):
			title_new_main = soup_main.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"})
			if soup_main.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
				subtitle_new_main = soup_main.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
				title_episode_dict3[title_new_main.text] = subtitle_new_main.text
			else:
				subtitle_new_main = 'No episode value exists'
				title_episode_dict3[title_new_main.text] = subtitle_new_main
		
		page_remain = requests.get(url_val_remaining)
		soup_remain = BeautifulSoup(page_remain.text, features="html.parser")
		if soup_remain.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"}):
			title_new_remain = soup_remain.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"})
			if soup_remain.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
				subtitle_new_remain = soup_remain.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
				title_episode_dict1[title_new_remain.text] = subtitle_new_remain.text
			else:
				subtitle_new_remain = 'No episode value exists'
				title_episode_dict1[title_new_remain.text] = subtitle_new_remain
		
		date_to_title_dict1[int(keys)] = title_episode_dict1
		date_to_title_dict3[int(keys)] = title_episode_dict3
		
	for b in soup.findAll("li", {"class": "BestOfGrid-item"}):
		type(b)
		res1 = b.find('h3', {"class": "Promo-headline Headline"})
		res2 = b.find('span', {"class": "Promo-subTitle"})
		res3 = b.find('a', {"class": "Promo Card Promo--iplayer"})
		res4 = b.find('h3', {"class": "Headline gel-double-pica Collection-headline"})
		res5 = b.find('a', {"class": "Media-wrapCta istats-notrack"})
		if (res1 != None and res1.text in final_lookup_dict):
			title2.append(res1.text)
			if (res2 != None):
				if (res2 != None and (res2.text).startswith('Series')):
					subtitle2.append(res2.text)
					title_episode_dict2[res1.text] = res2.text
		
				else:
					page_new_url_bestof = res3['href']
					pages_new_bestof = requests.get(page_new_url_bestof)
					soup_new_bestof = BeautifulSoup(pages_new_bestof.text, features="html.parser")
					if soup_new_bestof.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
						subtitle_bestof_new_page = soup_new_bestof.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
						subtitle2.append(subtitle_bestof_new_page.text)
						print ("Subtitle ", subtitle_bestof_new_page.text)
						title_episode_dict2[res1.text] = subtitle_bestof_new_page.text
			else:
				subtitle2.append("Standalone")
				title_episode_dict2[res1.text] = "Standalone"
			# print ("date is ", keys, " title episode dict 2 is ", title_episode_dict2)
		elif (res4 != None and res4.text in final_lookup_dict):
			arr = []
			title2.append(res4.text)
			url_new = res5['href']
			page_multiple = requests.get(url_new)
			soup_multiple = BeautifulSoup(page_multiple.text, features="html.parser")
			for z in soup_multiple.findAll('li', {"class": "grid__item gel-layout__item gel-1/2 gel-1/3@m gel-1/4@xl"}):
				type(z)
				episode_val = z.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
				arr.append(episode_val.text)
			print(arr)
			print (date_to_url_dict[keys])
			title_episode_dict2[res4.text] = arr
		else:
			title2.append("")
			subtitle2.append("")
		date_to_title_dict2[int(keys)] = title_episode_dict2
df1 = pd.DataFrame.from_dict(date_to_title_dict1, orient="index")
# df2 = pd.DataFrame.from_dict(date_to_title_dict2, orient="index")
df3 = pd.DataFrame.from_dict(date_to_title_dict3, orient="index")

df1.to_csv('bbcthreebestoffinal.csv')
# df2.to_csv('bbcthreeeditorspickshowfinal.csv')
df3.to_csv('bbcthreebestof_remain.csv')