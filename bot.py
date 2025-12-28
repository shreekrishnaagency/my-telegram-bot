from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = "8524217876:AAGWFO2g0vBnWsFQnwO1IEns9ZxZ148gcAU"
ADMIN_ID = 5265106993
# ==========================================

user_data_store = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💼 Our Services", callback_data="services")],
        [InlineKeyboardButton("💳 Pay Now", callback_data="pay")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🙏 Welcome!\n\n"
        "Main *Shree Krishna Agency* ka helping bot hoon 🤖\n\n"
        "Services dekhne ya payment karne ke liye niche option select kare 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Button click handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        await query.message.reply_text(
            "📌 *Our Services*\n\n"
            "• Influencer Marketing\n"
            "• Brand Promotion\n"
            "• Social Media Growth\n\n"
            "Payment ke liye *Pay Now* button dabaye 💳",
            parse_mode="Markdown"
        )

    elif query.data == "pay":
        user_data_store[query.from_user.id] = {}

        await query.message.reply_photo(
            photo=open("QR.png", "rb"),
            caption=(
                "💳 *Payment QR Code*\n\n"
                "Payment ke baad ye 3 cheeze bheje:\n\n"
                "1️⃣ Amount\n"
                "2️⃣ Paid From Name\n"
                "3️⃣ Screenshot 📸"
            ),
            parse_mode="Markdown"
        )

# Text handler (Amount & Paid From Name)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data_store:
        return

    data = user_data_store[user_id]

    if "amount" not in data:
        data["amount"] = text
        await update.message.reply_text(
            "✅ Amount noted.\n\nAb *Paid From Name* bheje.",
            parse_mode="Markdown"
        )

    elif "paid_name" not in data:
        data["paid_name"] = text
        await update.message.reply_text(
            "✅ Name noted.\n\nAb payment *screenshot* upload kare 📸",
            parse_mode="Markdown"
        )

# Screenshot handler
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]

    data = user_data_store.get(user.id, {})

    admin_caption = (
        "🔔 *NEW PAYMENT RECEIVED*\n\n"
        f"👤 Name: {user.first_name}\n"
        f"🔗 Username: @{user.username}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"💰 Amount: {data.get('amount', 'Not given')}\n"
        f"🏦 Paid From: {data.get('paid_name', 'Not given')}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=admin_caption,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "✅ Screenshot received!\n\n"
        "Payment verify hone ke baad team aapse contact karegi 🙏"
    )

    user_data_store.pop(user.id, None)

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
