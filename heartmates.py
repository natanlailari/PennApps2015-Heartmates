# PennApps

from flask import Flask, jsonify, render_template, request
import csv
import json
import requests
from requests.auth import HTTPBasicAuth
from threading import Thread

app = Flask(__name__)


@app.route('/')
def home():
    '''This is what you will see if you go to http://127.0.0.1:5000'''
    return render_template('main.html'); 

# @app.route('/nutrition_facts', methods=['POST'])
@app.route('/nutrition_facts/', methods=['POST'])
def nutrition_facts():
    # Get data from post request
    items = json.loads(request.data)['items']
    resps = ['' for x in xrange(len(items))]

    # Set up session
    FE_APIKey = 'n54k3jg9cpkwzvaam4vavc7c'
    params = {'uid': 'user1', 'devid':'device1',
               'appide': 'heartmates', 'f':'json',
               'api_key': FE_APIKey}
    url_create = 'http://api.foodessentials.com/createsession'
    resp = requests.get(url_create, params=params)
    sid = resp.json()['session_id']

    # Set profile
    # API requires entire JSON to be sent to set up profile
    prof_json = '{"session_id":' + str(sid) + ',"nutrients":[{"name":"Calcium","value":"true"},{"name":"Calories","value":"true"},{"name":"Calories from Fat","value":"false"},{"name":"Cholesterol","value":"false"},{"name":"Dietary Fiber","value":"true"},{"name":"Insoluble Fiber","value":"true"},{"name":"Iron","value":"true"},{"name":"Monounsaturated Fat","value":"true"},{"name":"Other Carbohydrate","value":"true"},{"name":"Polyunsaturated Fat","value":"true"},{"name":"Potassium","value":"true"},{"name":"Protein","value":"true"},{"name":"Saturated Fat","value":"false"},{"name":"Saturated Fat Calories","value":"false"},{"name":"Sodium","value":"false"},{"name":"Soluble Fiber","value":"true"},{"name":"Sugar Alcohol","value":"false"},{"name":"Sugars","value":"false"},{"name":"Total Carbohydrate","value":"true"},{"name":"Total Fat","value":"true"},{"name":"Vitamin A","value":"true"},{"name":"Vitamin C","value":"true"}],"allergens":[{"name":"Cereals","value":"false"},{"name":"Coconut","value":"false"},{"name":"Corn","value":"false"},{"name":"Egg","value":"true"},{"name":"Fish","value":"false"},{"name":"Gluten","value":"false"},{"name":"Lactose","value":"true"},{"name":"Milk","value":"true"},{"name":"Peanuts","value":"false"},{"name":"Sesame Seeds","value":"false"},{"name":"Shellfish","value":"false"},{"name":"Soybean","value":"false"},{"name":"Sulfites","value":"false"},{"name":"Tree Nuts","value":"false"},{"name":"Wheat","value":"false"}],"additives":[{"name":"Acidity Regulator","value":"true"},{"name":"Added Sugar","value":"false"},{"name":"Anti-Caking Agents","value":"true"},{"name":"Anti-Foaming Agent","value":"true"},{"name":"Antioxidants","value":"true"},{"name":"Artificial Color","value":"true"},{"name":"Artificial Flavoring Agent","value":"true"},{"name":"Artificial Preservative","value":"true"},{"name":"Bulking Agents","value":"true"},{"name":"Colors","value":"true"},{"name":"Emulsifiers","value":"true"},{"name":"Enzyme","value":"true"},{"name":"Firming Agent","value":"true"},{"name":"Flavor Enhancer","value":"true"},{"name":"Flour Treating Agent","value":"true"},{"name":"Food Acids","value":"true"},{"name":"Gelling Agents","value":"true"},{"name":"Glazing Agent","value":"true"},{"name":"Humectants","value":"true"},{"name":"Leavening Agent","value":"true"},{"name":"Mineral Salt","value":"true"},{"name":"Natural Color","value":"true"},{"name":"Natural Flavoring Agent","value":"true"},{"name":"Natural Preservative","value":"true"},{"name":"Preservatives","value":"true"},{"name":"Propellant","value":"true"},{"name":"Raising Agents","value":"true"},{"name":"Saturated Fat","value":"false"},{"name":"Sequestrant","value":"true"},{"name":"Stabilizers","value":"true"},{"name":"Sweeteners","value":"true"},{"name":"Thickeners","value":"true"},{"name":"Trans Fat","value":"true"},{"name":"Unsaturated Fat","value":"true"},{"name":"Vegetable Gum","value":"true"}],"myingredients":[],"mysort":[{"sort_variable":"Calories","sort_order":1,"variable_type":1}]}'
    params = {'json': prof_json, 'api_key': FE_APIKey}
    url_setprof = 'http://api.foodessentials.com/setprofile'
    resp = requests.post(url_setprof, params=params)


    # Get product info
    url_product = 'http://api.foodessentials.com/productscore'
    # Practice UPC values
    UPC_list = {'Bacon' : '093966004656', 
                'Broccoli': '032601025090',
                'Extra Firm Tofu' : '076371011075',
                'King Arthur Flour' : '030000012031',
                'Prairie Farms Milk' : '041234639642',
                'Quaker Steel Cut Oats' : '021908453361',
                'Sliced Peaches' :'024000167136',
                'Extra Virgin Oil' : '634039000016',
                'Kendall Brooke Salmon' : '15078'}

    # Multithreaded API calls to get item info, fully scalable
    threads = []
    for num in xrange(len(items)):
        params = {'u': UPC_list[items[num]], 'sid':sid, 'f':'json','api_key':FE_APIKey}
        threads.append(Thread(target=get_request, args=(params, num, resps)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Scrape product score from response JSON and return flattened JSON of all product scores
    scores = [str(resp.json()['product']['productscore']) for resp in resps]
    return json.dumps(dict(zip(items,scores)))

def get_request(params, num, resps):
    url_product = 'http://api.foodessentials.com/productscore'
    resps[num] = requests.get(url_product, params=params)


@app.route('/postmates_delivery/<dropoff_address>/')
def postmates_delivery(dropoff_address):

    # Preparing API call
    PM_Test_APIKey = 'd184ecab-5f46-42fd-bbfc-28b73b88cf4e'
    PM_cust_id = 'cus_KAay_YCGWhyi_k'
    url = 'https://api.postmates.com'
    url_delivery = url + '/v1/customers/' + PM_cust_id + '/delivery_quotes'
    headers = {'user': 'd184ecab-5f46-42fd-bbfc-28b73b88cf4e'}
    data = {'pickup_address': '2001 Pennsylvania Avenue Philadelphia, PA 19130',
    'dropoff_address': dropoff_address}
    
    # Sending API request
    resp = requests.post(url_delivery, data=data, auth=HTTPBasicAuth('d184ecab-5f46-42fd-bbfc-28b73b88cf4e', ''))

    # Parsing API response
    rj = resp.json()
    c_vals = (rj['created'].lstrip('0123456789-').lstrip('T').rstrip('Z')).split(':')
    eta_vals = (rj['dropoff_eta'].lstrip('0123456789-').lstrip('T').rstrip('Z')).split(':')
    fee = ('$'+str(int(rj['fee'])/100.0)+'0')[:6]

    # Return fee, request time, and expected delivery time (eta)
    return str(json.dumps({'fee': fee, 'created':str(int(c_vals[0]) - 5) +':'+ c_vals[1] +':'+ c_vals[2], 'eta': str(int(eta_vals[0]) - 5) +':'+ eta_vals[1] +':'+ eta_vals[2]}))





if __name__ == '__main__':
    app.run(debug=True)
