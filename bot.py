from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = '7715150782:AAF--OU_tdnvBecY2RWnzFXr0QrvADZApQY'
ADMIN_ID = 5775311631  # آیدی عددی خودت
SPECIAL_LINK = 'https://t.me/+mhsKSXyn5Is1ZTg8'  # لینکی که می‌خوای به افراد تایید شده بدی

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    user = message.from_user

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ تایید", callback_data=f"approve_{user.id}"),
        InlineKeyboardButton("❌ رد", callback_data=f"reject_{user.id}")
    )

    await bot.send_message(
        ADMIN_ID,
        f"درخواست جدید:\n\n👤 {user.full_name}\n🆔 @{user.username or 'یوزرنیم نداره'}\n🪪 ID: {user.id}",
        reply_markup=keyboard
    )

    await message.reply("درخواست شما ارسال شد ✅ لطفاً منتظر تأیید بمانید.")

@dp.callback_query_handler(lambda c: c.data.startswith('approve_') or c.data.startswith('reject_'))
async def process_callback(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split("_")
    user_id = int(user_id)

    if action == 'approve':
        await bot.send_message(user_id, f"درخواست شما تایید شد ✅\n\n🔗 لینک شما:\n{SPECIAL_LINK}")
        await callback_query.answer("کاربر تایید شد.")
    else:
        await bot.send_message(user_id, "درخواست شما رد شد ❌")
        await callback_query.answer("کاربر رد شد.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
