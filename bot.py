import telebot
from telebot import types
from datetime import datetime
import pytz   # 🔴 ADDED

# 🔴 ADDED
ist = pytz.timezone("Asia/Kolkata")

# ================== BASIC CONFIG ==================
BOT_TOKEN = "8524217876:AAGWFO2g0vBnWsFQnwO1IEns9ZxZ148gcAU"
ADMIN_ID = 5265106993

CHANNEL_USERNAME = "@shreekrishnaIMA"
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
    },
    "Telegram": {
        "1,000 Channel Members": "₹200",
        "10,000 Post Views": "₹100"
    },
    "Facebook": {
        "1,000 Reels Views": "₹100",
        "Page Likes + Followers": "₹150"
    },
    "Twitter/X": {
        "1,000 Likes": "₹220"
    }
}

PROJECT_SERVICES = {
    "Website & Subdomain Setup": ["Custom Website Creation", "Domain & Subdomain Setup", "Fully Functional & Responsive"],
    "Vlog Writing": ["Engaging Content Writing", "SEO Optimized Scripts", "Creative Vlog Ideas"],
    "Content Writing": ["High-Quality Blog Posts", "Website Articles & Captions", "SEO Optimized Content"],
    "Telegram Bot Creation": ["Custom Telegram Bot Setup", "Automation & Interaction", "Admin Control Features"]
}

user_selection = {}

# ================== START MENU ==================
def start_menu(chat_id, message_id=None):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("💰 View Paid Services", callback_data="paid"),
        types.InlineKeyboardButton("🛠 Projects", callback_data="projects"),
        types.InlineKeyboardButton("👤 Join as Creator", url=CREATOR_FORM),
        types.InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK),
        types.InlineKeyboardButton("📢 Join Telegram Channel", url=CHANNEL_LINK)
    )

    text = (
        "👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n"
        "🚀 We help brands grow with real & trusted promotion services.\n\n"
        "👇 Choose an option below"
    )

    if message_id:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=kb)
    else:
        bot.send_message(chat_id, text, reply_markup=kb)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    start_menu(message.chat.id)

# ================== PAID SERVICES ==================
@bot.callback_query_handler(func=lambda call: call.data == "paid")
def paid_platforms(call):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for platform in PAID_SERVICES:
        kb.add(types.InlineKeyboardButton(platform, callback_data=f"plat_{platform}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="start"))
    bot.edit_message_text("📌 *Select a platform:*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("plat_"))
def paid_services(call):
    platform = call.data.replace("plat_", "")
    user_selection[call.from_user.id] = {"platform": platform}

    kb = types.InlineKeyboardMarkup(row_width=1)
    for service, price in PAID_SERVICES[platform].items():
        kb.add(types.InlineKeyboardButton(f"{service} – {price}", callback_data=f"service_{platform}|{service}"))

    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="paid"))
    bot.edit_message_text(
        f"*{platform} Services*\nSelect a service:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def service_selected(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")

    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("💳 Pay Now", callback_data=f"paynow_{platform}|{service}"),
        types.InlineKeyboardButton("⏳ Pay Later", callback_data=f"paylater_{platform}|{service}")
    )
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"plat_{platform}"))

    bot.edit_message_text(
        f"You selected *{service}* on {platform}. How would you like to proceed?",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

# ================== PAYMENT ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("paynow_"))
def pay_now(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    user = call.from_user

    try:
        with open(QR_FILE, "rb") as qr:
            bot.send_photo(
                call.message.chat.id,
                qr,
                caption=f"💳 Scan QR to pay for *{service}* on {platform}.\n\n📸 Send payment screenshot here."
            )
    except:
        bot.send_message(call.message.chat.id, "❌ QR file not found. Please contact admin.")

    notify_admin(user, platform, service)

@bot.callback_query_handler(func=lambda call: call.data.startswith("paylater_"))
def pay_later(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    user = call.from_user

    bot.send_message(
        call.message.chat.id,
        f"✅ You chose to pay later for *{service}* on {platform}. Admin will contact you.",
        parse_mode="Markdown"
    )
    notify_admin(user, platform, service)

def notify_admin(user, platform, service):
    username_link = f"@{user.username}" if user.username else f"[Click Here](tg://user?id={user.id})"

    admin_text = (
        "🚨 *NEW PAID SERVICE REQUEST*\n\n"
        f"👤 Name: {user.first_name} {user.last_name or ''}\n"
        f"🔗 Username: {username_link}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"📦 Platform: {platform}\n"
        f"📦 Service: {service}\n\n"
        f"⏰ Time: {datetime.now(ist).strftime('%d-%m-%Y %I:%M %p')}"  # 🔴 CHANGED
    )

    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")

# ================== PROJECTS ==================
@bot.callback_query_handler(func=lambda call: call.data == "projects")
def projects(call):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for project in PROJECT_SERVICES:
        kb.add(types.InlineKeyboardButton(project, callback_data=f"proj_{project}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="start"))

    bot.edit_message_text("🛠 *Select a project:*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("proj_"))
def project_selected(call):
    project = call.data.replace("proj_", "")
    tasks = PROJECT_SERVICES[project]

    kb = types.InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        kb.add(types.InlineKeyboardButton(task, callback_data=f"task_{project}|{task}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="projects"))

    bot.edit_message_text(
        f"🛠 *{project} Details*:\nSelect task:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
def task_selected(call):
    project, task = call.data.replace("task_", "").split("|")
    user = call.from_user

    username_link = f"@{user.username}" if user.username else f"[Click Here](tg://user?id={user.id})"

    admin_text = (
        "🛠 *NEW PROJECT REQUEST*\n\n"
        f"👤 Name: {user.first_name} {user.last_name or ''}\n"
        f"🔗 Username: {username_link}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"📌 Project: {project}\n"
        f"📌 Task: {task}\n"
        f"⏰ Time: {datetime.now(ist).strftime('%d-%m-%Y %I:%M %p')}"  # 🔴 CHANGED
    )

    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    bot.send_message(
        call.message.chat.id,
        f"✅ You selected *{task}* from project *{project}*. Admin will contact you soon.",
        parse_mode="Markdown"
    )

# ================== RUN BOT ==================
print("🤖 SKIMA_bot is running...")
bot.infinity_polling()
