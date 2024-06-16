import aiogram.utils.markdown as fmt
from aiogram import Dispatcher, types

from bot import keyboards as kb
from bot.database.models import DataBase as models
from bot.misc.environment import secret_keys
from bot.templates import descriptions as dc
from bot.handlers.client.utils.cart_parser import cart_parser


def register_client_handlers(dp: Dispatcher, models: models):
    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        if not models.get_user_data(message.from_user.id):
            await models.create_user(message.from_user.id)
        await message.answer_sticker('CAACAgQAAxkBAAEJ9r1k01FoAzo2Gysv8QHETLyTswvirwACRAADg2rQEM7UCtdq5wg8MAQ')
        await message.answer(f'💢 Welcome to our fullz store, {message.from_user.first_name}!', reply_markup=kb.start_keyboard)

    @dp.message_handler(text='🛒Cart🛒')
    async def shopping_cart(message: types.Message):
        if models.get_user_data(message.from_user.id)[0][1]!= None:
            await message.answer_sticker('CAACAgQAAxkBAAEKH-pk6MTMUVbUoZpl8A6vOSKz4P9nBgACUgADg2rQEAnSAbE-A3P-MAQ', reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f'Items in your cart:\n\n{cart_parser(message, models)}', parse_mode='HTML', reply_markup=kb.cart_inlain_keyboard)
        else:
            await message.answer('Your cart is empty :(. \nTime for a new order!', reply_markup=kb.back_to_assortment_inlain_keyboard)

    @dp.message_handler(text='🎲Range of products🎲')
    async def assortment(message: types.Message):
        await message.answer_sticker('CAACAgQAAxkBAAEKAAJk19dVR9rwHlml2HOglfF0KHHysQACTAADg2rQENhMNgNvS0EOMAQ', reply_markup=types.ReplyKeyboardRemove())
        await message.answer(dc.ASSORTIMENT_DESCRIPTION, reply_markup=kb.dinamic_assortmen_keyboard())

    @dp.message_handler(text='🔧Support🔧')
    async def support(message: types.Message):
        await message.answer('Contact support - @godsamongus')

    @dp.callback_query_handler()
    async def callback_handlers(call: types.CallbackQuery):
        if call.data == 'assortment':
            await call.message.answer_sticker('CAACAgQAAxkBAAEKAAJk19dVR9rwHlml2HOglfF0KHHysQACTAADg2rQENhMNgNvS0EOMAQ', reply_markup=types.ReplyKeyboardRemove())
            await call.message.answer(dc.ASSORTIMENT_DESCRIPTION, reply_markup=kb.dinamic_assortmen_keyboard())
            await call.answer()        
        elif call.data in models.get_products_details()['name']:
            index = models.get_products_details()['name'].index(call.data)
            await call.bot.send_photo(call.from_user.id, models.get_products_details()['photo'][index], f"Name: {models.get_products_details()['name'][index]}\nDescription: {models.get_products_details()['description'][index]}\nItem price: {models.get_products_details()['price'][index]}руб", reply_markup=types.ReplyKeyboardRemove())
            await call.message.answer(text='What do you think?', reply_markup=kb.dinamic_product_inlain_keyboard(f"{models.get_products_details()['name'][index]} - {models.get_products_details()['price'][index]}руб"))
            await call.answer()       
        elif call.data == 'back_to_menu':
            if str(call.from_user.id) == secret_keys('ADMIN_ID'):
                await call.message.answer(fmt.text('You have entered the main menu', fmt.hbold('Administrator mode on'), sep='\n'), parse_mode='HTML', reply_markup=kb.main_menu_admin_keyboard)
                await call.answer()
            else:
                await call.message.answer('You have entered the main menu',reply_markup=kb.main_menu_keyboard)
                await call.answer()   
        elif call.data == 'clear_cart':
            await models.clear_cart(call.from_user.id)  
            await call.answer('Cart successfully emptied', show_alert=True)
        elif call.data[0] == '+':
            await models.add_product_to_cart(id=call.from_user.id, product_name=call.data[1:])
            await call.answer('Item successfully added to the cart', show_alert=True)
