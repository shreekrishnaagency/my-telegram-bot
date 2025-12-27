from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import qrcode
from io import BytesIO

# ---------------- CONFIG ----------------
TOKEN = "8524217876:AAEx5D24HSQMdGyG2fg9fuT7bDfeXi-fTXU"
ADMIN_USERNAME = "@krishnraj_3103"

# Knowledge base for auto replies
knowledge_base = {
    "service1": "Service 1 details: We offer amazing service 1...",
    "service2": "Service 2 details: We also offer service 2...",
    "payment": "For payment, please scan the QR code sent below.",
    "about": "This is Shree Krishna Agency helping bot. We help our clients with all business queries."
}

# ---------------- FUNCTIONS ----------------
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [["About", "Services"], ["Payment", "Contact Support"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        f"Hello {user.first_name}! Main aapki help karne ke liye yahan hoon.",
        reply_markup=reply_markup
    )

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

    if text == "about":
        update.message.reply_text(knowledge_base["about"])
    elif text == "services":
        services_text = "Here are our services:\n"
        services_text += "\n".join([f"- {k}: {v}" for k,v in knowledge_base.items() if "service" in k])
        update.message.reply_text(services_text)
    elif text == "payment":
        # QR code data (example UPI link)
        upi_link = "upi://pay?pa=exampleupi@bank&pn=ShreeKrishnaAgency&am=100"
        qr_image = generate_qr(upi_link)
        update.message.reply_photo(qr_image, caption="Scan this QR to pay ₹100. After payment, send screenshot here.")
    elif text == "contact support":
        update.message.reply_text(f"You can contact {ADMIN_USERNAME} directly for support.")
    else:
        # Auto reply using keywords
        replied = False
        for key in knowledge_base:
            if key in text:
                update.message.reply_text(knowledge_base[key])
                replied = True
                break
        if not replied:
            update.message.reply_text("Sorry, mujhe ye samajh nahi aaya. Menu se select kare.")

def payment_screenshot(update: Update, context: CallbackContext):
    if update.message.photo:
        # Forward screenshot to admin
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
