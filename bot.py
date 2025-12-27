from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import qrcode
from io import BytesIO

# ---------------- CONFIG ----------------
TOKEN = "8524217876:AAEx5D24HSQMdGyG2fg9fuT7bDfeXi-fTXU"
ADMIN_USERNAME = "@krishnraj_3103"

# ---------------- DEFAULT WELCOME MESSAGE ----------------
WELCOME_MESSAGE = (
    "👋 Hello! Welcome to Shree Krishna Influencer Marketing Agency Bot.\n\n"
    "🌐 Visit our website: https://shreekrishnaagency.github.io/Business/\n\n"
    "Please use the menu below to explore our services, projects, FAQ, contact info, and payment options."
)

# ---------------- BUSINESS DETAILS ----------------
about_text = (
    "Shree Krishna Influencer Marketing Agency helps brands grow through verified creators "
    "and provides result-oriented social media growth solutions."
)

services = {
    "Instagram Services": [
        "1,000 Views – ₹80",
        "1,000 Followers – ₹200",
        "1,000 Likes – ₹70",
        "1,000 Story Views – ₹60",
        "Reel Views Boost",
        "Engagement Package (Likes + Views)"
    ],
    "YouTube Services": [
        "1,000 Views – ₹150",
        "1,000 Likes – ₹140",
        "1,000 Subscribers – ₹2,580",
        "Watch Time Boost",
        "Video Promotion"
    ],
    "Telegram Services": [
        "1,000 Channel Members – ₹200",
        "10,000 Post Views – ₹100",
        "1,000 Reactions – ₹100",
        "Channel Growth Package"
    ],
    "Facebook Services": [
        "1,000 Reels Views – ₹100",
        "Page Likes + Followers (Combo) – ₹150",
        "1,000 Page Followers – ₹100",
        "1,000 Post Likes – ₹110"
    ],
    "Twitter / X Services": [
        "1,000 Likes – ₹220"
    ]
}

projects = {
    "Website & Subdomain Setup": [
        "Custom Website Creation",
        "Domain & Subdomain Setup",
        "Fully Functional & Responsive"
    ],
    "Vlog Writing": [
        "Engaging Content Writing",
        "SEO Optimized Scripts",
        "Creative Vlog Ideas"
    ],
    "Content Writing": [
        "High-Quality Blog Posts",
        "Website Articles & Captions",
        "SEO Optimized Content"
    ],
    "Telegram Bot Creation": [
        "Custom Telegram Bot Setup",
        "Automation & Interaction",
        "Admin Control Features"
    ]
}

faq = {
    "Do you offer refund?": "Yes ✅ 101% refund if work is not completed within given time.",
    "Is engagement real?": "Yes, we provide real and high-quality engagement only.",
    "How fast delivery?": "Mostly within 24–72 hours."
}

contact_info = {
    "Instagram": "https://www.instagram.com/shree.krishna.ima",
    "Telegram": "https://t.me/shreekrishnaIMA",
    "Email": "Influencers.shreekrishnaima@zohomail.in"
}

# ---------------- FUNCTIONS ----------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [["About Us", "Services"], ["Projects", "FAQ"], ["Contact", "Payment"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Send default welcome message with website link
    update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

def generate_qr(data: str):
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = BytesIO()
    bio.name = 'payment.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if text == "about us":
        update.message.reply_text(about_text)
    elif text == "services":
        msg = ""
        for key, items in services.items():
            msg += f"*{key}*\n" + "\n".join([f"- {i}" for i in items]) + "\n\n"
        update.message.reply_text(msg, parse_mode="Markdown")
    elif text == "projects":
        msg = ""
        for key, items in projects.items():
            msg += f"*{key}*\n" + "\n".join([f"- {i}" for i in items]) + "\n\n"
        update.message.reply_text(msg, parse_mode="Markdown")
    elif text == "faq":
        msg = ""
        for q, a in faq.items():
            msg += f"*{q}*\n{a}\n\n"
        update.message.reply_text(msg, parse_mode="Markdown")
    elif text == "contact":
        msg = "You can reach us here:\n"
        msg += f"Instagram: {contact_info['Instagram']}\n"
        msg += f"Telegram: {contact_info['Telegram']}\n"
        msg += f"Email: {contact_info['Email']}"
        update.message.reply_text(msg)
    elif text == "payment":
        upi_link = "upi://pay?pa=exampleupi@bank&pn=ShreeKrishnaAgency&am=100"
        qr_image = generate_qr(upi_link)
        update.message.reply_photo(qr_image, caption="Scan this QR to pay ₹100. After payment, send screenshot here.")
    else:
        update.message.reply_text("Sorry, I didn't understand that. Please use the menu buttons.")

def payment_screenshot(update: Update, context: CallbackContext):
    if update.message.photo:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=update.message.photo[-1].file_id,
                               caption=f"Payment screenshot from @{update.effective_user.username}")
        update.message.reply_text("Screenshot received! Thank you.")

# ---------------- MAIN ----------------
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.PHOTO, payment_screenshot))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
