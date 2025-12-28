# bot.py
import telebot
from telebot import types

# ====== BOT TOKEN ======
BOT_TOKEN = "8524217876:AAEx5D24HSQMdGyG2fg9fuT7bDfeXi-fTXU"
bot = telebot.TeleBot(8524217876:AAEx5D24HSQMdGyG2fg9fuT7bDfeXi-fTXU)

# ====== ADMIN ID ======
ADMIN_ID = 5265106993  # Aapka Telegram ID

# ====== BUSINESS INFO ======
BUSINESS_INFO = {
    "name": "Shree Krishna Influencer Marketing Agency",
    "website": "https://shreekrishnaagency.github.io/Business/",
    "services": {
        "Instagram": ["1,000 Views – ₹80", "1,000 Followers – ₹200", "1,000 Likes – ₹70", "Reel Views Boost", "Engagement Package (Likes + Views)"],
        "YouTube": ["1,000 Views – ₹150", "1,000 Likes – ₹140", "1,000 Subscribers – ₹2,580", "Watch Time Boost", "Video Promotion"],
        "Telegram": ["1,000 Channel Members – ₹200", "10,000 Post Views – ₹100", "1,000 Reactions – ₹100", "Channel Growth Package"],
        "Facebook": ["1,000 Reels Views – ₹100", "Page Likes + Followers (Combo) – ₹150", "1,000 Page Followers – ₹100", "1,000 Post Likes – ₹110"],
        "Twitter/X": ["1,000 Likes – ₹220"]
    },
    "projects": ["Website & Subdomain Setup", "Vlog Writing", "Content Writing", "Telegram Bot Creation"],
    "contacts": {
        "Instagram": "https://www.instagram.com/shree.krishna.ima",
        "Telegram": "https://t.me/shreekrishnaIMA",
        "Email": "Influencers.shreekrishnaima@zohomail.in"
    },
    "qr_file": "QR.png"
}

# ====== START / HELP COMMAND ======
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    services_text = ""
    for platform, services in BUSINESS_INFO['services'].items():
        services_text += f"\n*{platform} Services:*\n" + "\n".join(f"- {s}" for s in services)
    
    projects_text = "\n".join(f"- {p}" for p in BUSINESS_INFO['projects'])
    
    text = (
        f"Hello! Welcome to *{BUSINESS_INFO['name']}*.\n\n"
        f"🌐 Website: {BUSINESS_INFO['website']}\n\n"
        f"{services_text}\n\n"
        f"💼 Projects:\n{projects_text}\n\n"
        f"📩 Contact:\nInstagram: {BUSINESS_INFO['contacts']['Instagram']}\n"
        f"Telegram: {BUSINESS_INFO['contacts']['Telegram']}\n"
        f"Email: {BUSINESS_INFO['contacts']['Email']}"
    )
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====== PAYMENT COMMAND ======
@bot.message_handler(commands=['pay'])
def send_qr(message):
    try:
        with open(BUSINESS_INFO['qr_file'], 'rb') as qr:
            bot.send_photo(message.chat.id, qr)
        bot.send_message(message.chat.id, "✅ Please scan the QR to pay. After payment, send your screenshot here.")
    except Exception as e:
        bot.send_message(message.chat.id, "❌ QR code file not found. Contact admin.")
        print("QR Error:", e)

# ====== PAYMENT SCREENSHOT HANDLER ======
@bot.message_handler(content_types=['photo', 'document'])
def handle_payment_screenshot(message):
    # Forward screenshot to admin
    bot.send_message(message.chat.id, "✅ Screenshot received! Admin will check soon.")
    try:
        if message.photo:
            file_id = message.photo[-1].file_id
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        elif message.document:
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Could not send screenshot to admin.")
        print("Screenshot Error:", e)

# ====== FALLBACK MESSAGE ======
@bot.message_handler(func=lambda message: True)
def default_response(message):
    text = (
        "Hello! I can help you with our services and projects.\n\n"
        "Use /start or /help to get business info.\n"
        "Use /pay to get payment QR code."
    )
    bot.send_message(message.chat.id, text)

# ====== RUN BOT ======
print("Bot is running...")
bot.infinity_polling()
