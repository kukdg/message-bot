import telebot
from telebot import types

bot = telebot.TeleBot('Your token')
joinedUsers = set()  
joinedFile = open("users.txt", "r")



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('Начать')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет! Тут ты можешь анонимно отправить письмо. Чтобы продолжить, нажмите кнопку ниже', reply_markup=markup)
    
@bot.message_handler(func=lambda message: True and message.text == 'Начать')
def userStart(message):
    bot.send_message(message.chat.id, 'Перешлите сообщение того, кому вы хотите отправить письмо, чтобы получить ID пользователя')

@bot.message_handler(func=lambda message: message.forward_from is not None)
def handle_message(message):
    username = message.forward_from.username
    bot.reply_to(message, f'Username of the forwarded message sender: {username}\n\nPlease copy this username for further actions. Click here to continue: /text')
   
   
        
bot.message_handler(commands=['text'])
def handle_text(message):
    user_id = message.from_user.id
    bot.reply_to(message, f'ID пользователя: {user_id}\n\nТеперь, пожалуйста, отправьте мне ваше имя пользователя.')
    
bot.message_handler(func=lambda message: message.text.startswith('@'))
def handle_username(message):
    username = message.text[1:]  # Remove the '@' symbol from the username
    bot.reply_to(message, f'Имя пользователя: {username}\n\nСпасибо за предоставленную информацию!')

def handle_text(message):
    message_text = message.text
    joinedFile = open("users_text.txt", "a")
    joinedFile.write(message_text + "\n")
    joinedUsers.add(message_text)
    bot.send_message(message.chat.id, 'Текст добавлен в список, для продолжения нажмите сюда: /user')
    
    
    
@bot.message_handler(commands=['user'])
def after_send(message):
     bot.send_message(message.chat.id, "Введите ID пользователя")
     bot.register_next_step_handler(message, add_user)

def add_user(message):
    message_text = message.text
    joinedFile = open("users.txt", "a")
    joinedFile.write(message_text + "\n")
    joinedUsers.add(message_text)
    bot.send_message(message.chat.id, 'Пользователь добавлен в список, для продолжения нажмите сюда: /send')

@bot.message_handler(commands=['send'])
def bot_send(message):
    with open("users.txt", "r") as users_file:
        users = users_file.readlines()
        with open("users_text.txt", "r") as text_file:
            text = text_file.read()
            for user_id in users:
                user_id = user_id.strip()
                bot.send_message(user_id, text)
    open("users.txt", "w").close()
    open("users_text.txt", "w").close()
    bot.send_message(message.chat.id, 'Текст успешно отправлен!')        
    
       
bot.polling(none_stop=True)
