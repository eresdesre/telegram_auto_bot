from aiogram import Dispatcher
from aiogram import types
import aiogram.utils.markdown as fmt

from bot import keyboards as kb
from bot.filters.main import AdminFilter


def initial_admin_handlers(dp: Dispatcher):
    @dp.message_handler(AdminFilter(), text='Administration')
    async def admin_start(message: types.Message):
        await message.answer('You have entered the administration menu', reply_markup=kb.admin_menu_keyboard)

    @dp.message_handler(AdminFilter(), text='Back to the menu')
    async def admin_esc(message: types.Message):
        await message.answer(fmt.text('You have entered the main menu', fmt.hbold('Administrator mode on'), sep='\n'), parse_mode='HTML', reply_markup=kb.main_menu_admin_keyboard)
