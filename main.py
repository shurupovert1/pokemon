import telebot 
from config import token
from logic import Pokemon

from telebot.types import Message

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message: Message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=['attack'])
def attack_pokemon(message: Message):

    if message.reply_to_message:
        if message.from_user.username in Pokemon.pokemons.keys() and message.reply_to_message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            hero: Pokemon = Pokemon.pokemons[message.from_user.username]
            result = hero.attack(enemy)

            bot.send_message(message.chat.id, result)
        else:
            bot.reply_to(message, "У вас или у вашего противника нету покемона!")
    else: 
        bot.send_message(message.chat.id, "Чтобы атаковать нужно ответить на сообщение того, кого вы хотите атаковать.")

    
@bot.message_handler(commands=["info"])
def info(message:Message):

    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, f"Ваш покемон: {pok.name}, Вши хп: {pok.hp}")
    else:
        bot.send_message(message.chat.id, "У вас нет покемонов. Пожалуйста, сначала создайте покемона!")


@bot.message_handler(commands=['feed'])
def feed_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        response = pok.feed()
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас нет покемона!")



bot.infinity_polling(none_stop=True)

