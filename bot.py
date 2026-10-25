import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command

# Сюда вставь токен своего бота от BotFather
TOKEN = "ТВОЙ_ТОКЕН_БОТА"

# Сюда вставь ID чата мамы (куда будут падать заявки)
ADMIN_CHAT_ID = 123456789

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(
      inline_keyboard=[
          [
              types.InlineKeyboardButton(
                  text="✨ Открыть студию «Венера»",
                  web_app=types.WebAppInfo(
                      url="https://femboy1488.github.io/KURSY/"
                  ),
              )
          ]
      ]
  )
  await message.answer(
      "Добро пожаловать в студию & академию красоты **«Венера»**.\n\n"
      "Нажми кнопку ниже, чтобы открыть каталог и записаться:",
      reply_markup=keyboard,
      parse_mode=ParseMode.MARKDOWN,
  )


@router.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
  try:
    data = json.loads(message.web_app_data.data)
  except Exception:
    return

  # Сообщение клиенту
  client_text = (
      f"✨ **Заявка принята!**\n\n"
      f"📌 **Услуга:** {data.get('service')}\n"
      f"💰 **Стоимость:** {data.get('price')}\n"
      f"📅 **Дата:** {data.get('date')} в {data.get('time')}\n\n"
      "Мы свяжемся с вами в ближайшее время! 🤍"
  )

  # Сообщение маме (админу)
  admin_text = (
      "🚨 **НОВАЯ ЗАПИСЬ • ВЕНЕРА** 🚨\n\n"
      f"💅 **Услуга:** {data.get('service')}\n"
      f"💵 **Цена:** {data.get('price')}\n"
      f"🗓 **Дата:** {data.get('date')} ({data.get('time')})\n\n"
      f"👤 **Клиент:** {data.get('name')}\n"
      f"📞 **Телефон:** `{data.get('phone')}`\n"
      f"💬 **Username:** @{message.from_user.username or 'скрыт'}"
  )

  await message.answer(client_text, parse_mode=ParseMode.MARKDOWN)

  try:
    await message.bot.send_message(
        chat_id=ADMIN_CHAT_ID, text=admin_text, parse_mode=ParseMode.MARKDOWN
    )
  except Exception as e:
    logging.error(f"Ошибка отправки админу: {e}")


async def main():
  bot = Bot(token=TOKEN)
  dp = Dispatcher()
  dp.include_router(router)
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())
