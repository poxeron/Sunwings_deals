import requests
from pprint import pprint
from jsonpath_ng import jsonpath, parse
import math
import pandas as pd
import urllib.request, json 


def export_to_csv(json_data, output_file):
        df = pd.read_json(json_data)
        df.to_csv(output_file, index=False)


sunwing_url = "https://www.sunwing.ca/page-data/en/promotion/packages/family-vacations/page-data.json"
try:
    response = requests.get(sunwing_url, timeout=10)
    if response.status_code == 200:
        with urllib.request.urlopen(sunwing_url) as url:
            data = json.load(url)
    else:
        print(f"Failed to access the page, status code: {response.status_code}")
except:
      print("Some issue with request or response")

# # with open("./Sunwing/Sunwing_Family_vacation.json", encoding="utf-8") as file:
# #     data = json.load(file)

deals_list = []
if data != None:
    admodules = data["result"]["data"]["contentfulFluidLayout"]["pageSections"]["pageSections"][1]["fields"]["admodule"]
    for admodule in admodules:
        for promo_group in admodule["PromotionGroups"]:
            for offers in promo_group["Offers"]:
                country = offers["Destination"]["CountryName"]
                city =   offers["Destination"]["Name"]
                hotel_name = offers["AccommodationInfo"]["AccommodationName"]
                hotel_rating = f'rating:{offers["AccommodationInfo"]["StarRating"]}'
                hotel_link = offers["DeepLink"]
                duration = offers["Duration"]
                departure_date = offers["DepartureDate"][:10]
                meal_plan = offers["MealPlan"]
                reg_price = offers["RegPrice"]
                new_price = offers["Price"] 
                save_in_dollars = int(reg_price) - int(new_price)
                save_in_percentage = offers["SaveUpto"]
                gateway = f"{offers["Gateway"]["Name"]}:{offers["Gateway"]["Code"]}"
                new_excel_line = {
                            "DISCOUNT IN %": save_in_percentage,
                            "HOTEL_RATING": hotel_rating,
                            "NEW PRICE": f"${new_price:}",
                            "SAVE IN DOLLARS": f"${save_in_dollars:}",
                            "DEPARTURE DATE":departure_date,
                            "PACKAGE": meal_plan,
                            "DURATION": duration,
                            "COUNTRY": country,
                            "CITY":city,
                            "HOTEL": hotel_name,
                            "OLD PRICE": f"${reg_price}",
                            "GATEWAY": gateway,
                            "LINK": hotel_link
                        }
                
                deals_list.append(new_excel_line)
    new_json = json.dumps(deals_list)
else:
    print("Data is empty. Please check your internet connection")

export_to_csv(new_json,  "./Sunwing_deals_json.csv")
        