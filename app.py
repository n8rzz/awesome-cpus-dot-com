import requests
import os
from flask import Flask, render_template
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ASSOCIATE_TAG = os.getenv('ASSOCIATE_TAG')

    # search_results_amd = search_amazon_cpus(API_KEY, SECRET_KEY, ASSOCIATE_TAG, manufacturer='AMD')
    search_results = search_amazon_cpus(API_KEY, SECRET_KEY, ASSOCIATE_TAG)

    # Process and prepare data for HTML rendering
    data = process_results(search_results)

    return render_template('index.html', amd_data=data)

def search_amazon_cpus(api_key, secret_key, associate_tag, keywords='CPU', manufacturer=None):
    return
    # GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    base_url = 'https://webservices.amazon.com/paapi5/searchitems'
    access_key = api_key
    secret_key = secret_key
    partner_tag = associate_tag
    params = {
        'Keywords': keywords,
        'SearchIndex': 'Electronics',
        'SortBy': 'Relevance',
        'PartnerType': 'Associates',
        'PartnerTag': partner_tag,
        'AccessKey': access_key,
    }

    if manufacturer:
        params['Keywords'] = f'{manufacturer} {keywords}'

    url = f'{base_url}?{urlencode(params)}'
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return None

def process_results(results):
    data = []

    if results:
        for item in results.get('Items', []):
            title = item.get('ItemInfo', {}).get('Title', 'N/A')
            asin = item.get('ASIN', 'N/A')
            price = item.get('Offers', {}).get('Listings', [{}])[0].get('Price', {}).get('DisplayAmount', 'N/A')
            data.append({'Title': title, 'ASIN': asin, 'Price': price})
    return data

if __name__ == '__main__':
    app.run(debug=True)
