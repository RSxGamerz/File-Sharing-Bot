import telebot
import random
from telebot import types
from flask import Flask
import threading
from keep_alive import keep_alive
keep_alive()

# Replace 'YOUR_BOT_TOKEN' with your bot token
bot = telebot.TeleBot('6977268323:AAG5a7w7MEOxf-q-gm7NMtCUF6YH8IEG5dY')

# Dictionary to store user states
user_states = {}

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is alive!"

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    user_name = message.from_user.username if message.from_user.username else "User"
    welcome_message = f"ʜᴇʟʟᴏ, {user_name}❗ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙɪɴ x ʙᴏᴛ. ᴛʏᴘᴇ /cmd ᴛᴏ ᴄʜᴇᴄᴋ ᴄᴏᴍᴍᴀɴᴅꜱ."
    
    bot.send_message(user_id, welcome_message)
  
@bot.message_handler(commands=['gen'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_visa = types.KeyboardButton("『𝗩𝗜𝗦𝗔』")
    item_mastercard = types.KeyboardButton("『𝗠𝗔𝗦𝗧𝗘𝗥𝗖𝗔𝗥𝗗』")
    markup.add(item_visa, item_mastercard)

    bot.send_message(message.chat.id, "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙɪɴ x ʙᴏᴛ! ꜱᴇʟᴇᴄᴛ ᴀ ᴄᴀʀᴅ ᴛʏᴘᴇ:", reply_markup=markup)
    user_states[message.chat.id] = {"state": "select_card_type"}

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get("state") == "select_card_type")
def handle_card_type(message):
    user_id = message.chat.id
    card_type = message.text.lower()

    if card_type not in ("『𝗩𝗜𝗦𝗔』", "『𝗠𝗔𝗦𝗧𝗘𝗥𝗖𝗔𝗥𝗗』"):
        bot.send_message(user_id, "Invalid card type. Please select '『𝗩𝗜𝗦𝗔』' or '『𝗠𝗔𝗦𝗧𝗘𝗥𝗖𝗔𝗥𝗗』.")
        return

    user_states[user_id]["card_type"] = card_type
    bot.send_message(user_id, "ʜᴏᴡ ᴍᴀɴʏ ʙɪɴꜱ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ? (ᴇ.ɢ., 5)")

    user_states[user_id]["state"] = "enter_bin_count"

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get("state") == "enter_bin_count")
def handle_bin_count(message):
    user_id = message.chat.id

    try:
        bin_count = int(message.text)
        if bin_count <= 0:
            bot.send_message(user_id, "ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ 0. ❌")
            return

        user_states[user_id]["bin_count"] = bin_count
        generate_bins(user_id)
    except ValueError:
        bot.send_message(user_id, "ɪɴᴠᴀʟɪᴅ ɪɴᴘᴜᴛ ❌. ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ.")

@bot.message_handler(commands=['cmd'])
def handle_cmd(message):
    command_list = "𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n\n"
    command_list += "/start - Start the bot 🤖\n"
    command_list += "/cmd - Show available commands 📂\n"
    command_list += "/chk - Check your BINs 💳\n"
    command_list += "/gen - Generate random BINs ✅\n"

    bot.send_message(message.chat.id, command_list)

def generate_bins(user_id):
    card_type = user_states[user_id]["card_type"]
    bin_count = user_states[user_id]["bin_count"]
    results = []

    # Determine the first digit based on the card type
    first_digit = "4" if card_type == "『𝗩𝗜𝗦𝗔』" else "5"

    for i in range(bin_count):
        bin_suffix = ''.join(random.choice("0123456789") for _ in range(15))
        bin = first_digit + bin_suffix
        results.append(bin)

    result_text = "𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 𝗕𝗜𝗡𝘀:\n"
    result_text += "\n".join([f"`{bin[:6] + 'x' * 10}`" for bin in results])
    result_text += "\n\n✅ 𝗕𝗢𝗧 𝗕𝗬: 𝙍𝙀𝙓 𝕏"

    bot.send_message(user_id, result_text, parse_mode="Markdown")
    user_states.pop(user_id)

from chk import create_bin_message

# Create the bot and set up token

from chk import create_bin_message

# Create the bot and set up token

@bot.message_handler(func=lambda message: message.text.startswith('/chk '))
def handle_chk(message):
    bin = message.text.split(' ', 1)[1]
    message_to_send = create_bin_message(bin)
    bot.send_message(message.chat.id, message_to_send, parse_mode="Markdown")


if __name__ == "__main__":
    bot.remove_webhook()  # Remove any existing webhooks
    bot.polling(none_stop=True)

    # Start the Flask app in a separate thread to keep the bot alive
    t = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    t.start()
