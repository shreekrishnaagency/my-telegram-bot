import telebot
from telebot import types
from datetime import datetime, timedelta, timezone
import threading
import random 

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
PENDING_REQUESTS = set()  # Ye set un users ko yaad rakhega jo offline me aaye the

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
    """Generates a random 6-digit Order ID starting with SK"""
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

# ================== ONLINE / OFFLINE MODE (WITH AUTO ALERT) ==================
@bot.message_handler(commands=['online', 'offline'])
def toggle_status(message):
    global IS_ADMIN_ONLINE
    
    if message.chat.id == ADMIN_ID:
        if message.text == "/online":
            IS_ADMIN_ONLINE = True
            bot.reply_to(message, "✅ **You are now ONLINE.**\nUsers can contact you.")
            
            # 🔔 Notify Pending Users
            if PENDING_REQUESTS:
                count = 0
                for user_id in list(PENDING_REQUESTS):
                    try:
                        bot.send_message(
                            user_id,
                            "👋 **Good News!**\n\nFounder is now **ONLINE**. 🟢\nHe has received your request and will contact you shortly.",
                            parse_mode="Markdown"
                        )
                        count += 1
                    except:
                        pass # Agar user ne block kiya ho toh ignore karein
                
                bot.send_message(ADMIN_ID, f"📢 **Alert Sent:** Notified {count} users that you are online.")
                PENDING_REQUESTS.clear() # List khali kar do

        elif message.text == "/offline":
            IS_ADMIN_ONLINE = False
            bot.reply_to(message, "😴 **You are now OFFLINE.**\nBot will collect requests for later.")

# ================== TALK WITH FOUNDER (UPDATED) ==================
@bot.callback_query_handler(func=lambda call: call.data == "talk_founder")
def talk_founder_handler(call):
    user = call.from_user
    chat_id = call.message.chat.id
    username_link = f"@{user.username}" if user.username else f"[Click Profile](tg://user?id={user.id})"
    current_time_ist = datetime.now(IST).strftime('%d-%m-%Y %I:%M %p')

    if IS_ADMIN_ONLINE:
        # ✅ CASE 1: Admin Online Hai
        bot.send_message(chat_id, "✅ **Request Sent!**\n\nFounder has been notified. Please wait for a reply here.", parse_mode="Markdown")
        
        # Professional Link Format for Admin
        admin_text = (
            "📞 *NEW TALK REQUEST* 🟢\n\n"
            f"👤 **Name:** {user.first_name} {user.last_name or ''}\n"
            f"🔗 **Username:** {username_link}\n"
            f"🆔 **User ID:** `{user.id}`\n"
            f"⏰ **Time:** {current_time_ist}\n\n"
            "💬 *Action:* Copy ID and use `/reply ID Message`"
        )
        bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
        
    else:
        # 😴 CASE 2: Admin Offline Hai
        # Add User to Pending List
        PENDING_REQUESTS.add(chat_id)
        
        bot.send_message(
            chat_id, 
            "😴 **Founder is currently Offline / Sleeping.**\n\n"
            "✅ Your request has been saved.\n"
            "🔔 You will be notified automatically when he comes online.", 
            parse_mode="Markdown"
        )

        # Notify Admin about Missed Request (Professional Link Format)
        admin_text = (
            "🌙 *MISSED TALK REQUEST* (Offline)\n\n"
            f"👤 **Name:** {user.first_name} {user.last_name or ''}\n"
            f"🔗 **Username:** {username_link}\n"
            f"🆔 **User ID:** `{user.id}`\n"
            f"⏰ **Time:** {current_time_ist}\n\n"
            "📌 *Note:* User has been added to waiting list.\n"
            "👉 Type `/online` to notify them automatically."
        )
        bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")

