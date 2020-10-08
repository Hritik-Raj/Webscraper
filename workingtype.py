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
	# print(title)
	# print(season)
	# print(episode)
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
title_episode_dict1 = {}
title_episode_dict2 = {}
date_to_url_dict = {}
date_to_title_dict1 = {}
date_to_title_dict2 = {}


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
	page = requests.get(date_to_url_dict[keys])
	soup = BeautifulSoup(page.text, features="html.parser")
	for a in soup.findAll("li", {"class": "HeroGroup-item"}):
		type(a)
		resa = a.find('h3', {"class": "Hero-titleText"})
		resb = a.find('p', {"class": "Hero-subtitle"})
		resc = a.find('a', {"class": "Hero"})
		resd = a.find('a', {"class": "Hero Hero--primary"})
		if resa.text in final_lookup_dict:
			title1.append(resa.text)
			# print ("Best of title ", resa.text)
			
			# print (date_to_url_dict[keys])
			if (resb):
				# print("1")
				# print (resb.text)
				if ((resb.text).startswith('Series')):
					# print ("Best of episode number ", resb.text)
					# print("2")
					# if((resb.text) in final_lookup_dict[resa.text]):
						# print("3")
					subtitle1.append(resb.text)
					title_episode_dict1[resa.text] = resb.text
				else:
					# print("2")
					# print("resb != None and ", resb.text)
					page_url_new = resc['href']
					pages_new = requests.get(page_url_new)
					soup_new = BeautifulSoup(pages_new.text, features="html.parser")
					if (soup_new.find('h1', {"class": "tvip-hide"})):
						subtitle_val = soup_new.find('h1', {"class": "tvip-hide"})
						# if subtitle_val.text in final_lookup_dict[resa.text]:
						subtitle1.append(subtitle_val.text)
						title_episode_dict1[resa.text] = subtitle_val.text
						# print ("Best of episode number ", subtitle_val.text)
			else:
				# print("3")
				subtitle1.append("Standalone")
				title_episode_dict1[resa.text] = "Standalone"
				# page_url_new = resc['href']
				# pages_new = requests.get(page_url_new)
				# soup_new = BeautifulSoup(pages_new.text, features="html.parser")
				# # subtitle_val = soup_new.find('h1', {"class": "tvip-hide"})
				# if (soup_new.find('h1', {"class": "tvip-hide"})):
				# 	subtitle_val = soup_new.find('h1', {"class": "tvip-hide"})
				# 	if subtitle_val.text in final_lookup_dict[resa.text]:
				# 		subtitle1.append(subtitle_val.text)
				# 		title_episode_dict1[resa.text] = subtitle_val.text
			print(title_episode_dict1)
		else:
			title1.append("")
			subtitle1.append("")
		# print("title episode dict 1 is ", title_episode_dict1)
		date_to_title_dict1[int(keys)] = title_episode_dict1		# separate into bestof and editors 

	for b in soup.findAll("li", {"class": "BestOfGrid-item"}):
		type(b)
		res1 = b.find('h3', {"class": "Promo-headline Headline"})
		res2 = b.find('span', {"class": "Promo-subTitle"})
		res3 = b.find('a', {"class": "Promo Card Promo--iplayer"})
		if (res1 != None and res1.text in final_lookup_dict):
			# print("Editors pick", res1.text)
			title2.append(res1.text)
			if (res2 != None):
				# print("Editors pick episode number ", res2.text)
				if (res2 != None and (res2.text).startswith('Series')):
					subtitle2.append(res2.text)
					title_episode_dict2[res1.text] = res2.text
					# print ("1")
				

				else:
					# print ("2")
					page_new_url_bestof = res3['href']
					pages_new_bestof = requests.get(page_new_url_bestof)
					soup_new_bestof = BeautifulSoup(pages_new_bestof.text, features="html.parser")
					if soup_new_bestof.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
						subtitle_bestof_new_page = soup_new_bestof.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
						# if subtitle_bestof_new_page.text in final_lookup_dict[res1.text]:
							# print (subtitle_bestof_new_page.text)
						subtitle2.append(subtitle_bestof_new_page.text)
						title_episode_dict2[res1.text] = subtitle_bestof_new_page.text
						# print ("Editors pick episode number ", subtitle_bestof_new_page)
			else:
					# print("3")
				subtitle2.append("Standalone")
				title_episode_dict2[res1.text] = "Standalone"
			# print ("title episode dict 2 is ", title_episode_dict2)
		else:
			title2.append("")
			subtitle2.append("")
		date_to_title_dict2[int(keys)] = title_episode_dict2
			# print (date_to_title_dict2)
			# 	page_new_url_bestof = res3['href']
			# 	pages_new_bestof = requests.get(page_new_url_bestof)
			# 	soup_new_bestof = BeautifulSoup(pages_new_bestof.text, features="html.parser")
			# 	if soup_new_bestof.find('span', {"class": "typo typo--skylark play-cta__subtitle"}):
			# 		subtitle_bestof_new_page = soup_new_bestof.find('span', {"class": "typo typo--skylark play-cta__subtitle"})
			# 		if subtitle_bestof_new_page.text in final_lookup_dict[res1.text]:
			# 			subtitle2.append(subtitle_bestof_new_page.text)
			# 			title_episode_dict2[res1.text] = subtitle_bestof_new_page.text
	

# dat1 = json.loads(json.dumps(str(date_to_title_dict1)))
# dat2 = json.loads(json.dumps(str(date_to_title_dict2)))
# df1 = pd.DataFrame(dat1)
# df2 = pd.DataFrame(dat2)
df1 = pd.DataFrame.from_dict(date_to_title_dict1, orient="index")
df2 = pd.DataFrame.from_dict(date_to_title_dict2, orient="index")

df1.to_csv('bbcthreebestofshow.csv')
df2.to_csv('bbcthreeeditorspickshow.csv')