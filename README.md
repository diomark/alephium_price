# Alephium Price Integration for Home Assistant

This custom integration for Home Assistant fetches the current price of Alephium (ALPH) cryptocurrency from the DIA API and creates a sensor with price data and additional attributes.

## Installation

### Manual Installation

1. Copy the `alephium_price` folder into your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.
3. Go to **Configuration** → **Integrations** → **Add Integration**.
4. Search for "Alephium Price" and follow the configuration steps.

### Configuration via YAML

If the UI integration doesn't work, you can add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: alephium_price
```

Then restart Home Assistant.

### HACS Installation

1. Add this repository to HACS as a custom repository:
   - URL: `https://github.com/diomark/alephium_price`
   - Category: Integration
2. Install the integration through HACS.
3. Restart Home Assistant.
4. Go to **Configuration** → **Integrations** → **Add Integration**.
5. Search for "Alephium Price" and follow the configuration steps.

## Data Source

This integration uses the DIA API to fetch Alephium price data:
`https://api.diadata.org/v1/assetQuotation/Alephium/tgx7VNFoP9DJiFMFgXXtafQZkUvyEdDHT9ryamHJYrjq`

## Sensor Data

The integration creates a sensor with the following attributes:

- **State**: Current price in USD
- **Attributes**:
  - `price_yesterday`: Price 24 hours ago
  - `volume_yesterday_usd`: Trading volume in USD for the past 24 hours
  - `symbol`: Token symbol (ALPH)
  - `name`: Token name (Alephium)
  - `blockchain`: Blockchain (Alephium)
  - `data_source`: Source of the data (diadata.org)
  - `last_updated`: Timestamp of the last data update

## Update Frequency

By default, the sensor data is updated every 5 minutes. 