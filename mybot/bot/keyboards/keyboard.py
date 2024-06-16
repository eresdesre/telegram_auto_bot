from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

from bot.database.models import DataBase as models


models = models()

'''===============================================CLIENT KEYBOARDS==============================================='''
#just start button
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add('🧨Start🧨')

#2 various if main menu keyboard(admim/client)
main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add('🛒Cart🛒').add('🎲Range of products🎲').add('🔧Support🔧')
main_menu_admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add('🛒Cart🛒').add('🎲Range of products🎲').add('🔧Support🔧').add('Administration')

#back assortment inlain keyboard(if your cart is empty)
back_to_assortment_inlain_keyboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='🎲Ассортимент🎲', callback_data='assortment'))   

#back assortment inlain keyboard(if your cart is empty)
cart_inlain_keyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Back to menu', callback_data='back_to_menu'),
                                                             InlineKeyboardButton(text='Clear cart', callback_data='clear_cart')) 

#assortment inlain keyboard
def dinamic_assortmen_keyboard():
    if len(models.get_products())!= 0:
        assortment_inlain_keyboard = InlineKeyboardMarkup(row_width=1)
        for i in range(len(models.get_products())):
            assortment_inlain_keyboard.add(InlineKeyboardButton(text=models.get_products()[i][0], callback_data=models.get_products()[i][0]))
        return assortment_inlain_keyboard.add(InlineKeyboardButton(text='Back to menu', callback_data='back_to_menu'))                                                                    
    else:
        return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Back to menu', callback_data='back_to_menu'),)
    
def dinamic_delete_assortmen_keyboard():
    if len(models.get_products())!= 0:
        assortment_inlain_keyboard = InlineKeyboardMarkup(row_width=1)
        for i in range(len(models.get_products())):
            assortment_inlain_keyboard.add(InlineKeyboardButton(text=models.get_products()[i][0], callback_data=f'!{models.get_products()[i][0]}'))
        return assortment_inlain_keyboard                                                                    
    else:
        return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Back to the administration menu', callback_data='!back_to_admin_menu'))

#product inlain keyboard(add/back)
def dinamic_product_inlain_keyboard(product_name):
    product_inlain_keyboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Add to cart', callback_data=f'+{product_name}'),
                                                                    InlineKeyboardButton(text='Back to range of products', callback_data='assortment'))
    return product_inlain_keyboard

'''===============================================ADMIN KEYBOARDS==============================================='''
#admin main menu keyboard
admin_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add('Add product').add('Delete item').add('Back to menu')


            




