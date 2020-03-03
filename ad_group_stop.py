# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example updates status for a given ad group.
To get ad groups, run get_ad_groups.py.
The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.
"""

from googleads import adwords
import sys
from time import localtime, strftime
f = open('log.txt','a')
AD_GROUP_ID = '44703443887'

def main(client, allads, status):
  # Initialize appropriate service.
  ad_group_service = client.GetService('AdGroupService', version='v201809')

  operations = []
  for adgoup in allads:
    a = {'operator': 'SET',
        'operand': {
        'id': adgoup,
        'status': status
        }
    }
    operations.append(a)
  print (operations, "Yeah Baby")
  # Construct operations and update an ad group.


  ad_groups = ad_group_service.mutate(operations)

  # Display results.
  for ad_group in ad_groups['value']:
    if ad_group['name'] and ad_group['id'] and ad_group['status']:
      print ('Ad group with name \'%s\' and id \'%s\' was updated to \'%s\.'% (ad_group['name'], ad_group['id'],ad_group['status']))
      f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()))
      f.write('\n')
      f.write('Ad group with name \'%s\' and id \'%s\' was updated to \'%s\. \n'% (ad_group['name'], ad_group['id'],ad_group['status']))

if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client, AD_GROUP_ID, AD_GROUP_ID2, status)
