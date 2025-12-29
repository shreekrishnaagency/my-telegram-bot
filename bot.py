import telebot
from telebot import types
from datetime import datetime, timedelta, timezone
import threading
import random
import re  # ✅ Zaroori hai

# ================== BASIC CONFIG ==================
BOT_TOKEN = "8524217876:AAGWFO2g0vBnWsFQnwO1IEns9ZxZ148gcAU"
ADMIN_ID = 5265106993  # ✅ Check karein ye ID sahi ho

BOT_USERNAME = "SKIMA_Helper_bot" 
CHANNEL_USERNAME = "@shreekrishnaIMA"
CHANNEL_LINK = "https://t.me/shreekrishnaIMA"
WEBSITE_LINK = "https://shreekrishnaagency.github.io/Business/"
CREATOR_FORM = "https://forms.gle/eQgnMQff64L98y1Q9"
QR_FILE = "QR.png" 

IST = timezone(timedelta(hours=5, minutes=30))
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

IS_ADMIN_ONLINE = True
PENDING_REQUESTS = set()

# ================== BUSINESS DATA ==================
PAID_SERVICES = {
    "Instagram": {"1,000 Followers": "₹200", "1,000 Likes": "₹70", "1,000 Views": "₹80", "Reel Views Boost": "Custom Price"},
    "YouTube": {"1,000 Views": "₹150", "1,000 Likes": "₹140", "1,000 Subscribers": "₹2,580"},
    "Telegram": {"1,000 Channel Members": "₹200", "10,000 Post Views": "₹100"},
    "Facebook": {"1,000 Reels Views": "₹100", "Page Likes + Followers": "₹150"},
    "Twitter/X": {"1,000 Likes": "₹220"}
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

# ================== MAIN MENU ==================
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
    bot.send_message(message.chat.id, "👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n🚀 We help brands grow.\n👇 Choose an option below", reply_markup=get_main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "start")
def start_callback(call):
    bot.edit_message_text("👋 *Welcome to Shree Krishna Influencer Marketing Agency*\n\n🚀 We help brands grow.\n👇 Choose an option below", call.message.chat.id, call.message.message_id, reply_markup=get_main_menu_keyboard())

# ================== ADMIN COMMANDS ==================
@bot.message_handler(commands=['online', 'offline'])
def toggle_status(message):
    global IS_ADMIN_ONLINE
    if message.chat.id == ADMIN_ID:
        if message.text == "/online":
            IS_ADMIN_ONLINE = True
            bot.reply_to(message, "✅ **You are now ONLINE.**")
            if PENDING_REQUESTS:
                for user_id in list(PENDING_REQUESTS):
                    try: bot.send_message(user_id, "👋 **Good News!**\nFounder is now **ONLINE**. 🟢")
                    except: pass
                PENDING_REQUESTS.clear()
        elif message.text == "/offline":
            IS_ADMIN_ONLINE = False
            bot.reply_to(message, "😴 **You are now OFFLINE.**")

# ✅ UPDATED REPLY COMMAND WITH NEW SHORTCUT (RECEIVED)
@bot.message_handler(commands=['reply'])
def admin_reply_to_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            # Command format: /reply UserID Message
            parts = message.text.split(maxsplit=2)
            
            if len(parts) < 3:
                bot.reply_to(message, "⚠️ **Format:** `/reply UserID Message`\n\n💡 **Shortcuts:** complete, start, issue, received")
                return

            user_id = parts[1]
            raw_text = parts[2] # Ye wo hai jo aapne type kiya

            # 👇 SHORTCUTS DICTIONARY
            SHORTCUTS = {
                "complete": "✅ *Order Update: COMPLETED*\n\n🎉 Badhai ho! Aapka order successfully complete ho gaya hai.\nThank you for choosing Shree Krishna Agency! 🚀",
                
                "start": "🛠 *Order Update: STARTED*\n\n✅ Aapke order par kaam shuru ho gaya hai. Jald hi complete ho jayega.",
                
                "issue": "⚠️ *Order Update: ISSUE*\n\n❌ Aapke link ya order me kuch dikkat hai. Kripya 'Talk with Founder' option use karke sahi details bhejein.",
                
                # ✅ 4. Updated Message as requested
                "received": "📩 *Update: REQUEST RECEIVED*\n\nWe received your request (This Message from Admin).\nThank you, we will connect you soon..."
            }

            # Check karein agar aapne koi Shortcut word likha hai
            final_message = SHORTCUTS.get(raw_text.lower(), raw_text)

            # Message Bhejein
            bot.send_message(user_id, f"👨‍💻 *Admin Support:*\n\n{final_message}", parse_mode="Markdown")
            
            # Aapko confirm karein
            bot.reply_to(message, f"✅ **Message Sent!**\n\nContent: {final_message}")

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

# ================== ADMIN CHANNEL POSTING (PRIORITY 1) ==================
# Isme "func" add kiya hai taaki User ka Screenshot block na ho
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID, content_types=['photo', 'video', 'text'])
def admin_post_to_channel(message):
    
    # Check agar ye '/post' command hai
    msg_content = message.caption if message.caption else message.text
    
    # Agar text message hai aur /post se start nahi hota, to ignore karo (taaki /reply wagera chale)
    if message.content_type == 'text' and message.text.startswith("/") and not message.text.lower().startswith("/post"):
        return

    # Main Logic
    if msg_content and "/post" in msg_content.lower():
        try:
            clean_content = re.sub(r'(?i)/post', '', msg_content).strip()

            if message.content_type == 'text':
                if clean_content:
                    bot.send_message(CHANNEL_USERNAME, clean_content, parse_mode="Markdown")
                    bot.reply_to(message, "✅ Text successfully posted!")
                else:
                    bot.reply_to(message, "⚠️ Empty message!")

            elif message.content_type == 'photo':
                photo_id = message.photo[-1].file_id
                # Caption khali ho to None bhejo
                cap = clean_content if clean_content else None
                bot.send_photo(CHANNEL_USERNAME, photo_id, caption=cap)
                bot.reply_to(message, "✅ Photo successfully posted!")

            elif message.content_type == 'video':
                video_id = message.video.file_id
                cap = clean_content if clean_content else None
                bot.send_video(CHANNEL_USERNAME, video_id, caption=cap)
                bot.reply_to(message, "✅ Video successfully posted!")

        except Exception as e:
            bot.reply_to(message, f"❌ Failed to post: {e}")

