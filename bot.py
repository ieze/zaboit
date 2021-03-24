import telebot
import sqlite3

bot = telebot.TeleBot('1757637459:AAFh3jharjAWgnFEoxekM_EuGixtSXwZCuw')


# БД
conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT PRIMARY KEY,
   clas INT
   );
""")
conn.commit()

def adduser(id, clas):  # добавление юзера
    userdata = [(id, clas)]
    check = cur.execute('SELECT userid FROM users WHERE userid=' + str(id) + ';')
    a = check.fetchone()
    if not a or a[0] != id:
        cur.executemany("INSERT INTO users VALUES (?,?)", userdata)
        conn.commit()

def editclas(id, clas):  # меняем класс
    check = cur.execute('SELECT userid FROM users WHERE userid=' + str(id) + ';')
    a = check.fetchone()
    if a[0] == id:
        cur.execute('UPDATE users SET clas = ' + str(clas) + ' WHERE userid = ' + str(id) + ';')
        conn.commit()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    id = message.from_user.id
    if not cur.execute('SELECT userid FROM users WHERE userid=' + str(id) + ';').fetchone():
        bot.send_message(message.from_user.id, 'Привет! Я тебя запомнил')
        adduser(message.from_user.id, 0)
    elif message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    elif message.text.lower() == 'звонок':
        bot.send_message(message.from_user.id, 'В каком ты классе? (просто число без буквы)')
        if message.text.lower().isdigit():
            editclas(message.from_user.id, message.text.lower())
        else:
            bot.send_message(message.from_user.id, 'некорректный класс! Напиши "звонок" заново и введи свой класс нормально')
    else:
        bot.send_message(message.from_user.id, 'Чавось?')

bot.polling(none_stop=True)
