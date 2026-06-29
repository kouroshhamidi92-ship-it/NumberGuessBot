import os
import sys
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from game_core_of_bot import GameCore

# ======================== تنظیمات ========================
try:
    PLATFORM = os.getenv("PLATFORM", "telegram")
except:
    try:
        PLATFORM = input(str("bale/telegram"))
    except:
        PLATFORM = "telegram"
        
if PLATFORM == "bale":
    BASE_URL = "https://tapi.bale.ai/bot"
    try:
        BOT_TOKEN = os.getenv("BALE_BOT_TOKEN")
    except:
        BOT_TOKEN = input(str("BALE_BOT_TOKEN"))
else:
    BASE_URL = None
    try:
        BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    except:
        BOT_TOKEN = input(str("TELEGRAM_BOT_TOKEN"))

print(f"🤖 ربات در حالت {PLATFORM} راه‌اندازی می‌شود...")

if not BOT_TOKEN:
    print("❌ توکن ربات پیدا نشد! متغیرهای محیطی را تنظیم کنید.")
    print("   برای تلگرام: TELEGRAM_BOT_TOKEN=your_token")
    print("   برای بله: BALE_BOT_TOKEN=your_token")
    sys.exit(1)

print(f"✅ توکن ربات دریافت شد (طول: {len(BOT_TOKEN)} کاراکتر)")
# ========================================================

user_games = {}
user_duels = {}
user_states = {}

