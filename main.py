from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import logging
import asyncio
from keyboards import send_main_buttons, send_stop_button


dp = Dispatcher()

available_users = []
paired_users = {}

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Salom {message.from_user.full_name}\nmen sizga Suhbaddosh topib beruvchi botman", reply_markup=send_main_buttons())

@dp.message(F.text == "Qidirish")
async def handle_search(message: Message, bot: Bot):
    user_id = message.from_user.id

    if user_id in paired_users:
        await message.answer("⚠️ Sizing suhbaddoshingiz bor.")
        return

    if user_id in available_users:
        await message.answer("⏳ Siz Suhbaddosh qidiryapsiz.")
        return

    if available_users:
        partner_id = available_users.pop(0)
        paired_users[user_id] = partner_id
        paired_users[partner_id] = user_id

        await message.answer("✅ Suhbaddosh topildi, unga salom yo'llang", reply_markup=send_stop_button())
        await bot.send_message(partner_id, "✅ Suhbaddosh topildi, unga salom yo'llang", reply_markup=send_stop_button())
    else:
        available_users.append(user_id)
        await message.answer("🔍 Qidirilmoqda...")

@dp.message(F.text == "Stop")
async def handle_stop(message: Message, bot: Bot):
    user_id = message.from_user.id

    if user_id in paired_users:
        partner_id = paired_users.pop(user_id)
        paired_users.pop(partner_id, None)

        await message.answer("Suhbad tugatildi.")
        await bot.send_message(partner_id, "Sizning suhbaddoshingiz suhbadni tugatdi.")
        return

    if user_id in available_users:
        available_users.remove(user_id)
        await message.answer("Qidirish to'xtatildi")
        return

@dp.message()
async def forward_messages(message: Message, bot: Bot):
    user_id = message.from_user.id

    if user_id in paired_users:
        partner_id = paired_users[user_id]

        if message.text:
            await bot.send_message(partner_id, message.text)
        elif message.photo:
            await bot.send_photo(partner_id, message.photo[-1].file_id, caption=message.caption)
        elif message.sticker:
            await bot.send_sticker(partner_id, message.sticker.file_id)
        elif message.voice:
            await bot.send_voice(partner_id, message.voice.file_id, caption=message.caption)
        else:
            await message.answer("❗ bot bu turdagi xabarlarni qo'llab quvvatlamaydi .")
    else:
        pass

async def main():
    bot = Bot("token")
    await bot.set_my_description("Suhbaddosh Bot — Odamlarni anonim tarzda bogʻlaydigan suhbatdosh topuvchi Telegram bot")
    await bot.set_my_commands(
        [types.BotCommand(command="/start", description="Botni ishga tushirish")],
    )
    await dp.start_polling(bot)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
