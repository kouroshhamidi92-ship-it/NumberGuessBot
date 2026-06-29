import random
import json
import os
from datetime import datetime

class GameCore:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data_file = f"users/{user_id}.json"
        self.load_data()

    def load_data(self):
        os.makedirs("users", exist_ok=True)
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "username": "کاربر",
                "coins": 100,
                "best_score": None,
                "level": 0,
                "purchased": [],
                "current_min": 0,
                "current_max": 100,
                "secret_number": 0,
                "attempts": 0,
                "game_over": False,
                "start_time": None
            }
            self.save_data()
        self.init_game()

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def init_game(self):
        if not self.data["game_over"] and self.data["secret_number"] == 0:
            self.new_game()

    def new_game(self):
        self.data["secret_number"] = random.randint(
            self.data["current_min"], 
            self.data["current_max"]
        )
        self.data["attempts"] = 0
        self.data["game_over"] = False
        self.data["start_time"] = datetime.now().isoformat()
        self.save_data()
        return self.get_status()

    def get_status(self):
        return {
            "min": self.data["current_min"],
            "max": self.data["current_max"],
            "attempts": self.data["attempts"],
            "game_over": self.data["game_over"],
            "secret": self.data["secret_number"] if self.data["game_over"] else None
        }

    def guess(self, number):
        if self.data["game_over"]:
            return {"status": "game_over", "message": "🎮 بازی تمام شده! برای شروع جدید /newgame بفرست."}

        if number < self.data["current_min"] or number > self.data["current_max"]:
            return {
                "status": "error",
                "message": f"⚠️ عدد باید بین {self.data['current_min']} تا {self.data['current_max']} باشه."
            }

        self.data["attempts"] += 1

        if number == self.data["secret_number"]:
            self.data["game_over"] = True
            elapsed = self.get_elapsed_time()
            rating = self.get_rating()
            reward = max(10, 30 - self.data["attempts"])
            self.data["coins"] += reward

            is_best = False
            if self.data["best_score"] is None or self.data["attempts"] < self.data["best_score"]:
                self.data["best_score"] = self.data["attempts"]
                is_best = True

            level_up = False
            if self.data["attempts"] <= 10:
                self.data["level"] += 1
                self.data["current_max"] = min(1000, self.data["current_max"] + 50)
                level_up = True

            self.save_data()
            return {
                "status": "win",
                "message": f"🎉 {rating} | عدد {self.data['secret_number']} رو در {self.data['attempts']} تلاش پیدا کردی! ⏱️ {elapsed}",
                "coins": reward,
                "is_best": is_best,
                "level_up": level_up,
                "new_level": self.data["level"] if level_up else None,
                "best_score": self.data["best_score"]
            }

        hint = "⬆️ بالاتر" if number < self.data["secret_number"] else "⬇️ پایین‌تر"
        self.save_data()
        return {
            "status": "hint",
            "message": f"{hint} (حدس {number})",
            "attempts": self.data["attempts"]
        }

    # ✅ تغییرات شما: محاسبه rating بر اساس فاصله بازه
    def get_rating(self):
        distance = self.data['current_max'] - self.data['current_min']
        if self.data["attempts"] <= distance // 20:
            return "🏆 نابغه مطلق"
        elif self.data["attempts"] <= distance // 12.5:
            return "😎 حرفه‌ای"
        elif self.data["attempts"] <= distance // 8.33:
            return "👍 خوب بود"
        elif self.data["attempts"] <= distance // 10:
            return "بدک نبود\nدوباره تلاش کن😁"
        else:
            return "🤦‍♀️😂 دوباره تلاش کن"

    def get_elapsed_time(self):
        if self.data["start_time"]:
            start = datetime.fromisoformat(self.data["start_time"])
            elapsed = datetime.now() - start
            minutes = elapsed.seconds // 60
            seconds = elapsed.seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"

    # ✅ تغییرات شما: شرط حداقل فاصله ۱۰۰ در تغییر بازه
    def change_range(self, new_min, new_max):
        if new_min >= new_max:
            return {"status": "error", "message": "❌ حداقل باید از حداکثر کوچک‌تر باشه!"}
        if new_max - new_min < 99:
            return {"status" : "error", "message" : "❌ فاصله حداقل از حداکثر باید 100 باشه"}
        self.data["current_min"] = new_min
        self.data["current_max"] = new_max
        self.new_game()
        self.save_data()
        return {"status": "ok", "message": f"✅ بازه تغییر کرد به {new_min} تا {new_max}"}

    def buy_item(self, item_id):
        shop_items = {
            "gold": {"name": "تم طلایی", "price": 50},
            "dark": {"name": "تم شب", "price": 30},
            "hint": {"name": "راهنما (۵ بار)", "price": 20},
            "time": {"name": "زمان اضافه", "price": 15},
            "skip": {"name": "رد مرحله", "price": 25},
            "double": {"name": "سکه دوبرابر", "price": 40},
            "heart": {"name": "+۵ سکه روزانه", "price": 10},
            "shield": {"name": "حفاظت خطا", "price": 35},
            "boost": {"name": "شتاب زمان", "price": 45}
        }

        if item_id not in shop_items:
            return {"status": "error", "message": "❌ آیتم نامعتبر"}

        if item_id in self.data["purchased"]:
            return {"status": "error", "message": "✅ این آیتم قبلاً خریداری شده!"}

        price = shop_items[item_id]["price"]
        if self.data["coins"] < price:
            return {"status": "error", "message": f"💰 سکه کافی نیست! نیاز: {price}، داری: {self.data['coins']}"}

        self.data["coins"] -= price
        self.data["purchased"].append(item_id)
        self.save_data()
        return {
            "status": "ok",
            "message": f"🎉 {shop_items[item_id]['name']} خریداری شد! سکه باقی‌مانده: {self.data['coins']}"
        }

    def get_shop_list(self):
        shop_items = {
            "gold": {"name": "تم طلایی", "price": 50, "icon": "🌟"},
            "dark": {"name": "تم شب", "price": 30, "icon": "🌙"},
            "hint": {"name": "راهنما (۵ بار)", "price": 20, "icon": "💡"},
            "time": {"name": "زمان اضافه", "price": 15, "icon": "⏰"},
            "skip": {"name": "رد مرحله", "price": 25, "icon": "⏭️"},
            "double": {"name": "سکه دوبرابر", "price": 40, "icon": "💰"},
            "heart": {"name": "+۵ سکه روزانه", "price": 10, "icon": "❤️"},
            "shield": {"name": "حفاظت خطا", "price": 35, "icon": "🛡️"},
            "boost": {"name": "شتاب زمان", "price": 45, "icon": "🚀"}
        }
        return shop_items

    def get_leaderboard(self):
        leaderboard_file = "leaderboard.json"
        if os.path.exists(leaderboard_file):
            with open(leaderboard_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_score(self, username):
        if not self.data["game_over"] or self.data["attempts"] == 0:
            return {"status": "error", "message": "❌ اول یک بازی رو کامل کن!"}

        leaderboard_file = "leaderboard.json"
        scores = self.get_leaderboard()
        scores.append({
            "username": username or "کاربر",
            "user_id": self.user_id,
            "score": self.data["attempts"],
            "level": self.data["level"],
            "timestamp": datetime.now().isoformat()
        })
        scores.sort(key=lambda x: x["score"])
        scores = scores[:50]
        with open(leaderboard_file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        return {"status": "ok", "message": "✅ امتیاز شما در رتبه‌بندی ثبت شد!"}

    def duel_with_bot(self):
        bot_number = random.randint(self.data["current_min"], self.data["current_max"])
        return {
            "status": "duel_start",
            "message": "🤖 دوئل با ربات شروع شد! یک عدد حدس بزن.",
            "bot_number": bot_number,
            "player_attempts": 0,
            "bot_attempts": 0,
            "turn": "player"
        }