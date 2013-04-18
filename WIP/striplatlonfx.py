def latlon(y):
	split = laton.split(',')
	print split


-split and strip have no tuple object so --> regex


Test String: (37.78887833333333, -122.41146527777778) 
[^)](.*),(.*)\d

Match Groups:
1.	37.78887833333333
2.	 -122.4114652777777



match = re.search(r"field2:\s(.*)", subject)
if match:
    result = match.group(1)
else:
    result = ""

WORKS!






l = str(latlon)
def latlong(l):
	match = re.search(r"[^)](.*),(.*)\d", l)
	if match:
		latitude = match.group(1)
		print latitude
		longitude = match.group(2)
		print longitude
	else:
		print "?"


