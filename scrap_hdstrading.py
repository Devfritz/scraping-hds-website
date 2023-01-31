import requests
# import urllib.request
from bs4 import BeautifulSoup
import json
import pandas as pd


# read csv HDS data
HDS_product = pd.read_csv('hds_1.csv', encoding="ISO-8859-1")

is_create_csv_description = False
countHds = len(HDS_product)
count_items = 0
count_images = 0
count_hds = 0
for i in range(len(HDS_product)):
    try:
        no_vendor_item_no = str(HDS_product.iloc[i, 0])
        print(no_vendor_item_no)
        sku = str(HDS_product.iloc[i, 1])
        url = f"https://hdstrading.com/products/{no_vendor_item_no}"
        page = requests.get(url)
        print(page.status_code)
        count_items += 1
        if page.status_code == 200:
            count_hds += 1
            print(f"item {count_items} ====> {countHds}")
            print(f"count hds {count_hds}")
            content = page.content
            soup = BeautifulSoup(content, 'html.parser')

            # #######################    Images Products  ##########################################
            soap_images = soup.find(
                "div", {"class", "product-single__media-group-wrapper"})
            all_images = soap_images.find_all('img')
            print(f"{sku} ====> {len(all_images)} images")
            count_images += len(all_images)
            alt_img = 0
            for img in all_images:
                url_img = f"https:{img['src']}"
                if '_' not in url_img:
                    getOriginalSize = url_img
                    print(getOriginalSize)
                    print('link images => ' + getOriginalSize)
                    request_img = requests.get(getOriginalSize, stream=True)
                    if request_img.status_code:
                        name = str(sku) + ".jpg" if not alt_img else str(sku) + \
                            "_" + str(alt_img) + ".jpg"
                        with open(f"{name}", 'wb') as fileImg:
                            fileImg.write(request_img.content)
                        alt_img += 1
                        print(f"{name} download...............")

            #################################  Description Product  ###############################
            description = soup.find(
                "div", {"class", "product-single__description rte"})
            list_des = description.findAll('li')
            shortFull = ""
            for item in list_des:
                shortFull = shortFull + '<li>' + item.get_text() + '</li>'

            original_description = f"{description.find('p').get_text()} </br> <ul> {shortFull} </ul>"

            try:
                if not is_create_csv_description:
                    new_data = [[sku, original_description]]
                    new_df = pd.DataFrame(
                        new_data, columns=['SKU', 'Description'])
                    new_df.to_csv('description.csv', mode='a',
                                  header=True, index=False)
                    is_create_csv_description = True
                else:
                    new_data = [[sku, original_description]]
                    new_df = pd.DataFrame(
                        new_data, columns=['SKU', 'Description'])
                    new_df.to_csv('description.csv', mode='a',
                                  header=False, index=False)
                    print(f"description {sku} creating...")
            except:
                print('Error csv')
        else:
            print()
    except:
        continue


print('Finish..........')
print(f"Items  => {count_items}")
print(f"Images download => count_images")
