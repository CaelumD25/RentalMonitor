import datetime
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

class TelegramBot:
    def __init__(self, token, chat_id):
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id

    def send_message(self, url: str, name: str = None, cost: int = None, bedrooms: int = None, bathrooms: int = None,
                size: int = None, location: str = None, description: str = None, time: float = 0, website: str = ""):
        """
        Sends a message to the rental telegram given the attributes of a rental object
        :param url: The URL of the listing
        :param name: The title of the listing
        :param cost: The price/cost of the listing
        :param bedrooms: The number of bedrooms in the listing, not required as sometimes not easily parsable
        :param bathrooms: The number of bathrooms in the listing, not required as sometimes not easily parsable
        :param size: The size of the unit listed, not required as sometimes not easily parsable
        :param location: The location of the unit, not required as sometimes not easily parsable
        :param description: The rental description
        :param time: The time in which the bot found the rental
        :param website: Which website the rental was found on
        :return:
        """
        # The buttons set up for graphical fidelity, this can be altered later if embedding is possible for images
        buttons = [[InlineKeyboardButton(f"Open {website.capitalize()}", url=f"{url}")]]
        buttons = InlineKeyboardMarkup(buttons)

        # The actual message that will be sent through to the bot
        message = f"""<b>{name}</b>\n{"${:,.2f}".format(cost)}\n<i>Bed: {bedrooms if bedrooms!=-1 else "Unknown Bedrooms"} | Bath: {bathrooms if bathrooms!=-1 else "Unknown Bathrooms"}</i>\n<i>Size: {str(size) + ' sqft ' if size!=-1 else "Unknown Size "}</i>\nLocation: {location if location is None else "Greater Victoria"}\n{description[:128]+"..."}\n\nFound at: {datetime.datetime.fromtimestamp(time).strftime("%B %d, %Y, %I:%M %p")}"""
        # Sending the message, returns None if it fails
        response = self.bot.send_message(text=message, chat_id=self.chat_id, reply_markup=buttons, parse_mode="HTML")

        if response:
            print(f"Successfully Sent Message:\n{name}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        else:
            print(f"Message Sending Failed:\n{name}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
