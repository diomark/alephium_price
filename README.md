# Alephium Price Integration for Home Assistant

Home Assistant integration that provides real-time Alephium (ALPH) cryptocurrency price tracking. This custom component creates a sensor that fetches price data from the DIA Oracle, enabling price monitoring and automation triggers based on ALPH market values. Perfect for crypto enthusiasts who want to integrate Alephium price tracking into their home automation workflows.

## Features
• Real-time ALPH/USD price updates
• Data sourced from DIA Oracle for reliability
• Configurable update intervals
• Price change notifications (when used with automations)
• Easy integration with Home Assistant dashboards

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