from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главное меню."""
    keyboard = [
        [
            InlineKeyboardButton(text="💵 Курсы валют", callback_data="fiat_menu"),
            InlineKeyboardButton(text="🪙 Криптовалюта", callback_data="rates_crypto"),
        ],
        [
            InlineKeyboardButton(text="🧮 Как пользоваться калькулятором", callback_data="calc_help"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_fiat_choice_keyboard() -> InlineKeyboardMarkup:
    """Меню выбора базовой валюты."""
    keyboard = [
        [
            InlineKeyboardButton(text="🇺🇿 Сум (UZS)", callback_data="fiat_view:UZS"),
            InlineKeyboardButton(text="🇷🇺 Рубль (RUB)", callback_data="fiat_view:RUB"),
        ],
        [
            InlineKeyboardButton(text="🇺🇸 Доллар (USD)", callback_data="fiat_view:USD"),
            InlineKeyboardButton(text="🇪🇺 Евро (EUR)", callback_data="fiat_view:EUR"),
        ],
        [
            InlineKeyboardButton(text="🇨🇳 Юань (CNY)", callback_data="fiat_view:CNY"),
            InlineKeyboardButton(text="🇰🇿 Тенге (KZT)", callback_data="fiat_view:KZT"),
        ],
        [
            InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_currency_details_keyboard(currency_code: str) -> InlineKeyboardMarkup:
    """Кнопки под карточкой конкретной валюты."""
    keyboard = [
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"fiat_refresh:{currency_code}")],
        [InlineKeyboardButton(text="◀️ Выбрать другую валюту", callback_data="fiat_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_crypto_keyboard() -> InlineKeyboardMarkup:
    """Кнопки под криптовалютой."""
    keyboard = [
        [InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_crypto")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Кнопка возврата в главное меню — используется после ошибок и результатов."""
    keyboard = [
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)