import requests, json
from requests.auth import HTTPBasicAuth
from django.utils import timezone
from django.conf import settings
import base64
def access_token():
    consumer_key= settings.MPESA_CONSUMER_KEY
    consumer_secret= settings.MPESA_CONSUMER_SECRET 
    api_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response=requests.get(api_url, auth=HTTPBasicAuth(
        consumer_key, consumer_secret
    ))
    access_token=json.loads(response.text)    
    return access_token['access_token']

def mpesa_pay(phone, amount,callback, user_id, reason):
    timestamp=timezone.datetime.now().strftime('%Y%m%d%H%M%S')
    headers = {
    'Content-Type':'application/json',
    'Authorization':f'Bearer {access_token()}'
    }
    pwd="174379"+ settings.MPESA_PASS_KEY +timestamp
    password=base64.b64encode(pwd.encode('utf-8'))
    api_url='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    payload ={
        "BusinessShortCode":174379,
        "Password":password.decode('utf-8'),
        "Timestamp":timestamp,
        "TransactionType":"CustomerPayBillOnline",
        "Amount":amount,
        "PartyA":phone,
        "PartyB":174379,
        "PhoneNumber":phone,
        "CallBackURL":callback,
        "AccountReference":user_id,
        "TransactionDesc":f"{reason}"
    }
    response = requests.request("POST",api_url, headers=headers, json=payload)
    data=json.loads(response.text)   
    print(data) 