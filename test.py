import requests,json
payload=json.dumps({"title":"Welkomen Boys","content":"Requests in de ting"})


response = requests.post('http://127.0.0.1:8000/posts', data=payload,headers={ 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJleHAiOjE2Njc5MTA1NzR9.MYyVKgAaX4JBolGpGsNm025lLjFZ7XYHH7mxudEsNZo' })
print(response.json())


