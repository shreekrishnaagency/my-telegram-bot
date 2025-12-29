import telebot
from telebot import types
from datetime import datetime, timedelta, timezone
import threading
import random
import re  # ✅ IMPORT ADDED: Text safayi ke liye zaroori hai

# ================== BASIC CONFIG ==================
BOT_TOKEN = "8524217876:AAGWFO2g0vBnWsFQnwO1IEns9ZxZ148gcAU"
ADMIN_ID = 5265106993

# ✅ USERNAME
BOT_USERNAME = "SKIMA_Helper_bot" 

CHANNEL_USERNAME = "@shreekrishnaIMA"
CHANNEL_LINK = "https://t.me/shreekrishnaIMA"
WEBSITE_LINK = "https://shreekrishnaagency.github.io/Business/"
CREATOR_FORM = "https://forms.gle/eQgnMQff64L98y1Q9"

QR_FILE = "QR.png"

# IST Timezone Setup
IST = timezone(timedelta(hours=5, minutes=30))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# 🟢 STATUS VARIABLES
IS_ADMIN_ONLINE = True
PENDING_REQUESTS = set()

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

# ================== HELPER FUNCTIONS ==================
def generate_order_id():
    return f"SK-{random.randint(100000, 999999)}"

# ================== START / HELP / MAIN MENU ==================
def get_main_menu_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("💰 View Paid Services", callback_data="paid"),
        types.InlineKeyboardButton("🛠 Projects", callback_data="projects"),
        types.InlineKeyboardButton("🔎 Check Order Status", callback_data="check_status"),
        types.InlineKeyboardButton("👤 Join as Creator", url=CREATOR_FORM),
        types.InlineKeyboardButton("🗣️ Talk With Founder", callback_data="talk_founder"),
        types.InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK),
        types.InlineKeyboardButton("📢 Join Telegram Channel", url=CHANNEL_LINK)
    )
    return kb

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n"
        "🚀 We help brands grow with real & trusted promotion services.\n\n"
        "👇 Choose an option below",
        reply_markup=get_main_menu_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data == "start")
def start_callback(call):
    bot.edit_message_text(
        "👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n"
        "🚀 We help brands grow with real & trusted promotion services.\n\n"
        "👇 Choose an option below",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_main_menu_keyboard()
    )

# ================== ONLINE / OFFLINE MODE ==================
@bot.message_handler(commands=['online', 'offline'])
def toggle_status(message):
    global IS_ADMIN_ONLINE

    if message.chat.id == ADMIN_ID:
        if message.text == "/online":
            IS_ADMIN_ONLINE = True
            bot.reply_to(message, "✅ **You are now ONLINE.**\nUsers can contact you.")
            if PENDING_REQUESTS:
                count = 0
                for user_id in list(PENDING_REQUESTS):
                    try:
                        bot.send_message(user_id, "👋 **Good News!**\n\nFounder is now **ONLINE**. 🟢")
                        count += 1
                    except: pass
                bot.send_message(ADMIN_ID, f"📢 Notified {count} users.")
                PENDING_REQUESTS.clear()

        elif message.text == "/offline":
            IS_ADMIN_ONLINE = False
            bot.reply_to(message, "😴 **You are now OFFLINE.**")

# ================== TALK WITH FOUNDER ==================
@bot.callback_query_handler(func=lambda call: call.data == "talk_founder")
def talk_founder_handler(call):
    user = call.from_user
    chat_id = call.message.chat.id
    current_time_ist = datetime.now(IST).strftime('%d-%m-%Y %I:%M %p')

    if IS_ADMIN_ONLINE:
        bot.send_message(chat_id, "✅ **Request Sent!** Founder will reply shortly.")
        admin_text = f"📞 *NEW TALK REQUEST*\n👤 {user.first_name}\n🆔 `{user.id}`\n⏰ {current_time_ist}"
        bot.send_message(ADMIN_ID, admin_text)
    else:
        PENDING_REQUESTS.add(chat_id)
        bot.send_message(chat_id, "😴 **Founder is Offline.** You will be notified when he is back.")
        bot.send_message(ADMIN_ID, f"🌙 *MISSED REQUEST* (Offline)\n👤 {user.first_name}\n🆔 `{user.id}`")

# ================== CHECK STATUS ==================
@bot.callback_query_handler(func=lambda call: call.data == "check_status")
def check_status_request(call):
    msg = bot.send_message(call.message.chat.id, "🔎 Send Order ID or Screenshot.")
    bot.register_next_step_handler(msg, process_status_inquiry)

def process_status_inquiry(message):
    bot.reply_to(message, "✅ Admin will update you.")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📩 *New Inquiry* from `{message.chat.id}`. Use `/reply ID message`.")

