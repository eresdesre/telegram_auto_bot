from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import keyboards as kb
from bot.filters.main import AdminFilter
from bot.database.models import DataBase as models
from bot.states.fsm_add_product import FSMAdminAddProduct


def admin_add_product_handler(dp: Dispatcher, models: models):
    @dp.message_handler(AdminFilter(), text='Add item', state=None)
    async def fsm_start(message: types.Message):
        await FSMAdminAddProduct.name.set()
        await message.answer('Send item', reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler(AdminFilter(), state=FSMAdminAddProduct.name)
    async def add_product_to_assortment(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdminAddProduct.next()
        await message.answer('Enter the description of the item')

    @dp.message_handler(AdminFilter(), state=FSMAdminAddProduct.description)
    async def add_description(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdminAddProduct.next()
        await message.answer('Send a photo of the item')

    @dp.message_handler(AdminFilter(), content_types=['photo'], state=FSMAdminAddProduct.photo)
    async def add_photo(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdminAddProduct.next()
        await message.answer('Price')

    @dp.message_handler(AdminFilter(), state=FSMAdminAddProduct.price)
    async def add_price(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['price'] = message.text

        await models.add_product_to_assortment(state)
        await message.answer('Item successfully added', reply_markup=kb.admin_menu_keyboard)
        
        await state.finish()
