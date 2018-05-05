from bot import Bot

bot = Bot()

while True:
    user_input = input("You > ")
    print("Bot : ", bot.handle_command(user_input))