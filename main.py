import asyncio
from db import BotDB
from aiogram import Bot, Dispatcher, types
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class MyForm(StatesGroup):
    text = State()
    photo = State()
    link = State()


BotDB = BotDB('accounts.db')

# создаем экземпляр бота
bot = Bot(token="5999195979:AAEJOeiGM690Q9GAIxVW3byWUtzksThv0Zk")

# создаем диспетчер, который будет обрабатывать входящие сообщения
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['admin_mode'])
async def ask_for_text(message: types.Message):
    await message.answer("Введите текст сообщения")
    await MyForm.text.set()

async def ask_for_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer("Пришлите фото")
    await MyForm.photo.set()

async def ask_for_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    yesButt = types.KeyboardButton('Да')
    noButt = types.KeyboardButton('Нет')
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(yesButt, noButt)
    await message.answer("Нужна ли ссылка?", reply_markup=keyboard)
    await MyForm.link.set()

async def send_mailing(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
        text = data['text']
        photo = data['photo']
        link = data['link']
    users = BotDB.get_all_users()
    n = 0
    for user in users:
        try:
            await bot.send_photo(user[0], photo)
            await bot.send_message(user[0], text)
            if link == "Да":
                linkButt = types.InlineKeyboardButton('Ссылка', url='google.com')
                keyboard_link = types.InlineKeyboardMarkup(linkButt)
                await bot.send_message(user[0], "Ссылка", reply_markup=keyboard_link)
            n += 1
        except:
            pass
    await message.answer(f"Рассылка выполнена успешно! Сообщение успешно дошло {n} пользователям из {len(users)}")
    await state.finish()

dp.register_message_handler(ask_for_text, commands=['admin_mode'])

dp.register_message_handler(ask_for_photo, state=MyForm.text, content_types=types.ContentType.TEXT)

dp.register_message_handler(ask_for_link, state=MyForm.photo, content_types=types.ContentType.PHOTO)

dp.register_message_handler(send_mailing, state=MyForm.link, content_types=types.ContentType.TEXT, text=Text(equals="Да") | Text(equals="Нет"))
    # users = BotDB.get_all_users()
    # n = 0
    # for user in users:
    #     try:
    #         await asyncio.sleep(3)
    #         await bot.send_message(user[0], text)
    #         n += 1
    #     except:
    #         pass
    # await bot.send_message(message.from_user.id, f"Рассылка выполнена успешно! Сообщение успешно дошло {n} пользователям из {len(users)}")

# функция-обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # проверяем наличие пользователя в базе данных
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_nick = message.from_user.username
    inst_nick = '-'
    if not BotDB.user_exists(user_id):
        BotDB.add_user(user_id, user_name, user_nick, inst_nick)
    # здесь должна быть ваша логика по работе с базой данных
    # ...

    # отправляем сообщение пользователю
    await message.answer("Добро пожаловать!")
    await mainMenu(message)
async def mainMenu(message: types.Message):
    # отправляем сообщение с клавиатурой
    urlButton = types.InlineKeyboardButton(text = "Определить асцедент", url = 'https://ru.astro-seek.com/ascendent-rasschitat-onlayn?ysclid=ld0n0rddht793516998')
    ascButton = types.InlineKeyboardButton("ASC", callback_data="determine_ascendant")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(urlButton, ascButton)
    await message.answer("Для того чтобы прочитать свою трактовку астроимиджа Вам необходимо рассчитать свой знак асцендента. После расчёта асцендента выберите команду ASC", reply_markup=markup)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "determine_ascendant")
async def determine_ascendant_callback_handler(callback_query: types.CallbackQuery):
    await asc_handler(callback_query.message)

# функция-обработчик кнопки "ASC"
@dp.message_handler(text="ASC")
async def asc_handler(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*[types.KeyboardButton(sign) for sign in ["Овен", "Телец", "Близнецы"]])
    markup.row(*[types.KeyboardButton(sign) for sign in ["Рак", "Лев", "Дева"]])
    markup.row(*[types.KeyboardButton(sign) for sign in ["Весы", "Скорпион", "Стрелец"]])
    markup.row(*[types.KeyboardButton(sign) for sign in ["Козерог", "Водолей", "Рыбы"]])
    await message.answer("Выберите ваш асцедент", reply_markup=markup)

@dp.message_handler(text="Овен")
async def oven_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("1.png", "rb"))
    await message.answer_photo(open("2.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
    
@dp.message_handler(text="Телец")
async def telez_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("3.png", "rb"))
    await message.answer_photo(open("4.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Близнецы")
async def blizn_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("5.png", "rb"))
    await message.answer_photo(open("6.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Рак")
async def rak_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("7.png", "rb"))
    await message.answer_photo(open("8.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Лев")
async def lev_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("9.png", "rb"))
    await message.answer_photo(open("10.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Дева")
async def deva_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("11.png", "rb"))
    await message.answer_photo(open("12.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Весы")
async def vesi_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("13.png", "rb"))
    await message.answer_photo(open("14.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Скорпион")
async def scorp_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("15.png", "rb"))
    await message.answer_photo(open("16.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Стрелец")
async def strel_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("17.png", "rb"))
    await message.answer_photo(open("18.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Козерог")
async def kozel_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("19.png", "rb"))
    await message.answer_photo(open("20.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Водолей")
async def vodo_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("21.png", "rb"))
    await message.answer_photo(open("22.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)
@dp.message_handler(text="Рыбы")
async def fish_handler(message: types.Message):
    # отправляем три картинки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("Повторить"))
    await message.answer_photo(open("23.png", "rb"))
    await message.answer_photo(open("24.png", "rb"))
    await message.answer_photo(open("25.png", "rb"), reply_markup=markup)

@dp.message_handler(text='Повторить')
async def repeat_again(message: types.Message):
    await mainMenu(message)

# @dp.message_handler(text='AdminMode:Dayana')
# async def admin_handler(message: types.Message):
#     await message.answer("Вы в админ режиме!")
#     await mail_service(message)

async def main():
    # запускаем цикл событий
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
