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


if __name__ == "__main__":
    confirm_config()
    client = Client(
        access_token = ACCESS_TOKEN,
        environment = config.get("DEFAULT", "environment")
    )
    # location = client.locations.retrieve_location(location_id=LOCATION_ID).body["location"]
    # result = request_catalog(client)
    # result = request_modifiers(client, "Add Toppings")
    categories_out(client)

    

    # print(result['items'][1]['item_data'])
    
    # for mod_list in result['objects']:
    #     for modifier in mod_list['modifier_list_data']['modifiers']:
    #         file.write(f"{str(modifier['modifier_data']['name'])}: {str(modifier['modifier_data']['price_money']['amount'])}\n")
    #     file.write("\n")
