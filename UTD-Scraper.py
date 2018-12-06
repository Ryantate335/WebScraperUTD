
# coding: utf-8

# In[52]:


import requests
from bs4 import BeautifulSoup

starter_page = 'https://catalog.utdallas.edu/'
years = ['2018', '2017', '2016', '2015', '2014', '2013', '2012']
undergraduate_courses = '/undergraduate/courses/school/'
schools = ['jsom', 'nsm', 'ah', 'is', 'ecs', 'bbs', 'epps', 'ugrad']

for year in years:
    txtfile = open("UTD_Courses"+ year +".txt", "w")
    for school in schools:
        full_url = starter_page + year + undergraduate_courses + school
        site = requests.get(full_url)
        if site.status_code is 200:
            content = BeautifulSoup(site.content, 'html.parser')
            container_courses = content.findAll('p')
            for course in container_courses:
                if course is not None:
                    txtfile.write(course.text + "\n")
        else:
            print("Failed to open site")
    txtfile.close()
    
print("Finished!")

