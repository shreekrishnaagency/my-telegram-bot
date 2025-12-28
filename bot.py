import telebot
from telebot import types
from datetime import datetime
import pytz

# ================== TIMEZONE ==================
ist = pytz.timezone("Asia/Kolkata")

# ================== BASIC CONFIG ==================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 5265106993

CHANNEL_LINK = "https://t.me/shreekrishnaIMA"
WEBSITE_LINK = "https://shreekrishnaagency.github.io/Business/"
CREATOR_FORM = "https://forms.gle/eQgnMQff64L98y1Q9"

QR_FILE = "QR.png"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# ================== BUSINESS DATA ==================
PAID_SERVICES = {
    "Instagram": {
        "1,000 Followers": "₹200",
        "1,000 Likes": "₹70",
        "1,000 Views": "₹80",
        "Reel Views Boost": "Custom Price"
    },
    "YouTube": {
        "1,000 Views": "₹150",
        "1,000 Likes": "₹140",
        "1,000 Subscribers": "₹2,580"
    }
}

PROJECT_SERVICES = {
    "Website Setup": ["Business Website", "Landing Page"],
    "Telegram Bot": ["Bot Creation", "Automation Setup"]
}

# ================== START MENU ==================
def start_menu(chat_id, msg_id=None):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("💰 Paid Services", callback_data="paid"),
        types.InlineKeyboardButton("🛠 Projects", callback_data="projects"),
        types.InlineKeyboardButton("👤 Join as Creator", url=CREATOR_FORM),
        types.InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK),
        types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
    )

    text = (
        "👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n"
        "🚀 24×7 Support via Telegram Bot\n"
        "👇 Choose an option below"
    )

    if msg_id:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=kb)
    else:
        bot.send_message(chat_id, text, reply_markup=kb)

@bot.message_handler(commands=["start", "help"])
def start(message):
    start_menu(message.chat.id)

# ================== PAID SERVICES ==================
@bot.callback_query_handler(func=lambda c: c.data == "paid")
def paid_menu(call):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for p in PAID_SERVICES:
        kb.add(types.InlineKeyboardButton(p, callback_data=f"plat_{p}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="start"))
    bot.edit_message_text("Select Platform:", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("plat_"))
def services(call):
    platform = call.data.replace("plat_", "")
    kb = types.InlineKeyboardMarkup(row_width=1)
    for s, price in PAID_SERVICES[platform].items():
        kb.add(types.InlineKeyboardButton(f"{s} – {price}", callback_data=f"buy_{platform}|{s}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="paid"))
    bot.edit_message_text(f"*{platform} Services*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def buy(call):
    platform, service = call.data.replace("buy_", "").split("|")
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💳 Pay Now", callback_data=f"pay_{platform}|{service}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"plat_{platform}"))
    bot.edit_message_text(
        f"You selected *{service}* on {platform}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("pay_"))
def pay(call):
    platform, service = call.data.replace("pay_", "").split("|")
    user = call.from_user

    try:
        with open(QR_FILE, "rb") as qr:
            bot.send_photo(call.message.chat.id, qr, caption="Scan QR & send screenshot")
    except:
        bot.send_message(call.message.chat.id, "QR not found")

    time_now = datetime.now(ist).strftime("%d-%m-%Y %I:%M %p")

    admin_text = (
        "💰 *NEW PAYMENT REQUEST*\n\n"
        f"👤 {user.first_name}\n"
        f"🆔 {user.id}\n"
        f"📦 {platform} - {service}\n"
        f"⏰ {time_now}"
    )
    bot.send_message(ADMIN_ID, admin_text)

# ================== PROJECTS ==================
@bot.callback_query_handler(func=lambda c: c.data == "projects")
def projects(call):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for p in PROJECT_SERVICES:
        kb.add(types.InlineKeyboardButton(p, callback_data=f"proj_{p}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="start"))
    bot.edit_message_text("Select Project:", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("proj_"))
def project_tasks(call):
    project = call.data.replace("proj_", "")
    kb = types.InlineKeyboardMarkup(row_width=1)
    for t in PROJECT_SERVICES[project]:
        kb.add(types.InlineKeyboardButton(t, callback_data=f"task_{project}|{t}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="projects"))
    bot.edit_message_text(project, call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("task_"))
def task(call):
    project, task = call.data.replace("task_", "").split("|")
    user = call.from_user

    time_now = datetime.now(ist).strftime("%d-%m-%Y %I:%M %p")

    admin_text = (
        "🛠 *NEW PROJECT REQUEST*\n\n"
        f"👤 {user.first_name}\n"
        f"📌 {project} - {task}\n"
        f"⏰ {time_now}"
    )

    bot.send_message(ADMIN_ID, admin_text)
    bot.send_message(call.message.chat.id, "✅ Request sent to admin")

# ================== BACK HANDLER ==================
@bot.callback_query_handler(func=lambda c: c.data == "start")
def back_start(call):
    start_menu(call.message.chat.id, call.message.message_id)

# ================== RUN ==================
print("🤖 Bot Running...")
bot.infinity_polling()
