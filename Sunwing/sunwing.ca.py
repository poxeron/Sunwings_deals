import json
from hmac import new
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd



def export_to_csv(json_data, output_file):
        df = pd.read_json(json_data)
        df.to_csv(output_file, index=False)


# try:
#     url = 'https://www.sunwing.ca/en/promotion/packages/all-inclusive-vacation-packages'
      
#     response = requests.get(url, timeout=10)
#     response.encoding = 'utf-8'
#     # Проверяем статус-код ответа
#     if response.status_code == 200:
#         # Инициализируем объект BeautifulSoup для парсинга HTML
#         soup = BeautifulSoup(response.text, "lxml")
#     else:
#         print(f"Не удалось получить доступ к странице, статус-код: {response.status_code}")
# except requests.Timeout:
#     print("Слишком долгое ожидание!")
# except requests.RequestException as e:
#     print(f"Произошла ошибка: {e}")


with open("./Sunwing/Sunwing_Packages.html", encoding="utf-8") as file:
    html_page = file.read()
soup = BeautifulSoup(html_page, "lxml")

deals_list = list()

load_all_deals = soup.find("div", id="travel-deals")

all_deals = soup.find_all("div", id="travel-deals")
for one_deal in all_deals:
    city, country = one_deal.find("h3", class_="Heading-module--heading--h5--3c7Iw Heading-module--heading--left--32lFv Hotel-module--hotelHeading--k73-z")\
        .find("span").text.strip().split(",")
    hotel = one_deal.find("div", class_="Hotel-module--hotelHeading__text--wJAbe").text.strip()
    rating = one_deal.find("div", class_="StarRating-module--rating--2P6IC")["rating"]
    dates = one_deal.find("div", class_="Hotel-module--hotelDetailsDays--1_9lF").find("span").text.strip()
    duration = one_deal.find("div", class_="Hotel-module--hotelDetailsDays--1_9lF").find("span").find_next("span").text.strip()
    pckg_type = one_deal.find("div", class_="Hotel-module--hotelDetailsDays--1_9lF").find("span").find_next("span").find_next("span").text.strip()
    discount = one_deal.find("div", class_="Hotel-module--hotelDetailsSave--3o-Wy").text.strip()
    old_price = one_deal.find("div", class_="Hotel-module--hotelDetailsWas--3fLWK").find("span").text.strip()
    new_price = one_deal.find("span", class_="Hotel-module--hotelDetailsAmount--2oExH").text.strip()
    link = one_deal.find("a",class_="CardBuilder-module--cardLink--uva-c")["href"]
    save = float(old_price[1:]) - float(new_price[1:])
    new_excel_line = {
                            "DISCOUNT": discount,
                            "RATING": rating,
                            "NEW PRICE": new_price,
                            "Save $": save,
                            "PACKAGE": pckg_type,
                            "DURATION": duration,
                            "DATES": dates,
                            "COUNTRY": country[1:],
                            "CITY":city,
                            "HOTEL": hotel,
                            "OLD PRICE": old_price,
                            "LINK": link
                        }
    deals_list.append(new_excel_line)
new_json = json.dumps(deals_list)

# export_to_csv(new_json, f"{destination_path}\\Multiplied_{summary_string_usStory}_{summary_provider}.csv")
export_to_csv(new_json, "./Sunwing_deals.csv")