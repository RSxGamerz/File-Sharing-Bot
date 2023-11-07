import requests
from telebot import types

def check_bin(bin):
    # Remove 'x' characters and make sure the BIN is 6 digits
    bin = bin.replace('x', '')[:6]

    url = f"https://lookup.binlist.net/{bin}"
    headers = {"Accept-Version": "3"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        bin_info = response.json()
        return bin_info, bin  # Return both bin_info and the checked BIN
    else:
        return None, bin  # Return the checked BIN even if no info is found

def generate_bin_message(bin_info, checked_bin):
    if bin_info:
        brand = bin_info.get('brand')
        card_type = bin_info.get('type')
        country_name = bin_info.get('country').get('name')
        country_emoji = bin_info.get('country').get('emoji')

        # Format the checked BIN in monospaced text
        checked_bin_monospaced = f"`{checked_bin}`"

        message = f"𝗕𝗜𝗡 𝗜𝗡𝗙𝗢\n\n"
        message += f"• ʙɪɴ: {checked_bin_monospaced}\n"  # Include the checked BIN in monospaced style
        message += f"• ʙʀᴀɴᴅ: {brand}\n"
        message += f"• ᴛʏᴘᴇ: {card_type}\n"
        message += f"• ᴄᴏᴜɴᴛʀʏ: {country_name} {country_emoji}\n\n"
        message += f"✅ 𝗕𝗢𝗧 𝗕𝗬: 𝙍𝙀𝙓 𝕏\n"

        return message
    else:
        return f"Failed to retrieve information for the BIN {checked_bin_monospaced}."

def create_bin_message(bin):
    bin_info, checked_bin = check_bin(bin)
    message = generate_bin_message(bin_info, checked_bin)

    # Create a button for copying the checked BIN
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    copy_button = types.KeyboardButton("Copy BIN")
    markup.add(copy_button)

    return message, markup
