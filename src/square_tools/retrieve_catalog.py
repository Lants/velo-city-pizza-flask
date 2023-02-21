import configparser
from square.client import Client

# Parse config file
config = configparser.ConfigParser()
config.read("square_config.ini")

# Read environment mode
PROD_TYPE = config.get("DEFAULT", "environment").upper()
if PROD_TYPE == "PRODUCTION":
    IS_PROD = True
elif PROD_TYPE == "SANDBOX":
    IS_PROD = False
else:
    raise Exception(f"Invalid production mode (expected 'sandbox' or 'production', received '{PROD_TYPE.lower()}')")

# Retrieve config data based on production mode
APPLICATION_ID = config.get(PROD_TYPE, "square_application_id")
ACCESS_TOKEN = config.get(PROD_TYPE, "square_access_token")
LOCATION_ID = config.get(PROD_TYPE, "square_location_id")


def confirm_config():
    print(f"PROD_TYPE={PROD_TYPE}")
    print(f"IS_PROD={IS_PROD}")

def request_catalog(client):
    return client.catalog.search_catalog_items(
        body = {
            "text_filter": "artichoke"
        }
    ).body

def request_modifiers(client, query):
    return client.catalog.search_catalog_objects(
        body = {
            "object_types": ["MODIFIER_LIST"],
            "query": {"text_query": {"keywords": ["Add Toppings"]}}
        }
    ).body

def categories_out(client):
    result = client.catalog.list_catalog(
        types = "category"
    ).body

    file = open("categories.out", "w")
    for category in result['objects']:
        file.write(f"{category['category_data']['name']}\n")

    file.close()

def topping_modifiers_out(client, file):
    result = request_modifiers(client, "Toppings")

    if len(result['objects']) != 2:
        print("ERROR in topping_modifiers_out(): Unexpected number of modifiers")
        file.close()
        return

    def retrieve_toppings(modifier):
        ret = f"\"{str(modifier['modifier_data']['name'])}\" = {float(modifier['modifier_data']['price_money']['amount']) / 100}\n"
        return ret.replace(":", " —").replace("Housemade ", "").replace("Add ", "")

    # Big Toppings
    file.write("\n[TOPPINGS BIG]\n")
    for modifier in result['objects'][0]['modifier_list_data']['modifiers']:
        file.write(retrieve_toppings(modifier))

    # Small Toppings
    file.write("\n[TOPPINGS SMALL]\n")
    for modifier in result['objects'][1]['modifier_list_data']['modifiers']:
        file.write(retrieve_toppings(modifier))
    

def search_categories(client, category_names):
    category_ids = []
    for category in category_names:
        category_ids.append(
            client.catalog.search_catalog_objects(
                body = {
                    "object_types": ["CATEGORY"],
                    "query": {"text_query": {"keywords":[category]}}
                }
            ).body['objects'][0]['id']
    )
    return category_ids

def starters_out(client):
    category_names = ["starter", "salad", "soup"]
    category_ids = search_categories(client, category_names)
    file = open("starters.ini", "w")
    file.write("[STARTERS]\n")

    for id in category_ids:
        result = client.catalog.search_catalog_items(
            body = {
                "category_ids": [id]
            }
        )
        for item in result.body['items']:
            file.write(f"\"{item['item_data']['name']}\" = ")
            if 'description' in item['item_data'].keys():
                file.write(f"\"{item['item_data']['description']}\"\n")
            else:
                file.write("\"\"\n")

    file.close()


def pizzas_out(client):
    category_names = ["pizzas"]
    category_ids = search_categories(client, category_names)
    file = open("pizzas.ini", "w")
    pizzas = {}
    pizzas["Big Wheel Pizza: 16 Inch"] = ""
    pizzas["Small Wheel Pizza: 7 Inch"] = ""
    pizzas["Calzone (7 inch) *"] = ""
    prices = []

    result = client.catalog.search_catalog_items(
        body = {
            "category_ids": [category_ids[0]]
        }
    )
    for item in result.body['items']:
        name = item['item_data']['name']
        # print(item['item_data']['modifier_list_info']['modifier_list_id'])
        print(item['item_data']['variations'][0]['item_variation_data']['price_money']['amount'])
        prices.append((item['item_data']['variations'][0]['item_variation_data']['price_money']['amount'] / 100))
        if 'description' not in item['item_data'].keys():
            continue
        inch_conversion_desc = item['item_data']['description'].replace("\"", " Inch")
        if "big wheel" in name.lower():
            pizzas["Big Wheel Pizza (16 Inch)"] = inch_conversion_desc
        elif "small wheel" in name.lower():
            pizzas["Small Wheel Pizza: (7 Inch)"] = inch_conversion_desc
        else: # Calzone
            pizzas["Calzone (7 inch) *"] = inch_conversion_desc

    # Write Prices
    file.write("[PRICES]\n")
    file.write(f"prices = {prices}\n")

    # Write Names and Descriptions
    file.write("\n[PIZZAS]\n")
    for pizza_name in pizzas.keys():
        file.write(f"\"{pizza_name}\" = \"{pizzas[pizza_name]}\"\n")

    topping_modifiers_out(client, file)
    file.close()


if __name__ == "__main__":
    confirm_config()
    client = Client(
        access_token = ACCESS_TOKEN,
        environment = config.get("DEFAULT", "environment")
    )
    # location = client.locations.retrieve_location(location_id=LOCATION_ID).body["location"]

    # categories_out(client)
    starters_out(client)
    pizzas_out(client)

    

    # print(result['items'][1]['item_data'])
    