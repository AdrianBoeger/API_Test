import requests
import pandas as pd

print('Which ID do you want:')
objects_id = input()
url = 'https://api.restful-api.dev/objects/%s' % objects_id

try:
    response = requests.get(url)

    if response.status_code == 200:
        print('Response')
        objects_df = pd.json_normalize(response.json())
        print(response.json())
        # objects_df.to_excel(r'C:\Users\adrian.boeger\Desktop\Python\API_Test\data\objects.xlsx')
        print(objects_df)
    else:
        print('Error: Request failed with status code', response.status_code)

except requests.exceptions.RequestException as e:
    print('Error: It failed because of:', str(e))
