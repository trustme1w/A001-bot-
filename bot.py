import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TELEGRAM_BOT_TOKEN
from data_handler import DataHandler
from predictor import Predictor

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

data_handler = DataHandler()
predictor = Predictor()

MAIN_MENU = types.ReplyKeyboardMarkup(resize_keyboard=True)
MAIN_MENU.add(
    types.KeyboardButton("⚽ Live Football"),
    types.KeyboardButton("📅 Pre-Match Football")
)
MAIN_MENU.add(
    types.KeyboardButton("🎾 Live Tennis"),
    types.KeyboardButton("🎾 Pre-Match Tennis")
)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Выбери режим:", reply_markup=MAIN_MENU)

@dp.message_handler(lambda m: m.text == "⚽ Live Football")
async def live_football_handler(message: types.Message):
    data = data_handler.get_live_football()
    if not data or not data.get('response'):
        await message.answer("Нет live футбольных матчей.")
        return

    matches = []
    for fixture in data['response']:
        league = fixture['league']['name']
        teams = f"{fixture['teams']['home']['name']} - {fixture['teams']['away']['name']}"
        score = fixture['goals']['home'], fixture['goals']['away']
        time = fixture['fixture']['status']['elapsed']
        match_id = str(fixture['fixture']['id'])
        # Генерируем фиктивные признаки, заменить на реальные
        features = [score[0], score[1], time]
        predictions = predictor.predict(features)
        # Форматируем 3 варианта ставок
        bets = []
        for pred, prob in predictions:
            bets.append(f"{pred}: {prob*100:.1f}%")
        bets_text = "\n".join(bets) if bets else "Прогнозов пока нет."
        matches.append(f"{league}: {teams} | {score[0]}:{score[1]} ({time} мин)\n{bets_text}")
    await message.answer("\n\n".join(matches))

@dp.message_handler(lambda m: m.text == "📅 Pre-Match Football")
async def prematch_football_handler(message: types.Message):
    data = data_handler.get_prematch_football()
    if not data or not data.get('response'):
        await message.answer("Нет предстоящих футбольных матчей.")
        return
    matches = []
    for fixture in data['response']:
        league = fixture['league']['name']
        teams = f"{fixture['teams']['home']['name']} - {fixture['teams']['away']['name']}"
        date = fixture['fixture']['date'].replace("T", " ")[:16]
        matches.append(f"{league}: {teams} | {date}")
    await message.answer("\n".join(matches))

@dp.message_handler(lambda m: m.text == "🎾 Live Tennis")
async def live_tennis_handler(message: types.Message):
    data = data_handler.get_live_tennis()
    if not data:
        await message.answer("Нет live теннисных матчей.")
        return
    matches = []
    for event in data:
        teams = f"{event['home_team']} - {event['away_team']}"
        # Пример признаков и прогнозов, заменить на реальные
        features = [0]  # Заполнить нужными признаками
        predictions = predictor.predict(features)
        bets = []
        for pred, prob in predictions:
            bets.append(f"{pred}: {prob*100:.1f}%")
        bets_text = "\n".join(bets) if bets else "Прогнозов пока нет."
        matches.append(f"{teams} | LIVE\n{bets_text}")
    await message.answer("\n\n".join(matches))

@dp.message_handler(lambda m: m.text == "🎾 Pre-Match Tennis")
async def prematch_tennis_handler(message: types.Message):
    data = data_handler.get_prematch_tennis()
    if not data:
        await message.answer("Нет предстоящих теннисных матчей.")
        return
    matches = []
    for event in data:
        teams = f"{event['home_team']} - {event['away_team']}"
        matches.append(f"{teams} | {event.get('commence_time', '')}")
    await message.answer("\n".join(matches))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
