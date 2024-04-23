import requests
import json
import time


class CryptoPriceFetcher:
    def __init__(self, config_path="config.json", output_path="crypto_prices.json"):
        self.config = self.load_config(config_path)
        self.output_path = output_path
        self.currencies = self.config.get("CURRENCIES", ["BTC", "ETH"])

    def load_config(self, config_path):
        with open(config_path, "r") as f:
            return json.load(f)

    def get_crypto_prices(self):
        response = requests.get("https://api.coingecko.com/api/v3/simple/price",
                                params={"ids": ",".join(self.currencies), "vs_currencies": "usd"})
        data = response.json()
        return data

    def write_to_json(self, data):
        with open(self.output_path, "w") as f:
            json.dump(data, f, indent=4)

    def run(self):
        while True:
            try:
                prices = self.get_crypto_prices()
                print("Crypto Prices:")
                for currency, price_info in prices.items():
                    print(f"{currency}: ${price_info['usd']}")

                self.write_to_json(prices)
            except Exception as e:
                print("Error:", e)

            print("Waiting for 10 seconds...")
            time.sleep(10)  # 等待1小时后继续查询


if __name__ == "__main__":
    fetcher = CryptoPriceFetcher()
    fetcher.run()
