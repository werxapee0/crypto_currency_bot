import aiohttp
from datetime import datetime
from cachetools import TTLCache

fiat_cache = TTLCache(maxsize=10, ttl=300)
crypto_cache = TTLCache(maxsize=10, ttl=300)


async def get_fiat_rates() -> dict:
    """Получает курсы ЦБ РФ с кэшированием."""
    if "rates" in fiat_cache:
        return fiat_cache["rates"]

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    valute = data.get("Valute", {})

                    def get_rate(code: str) -> float:
                        item = valute.get(code, {})
                        nominal = item.get("Nominal", 1)
                        value = item.get("Value", 0.0)
                        return value / nominal if nominal else 0.0

                    rates = {
                        "RUB": 1.0,
                        "USD": get_rate("USD"),
                        "EUR": get_rate("EUR"),
                        "CNY": get_rate("CNY"),
                        "UZS": get_rate("UZS"),
                        "KZT": get_rate("KZT"),  # Казахстанский тенге
                        "updated_at": datetime.now().strftime("%H:%M:%S")
                    }
                    fiat_cache["rates"] = rates
                    return rates
    except Exception as e:
        print(f"Ошибка получения фиатных валют: {e}")

    return fiat_cache.get("rates", {})


async def get_crypto_rates() -> dict:
    """Получает курсы криптовалют (USD) с кэшированием."""
    if "rates" in crypto_cache:
        return crypto_cache["rates"]

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,the-open-network,solana,tether",
        "vs_currencies": "usd"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = {
                        "BTC": data.get("bitcoin", {}).get("usd", 0.0),
                        "ETH": data.get("ethereum", {}).get("usd", 0.0),
                        "TON": data.get("the-open-network", {}).get("usd", 0.0),
                        "SOL": data.get("solana", {}).get("usd", 0.0),
                        "USDT": data.get("tether", {}).get("usd", 1.0),
                        "updated_at": datetime.now().strftime("%H:%M:%S")
                    }
                    crypto_cache["rates"] = rates
                    return rates
    except Exception as e:
        print(f"Ошибка получения крипты: {e}")

    return crypto_cache.get("rates", {})