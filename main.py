# -*- coding: utf-8 -*-
import logging
import time
from googleads import adwords
import json
import requests
import re
import get_campaigns
import get_ad_groups
import json_parse
import ad_group_stop
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

#auth info
#adwords_client = adwords.AdWordsClient.LoadFromStorage('C:\Users\Administrator\Desktop\AdWordsPython/googleads.yaml')

adwords_client = adwords.AdWordsClient.LoadFromStorage('/home/user/Desktop/AdWordsPython/googleads.yaml')

import csv
#create temporary file
with open("newgroupads.csv", "w") as file:
	columns = ["id", "status"]
	writer = csv.DictWriter(file, fieldnames=columns)
	writer.writeheader()

#write statuses of ad groupes to temporary file
def WriteToDoc(resto):
	with open("newgroupads.csv", 'a') as file:
		writer = csv.writer(file)
		writer.writerow(resto)


#get feed
rest_feed = json_parse.main()
#get all campaigns
campaigns_feed = get_campaigns.main(adwords_client)
#get list of dicts of ad groups in campaigns, dict(Ad group NAME:Ad group ID)
ads_group_feed = {}
for campaign in campaigns_feed:
    ads_group_feed.update(get_ad_groups.main(adwords_client,campaign))


#search suitable ad grupes's statuses
def SearchFromDoc(rest_id, status):
	with open('new_file.csv', "r") as file:
		reader = csv.DictReader(file)
		for row in reader:
			if row["id"] == rest_id and row["status"] == str(status):
				return True
			elif row["id"] == rest_id and row["status"] != str(status):
				return False
		return False

enable_adgroups = []
pause_adgroups = []
for ad_group_name in ads_group_feed:
	for rest in rest_feed:
		rest_id = '[%s]' % rest['id']
		if rest_id in ad_group_name:
			if rest['status'] == 'active':
				if rest['is_working_now'] == 1:
					print ('work')
					if SearchFromDoc(rest_id, rest['is_working_now']) == False:
						enable_adgroups.append(str(ads_group_feed[ad_group_name]))
						WriteToDoc([rest_id, rest['is_working_now']])

				elif rest['is_working_now'] == 0:
					print ('dont work')
					print (enable_adgroups)
					if SearchFromDoc(rest_id, rest['is_working_now']) == False:
						print ('yup')
						pause_adgroups.append(str(ads_group_feed[ad_group_name]))
						WriteToDoc([rest_id, rest['is_working_now']])
			elif rest['status'] != 'active':
				print ('dont work')
				if SearchFromDoc(rest_id, 0) == False:
					print ('yup')
					pause_adgroups.append(str(ads_group_feed[ad_group_name]))
				WriteToDoc([rest_id, '0'])

if enable_adgroups:
	ad_group_stop.main(adwords_client, enable_adgroups, 'ENABLED')
if pause_adgroups:
	ad_group_stop.main(adwords_client, pause_adgroups, 'PAUSED')

#copy temporary file to new file                        
import shutil
shutil.copy(r'newgroupads.csv', r'new_file.csv')

#remove temporary file
import os

#os.remove("C:\Users\Administrator\Desktop\AdWordsPython/newgroupads.csv")
os.remove("/home/user/Desktop/AdWordsPython/newgroupads.csv")