# ================== CHECK ORDER STATUS ==================
@bot.callback_query_handler(func=lambda call: call.data == "check_status")
def check_status_request(call):
    msg = bot.send_message(
        call.message.chat.id, 
        "🔎 *Check Order Status*\n\n"
        "Please send your **Order ID** (e.g., SK-123456) or a Screenshot.\n"
        "Admin will check and reply here.",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(msg, process_status_inquiry)

def process_status_inquiry(message):
    user = message.from_user
    username_link = f"@{user.username}" if user.username else f"[Click Profile](tg://user?id={user.id})"
    
    bot.reply_to(message, "✅ **Request Sent!** Admin will update you shortly.")

    current_time_ist = datetime.now(IST).strftime('%d-%m-%Y %I:%M %p')
    admin_text = (
        "📩 *NEW ORDER INQUIRY*\n\n"
        f"👤 User: {user.first_name} ({username_link})\n"
        f"🆔 User ID: `{message.chat.id}`\n"
        f"⏰ Time: {current_time_ist}\n\n"
        "👇 *Message Content Below:*"
    )
    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    
    if message.content_type == 'text':
        bot.send_message(ADMIN_ID, f"📝 *Message:* {message.text}", parse_mode="Markdown")
    elif message.content_type == 'photo':
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        
    bot.send_message(ADMIN_ID, f"💡 **To Reply:** `/reply {message.chat.id} Your Message`", parse_mode="Markdown")

# ================== ADMIN REPLY SYSTEM ==================
@bot.message_handler(commands=['reply'])
def admin_reply_to_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            parts = message.text.split(maxsplit=2)
            if len(parts) < 3:
                bot.reply_to(message, "⚠️ **Format:** `/reply UserID Message`")
                return
            
            user_id = parts[1]
            reply_text = parts[2]
            
            bot.send_message(user_id, f"👨‍💻 *Admin Support:*\n\n{reply_text}", parse_mode="Markdown")
            bot.reply_to(message, "✅ Message sent to user!")
        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

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
    bot.edit_message_text(f"*{platform} Services*\nSelect a service:", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("service_"))
def service_selected(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    user_selection[call.from_user.id]["service"] = service
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton("💳 Pay Now", callback_data=f"paynow_{platform}|{service}"),
        types.InlineKeyboardButton("⏳ Pay Later", callback_data=f"paylater_{platform}|{service}")
    )
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"plat_{platform}"))
    bot.edit_message_text(f"You selected *{service}* on {platform}. How would you like to proceed?", call.message.chat.id, call.message.message_id, reply_markup=kb)

# ================== ADMIN APPROVE / REJECT HANDLER ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("app_") or call.data.startswith("rej_"))
def handle_order_control(call):
    try:
        action, user_id_str, order_id = call.data.split("_")
        user_id = int(user_id_str)
        
        if action == "app":
            bot.edit_message_text(
                f"✅ **ORDER APPROVED!**\n\nOrder ID: `{order_id}`\nUser ID: `{user_id}`\nStatus: Processing started.",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown"
            )
            try:
                bot.send_message(
                    user_id,
                    f"🎉 **Order Update: APPROVED**\n\nYour Order **{order_id}** has been accepted!\nWork will start shortly.\nThank you for choosing SKIMA! 🚀",
                    parse_mode="Markdown"
                )
            except:
                pass
            
        elif action == "rej":
            bot.edit_message_text(
                f"❌ **ORDER REJECTED!**\n\nOrder ID: `{order_id}`\nUser ID: `{user_id}`\nStatus: Cancelled.",
                call.message.chat.id,
                call.message.message_id,
                parse_mode="Markdown"
            )
            try:
                bot.send_message(
                    user_id,
                    f"⚠️ **Order Update: REJECTED**\n\nYour Order **{order_id}** could not be processed.\nPossible reasons: Payment issue or Invalid link.\n\nPlease contact Admin via 'Talk with Founder'.",
                    parse_mode="Markdown"
                )
            except:
                pass
            
    except Exception as e:
        print(f"Error processing order: {e}")

