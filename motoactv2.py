import requests,json,logging
from requests.auth import HTTPBasicAuth
import http.client as http_client

http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

s = requests.Session()
s.verify=False
#s.get("https://www.motoactv.com/")

loginUrl = "https://www.motoactv.com/session/login.json"
email="richard.young00@gmail.com"
password="0706402y"
data = "screen_name="+email+"&password="+password+"&remember_me=1"
loginResponse = s.get(loginUrl+"?"+data)

if '{"code":"1","return_url":"/dashboard/index"}' in loginResponse.text:
    print("MOTO - Logged in.")
else:
    print("MOTO - Failed login")
    print(loginResponse.text)
    sys.exit()

#export

exportUrl = 'https://www.motoactv.com/export/exportData.json'
params = {'startDate':'','endDate':'','exportAll':'true','formats[]':'TCX'}


r = s.post(exportUrl, data=params)
if r.status_code == requests.codes.ok:
    print("\n" + r.text)
    print("\nExporting " + str(r.json().get("workoutsExported")) + " workouts")
else:
    print("Unable to download workouts")
    print(r.text)
    sys.exit()
    
exportId = r.json().get('exportID')
print('\nExport ID is ' + exportId)

fileResponse = s.get('https://www.motoactv.com/export/downloadExport?exportID=' + exportId, stream=True)

with open('workout.zip', 'wb') as f:
        for chunk in fileResponse:
            f.write(chunk)
