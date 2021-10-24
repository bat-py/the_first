from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Products(StatesGroup):
    waiting_for_product_type = State()
    waiting_for_product_district = State()
    waiting_for_product_fasovka = State()
    # Тип клада (прикоп, тайник, магнит)
    waiting_for_treasure_type = State()
    waiting_for_payment_method = State()
    waiting_for_confirm = State()


async def product_type_chosen(callback_query: types.CallbackQuery, state: FSMContext):



def register_handlers_products(dp: Dispatcher):
    dp.register_callback_query_handler(product_type_chosen, state=Products.waiting_for_product_type)
