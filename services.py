import aiohttp
from datetime import datetime
from cachetools import TTLCache

fiat_cache = TTLCache(maxsize=10, ttl=300)
crypto_cache = TTLCache(maxsize=10, ttl=300)

# Заголовок, имитирующий реальный браузер (обходит блокировки WAF/Cloudflare)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def get_fiat_rates() -> dict:
    """Получает курсы ЦБ РФ с кэшированием."""
    if "rates" in fiat_cache:
        return fiat_cache["rates"]

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
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
                        "KZT": get_rate("KZT"),
                        "updated_at": datetime.now().strftime("%H:%M:%S")
                    }
                    fiat_cache["rates"] = rates
                    return rates
    except Exception as e:
        print(f"Ошибка получения фиатных валют: {e}")

    return fiat_cache.get("rates", {})


async def get_crypto_rates() -> dict:
    """
    Получает курсы криптовалют с дублирующим источником:
    1. Binance API (основной)
    2. CryptoCompare API (запасной)
    """
    if "rates" in crypto_cache:
        return crypto_cache["rates"]

    # -------------------------------------------------------------
    # Попытка 1: Binance API
    # -------------------------------------------------------------
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbols=%5B%22BTCUSDT%22,%22ETHUSDT%22,%22TONUSDT%22,%22SOLUSDT%22%5D"
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    price_map = {item["symbol"]: float(item["price"]) for item in data}
                    rates = {
                        "BTC": price_map.get("BTCUSDT", 0.0),
                        "ETH": price_map.get("ETHUSDT", 0.0),
                        "TON": price_map.get("TONUSDT", 0.0),
                        "SOL": price_map.get("SOLUSDT", 0.0),
                        "USDT": 1.0,
                        "updated_at": datetime.now().strftime("%H:%M:%S")
                    }
                    if rates["BTC"] > 0:
                        crypto_cache["rates"] = rates
                        return rates
    except Exception as e:
        print(f"Binance API временно недоступен: {e}")

    # -------------------------------------------------------------
    # Попытка 2: CryptoCompare API (если Binance не ответил)
    # -------------------------------------------------------------
    try:
        url = "https://min-api.cryptocompare.com/data/pricemulti"
        params = {"fsyms": "BTC,ETH,TON,SOL,USDT", "tsyms": "USD"}
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, params=params, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = {
                        "BTC": float(data.get("BTC", {}).get("USD", 0.0)),
                        "ETH": float(data.get("ETH", {}).get("USD", 0.0)),
                        "TON": float(data.get("TON", {}).get("USD", 0.0)),
                        "SOL": float(data.get("SOL", {}).get("USD", 0.0)),
                        "USDT": float(data.get("USDT", {}).get("USD", 1.0)),
                        "updated_at": datetime.now().strftime("%H:%M:%S")
                    }
                    if rates["BTC"] > 0:
                        crypto_cache["rates"] = rates
                        return rates
    except Exception as e:
        print(f"CryptoCompare API временно недоступен: {e}")

    return crypto_cache.get("rates", {})