import requests
import json
r = requests.post('https://smp.co.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices?priceHistory=1', json={"marketIds":["708.52326592","708.52454495","708.52391935","708.52402670","708.52328823","708.52389496","708.52372737","708.52374294","708.52448732","708.52465504","708.52465622","708.52454505","708.52454494"]})
json_object = json.dumps(r.json(), indent=4)
print(r.status_code)

f = open('test_file.json', 'w')
f.write(json_object)
f.close()