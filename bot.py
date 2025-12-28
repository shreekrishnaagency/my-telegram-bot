import telebot
from telebot import types
from datetime import datetime

# ================== BASIC CONFIG ==================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
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
    }
}

PROJECT_SERVICES = [
    "Website & Subdomain Setup",
    "Vlog Writing",
    "Content Writing",
    "Telegram Bot Creation"
]

user_selection = {}

# ================== START ==================
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup(row_width=1)

    kb.add(
        types.InlineKeyboardButton("💰 View Paid Services", callback_data="paid"),
        types.InlineKeyboardButton("🛠 Projects", callback_data="projects"),
        types.InlineKeyboardButton("👤 Join as Creator", url=CREATOR_FORM),
        types.InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK),
        types.InlineKeyboardButton("📢 Join Telegram Channel", url=CHANNEL_LINK)
    )

    bot.send_message(
        message.chat.id,
        "👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n"
        "🚀 We help brands grow with real & trusted promotion services.\n\n"
        "👇 Choose an option below",
        reply_markup=kb
    )

# ================== PAID SERVICES ==================
@bot.callback_query_handler(func=lambda call: call.data == "paid")
def paid_platforms(call):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for platform in PAID_SERVICES:
        kb.add(types.InlineKeyboardButton(platform, callback_data=f"plat_{platform}"))
    bot.edit_message_text("📌 *Select a platform:*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("plat_"))
def paid_services(call):
    platform = call.data.replace("plat_", "")
    user_selection[call.from_user.id] = {"platform": platform}

    kb = types.InlineKeyboardMarkup(row_width=1)
    for service, price in PAID_SERVICES[platform].items():
        kb.add(types.InlineKeyboardButton(f"{service} – {price}", callback_data=f"service_{service}"))

    bot.edit_message_text(
        f"*{platform} Services*\nSelect a service:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def confirm_service(call):
    service = call.data.replace("service_", "")
    data = user_selection.get(call.from_user.id, {})
    platform = data.get("platform")

    user = call.from_user

    bot.send_message(
        call.message.chat.id,
        "🙏 *Thank you for choosing our service!*\n\n"
        "⏳ Please wait, our admin will contact you shortly.\n\n"
        f"🌐 Website: {WEBSITE_LINK}"
    )

    admin_text = (
        "🚨 *NEW PAID SERVICE REQUEST*\n\n"
        f"👤 Name: {user.first_name}\n"
        f"🔗 Username: @{user.username}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"📦 Platform: {platform}\n"
        f"📦 Service: {service}\n\n"
        f"⏰ Time: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
    )

    bot.send_message(ADMIN_ID, admin_text)

    send_payment_qr(call.message.chat.id)

# ================== PAYMENT ==================
def send_payment_qr(chat_id):
    try:
        with open(QR_FILE, "rb") as qr:
            bot.send_photo(chat_id, qr, caption="💳 *Scan QR & Pay*\n\n📸 Send payment screenshot here.")
    except:
        bot.send_message(chat_id, "❌ QR file not found. Please contact admin.")

@bot.message_handler(content_types=['photo', 'document'])
def payment_screenshot(message):
    bot.send_message(message.chat.id, "✅ Screenshot received. Admin will verify.")

    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

# ================== PROJECTS ==================
@bot.callback_query_handler(func=lambda call: call.data == "projects")
def projects(call):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for p in PROJECT_SERVICES:
        kb.add(types.InlineKeyboardButton(p, callback_data=f"proj_{p}"))
    bot.edit_message_text("🛠 *Select a project:*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("proj_"))
def project_selected(call):
    project = call.data.replace("proj_", "")
    user = call.from_user

    bot.send_message(
        call.message.chat.id,
        "🙏 *Thank you for your project request!*\n"
        "⏳ Admin will contact you shortly."
    )

    admin_text = (
        "🛠 *NEW PROJECT REQUEST*\n\n"
        f"👤 Name: {user.first_name}\n"
        f"🔗 Username: @{user.username}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"📌 Project: {project}"
    )

    bot.send_message(ADMIN_ID, admin_text)

# ================== RUN ==================
print("🤖 SKIMA_bot is running...")
bot.infinity_polling()
