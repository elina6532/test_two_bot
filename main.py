import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = "7745083692:AAF5OnuKkkHtBP5SbrCINR3n-KdI6G5zZdI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

questions = {
    "1": [  # Математика 7 класс
        {"q": "2 + 2?", "a": "4", "options": ["4", "5", "8"]},
        {"q": "5 + 3?", "a": "8", "options": ["6", "7", "8"]},
        {"q": "10 - 7?", "a": "3", "options": ["2", "3", "4"]},
        {"q": "6 * 6?", "a": "36", "options": ["34", "36", "38"]},
        {"q": "12 / 4?", "a": "3", "options": ["2", "3", "4"]},
        {"q": "Корень из 49?", "a": "7", "options": ["6", "7", "8"]},
        {"q": "15 - 9?", "a": "6", "options": ["5", "6", "7"]},
        {"q": "9 * 8?", "a": "72", "options": ["70", "72", "74"]},
        {"q": "81 / 9?", "a": "9", "options": ["8", "9", "10"]},
        {"q": "3 в квадрате?", "a": "9", "options": ["6", "9", "12"]},
    ],
    "2": [  # Русский язык 7 класс
        {"q": "Сколько гласных букв в русском алфавите?", "a": "10", "options": ["8", "10", "12"]},
        {"q": "Какой частью речи является слово 'красивый'?", "a": "прилагательное",
         "options": ["существительное", "прилагательное", "глагол"]},
        {"q": "Как пишется слово: пр_красный?", "a": "прекрасный",
         "options": ["прекрасный", "прикрасный", "прокрасный"]},
        {"q": "Что означает слово 'омонимы'?", "a": "одинаковые по звучанию, но разные по значению слова",
         "options": ["одинаковые по звучанию, но разные по значению слова", "слова с противоположным значением",
                     "слова с одинаковым значением"]},
        {"q": "Сколько падежей в русском языке?", "a": "6", "options": ["5", "6", "7"]},
        {"q": "Какой суффикс в слове 'бегущий'?", "a": "ущ", "options": ["ущ", "ющ", "ащ"]},
        {"q": "Какой частью речи является слово 'небо'?", "a": "существительное",
         "options": ["существительное", "прилагательное", "глагол"]},
        {"q": "Какое слово является антонимом к слову 'высокий'?", "a": "низкий",
         "options": ["низкий", "широкий", "маленький"]},
        {"q": "Какой глагол в форме прошедшего времени? (бежит, прыгнул, рисует)", "a": "прыгнул",
         "options": ["бежит", "прыгнул", "рисует"]},
        {"q": "Какой частью речи является слово 'очень'?", "a": "наречие",
         "options": ["наречие", "прилагательное", "существительное"]},
    ]
}

user_data = {}


@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите вариант теста: 1 - Математика, 2 - Русский язык", reply_markup=keyboard)


@dp.message(lambda message: message.text in ["1", "2"])
async def select_variant(message: types.Message):
    user_data[message.from_user.id] = {"variant": message.text, "score": 0, "current_q": 0}
    await ask_question(message)


async def ask_question(message):
    user_id = message.from_user.id
    data = user_data[user_id]
    variant = data["variant"]
    current_q = data["current_q"]

    if current_q < len(questions[variant]):
        question_data = questions[variant][current_q]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=option)] for option in question_data["options"]],
            resize_keyboard=True
        )
        await message.answer(question_data["q"], reply_markup=keyboard)
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/start")]],
            resize_keyboard=True
        )
        await message.answer(
            f"Тест завершен! Ваш результат: {data['score']} из {len(questions[variant])}\n\nВы можете пройти тест заново, нажав кнопку ниже.",
            reply_markup=keyboard)
        del user_data[user_id]


@dp.message()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Сначала выберите вариант теста: /start")
        return
    data = user_data[user_id]
    variant = data["variant"]
    current_q = data["current_q"]

    if message.text.lower() == questions[variant][current_q]["a"].lower():
        data["score"] += 1

    data["current_q"] += 1
    await ask_question(message)


@dp.message(lambda message: message.text == "Начать тест заново")
async def restart_test(message: types.Message):
    await start(message)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())