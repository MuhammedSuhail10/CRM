from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from django.conf import settings
from facebook_business.adobjects.lead import Lead
from facebook_business.exceptions import FacebookRequestError
import requests

def fetch_facebook_lead_data(id):
    access_token=settings.FACEBOOK_ACCESS_TOKEN
    url = f"https://graph.facebook.com/{id}?fields=field_data&access_token={access_token}"
    response = requests.get(url)
    print(f'Response is {response}')
    if response.status_code == 200:
        lead_data = response.json().get("field_data", [])
        print(f'Lead data is {lead_data}')
        lead_info = {"email": None, "number": None, "name": None}
        for data in lead_data:
            print(data)
            if data.get("name", None) in ["email", "email"]:
                lead_info["email"] = data.get("values")[0].strip().lower()
            elif data.get("name", None) in ["phone_number", "phone"]:
                lead_info["number"] = data.get("values")[0].strip()
            elif data.get("name", None) in ["full_name", "name"]:
                lead_info["name"] = data.get("values")[0].strip()
        return lead_info