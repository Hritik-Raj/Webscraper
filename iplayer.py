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
hero = []
titles = []
# title_episode_dict1 = {}
# title_episode_dict2 = {}
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
# date_to_title_dict = {}
# date_to_title_dict2 = {}


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


# print (date_to_url_dict)

# new_values = {'20181101004253': 'http://web.archive.org/web/20181101004253/http://www.bbc.co.uk/iplayer', '20181102005853': 'http://web.archive.org/web/20181102005853/http://www.bbc.co.uk/iplayer', '20181103000619': 'http://web.archive.org/web/20181103000619/http://www.bbc.co.uk/iplayer', '20181104004737': 'http://web.archive.org/web/20181104004737/http://www.bbc.co.uk/iplayer', '20181105014841': 'http://web.archive.org/web/20181105014841/http://www.bbc.co.uk/iplayer', '20181106021653': 'http://web.archive.org/web/20181106021653/http://www.bbc.co.uk/iplayer', '20181107045000': 'http://web.archive.org/web/20181107045000/http://www.bbc.co.uk/iplayer', '20181108085915': 'http://web.archive.org/web/20181108085915/http://www.bbc.co.uk/iplayer'}

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
	# for a in soup.findAll('div', {"class": "homepage-sections"}):
	# 	type(a)
	# 	resultherotitle = a.find('h2', {"class": "hero-section__title typo typo--bold typo--buzzard"})
	# 	# resultherosubtitle = a.find()
	# 	if resultherotitle in final_lookup_dict:
	# 		hero.append(resultherotitle.text)
		# resultfeatured = a.find('section', {"aria-label":})
	if soup.findAll('section', {"aria-label": "Featured"}):
		flag = False
		for featured in soup.findAll('section', {"aria-label": "Featured"}):
			type(featured)
			resultfeatured = featured.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = featured.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = featured.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = featured['data-section-type'] 
			if (resultfeatured):
				if (resultfeatured.text in final_lookup_dict):
					titles.append(resultfeatured.text)
					string_val = "https://web.archive.org" + subtitle_url
					# print (string_val)
					page_new = requests.get(string_val)
					# print("i")
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						# print("Episode number type 1", subtitle_val)
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						# print("Episode number type 2", subtitle_val)
						flag = True
					if (flag == True):
						title_priority_dict_featured[resultfeatured.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_featured[resultfeatured.text] = ("No episode Priority Level ", priority, " Genre ", type_val.text)
				else:
					titles.append("")
					title_priority_dict_featured[""] = ("")

			date_to_title_dict_featured[int(keys)] = title_priority_dict_featured
			# print(date_to_title_dict_featured)

			# print(resultfeatured)
	if soup.findAll('section', {"aria-label": "BBC Three"}):
		flag = False
		for bbcthree in soup.findAll('section', {"aria-label": "BBC Three"}):
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
						title_priority_dict_bbcthree[resultbbcthree.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_bbcthree[resultbbcthree.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)
				else:
					titles.append("")
					title_priority_dict_bbcthree[""] = ("")
			date_to_title_dict_bbcthree[int(keys)] = title_priority_dict_bbcthree
			print(date_to_title_dict_bbcthree)
				
	if soup.findAll('section', {"aria-label": "Best of BBC Three"}):
		flag = False
		for bestofbbcthree in soup.findAll('section', {"aria-label": "Best of BBC Three"}):
			type(bestofbbcthree)
			resultbestofbbcthree = bestofbbcthree.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = bestofbbcthree.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = bestofbbcthree.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = bestofbbcthree['data-section-type']
			if (resultbestofbbcthree):
				if (resultbestofbbcthree.text in final_lookup_dict):
					titles.append(resultbestofbbcthree.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_bestofbbcthree[resultbestofbbcthree.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_bestofbbcthree[resultbestofbbcthree.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)
				else:
					titles.append("")
					title_priority_dict_bestofbbcthree[""] = ("")
			date_to_title_dict_bestofbbcthree[int(keys)] = title_priority_dict_bestofbbcthree
				
	if soup.findAll('section', {"aria-label": "Most Popular"}):
		flag = False
		for popular in soup.findAll('section', {"aria-label": "Most Popular"}):
			type(popular)
			resultpopular = popular.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
			resultsubtitle = popular.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = popular.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = popular['data-section-type']
			if (resultpopular):
				if (resultpopular.text in final_lookup_dict):
					titles.append(resultpopular.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_popular[resultpopular.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_popular[resultpopular.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)

				else:
					titles.append("")
					title_priority_dict_popular[""] = ("")
			date_to_title_dict_popular[int(keys)] = title_priority_dict_popular
			
				
	if soup.findAll('section', {"aria-label": "Binge-worthy Series"}):
		flag = False
		for binge in soup.findAll('section', {"aria-label": "Binge-worthy Series"}):
			type(binge)
			resultbinge = binge.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = binge.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = binge.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = binge['data-section-type']
			if (resultbinge):
				if (resultbinge.text in final_lookup_dict):
					titles.append(resultbinge.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_binge[resultbinge.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_binge[resultbinge.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)

			else:
				titles.append("")
				title_priority_dict_binge[""] = ("")

			date_to_title_dict_binge[int(keys)] = title_priority_dict_binge
				
	if soup.findAll('section', {"aria-label": "Documentaries"}):
		flag = False
		for documentary in soup.findAll('section', {"aria-label": "Documentaries"}):
			type(documentary)
			resultdocumentary = documentary.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = documentary.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = documentary.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = documentary['data-section-type']
			if (resultdocumentary):
				if (resultdocumentary.text in final_lookup_dict):
					titles.append(resultdocumentary.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_documentary[resultdocumentary.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_documentary[resultdocumentary.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)

				else:
					titles.append("")
					title_priority_dict_documentary[""] = ("")
			date_to_title_dict_documentary[int(keys)] = title_priority_dict_documentary
				
	if soup.findAll('section', {"aria-label": "Drama"}):
		flag = False
		for drama in soup.findAll('section', {"aria-label": "Drama"}):
			type(drama)
			resultdrama = drama.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
			resultsubtitle = drama.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = drama.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = drama['data-section-type']
			if (resultdrama):
				if (resultdrama.text in final_lookup_dict):
					titles.append(resultdrama.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True
					if (flag == True):
						title_priority_dict_drama[resultdrama.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_drama[resultdrama.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)
				else:
					titles.append("")
					title_priority_dict_drama[""] = ("")
			date_to_title_dict_drama[int(keys)] = title_priority_dict_drama
				
	if soup.findAll('section', {"aria-label": "Films"}):
		flag = False
		for films in soup.findAll('section', {"aria-label": "Films"}):
			type(films)
			resultfilms = films.find('div', {"class": "content-item__title typo typo--skylark typo--bold"})
			resultsubtitle = films.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = films.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = films['data-section-type']
			if (resultfilms):
				if (resultfilms.text in final_lookup_dict):
					titles.append(resultfilms.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True 
					if (flag == True):
						title_priority_dict_films[resultfilms.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_films[resultfilms.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)
				else:
					titles.append("")
					title_priority_dict_films[""] = ("")
			date_to_title_dict_films[int(keys)] = title_priority_dict_films

	if soup.findAll('section', {"aria-label": "Entertainment"}):
		flag = False
		for entertainment in soup.findAll('section', {"aria-label": "Entertainment"}):
			type(entertainment)
			resultentertainment = entertainment.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
			resultsubtitle = entertainment.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = entertainment.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = entertainment['data-section-type']
			if (resultentertainment):
				if (resultentertainment.text in final_lookup_dict):
					titles.append(resultentertainment.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True 
					if (flag == True):
						title_priority_dict_entertainment[resultentertainment.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_entertainment[resultentertainment.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)
				else:
					titles.append("")
					title_priority_dict_entertainment[""] = ("")
			date_to_title_dict_entertainment[int(keys)] = title_priority_dict_entertainment
				
	if soup.findAll('section', {"aria-label": "Sport"}):
		flag = False
		for sport in soup.findAll('section', {"aria-label": "Sport"}):
			type(sport)
			resultsport = sport.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
			resultsubtitle = sport.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = sport.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			priority = sport['data-section-type']
			if (resultsport):
				if (resultsport.text in final_lookup_dict):
					titles.append(resultsport.text)
					page_new = requests.get("https://web.archive.org" + subtitle_url)
					soup_new = BeautifulSoup(page_new.text, features = "html.parser")
					if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
						flag = True
					elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
						subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
						flag = True 
					if (flag == True):
						title_priority_dict_sport[resultsport.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_sport[resultsport.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)

				else:
					titles.append("")
					title_priority_dict_sport[""] = ("")
			date_to_title_dict_sport[int(keys)] = title_priority_dict_sport
				
	if soup.findAll('section', {"aria-label": "Box Sets"}):
		flag = False
		for box in soup.findAll('section', {"aria-label": "Box Sets"}):
			type(box)
			resultbox = box.find('div', {"class": "content-item__title typo typo--skylark typo--bold"}) 
			resultsubtitle = box.find('a', {"class": "content-item__link gel-layout gel-layout--flush"})
			type_val = box.find('span', {"class": "typo typo--bullfinch content-item__label typo--bold content-item__label--wrap"})
			subtitle_url = resultsubtitle['href']
			page_new = requests.get("https://web.archive.org" + subtitle_url)
			soup_new = BeautifulSoup(page_new.text, features = "html.parser")
			if soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"}):
				subtitle_val = soup_new.find('span', {"class": "typo typo--skylark play-cta__text__subtitle"})
				flag = True
			elif soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"}):
				subtitle_val = soup_new.find('span', {"class": "typo typo--bold play-cta__title typo--skylark"})
				flag = True 
			priority = box['data-section-type']
			if (resultbox):
				if (resultbox.text in final_lookup_dict):
					titles.append(resultbox.text)
					if (flag == True):
						title_priority_dict_box[resultbox.text] = (subtitle_val.text, " Priority Level ", priority, " Genre ", type_val.text)
					else:
						title_priority_dict_box[resultbox.text] = ("No episode", " Priority Level ", priority, " Genre ", type_val.text)
			# print(resultfeatured)

				else:
					titles.append("")
					title_priority_dict_box[""] = ("")
			date_to_title_dict_box[int(keys)] = title_priority_dict_box


df_featured = pd.DataFrame.from_dict(date_to_title_dict_featured, orient="index")
df_bbcthree = pd.DataFrame.from_dict(date_to_title_dict_bbcthree, orient="index")
df_bestofbbcthree = pd.DataFrame.from_dict(date_to_title_dict_bestofbbcthree, orient="index")
df_popular = pd.DataFrame.from_dict(date_to_title_dict_popular, orient="index")
df_binge = pd.DataFrame.from_dict(date_to_title_dict_binge, orient="index")
df_documentary = pd.DataFrame.from_dict(date_to_title_dict_documentary, orient="index")
df_drama = pd.DataFrame.from_dict(date_to_title_dict_drama, orient="index")
df_films = pd.DataFrame.from_dict(date_to_title_dict_films, orient="index")
df_entertainment = pd.DataFrame.from_dict(date_to_title_dict_entertainment, orient="index")
df_sport = pd.DataFrame.from_dict(date_to_title_dict_sport, orient="index")
df_box = pd.DataFrame.from_dict(date_to_title_dict_box, orient="index")

df_featured.to_csv('iplayer_featured1.csv')
df_bbcthree.to_csv('iplayer_bbcthree1.csv')
df_bestofbbcthree.to_csv('iplayer_bestofbbcthree1.csv')
df_popular.to_csv('iplayer_popular1.csv')
df_binge.to_csv('iplayer_binge1.csv')
df_documentary.to_csv('iplayer_documentary1.csv')
df_drama.to_csv('iplayer_drama1.csv')
df_films.to_csv('iplayer_films1.csv')
df_entertainment.to_csv('iplayer_entertainment1.csv')
df_sport.to_csv('iplayer_sport1.csv')
df_box.to_csv('iplayer_box1.csv')
