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

# print(required_show_dict)

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
date_to_title_dict_popular = {}


response = requests.get("http://web.archive.org/cdx/search/cdx?url=bbc.co.uk/tv/bbcthree&output=json&filter=statuscode:200&from=201811&to=201910&fl=timestamp&collapse=timestamp:8")
dates = response.json()
for elements in dates:
	for inner in elements:
		url_val = "http://web.archive.org/web/" + inner + "/https://www.bbc.co.uk/tv/bbcthree"
		dates_list.append(inner)
		url_list.append(url_val)
		date_to_url_dict[inner] = url_val
del url_list[0]
del dates_list[0]
del date_to_url_dict["timestamp"]

for keys in date_to_url_dict.keys():
	print(date_to_url_dict[keys])
	title_priority_dict_featured = {}
	title_priority_dict_bbcthree = {}
	title_priority_dict_popular = {}

	page = requests.get(date_to_url_dict[keys])
	soup = BeautifulSoup(page.text, features= "html.parser")
	if soup.findAll('section', {"aria-label": "Featured on BBC Three"}):
		flag1 = False
		for featured in soup.findAll('section', {"aria-label": "Featured on BBC Three"}):
			print("!")
			type(featured)
			resultfeatured = featured.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = featured.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = featured.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			# if (resultfeatured):
			# 	if (resultfeatured.text in final_lookup_dict):
					# titles.append(resultfeatured.text)
			string_val = "https://web.archive.org" + subtitle_url
			print (string_val)
			page_new = requests.get(string_val)
					# print("i")
			soup_new = BeautifulSoup(page_new.text, features = "html.parser")
			if soup_new.find('span', {"class": "typo typo--bold play-cta__text__title typo--buzzard"}):
				title_val = soup_new.find('span', {"class": "typo typo--bold play-cta__text__title typo--buzzard"})
				print(title_val)
				if (title_val.text in final_lookup_dict):
					titles.append(title_val.text)
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						# print("Episode number type 1", subtitle_val)
						flag1 = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						# print("Episode number type 2", subtitle_val)
						flag1 = True
					if (flag1 == True):
						title_priority_dict_featured[title_val.text] = (subtitle_val.text,  " Genre ", type_val.text)
					else:
						title_priority_dict_featured[title_val.text] = ("No episode,  Genre ", type_val.text)
				# else:
				# 	titles.append("")
				# 	title_priority_dict_featured[""] = ("")

			date_to_title_dict_featured[int(keys)] = title_priority_dict_featured
			print(date_to_title_dict_featured)

			# print(resultfeatured)
	if soup.findAll('div', {"class": "channel-panel-item__content"}):
		flag = False
		for bbcthree in soup.findAll('div', {"class": "channel-panel-item__content"}):
			type(bbcthree)
			resultbbcthree = bbcthree.find('p', {"class": "channel-panel-item__link__title typo typo--skylark typo--bold"})
			resultsubtitle = bbcthree.find('a', {"class": "channel-panel-item__link channel-panel-item__link--with-hover"})
			type_val = bbcthree.find('span', {"class": "channel-panel-item__time-info__label typo typo--bullfinch typo--bold"})
			subtitle_url = resultsubtitle['href']
			# priority = bbcthree['data-section-type']
			# if (resultbbcthree):
			# 	if (resultbbcthree.text in final_lookup_dict):
			# 		titles.append(resultbbcthree.text)
			page_new = requests.get("https://web.archive.org" + subtitle_url)
			soup_new = BeautifulSoup(page_new.text, features = "html.parser")
			if soup_new.find('span', {"class": "typo typo--bold play-cta__text__title typo--buzzard"}):
				title_val = soup_new.find('span', {"class": "typo typo--bold play-cta__text__title typo--buzzard"})
				print(title_val)
				if (title_val.text in final_lookup_dict):
					titles.append(title_val.text)
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_bbcthree[title_val.text] = (subtitle_val.text, " Genre ", type_val.text)
					else:
						title_priority_dict_bbcthree[title_val.text] = ("No episode", " Genre ", type_val.text)
			# print(resultfeatured)
				# else:
				# 	titles.append("")
				# 	title_priority_dict_bbcthree[""] = ("")
			date_to_title_dict_bbcthree[int(keys)] = title_priority_dict_bbcthree
			print(date_to_title_dict_bbcthree)

	if soup.findAll('div', {"class": "channel-groups"}):
		flag = False
		for popular in soup.findAll('div', {"class": "channel-groups"}):
			type(popular)
			resultpopular = popular.find('a', {"class": "content-item__link gel-layout gel-layout--flush"}) 
			if (resultpopular):
				url_new = resultpopular['href']
				page_new = requests.get("https://web.archive.org" + subtitle_url)
				soup_new = BeautifulSoup(page_new.text, features = "html.parser")
				if soup_new.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"}):
					title_val = soup_new.find('span', {"class": "typo typo--buzzard typo--bold play-cta__text__title"})
					# print(title_val)
					if (title_val.text in final_lookup_dict):

						if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
							subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
							flag = True
						elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
							subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
							flag = True
						if (flag == True):
							title_priority_dict_popular[title_val.text] = (subtitle_val.text, " Genre ", type_val.text)
						else:
							title_priority_dict_popular[title_val.text] = ("No episode", " Genre ", type_val.text)
			# else:
			# 	titles.append("")
			# 	title_priority_dict_popular[""] = ("")

			date_to_title_dict_popular[int(keys)] = title_priority_dict_popular
			print(date_to_title_dict_popular)

df_featured = pd.DataFrame.from_dict(date_to_title_dict_featured, orient="index")
df_bbcthree = pd.DataFrame.from_dict(date_to_title_dict_bbcthree, orient="index")
df_remaining = pd.DataFrame.from_dict(date_to_title_dict_popular, orient="index")


df_featured.to_csv('iplayer_bbcthree_featured.csv')
df_bbcthree.to_csv('iplayer_bbcthree_top_pick.csv')
df_remaining.to_csv('iplayer_bbcthree_others.csv')

