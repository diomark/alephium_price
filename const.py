"""Constants for the Alephium Price integration."""

DOMAIN = "alephium_price"
NAME = "Alephium Price"
API_ENDPOINT = "https://api.diadata.org/v1/assetQuotation/Alephium/tgx7VNFoP9DJiFMFgXXtafQZkUvyEdDHT9ryamHJYrjq"

UPDATE_INTERVAL = 120  # Update every 2 minutes by default

# Sensor attributes
ATTR_PRICE = "price"
ATTR_PRICE_YESTERDAY = "price_yesterday"
ATTR_VOLUME_YESTERDAY = "volume_yesterday_usd"
ATTR_SYMBOL = "symbol"
ATTR_NAME = "name"
ATTR_BLOCKCHAIN = "blockchain"
ATTR_DATA_SOURCE = "data_source"
ATTR_LAST_UPDATED = "last_updated"
ATTR_COLOR = "color" 