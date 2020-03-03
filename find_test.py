# -*- coding: utf-8 -*-
#!/usr/bin/python
import re
a = ['[16] Happy Pizza (09:00 - 22:00)','[22] Стоп_Fishka (10:30 - 20:30)','[31] Центр плова и шашлыка (11:00 — 23:00)','[45] OZYURT (11:00 — 22:00)']
for element in a:
	if '[16]' in element:
		print 'True'
	else:
		print 'False'