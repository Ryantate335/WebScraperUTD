
# coding: utf-8

# In[103]:


#This program goes through each degree plan page at UTD starting from 2018 going down to 2012.
#It makes a text file showing the requirements for each degree plan and grabs details including name,
#required credit hours, courses, and minor information. It also keeps classes with "or" by them on the same line and removes
#footnote numbers and commas from wherever they appear to make parsing easier. To prevent making a file 
#for degrees which share a link, redundant links are removed from the list. It also organizes each text file 
#by putting them into a file category based off of their year followed by their school. 
#Note: atec folders will be empty before 2015 due to the school not existing before then.
import requests
from bs4 import BeautifulSoup
import re
import pathlib
import time
import os
import string

def removeDuplicates (containers):
    final_list = []
    for links in containers:
        duplicate = False
        url = links.get('href')
        for final_list_link in final_list:
            if (final_list_link.get('href') == url) or (url.find('#') is not -1):
                duplicate = True
                break
        if duplicate is False:
            final_list.append(links)
    return final_list
            

pathlib.Path('./DegreePlans').mkdir(parents=True, exist_ok=True)
print("start")
schools = ['ah','jsom', 'nsm',  'is', 'ecs', 'bbs', 'epps', 'atec']
main_URL = 'http://catalog.utdallas.edu/'
years = ['2018', '2017', '2016', '2015', '2014', '2013', '2012']
main_URL_part = '/undergraduate/programs'

for year in years:
    file_path = './DegreePlans/' + year
    pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
    main_URL_full = main_URL + year + main_URL_part
    main_site = requests.get(main_URL_full)
    if main_site.status_code is not 200:
        print("Failed to open link")
        time.sleep(2)
        continue
    content = BeautifulSoup(main_site.content, 'html.parser')
    main_container = content.find('div', attrs = {'id':'bukku-page'})
    for school in schools:
        file_path = './DegreePlans/' + year + '/' + school
        pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
        school_URLs = main_URL_full + '/' + school + '/'
        degreeplans_containers = removeDuplicates(main_container.findAll('a', href = re.compile(school_URLs)))
        for link in degreeplans_containers:
            #setting up file and directory
            degree_name = link.text
            if degree_name.find('/') is not -1:
                degree_name = degree_name.replace('/',':')
            filename = os.path.join(file_path, degree_name + '.txt')
            txtfile = open(filename, "w")
            #going onto degree plan site
            degree_page = requests.get(link.get('href'))
            if degree_page.status_code is not 200:
                print("Failed to open link")
                time.sleep(2)
                continue
            degree_page_content = BeautifulSoup(degree_page.content, 'html.parser')
            degree_requirements = degree_page_content.find_all(class_= ['cat-reqa','cat-reqg', 'cat-reqi', 'cat-cat3'])
            for requirements in degree_requirements:
                text_for_requirements = requirements.text
                #removes footnotes
                if text_for_requirements is not -1:
                    without_footnotes = text_for_requirements.split(',')
                    text_for_requirements = without_footnotes[0] 
                if text_for_requirements.find('or ',0,4) is -1:
                    txtfile.write('\n')
                text_for_requirements = text_for_requirements.rstrip(string.digits)
                txtfile.write(text_for_requirements)
            txtfile.close()


print("Done!")

