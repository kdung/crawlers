#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 16:18:46 2017

@author: sophie
"""

import requests
from bs4 import BeautifulSoup
import csv


def crawl_staffs(url):
    
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    container = soup.find('div',{'id':'ISS_Main_T467AEC33012_Col00'})
    
    total_page = 1
    pagination = container.find('i',{'class':'pagination_total'})
    if pagination:
        total_page = int(pagination.text)
    url_pages = []
    for i in range(total_page):
        url_pages.append(url + '/' + str(i+1))
    
    staff_list = []
    for url_page in url_pages:
        print('crawling data from ' + url_page)
        html = requests.get(url_page)
        soup = BeautifulSoup(html.content, 'html.parser')
        container = soup.find('div',{'id':'ISS_Main_T467AEC33012_Col00'})
        staffs_container = container.findAll('div',{'class':'block-profile-thumb'})
        for staff in staffs_container:    
            staff_item = {}
            staff_item['name'] = staff.h2.a.text.strip()
            staff_item['title'] = staff.h3.text.strip()
            staff_item['email'] = ''
            email_tags = staff.findAll('my-email')
            if len(email_tags) == 1:
                email_tag = email_tags[0]
                staff_item['email'] = email_tag['data-user'] + '@' + email_tag['data-domain']
            staff_list.append(staff_item)
    print('total staffs ' + str(len(staff_list)))
    return staff_list

def export_csv(staff_list):
    f = csv.writer(open('iss_staffs.csv', 'w'))
    f.writerow(['name','title','email'])
    for staff_dict in staff_list: 
        f.writerow([str(staff_dict['name']), staff_dict['title'], staff_dict['email']])

if __name__ == '__main__':
    urls = ['https://www.iss.nus.edu.sg/about-us/iss-team/graduate-programme-chiefs',
        'https://www.iss.nus.edu.sg/about-us/iss-team/management',
        'https://www.iss.nus.edu.sg/about-us/iss-team/centres-of-excellence',
        'https://www.iss.nus.edu.sg/about-us/iss-team/practice-chiefs',
        'https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff',
        'https://www.iss.nus.edu.sg/about-us/iss-team/administration-staff',
        'https://www.iss.nus.edu.sg/about-us/iss-team/adjunct-staff']
    
    staffs = []
    for url in urls:
        staffs.extend(crawl_staffs(url))
    print('exporting to csv, total staffs: ' + str(len(staffs)))
    export_csv(staffs)