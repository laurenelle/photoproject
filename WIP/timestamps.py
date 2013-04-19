
Sample output:
2013:04:10 17:45:55

2013:04:07 12:12:54

smalldatetime
1900-01-01 00:00:00
datetime
1753-01-01 00:00:00.000

strpdatetime(yy)

2013:04:10 17:45:55


 ALTER [ COLUMN ] column [ SET DATA ] TYPE type [ USING expression ]
 ALTER TABLE photos ALTER COLUMN timestamp TYPE smallDateTime;

 // smalldatetime doesn't exist?????




 current_time = datetime.datetime.now()


 import time




THIS WORKS

output = '2013:04:07 12:12:54'
correctformat = time.strptime(output, "%Y:%m:%d %H:%M:%S")

print correctformat

