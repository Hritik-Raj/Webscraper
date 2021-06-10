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

col_list = ["Title", "Series number"]
df = pd.read_excel("/Users/hritikraj/Desktop/Media Research/Harsh Fixed format/BBC_Three_episodes_consumed_on_iplayer_after_channel_reinvented_itself_online_-_with_genres_1.xlsx", usecols = col_list)
df["Title"] = df["Title"].fillna("")
df["Series number"] = df["Series number"].fillna(0)
result = df.to_dict(orient='records')
for entries in result:
	
	default[entries["Title"]]["Series number"].append(str(int(entries["Series number"])))

required_show_dict = [
    {'Title': name.rstrip(), **{inner_titles: ' '.join(inner_values) for inner_titles, inner_values in values.items()}}
    for name, values in default.items()
]

print(required_show_dict)


for dicts in required_show_dict:
	title = dicts["Title"]
	list_store = []
	season = (dicts["Series number"]).split()
	for i in range(len(season)):
		if "Series " + season[i] not in list_store:
			list_store.append("Series " + season[i])
	final_lookup_dict[title] = list_store
del final_lookup_dict[""]


dates_list = []
url_list = []
hero = []
titles = []
date_to_url_dict = {}
date_to_title_dict_bbcthree = {}

data = {}

for items in final_lookup_dict:
	for item_vals in final_lookup_dict[items]:
		data[items + " " + item_vals] = {}
		data[items + " " + item_vals]["Series"] = item_vals
		data[items + " " + item_vals]["iPlayer Home #1"] = 0
		data[items + " " + item_vals]["iPlayer Home #1 Days"] = 0


columns = ("Series", "iPlayer Home #1", "iPlayer Home #1 Days")

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
	print(keys)
	
	title_priority_dict_bbcthree = {}
	page = requests.get(date_to_url_dict[keys])
	soup = BeautifulSoup(page.text, features= "html.parser")

	if soup.findAll('section', {"data-section-type": "editorial"}):
		for featured in soup.findAll('section', {"data-section-type": "editorial"}):
			type(featured)
			for resultsubtitle in featured.findAll('a', {"class": "content-item__link gel-layout gel-layout--flush"}):
				subtitle_url = resultsubtitle['href']
				session = requests.Session()
				session.max_redirects = 4
				page_new = session.get("https://web.archive.org" + subtitle_url)
				soup_new = BeautifulSoup(page_new.text, features = "html.parser")
				x = ""
				if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
					subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
					x = subtitle_val.text
				elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
					subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
					x = subtitle_val.text
				elif soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
					subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
					x = subtitle_val.text


				if soup_new.find('span', {"class": "typo typo--bold play-cta__text__title typo--buzzard"}):
					title_val = soup_new.find('span', {"class": "typo typo--bold play-cta__text__title typo--buzzard"})

					# if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
					# 	x = subtitle_val.text
					# elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
					# 	x = subtitle_val.text
					# elif soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
					# 	x = subtitle_val.text

					# if title_val.text + " " + x.split(':')[0] in data:
					# 	data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1"] = 1
					# 	data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1 Days"] += 1

				elif soup_new.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"}):
					title_val = soup_new.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"})

					# if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
					# 	x = subtitle_val.text
					# elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
					# 	x = subtitle_val.text
					# elif soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
					# 	x = subtitle_val.text

					# if title_val.text + " " + x.split(':')[0] in data:
					# 	data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1"] = 1
					# 	data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1 Days"] += 1
				
				elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--buzzard"}):
					title_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--buzzard"})

					# if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
					# 	x = subtitle_val.text
						
					# elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
					# 	x = subtitle_val.text
					# elif soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
					# 	x = subtitle_val.text

					# if title_val.text + " " + x.split(':')[0] in data:
					# 	data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1"] = 1
					# 	data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1 Days"] += 1

				elif soup_new.find('h1', {"class": "hero-header__title typo typo--bold typo--buzzard"}):
					title_val = soup_new.find('span', {"class": "hero-header__title typo typo--bold typo--buzzard"})	

					# if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
					# 	x = subtitle_val.text
						
					# elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
					# 	x = subtitle_val.text
						
					# elif soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
					# 	subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
					# 	x = subtitle_val.text

				if title_val.text + " " + x.split(':')[0] in data:
					data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1"] = 1
					data[title_val.text + " " + x.split(':')[0]]["iPlayer Home #1 Days"] += 1

df1 = pd.DataFrame(data = data, index = columns).T
df1.to_csv('iplayer_home1.csv')

