from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token= api)
dp = Dispatcher(bot, storage= MemoryStorage())

#kb = ReplyKeyboardMarkup()
#button = KeyboardButton(text= 'Информация')
#button2 = KeyboardButton(text= 'Рассчитать')
#kb.add(button)
#kb.row(button2)

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы рассчета', callback_data='form')
kb.add(button)
kb.add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text= "Рассчитать")
async def set_age(message):
    await message.answer('Выберите опцию:', reply_markup= kb)
    await UserState.age.set()

@dp.callback_query_handler(text = 'form')
async def calo(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text = 'calories')
async def calo(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()
    
@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(first= message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(thousand = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(three = message.text)
    data = await state.get_data()
    calories = 10 * int(data['three']) + 6.25 * int(data['thousand']) - 5 * int(data['first']) - 161
    await message.answer(f'Ваша норма калорий: {calories}')

    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