# ================== TALK & STATUS ==================
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
        bot.send_message(ADMIN_ID, f"🌙 *MISSED REQUEST*\n👤 {user.first_name}\n🆔 `{user.id}`")

@bot.callback_query_handler(func=lambda call: call.data == "check_status")
def check_status_request(call):
    msg = bot.send_message(call.message.chat.id, "🔎 Send Order ID or Screenshot.")
    bot.register_next_step_handler(msg, process_status_inquiry)

def process_status_inquiry(message):
    bot.reply_to(message, "✅ Admin will update you.")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"📩 *New Inquiry* from `{message.chat.id}`. Use `/reply ID message`.")

# ================== SERVICES & PAYMENTS ==================
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

# 🚨🚨 SCREENSHOT HANDLER 🚨🚨
@bot.message_handler(content_types=['photo', 'document'])
def payment_screenshot(message):
    # Agar Admin Post wala function upar handle nahi hua, to yahan aayega.
    # Lekin hum Admin ko yahan ignore karenge.
    if message.chat.id != ADMIN_ID:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, f"📸 Screenshot from `{message.chat.id}`")
        bot.reply_to(message, "✅ Payment Screenshot Received!")

# ================== WELCOME ==================
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

# ================== SMART AI REPLY ==================
@bot.message_handler(func=lambda message: message.text and not message.text.startswith("/"))
def smart_user_reply(message):
    text = message.text.lower()
    if any(word in text for word in ['hi', 'hello', 'hey', 'namaste', 'hola', 'start']):
        reply = "👋 **Namaste! Welcome to Shree Krishna Agency.**\n🚀 Hum aapki Social Media Growth me madad kar sakte hain.\n👇 Niche diye gaye button se shuru karein!"
    elif any(word in text for word in ['price', 'rate', 'cost', 'paisa', 'kitna', 'charge']):
        reply = "💰 **Best Rates!**\nInstagram, YouTube aur Telegram ke rates dekhne ke liye **'💰 View Paid Services'** button dabayein."
    elif any(word in text for word in ['help', 'madad', 'support', 'problem', 'baat karni']):
        reply = "🤝 **Help Center**\nFounder se baat karne ke liye Menu me **'🗣️ Talk With Founder'** option select karein."
    elif any(word in text for word in ['status', 'order', 'kab hoga', 'check']):
        reply = "🔎 **Order Status Check**\nApna status check karne ke liye Menu me **'🔎 Check Order Status'** dabayein."
    else:
        reply = "🤖 **Main SKIMA Assistant hu.**\nMain aapki baat samajh nahi paya, lekin main growth me aapki madad kar sakta hu!\n👇 Niche Menu check karein."
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🚀 Open Main Menu", callback_data="start"))
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, reply, reply_markup=kb, parse_mode="Markdown")

# ================== RUN BOT ==================
print("🤖 SKIMA Bot is running (All Fixed & Updated)...")
bot.infinity_polling(allowed_updates=['message', 'callback_query', 'chat_member'])
