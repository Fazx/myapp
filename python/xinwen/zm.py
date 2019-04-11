import requests
proxy={"http": "http://37.59.35.174:1080", "https": "http://37.59.35.174:1080"}
res=requests.get('https://www.leshui365.com/')
print(res.text)
