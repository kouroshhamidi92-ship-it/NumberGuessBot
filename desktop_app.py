# desktop_app.py
import sys, random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QGroupBox, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class NumberGuessGame:
    def __init__(self, min_range = 0, max_range = 100):
        self.min_range = min_range
        self.max_range = max_range
        self.secret_number = random.randint(min_range, max_range)
        self.attempts = 0
        self.game_over = False
        self.history = []

    def guess(self, number):
        if self.game_over:
            return None, "بازی تمام شده! برای شروع دوباره، از متد reset() استفاده کن."

        if number < self.min_range or number > self.max_range:
            return None, f"⚠️ عدد باید بین {self.min_range} تا {self.max_range} باشه."

        self.attempts += 1
        self.history.append(number)

        if number == self.secret_number:
            self.game_over = True
            # محاسبه امتیاز

            distance = self.max_range - self.min_range

            if self.attempts <= distance // 20:
                score = "🏆 نابغه"
            elif self.attempts <= distance // 10:
                score = "😎 خوبه"
            elif self.attempts <= distance // 5:
                score = "بدک نبود👌"
            elif self.attempts <= distance // 4:
                score = "خراب کردی"
            else:
                score = "😂 اینقدر بد بودی که به نظر من دوباره امتحان کن"
            return (True, self.attempts, score,
                    f"🎉 آفرین! عدد {self.secret_number} رو در {self.attempts} تلاش پیدا کردی. {score}")

        elif number < self.secret_number:
            return (False, self.attempts, "⬆️ بالاتر!",
                    f"عدد {number} کوچیک‌تر از عدد مخفیه. یه عدد بزرگ‌تر امتحان کن.")
        else:
            return (False, self.attempts, "⬇️ پایین‌تر!",
                    f"عدد {number} بزرگ‌تر از عدد مخفیه. یه عدد کوچیک‌تر امتحان کن.")

    def reset(self):
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_over = False
        self.history.clear()

    def change_range(self, new_min, new_max):
        if new_min >= new_max:
            return False, "❌ حداقل باید از حداکثر کوچیک‌تر باشه!"
        distance = self.max_range - self.min_range
        if distance < 100 :
            return False, "فاصله اعداد باید از 100 بیشتر باشه ❌"
        self.min_range = new_min
        self.max_range = new_max
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_over = False
        self.history.clear()
        return True, f"✅ بازه تغییر کرد به {new_min} تا {new_max}"


class NumberGuessGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = NumberGuessGame()
        self.setWindowTitle("🎮 بازی تشخیص عدد مخفی - نسخه حرفه‌ای: 1.0.0")
        self.setMinimumSize(500, 600)
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # بخش تنظیمات بازه
        range_group = QGroupBox("⚙️ تنظیمات بازه اعداد")
        range_layout = QHBoxLayout()
        self.min_spin = QSpinBox()
        self.min_spin.setRange(1, 999)
        self.min_spin.setValue(1)
        self.max_spin = QSpinBox()
        self.max_spin.setRange(2, 1000)
        self.max_spin.setValue(100)
        self.apply_btn = QPushButton("اعمال و شروع مجدد")
        self.apply_btn.clicked.connect(self.change_range)
        range_layout.addWidget(QLabel("از:"))
        range_layout.addWidget(self.min_spin)
        range_layout.addWidget(QLabel("تا:"))
        range_layout.addWidget(self.max_spin)
        range_layout.addWidget(self.apply_btn)
        range_layout.addStretch()
        range_group.setLayout(range_layout)
        layout.addWidget(range_group)

        # نمایش وضعیت بازی
        self.status_label = QLabel(f"🔢 عدد مخفی بین ۱ تا ۱۰۰ انتخاب شده.")
        self.status_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.status_label)

        self.attempt_label = QLabel("📊 تعداد تلاش‌ها: 0")
        self.attempt_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.attempt_label)

        # ورودی و دکمه‌ها
        input_layout = QHBoxLayout()
        self.guess_input = QLineEdit()
        self.guess_input.setPlaceholderText("عدد مورد نظرت رو وارد کن...")
        self.guess_input.returnPressed.connect(self.make_guess)
        self.guess_btn = QPushButton("🔍 حدس بزن")
        self.guess_btn.clicked.connect(self.make_guess)
        self.reset_btn = QPushButton("🔄 بازی جدید")
        self.reset_btn.clicked.connect(self.reset_game)
        input_layout.addWidget(self.guess_input)
        input_layout.addWidget(self.guess_btn)
        input_layout.addWidget(self.reset_btn)
        layout.addLayout(input_layout)

        # پیام راهنما
        self.hint_label = QLabel("✨ منتظر حدس تو هستم...")
        self.hint_label.setWordWrap(True)
        self.hint_label.setStyleSheet("background-color: #2a2a3a; padding: 10px; border-radius: 8px;")
        layout.addWidget(self.hint_label)

        # تاریخچه حدس‌ها
        history_group = QGroupBox("📜 تاریخچه حدس‌ها")
        history_layout = QVBoxLayout()
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(150)
        history_layout.addWidget(self.history_text)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)

        self.guess_input.setFocus()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2f; }
            QLabel, QGroupBox { color: #f0f0f0; font-family: 'Segoe UI'; }
            QLineEdit { background-color: #2d2d3a; color: white; border: 1px solid #5a5a6e; border-radius: 8px; padding: 8px; font-size: 14px; }
            QPushButton { background-color: #3c3c4e; color: white; border: none; border-radius: 8px; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #55556e; }
            QTextEdit { background-color: #2d2d3a; color: #e0e0e0; border: 1px solid #5a5a6e; border-radius: 8px; }
        """)

    def make_guess(self):
        try:
            guess = int(self.guess_input.text())
        except ValueError:
            self.hint_label.setText("❌ لطفاً یه عدد معتبر وارد کن!")
            return

        result = self.game.guess(guess)
        if result[0] is None:
            self.hint_label.setText(result[1])
            return

        is_correct, attempts, direction_or_score, message = result

        if is_correct:
            self.hint_label.setText(message)
            self.status_label.setText(f"🎉 بازی تمام شد! عدد مخفی {self.game.secret_number} بود.")
            self.guess_btn.setEnabled(False)
            self.guess_input.setEnabled(False)
        else:
            self.hint_label.setText(message)

        self.attempt_label.setText(f"📊 تعداد تلاش‌ها: {attempts}")
        self.update_history()
        self.guess_input.clear()
        self.guess_input.setFocus()

    def update_history(self):
        self.history_text.clear()
        for i, g in enumerate(self.game.history, 1):
            self.history_text.append(f"تلاش {i}: {g}")

    def change_range(self):
        new_min = self.min_spin.value()
        new_max = self.max_spin.value()
        success, msg = self.game.change_range(new_min, new_max)
        QMessageBox.information(self, "تغییر بازه", msg)
        if success:
            self.status_label.setText(f"🔢 عدد مخفی بین {new_min} تا {new_max} انتخاب شده.")
            self.attempt_label.setText("📊 تعداد تلاش‌ها: 0")
            self.hint_label.setText("✨ بازی جدید با بازه جدید!")
            self.history_text.clear()
            self.guess_btn.setEnabled(True)
            self.guess_input.setEnabled(True)
            self.guess_input.clear()
            self.guess_input.setFocus()

    def reset_game(self):
        self.game.reset()
        self.status_label.setText(f"🔢 عدد مخفی بین {self.game.min_range} تا {self.game.max_range} انتخاب شده.")
        self.attempt_label.setText("📊 تعداد تلاش‌ها: 0")
        self.hint_label.setText("✨ بازی جدید! یه عدد حدس بزن.")
        self.history_text.clear()
        self.guess_btn.setEnabled(True)
        self.guess_input.setEnabled(True)
        self.guess_input.clear()
        self.guess_input.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumberGuessGUI()
    window.show()
    sys.exit(app.exec())