# ================== PAYMENT ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith("paynow_"))
def pay_now(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    user = call.from_user
    order_id = generate_order_id()
    
    try:
        with open(QR_FILE, "rb") as qr:
            caption = (
                f"💳 **Payment Request**\n\n"
                f"🔢 **Order ID:** `{order_id}`\n"
                f"📦 **Service:** {service} ({platform})\n\n"
                f"scan the QR code to pay. After paying, send the screenshot here."
            )
            bot.send_photo(call.message.chat.id, qr, caption=caption)
    except:
        bot.send_message(call.message.chat.id, "❌ QR file not found. Please contact admin.")
    
    notify_admin_new_order(user, platform, service, order_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("paylater_"))
def pay_later(call):
    _, data = call.data.split("_", 1)
    platform, service = data.split("|")
    user = call.from_user
    order_id = generate_order_id()

    bot.send_message(
        call.message.chat.id, 
        f"✅ **Request Received!**\n\n"
        f"🔢 **Your Order ID:** `{order_id}`\n"
        f"📌 Please save this ID. Admin will contact you soon.", 
        parse_mode="Markdown"
    )
    notify_admin_new_order(user, platform, service, order_id)

def notify_admin_new_order(user, platform, service, order_id):
    username = user.username
    username_link = f"@{username}" if username else f"[Click Profile](tg://user?id={user.id})"
    current_time_ist = datetime.now(IST).strftime('%d-%m-%Y %I:%M %p')
    
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Approve", callback_data=f"app_{user.id}_{order_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{user.id}_{order_id}")
    )

    admin_text = (
        "🚨 *NEW ORDER REQUEST*\n\n"
        f"🔢 *Order ID:* `{order_id}`\n"
        f"👤 Name: {user.first_name} {user.last_name or ''}\n"
        f"🔗 Username: {username_link}\n"
        f"🆔 User ID: `{user.id}`\n\n"
        f"📦 Platform: {platform}\n"
        f"📦 Service: {service}\n\n"
        f"⏰ Time (IST): {current_time_ist}\n\n"
        "👇 *Take Action:*"
    )
    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(content_types=['photo', 'document'])
def payment_screenshot(message):
    if message.chat.id == ADMIN_ID: return 
    
    user = message.from_user
    username_link = f"@{user.username}" if user.username else f"[Click Profile](tg://user?id={user.id})"
    admin_text = (
        "📸 *Payment Screenshot Received*\n\n"
        f"👤 Name: {user.first_name} {user.last_name or ''}\n"
        f"🔗 Username: {username_link}\n"
        f"🆔 User ID: `{message.chat.id}`\n"
        "💡 Check their Order ID in previous messages and Approve/Reject there."
    )
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ Screenshot received! Admin will verify.", parse_mode="Markdown")

# ================== PROJECTS ==================
@bot.callback_query_handler(func=lambda call: call.data == "projects")
def projects(call):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for project, tasks in PROJECT_SERVICES.items():
        kb.add(types.InlineKeyboardButton(project, callback_data=f"proj_{project}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="start"))
    bot.edit_message_text("🛠 *Select a project:*", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("proj_"))
def project_selected(call):
    project = call.data.replace("proj_", "")
    tasks = PROJECT_SERVICES.get(project, [])
    kb = types.InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        kb.add(types.InlineKeyboardButton(task, callback_data=f"task_{project}|{task}"))
    kb.add(types.InlineKeyboardButton("🔙 Back", callback_data="projects"))
    bot.edit_message_text(f"🛠 *{project} Details*:\nSelect task:", call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith("task_"))
def task_selected(call):
    data = call.data.replace("task_", "")
    project, task = data.split("|")
    user = call.from_user
    current_time_ist = datetime.now(IST).strftime('%d-%m-%Y %I:%M %p')
    order_id = generate_order_id()
    
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✅ Approve", callback_data=f"app_{user.id}_{order_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{user.id}_{order_id}")
    )

    admin_text = (
        "🛠 *NEW PROJECT REQUEST*\n\n"
        f"🔢 *Order ID:* `{order_id}`\n"
        f"👤 User: {user.first_name}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📌 Project: {project}\n"
        f"📌 Task: {task}\n"
        f"⏰ Time: {current_time_ist}"
    )
    bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown", reply_markup=kb)
    bot.send_message(call.message.chat.id, f"✅ Request Received!\n\nOrder ID: `{order_id}`\nAdmin will contact you soon.", parse_mode="Markdown")

# ================== ADMIN CHANNEL POSTING ==================
@bot.message_handler(content_types=['photo', 'video', 'text'])
def admin_post_to_channel(message):
    if message.chat.id == ADMIN_ID:
        if message.text and (message.text.startswith("/reply") or message.text.startswith("/online") or message.text.startswith("/offline")):
             pass
        else:
            caption = message.caption if message.caption else message.text
            if caption and "/post" in caption:
                try:
                    clean_caption = caption.replace("/post", "").strip()
                    bot.copy_message(CHANNEL_USERNAME, ADMIN_ID, message.message_id, caption=clean_caption, parse_mode="Markdown")
                    bot.reply_to(message, "✅ Successfully posted to Channel!")
                except Exception as e:
                    bot.reply_to(message, f"❌ Failed to post: {e}")

# ================== CHANNEL WELCOME ==================
def delete_message_after_delay(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

@bot.chat_member_handler()
def channel_welcome(message: types.ChatMemberUpdated):
    new_member = message.new_chat_member
    if new_member.status in ["member", "administrator", "creator"]:
        user_name = new_member.user.first_name
        chat_id = message.chat.id
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🔥 Boost Your Growth Now", url=f"https://t.me/{BOT_USERNAME}?start=welcome"))
        welcome_text = (
            f"🌟 *Welcome, {user_name}!* 🌟\n\n"
            "🚀 *Take Your Brand to the Next Level with Shree Krishna IMA!*\n\n"
            "👇 *Click below to check our prices & services.*"
        )
        try:
            sent_msg = bot.send_message(chat_id, welcome_text, reply_markup=kb, parse_mode="Markdown")
            threading.Timer(60, delete_message_after_delay, args=[chat_id, sent_msg.message_id]).start()
        except:
            pass

# ================== AI FALLBACK ==================
@bot.message_handler(func=lambda message: True)
def default_response(message):
    if message.chat.id == ADMIN_ID: return
    text = (
        "Hello! I can help you with our services and projects.\n\n"
        "Use /start to get business info."
    )
    bot.send_message(message.chat.id, text)

# ================== RUN BOT ==================
print("🤖 SKIMA_Helper_bot is running with Smart Alert System...")
bot.infinity_polling(allowed_updates=['message', 'callback_query', 'chat_member'])
