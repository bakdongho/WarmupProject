import requests
from bs4 import BeautifulSoup
import csv
import re

import socket
socket.getaddrinfo('localhost', 8080)

soup_objects = []

for i in range(1, 5981):
    base_url = f"https://www.haemukja.com/recipes/{i}"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_objects.append(soup)

    if soup.select_one('div.top > h1 > strong') is not None:
        food = soup.select_one('div.top > h1 > strong').get_text()
    else:
        food = ""
    # print(food)
    
    recipe_list = []
    sections = soup.select('section.sec_rcp_step > ol > li')
    for section in sections:
        if section.select_one('p') is not None:
            recipe = section.select_one('p').get_text()
            recipe_list.append(recipe)
        else:
            recipe = ""
        # print(recipe)

    ingredient_list = []
    sections2 = soup.select('div.btm > ul > li')
    for section2 in sections2:
        if section2.select_one('span') is None:
            ingredient = ""
        else:
            ingredient = section2.select_one('span').get_text()
            ingredient_list.append(ingredient)
        # print(ingredient)

    nutrition_list = []
    sections3 = soup.select('div.nutrition > ul > li')

    for section3 in sections3:
        if section3.select_one('p').get_text() is None:
            nutrition = ""
        else:
            nutrition = section3.select_one('p').get_text()
            nutrition_list.append(nutrition)
    # print(nutrition_list)

    tag_list = []
    sections4 = soup.select('div.box_tag')

    for section4 in sections4:
        tag_section = section4.find_all('a')
        for tags in tag_section:
            if tags.get_text() is None:
                tag = ""
            else:
                tag = tags.get_text()
                tag_list.append(tag)
    # print(tag_list)
    
    time_list = []
    sections5 = soup.select("div.top")

    for section5 in sections5:
        if section5.select_one("dl > dd").get_text() is None:
            time = ""
        else:
            time = section5.select_one("dl > dd").get_text()
            time_list.append(time)
    # print(time)

    scrap_list = []
    for section5 in sections5:
        if section5.select_one("dl > #scrap-cnt").get_text() is None:
            scrap = ""
        else:
            scrap = section5.select_one("dl > #scrap-cnt").get_text()
            scrap_list.append(scrap)
    # print(scrap)

    if soup.select_one('div.btm > div.dropdown') is None:
        person = ""
    else:
        person = soup.select_one('div.btm > div.dropdown').get_text().replace(' ', '').replace('\n', '')
    # print(person)


    data = {
        'food' : food,
        'recipe' : recipe_list,
        'ingredient' : ingredient_list,
        'nutrition' : nutrition_list,
        'tag' : tag_list,
        'time' : time_list,
        'scrap' : scrap_list,
        'person' : person
    }
    print(data)

    with open('./haemuk_data.csv', 'a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['food', 'recipe', 'ingredient', 'nutrition', 'tag', 'time', 'scrap', 'person']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writerow(data)
