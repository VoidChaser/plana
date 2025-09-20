from telegram import Bot

BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # замени на свой
bot = Bot(token=BOT_TOKEN)

def send_message_to_user(user_id: int, text: str):
    try:
        bot.send_message(chat_id=user_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