# ======================== دکمه‌های شیشه‌ای ========================
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🎮 بازی جدید", callback_data="new_game"), InlineKeyboardButton("📊 وضعیت", callback_data="status")],
        [InlineKeyboardButton("💰 فروشگاه", callback_data="shop"), InlineKeyboardButton("🏆 رتبه‌بندی", callback_data="leaderboard")],
        [InlineKeyboardButton("⚔️ دوئل با ربات", callback_data="duel"), InlineKeyboardButton("⚙️ تنظیم بازه", callback_data="range")],
        [InlineKeyboardButton("📖 راهنما", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_shop_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌟 تم طلایی (۵۰)", callback_data="buy_gold"), InlineKeyboardButton("🌙 تم شب (۳۰)", callback_data="buy_dark")],
        [InlineKeyboardButton("💡 راهنما (۲۰)", callback_data="buy_hint"), InlineKeyboardButton("⏰ زمان اضافه (۱۵)", callback_data="buy_time")],
        [InlineKeyboardButton("⏭️ رد مرحله (۲۵)", callback_data="buy_skip"), InlineKeyboardButton("💰 سکه دوبرابر (۴۰)", callback_data="buy_double")],
        [InlineKeyboardButton("❤️ +۵ سکه (۱۰)", callback_data="buy_heart"), InlineKeyboardButton("🛡️ حفاظت خطا (۳۵)", callback_data="buy_shield")],
        [InlineKeyboardButton("🚀 شتاب زمان (۴۵)", callback_data="buy_boost")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_range_keyboard():
    keyboard = [
        [InlineKeyboardButton("🗂️ ۱ تا ۱۰۰", callback_data="range_1_100"), InlineKeyboardButton("🗂️ ۱ تا ۵۰۰", callback_data="range_1_500")],
        [InlineKeyboardButton("🗂️ ۱ تا ۱۰۰۰", callback_data="range_1_1000"), InlineKeyboardButton("✏️ سفارشی", callback_data="range_custom")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_duel_keyboard():
    keyboard = [
        [InlineKeyboardButton("⚔️ شروع دوئل", callback_data="duel_start")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_leaderboard_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 تازه‌سازی", callback_data="refresh_leaderboard")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ======================== دستورات ========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "کاربر"
    
    if user_id not in user_games:
        user_games[user_id] = GameCore(user_id)
        user_games[user_id].data["username"] = username
        user_games[user_id].save_data()
    
    await update.message.reply_text(
        f"🎮 به نابغه‌باز خوش آمدی {username}!\n\n"
        f"💰 سکه: {user_games[user_id].data['coins']}\n"
        f"🏆 بهترین: {user_games[user_id].data['best_score'] or '—'}\n"
        f"📈 مرحله: {user_games[user_id].data['level']}\n\n"
        "👇 یکی از گزینه‌های زیر را انتخاب کن:",
        reply_markup=get_main_menu()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if user_id not in user_games:
        user_games[user_id] = GameCore(user_id)
        user_games[user_id].data["username"] = query.from_user.first_name or "کاربر"
        user_games[user_id].save_data()

    game = user_games[user_id]

    if data == "new_game":
        game.new_game()
        await query.edit_message_text(
            f"🎯 بازی جدید!\n"
            f"🔢 عددی بین {game.data['current_min']} تا {game.data['current_max']} حدس بزن.\n"
            f"📝 عدد خود را به صورت پیام بفرست.",
            reply_markup=get_main_menu()
        )

    elif data == "status":
        status = game.get_status()
        await query.edit_message_text(
            f"📊 وضعیت بازی:\n"
            f"🔢 بازه: {status['min']} تا {status['max']}\n"
            f"📝 تلاش‌ها: {status['attempts']}\n"
            f"🎯 وضعیت: {'✅ تمام شده' if status['game_over'] else '🔄 در حال بازی'}\n"
            f"💰 سکه: {game.data['coins']}\n"
            f"🏆 بهترین: {game.data['best_score'] or '—'}\n"
            f"📈 مرحله: {game.data['level']}",
            reply_markup=get_main_menu()
        )

    elif data == "shop":
        shop = game.get_shop_list()
        msg = "🏪 فروشگاه:\n\n"
        for key, item in shop.items():
            owned = "✅" if key in game.data["purchased"] else "❌"
            msg += f"{item['icon']} {item['name']} - 🪙{item['price']} {owned}\n"
        msg += f"\n💰 سکه شما: {game.data['coins']}"
        await query.edit_message_text(msg, reply_markup=get_shop_keyboard())

    elif data.startswith("buy_"):
        item_id = data.replace("buy_", "")
        result = game.buy_item(item_id)
        await query.edit_message_text(result["message"], reply_markup=get_shop_keyboard())

    elif data == "leaderboard":
        scores = game.get_leaderboard()
        if not scores:
            msg = "🏆 هنوز امتیازی ثبت نشده، اولین نفر باش!"
        else:
            msg = "🏆 رتبه‌بندی جهانی:\n\n"
            for idx, s in enumerate(scores[:15], 1):
                msg += f"{idx}. {s['username']} - 🎯 {s['score']} تلاش (مرحله {s.get('level', 1)})\n"
        await query.edit_message_text(msg, reply_markup=get_leaderboard_keyboard())

    elif data == "refresh_leaderboard":
        scores = game.get_leaderboard()
        if not scores:
            msg = "🏆 هنوز امتیازی ثبت نشده، اولین نفر باش!"
        else:
            msg = "🏆 رتبه‌بندی جهانی:\n\n"
            for idx, s in enumerate(scores[:15], 1):
                msg += f"{idx}. {s['username']} - 🎯 {s['score']} تلاش (مرحله {s.get('level', 1)})\n"
        await query.edit_message_text(msg, reply_markup=get_leaderboard_keyboard())

    elif data == "range":
        await query.edit_message_text(
            f"⚙️ تنظیم بازه اعداد:\n"
            f"بازه فعلی: {game.data['current_min']} تا {game.data['current_max']}\n\n"
            "یکی از گزینه‌ها را انتخاب کن یا عدد سفارشی را به صورت `min max` بفرست.",
            reply_markup=get_range_keyboard()
        )

    elif data.startswith("range_"):
        if data == "range_1_100":
            result = game.change_range(1, 100)
        elif data == "range_1_500":
            result = game.change_range(1, 500)
        elif data == "range_1_1000":
            result = game.change_range(1, 1000)
        elif data == "range_custom":
            await query.edit_message_text(
                "✏️ لطفاً بازه جدید را به صورت `min max` بفرست.\nمثال: `10 200`",
                reply_markup=get_main_menu()
            )
            user_states[user_id] = "waiting_range"
            return
        else:
            result = {"status": "error", "message": "❌ گزینه نامعتبر"}
        await query.edit_message_text(result["message"], reply_markup=get_main_menu())

    elif data == "duel":
        await query.edit_message_text(
            "⚔️ حالت دوئل با ربات هوشمند!\n\n"
            "🤖 ربات یک عدد انتخاب می‌کند و شما باید حدس بزنید.\n"
            "هر کس زودتر پیدا کنه برنده است.\n\n"
            "💰 جایزه برنده: ۳۰ سکه",
            reply_markup=get_duel_keyboard()
        )

    elif data == "duel_start":
        result = game.duel_with_bot()
        user_duels[user_id] = result
        await query.edit_message_text(
            f"{result['message']}\n\n"
            f"🔢 بازه: {game.data['current_min']} تا {game.data['current_max']}\n"
            f"📝 عدد خود را بفرست.",
            reply_markup=get_main_menu()
        )
        user_states[user_id] = "waiting_duel"

    elif data == "help":
        await query.edit_message_text(
            "📖 راهنمای نابغه‌باز:\n\n"
            "🎯 هدف: عدد مخفی را در کمترین تلاش پیدا کن.\n"
            "💰 سکه: با هر برد سکه دریافت می‌کنی.\n"
            "🏆 رکورد: بهترین عملکردت ذخیره می‌شود.\n"
            "🛒 فروشگاه: با سکه‌ها آیتم‌های مختلف بخر.\n"
            "⚔️ دوئل: با ربات هوشمند مسابقه بده.\n"
            "📈 مرحله: با هر برد، سختی افزایش می‌یابد.\n\n"
            "دستورات:\n"
            "/start - منوی اصلی\n"
            "/newgame - شروع بازی جدید\n"
            "/status - وضعیت فعلی\n"
            "/shop - فروشگاه\n"
            "/leaderboard - رتبه‌بندی\n"
            "/duel - دوئل با ربات\n"
            "/range - تنظیم بازه\n"
            "/help - این راهنما",
            reply_markup=get_main_menu()
        )

    elif data == "back_main":
        await query.edit_message_text(
            f"🎮 به منوی اصلی بازگشتید.\n"
            f"💰 سکه: {game.data['coins']}\n"
            f"🏆 بهترین: {game.data['best_score'] or '—'}",
            reply_markup=get_main_menu()
        )

# ======================== هندلر پیام‌ها ========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_games:
        user_games[user_id] = GameCore(user_id)
        user_games[user_id].data["username"] = update.effective_user.first_name or "کاربر"
        user_games[user_id].save_data()

    game = user_games[user_id]

    if user_states.get(user_id) == "waiting_range":
        parts = text.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            result = game.change_range(int(parts[0]), int(parts[1]))
            if result["status"] == "ok":
                await update.message.reply_text(result["message"], reply_markup=get_main_menu())
            else:
                await update.message.reply_text(result["message"], reply_markup=get_range_keyboard())
        else:
            await update.message.reply_text("❌ لطفاً به صورت `min max` بفرست. مثال: `10 200`")
        user_states[user_id] = None
        return

    if user_states.get(user_id) == "waiting_duel":
        if not text.isdigit():
            await update.message.reply_text("❌ لطفاً یک عدد معتبر بفرست!")
            return

        duel_data = user_duels.get(user_id)
        if not duel_data:
            await update.message.reply_text("❌ دوئلی فعال نیست! از منوی دوئل شروع کن.")
            user_states[user_id] = None
            return

        player_guess = int(text)
        bot_number = duel_data["bot_number"]
        duel_data["player_attempts"] += 1

        if player_guess == bot_number:
            game.data["coins"] += 30
            game.save_data()
            await update.message.reply_text(
                f"🎉 برنده شدی! عدد {bot_number} بود.\n"
                f"💰 +۳۰ سکه به حساب تو واریز شد.\n"
                f"🪙 سکه فعلی: {game.data['coins']}",
                reply_markup=get_main_menu()
            )
            user_states[user_id] = None
            del user_duels[user_id]
            return

        hint = "⬆️ بالاتر" if player_guess < bot_number else "⬇️ پایین‌تر"
        bot_guess = random.randint(game.data["current_min"], game.data["current_max"])
        duel_data["bot_attempts"] += 1

        if bot_guess == bot_number:
            await update.message.reply_text(
                f"😢 ربات برنده شد! عدد {bot_number} بود.\n"
                f"🤖 ربات حدس زد: {bot_guess}\n"
                f"📝 شما حدس زدید: {player_guess} ({hint})",
                reply_markup=get_main_menu()
            )
            user_states[user_id] = None
            del user_duels[user_id]
            return

        await update.message.reply_text(
            f"📝 شما: {player_guess} ({hint})\n"
            f"🤖 ربات: {bot_guess}\n\n"
            f"🎯 نوبت شماست، دوباره حدس بزن!\n"
            f"💡 راهنما: عدد بین {game.data['current_min']} تا {game.data['current_max']} است."
        )
        return

    if game.data["game_over"]:
        await update.message.reply_text("🎮 بازی تمام شده! از منوی اصلی بازی جدید شروع کن.", reply_markup=get_main_menu())
        return

    if not text.isdigit():
        await update.message.reply_text("❌ لطفاً یک عدد معتبر بفرست!")
        return

    number = int(text)
    result = game.guess(number)

    if result["status"] == "win":
        msg = result["message"]
        if result.get("is_best"):
            msg += "\n🔥 رکورد شخصی شکسته شد! 🏆"
        if result.get("level_up"):
            msg += f"\n📈 مرحله {result['new_level']} شروع شد! (بازه: {game.data['current_min']} تا {game.data['current_max']})"
        msg += f"\n💰 +{result['coins']} سکه (مجموع: {game.data['coins']})"
        await update.message.reply_text(msg, reply_markup=get_main_menu())

    elif result["status"] == "hint":
        msg = f"{result['message']}\n📝 تلاش‌ها: {result['attempts']}"
        await update.message.reply_text(msg)

    else:
        await update.message.reply_text(result["message"], reply_markup=get_main_menu())

# ======================== تابع اصلی اصلاح‌شده با await ========================
def main():
    """تابع اصلی اجرای ربات"""
    async def run():
        try:
            builder = Application.builder().token(BOT_TOKEN)
            if BASE_URL:
                builder = builder.base_url(BASE_URL)
            application = builder.build()

            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("newgame", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CommandHandler("status", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CommandHandler("shop", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CommandHandler("leaderboard", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CommandHandler("duel", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CommandHandler("range", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CommandHandler("help", lambda u,c: handle_callback(u.update(c), c)))
            application.add_handler(CallbackQueryHandler(handle_callback))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

            print(f"🤖 ربات {PLATFORM} روشن شد...")
            # ✅ اصلاح: اضافه کردن await
            await application.run_polling(allowed_updates=["message", "callback_query"])
        except Exception as e:
            print(f"❌ خطا در اجرای ربات: {e}")
            raise

    asyncio.run(run())

if __name__ == "__main__":
    main()