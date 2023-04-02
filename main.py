from resources import config as cfg
import telebot
import service

bot = telebot.TeleBot(cfg.TELEGRAM_BOT_API_TOKEN)

bot.set_my_commands([
    telebot.types.BotCommand("/homeworks", "Домашнее задание на завтра"),
    telebot.types.BotCommand("/homeworks10d", "Домашнее задание на 10 дней"),
    telebot.types.BotCommand("/studentgrades10d", "Оценки ученика за 10 дней"),
    telebot.types.BotCommand("/grades3d", "Оценки за 3 дня")
])


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    service.init_session_parameters()

    if message.text == '/homeworks':
        bot.send_message(message.from_user.id, service.get_homework_tomorrow())
    elif message.text == '/homeworks10d':
        bot.send_message(message.from_user.id, service.get_homeworks_10_days())
    elif message.text == '/studentgrades10d':
        bot.send_message(message.from_user.id, service.get_person_grades_in_10_days())
    elif message.text == '/grades3d':
        bot.send_message(message.from_user.id, service.get_grades_in_3_days())


if __name__ == '__main__':
    bot.infinity_polling()