# ================== ADMIN REPLY ==================
@bot.message_handler(commands=['reply'])
def admin_reply_to_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            parts = message.text.split(maxsplit=2)
            user_id, reply_text = parts[1], parts[2]
            bot.send_message(user_id, f"👨‍💻 *Admin Support:*\n\n{reply_text}")
            bot.reply_to(message, "✅ Sent!")
        except:
            bot.reply_to(message, "⚠️ Format: `/reply UserID Message`")

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
    bot.edit_message_text(f"*{platform} Services*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def service_selected(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    user_selection[call.from_user.id]["service"] = service
    kb = types.InlineKeyboardMarkup()
    kb.row(types.InlineKeyboardButton("💳 Pay Now", callback_data=f"paynow_{platform}|{service}"),
           types.InlineKeyboardButton("⏳ Pay Later", callback_data=f"paylater_{platform}|{service}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"plat_{platform}"))
    bot.edit_message_text(f"Selected: *{service}*", call.message.chat.id, call.message.message_id, reply_markup=kb)

# ================== PAYMENTS & ORDERS ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("app_") or call.data.startswith("rej_"))
def handle_order_control(call):
    action, user_id, order_id = call.data.split("_")
    status = "APPROVED" if action == "app" else "REJECTED"
    bot.edit_message_text(f"✅ Order {status} ({order_id})", call.message.chat.id, call.message.message_id)
    try: bot.send_message(user_id, f"📢 **Order Update:** Your order `{order_id}` is **{status}**.")
    except: pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("paynow_"))
def pay_now(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    order_id = generate_order_id()
    try:
        with open(QR_FILE, "rb") as qr:
            bot.send_photo(call.message.chat.id, qr, caption=f"💳 Scan to Pay\nOrder ID: `{order_id}`")
    except: bot.send_message(call.message.chat.id, "❌ QR Error. Contact Admin.")
    notify_admin(call.from_user, platform, service, order_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("paylater_"))
def pay_later(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    order_id = generate_order_id()
    bot.send_message(call.message.chat.id, f"✅ Order Saved! ID: `{order_id}`")
    notify_admin(call.from_user, platform, service, order_id)

def notify_admin(user, platform, service, order_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"app_{user.id}_{order_id}"),
           types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{user.id}_{order_id}"))
    bot.send_message(ADMIN_ID, f"🚨 *NEW ORDER*\n👤 {user.first_name}\n📦 {service}\n🆔 `{order_id}`", reply_markup=kb)

@bot.message_handler(content_types=['photo', 'document'])
def payment_screenshot(message):
    if message.chat.id != ADMIN_ID:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, f"📸 Screenshot from `{message.chat.id}`")
        bot.reply_to(message, "✅ Payment Screenshot Received!")

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
    kb = types.InlineKeyboardMarkup(row_width=1)
    for task in PROJECT_SERVICES[project]:
        kb.add(types.InlineKeyboardButton(task, callback_data=f"task_{project}|{task}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="projects"))
    bot.edit_message_text(f"🛠 *{project}*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
def task_selected(call):
    data = call.data.replace("task_", "")
    project, task = data.split("|")
    order_id = generate_order_id()
    bot.send_message(call.message.chat.id, f"✅ Request Sent! ID: `{order_id}`")
    notify_admin(call.from_user, project, task, order_id)

# ================== CHANNEL WELCOME ==================
def delete_message_after_delay(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass

@bot.chat_member_handler()
def channel_welcome(message: types.ChatMemberUpdated):
    if message.new_chat_member.status in ["member", "administrator", "creator"]:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔥 Boost Your Growth", url=f"https://t.me/{BOT_USERNAME}?start=welcome"))
        try:
            sent = bot.send_message(message.chat.id, f"🌟 Welcome {message.new_chat_member.user.first_name}!", reply_markup=kb)
            threading.Timer(60, delete_message_after_delay, args=[message.chat.id, sent.message_id]).start()
        except: pass

# ================== ADMIN CHANNEL POSTING (FIXED A-Z) ==================
@bot.message_handler(content_types=['photo', 'video', 'text'])
def admin_post_to_channel(message):
    # 1. Sirf Admin allow karega
    if message.chat.id != ADMIN_ID:
        if message.text and not message.text.startswith("/"):
             bot.send_message(message.chat.id, "Hello! Use /start to begin.")
        return

    # 2. Check agar ye '/post' command hai
    msg_content = message.caption if message.caption else message.text
    
    # Ignore commands like /online, /reply etc.
    if message.text and message.text.startswith("/") and not message.text.lower().startswith("/post"):
        return

    if msg_content and "/post" in msg_content.lower():
        try:
            # 3. Clean the text (Remove /post, /Post, /POST)
            clean_content = re.sub(r'(?i)/post', '', msg_content).strip()

            # 4. Handle TEXT Messages (No Copy Message, Use Send Message)
            if message.content_type == 'text':
                if clean_content:
                    bot.send_message(CHANNEL_USERNAME, clean_content, parse_mode="Markdown")
                    bot.reply_to(message, "✅ Text successfully posted to Channel!")
                else:
                    bot.reply_to(message, "⚠️ Empty message! Write something after /post.")

            # 5. Handle MEDIA Messages (Use Copy Message + New Caption)
            elif message.content_type in ['photo', 'video']:
                bot.copy_message(
                    chat_id=CHANNEL_USERNAME,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    caption=clean_content,
                    parse_mode="Markdown"
                )
                bot.reply_to(message, "✅ Media successfully posted to Channel!")

        except Exception as e:
            bot.reply_to(message, f"❌ Failed to post: {e}")

# ================== RUN BOT ==================
print("🤖 SKIMA Bot is running...")
bot.infinity_polling(allowed_updates=['message', 'callback_query', 'chat_member'])
