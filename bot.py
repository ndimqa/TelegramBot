import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import message
from aiogram.utils import executor

from main import Currency
#from config import TOKEN  'NEED TO MAKE YOUR OWN config FILE WITH TOKEN'
from sqliter import SQLighter

async def schedruled(result):
   await bot.send_message(message.from_user.id,result)

# Инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Инициализируем БД
db = SQLighter('db.db') # 'NEED TO MAKE DATA BASE'

# Команда /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЭтот телеграм бот нужен для отслеживания цен на валюты, криптовалюты, акции и.т.д\nДля связи со мной в случаи сбоев напишите команду /help")

# Команда /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("ссылка на мой телеграм для связи: https://t.me/ndimqa")

# Активация подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exist(message.from_user.id)):
        # Если юзера нет то создаем запись
        db.add_subscriber(message.from_user.id)
    else:
        # Если есть то обновляем статус
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы успешно подписаны.")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.message):
    if(not db.subscriber_exist(message.from_user.id)):
        # Если юзера нет добавляем его с не активнной подпиской
        db.add_subscriber(message.from_user.id, False)
    else:
        # Если был подписан то меняем статус
        db.update_subscription(message.from_user.id, False)
    await message.answer("Вы успешно отписаны.")

@dp.message_handler(text="Валюты")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="XRP", callback_data="XRP"))
    keyboard.add(types.InlineKeyboardButton(text="Etherium", callback_data="Etherium"))
    await message.answer("Нажмите на кнопку, чтобы бот начал отслеживание валюты", reply_markup=keyboard)

@dp.callback_query_handler(text="XRP")
async def send_answer_value(call: types.CallbackQuery):
    await call.message.answer('запущено отслеживание XRP')
    currency = Currency()
    while True:
        if currency.get_result():
            try:
                answer = currency.get_answer()
                await schedruled(answer)
            except AttributeError:
                pass
        currency.check_currency()
    

if __name__ == '__main__':
    executor.start_polling(dp)