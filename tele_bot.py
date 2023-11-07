import os
import pathlib

import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from langchain_chatbot import LangChainChatBot

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELE_BOT_API_TOKEN"))
chatbot = LangChainChatBot(process_docs=os.getenv("PROCESS_DOCS").lower() == "true")


def gen_start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("location", callback_data="location"),
        InlineKeyboardButton("support", callback_data="support"),
        InlineKeyboardButton("policies", callback_data="policies"),
    )
    return markup


def gen_location_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("dental", callback_data="location_dental"),
        InlineKeyboardButton("mental", callback_data="location_mental"),
    )
    return markup


def gen_support_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("dental", callback_data="support_dental"),
        InlineKeyboardButton("mental", callback_data="support_mental"),
        InlineKeyboardButton("medical", callback_data="support_medical"),
    )
    return markup


def gen_policies_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("primary care", callback_data="policies_primaryCare"),
        InlineKeyboardButton("work injury", callback_data="policies_workInjury"),
    )
    return markup


def gen_work_injury_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(
            "medical expenses", callback_data="policies_workInjury_medicalExpenses"
        ),
        InlineKeyboardButton("medical leave", callback_data="policies_workInjury_medicalLeave"),
        InlineKeyboardButton(
            "permanent incapacity", callback_data="policies_workInjury_incapacity"
        ),
        InlineKeyboardButton("death benefits", callback_data="policies_workInjury_death"),
    )
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    welcome_message = pathlib.Path("./custom_response/welcome_message.txt").read_text()
    bot.send_message(message.chat.id, welcome_message, reply_markup=gen_start_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "location":
        bot.send_message(
            call.message.chat.id,
            "Please choose one of the following:",
            parse_mode="Markdown",
            reply_markup=gen_location_markup(),
        )
    elif call.data == "support":
        bot.send_message(
            call.message.chat.id,
            "Please choose one of the following:",
            parse_mode="Markdown",
            reply_markup=gen_support_markup(),
        )
    elif call.data == "policies":
        bot.send_message(
            call.message.chat.id,
            "Please choose one of the following:",
            parse_mode="Markdown",
            reply_markup=gen_policies_markup(),
        )
    elif call.data == "location_dental":
        with open("./custom_response/location_dental.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "location_mental":
        with open("./custom_response/location_mental.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "support_dental":
        with open("./custom_response/support_dental.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "support_mental":
        with open("./custom_response/support_mental.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "support_medical":
        with open("./custom_response/support_medical.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "policies_primaryCare":
        with open("./custom_response/policies_primaryCare.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "policies_workInjury":
        with open("./custom_response/policies_workInjury.txt") as f:
            bot.send_message(
                call.message.chat.id,
                f.read(),
                parse_mode="Markdown",
                reply_markup=gen_work_injury_markup(),
            )
    elif call.data == "policies_workInjury_medicalExpenses":
        with open("./custom_response/policies_workInjury_medicalExpenses.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "policies_workInjury_medicalLeave":
        with open("./custom_response/policies_workInjury_medicalLeave.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "policies_workInjury_incapacity":
        with open("./custom_response/policies_workInjury_incapacity.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")
    elif call.data == "policies_workInjury_death":
        with open("./custom_response/policies_workInjury_death.txt") as f:
            bot.send_message(call.message.chat.id, f.read(), parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def echo_all(message):
    res = chatbot.req_openai(message.text)
    bot.send_message(message.chat.id, res, parse_mode="Markdown")


@bot.message_handler(commands=["location"])
def start(message):
    welcome_message = pathlib.Path("./welcome_message.txt").read_text()
    bot.send_message(message.chat.id, welcome_message, reply_markup=gen_start_markup())
