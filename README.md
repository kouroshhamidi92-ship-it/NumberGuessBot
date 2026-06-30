ببخشید، اشتباه کردم. حق با شماست. این دقیقاً همان README اولیه است که فقط جداولش رو برداشتم و به لیست ساده تبدیل کردم. هیچ چیز دیگه‌ای تغییر نکرده.

---

# 🎯 NumberGuessBot | نابغه‌باز

> 🤖 Smart Number Guessing Game with Coin System, Shop, AI Duels & Global Leaderboard  
> 📱 Works on Telegram | Bale | Desktop | Web

---

## 📌 About

**NumberGuessBot** is a complete cross-platform number guessing game.  
One codebase runs on **4 platforms**:

- 🤖 **Telegram** – Inline keyboard + professional menu
- 💬 **Bale** – Same code, different BASE_URL
- 🖥️ **Desktop** – PyQt6 GUI app
- 🌐 **Web / Android** – PWA-ready HTML version

---

## ✨ Features

- 🎮 Number guessing with higher/lower hints
- 💰 Coin system (earn per win)
- 🏪 Shop with 9 items (themes, hints, boosts, etc.)
- 🏆 Global leaderboard
- ⚔️ AI bot duels
- 📈 Progressive difficulty levels
- ⏱️ Timer
- 🎯 Personal best score
- ⚙️ Customizable range
- 🎨 Glassmorphism UI (web version)
- 🧠 AI-powered hints
- 🔥 PWA support
- 📝 Phone/Email auth (web version)
- 📦 No database required (JSON storage)
- 🚀 High performance
- 🛡️ Error handling
- 🌍 Full Persian + English support

---

## 📸 Preview

### Telegram / Bale
```
🎮 Welcome to NumberGuessBot!
💰 Coins: 100
🏆 Best: —
📈 Level: 1

[🎮 New Game]  [📊 Status]
[💰 Shop]     [🏆 Leaderboard]
[⚔️ Duel]     [⚙️ Set Range]
[📖 Help]
```

### Web / Android
- Glassmorphism design
- 200+ animations
- 350+ floating particles
- 9-item shop
- AI duel system
- Local authentication

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- `python-telegram-bot`

### Steps

```bash
# Clone
git clone https://github.com/kouroshhamidi92-ship-it/NumberGuessBot.git
cd NumberGuessBot

# Install
pip install -r requirements.txt

# Set environment variables (create .env file)
PLATFORM=telegram
TELEGRAM_BOT_TOKEN=your_token_here
# or
PLATFORM=bale
BALE_BOT_TOKEN=your_token_here

# Run
python bot.py
```

---

## 🖥️ Desktop Version

```bash
python desktop_app.py
```

### Build EXE (Nuitka – fast)
```bash
python -m nuitka --standalone --enable-plugin=pyqt6 --windows-console-mode=disable --lto=yes --assume-yes-for-downloads --remove-output --output-dir=output --jobs=4 desktop_app.py
```

### Build EXE (PyInstaller – simple)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name="NumberGuessGame" desktop_app.py
```

---

## 🌐 Web / Android

Open `index.html` in any browser.

Convert to Android app using:
- PWA2APK
- WebViewGold
- Android Studio WebView

---

## ☁️ Free Hosting (Render)

1. Sign up at [render.com](https://render.com)
2. Create a **Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variables:
   - `PLATFORM` = `telegram` or `bale`
   - `TELEGRAM_BOT_TOKEN` / `BALE_BOT_TOKEN`
6. Deploy

### Keep Alive (Prevent Sleep)
Use [UptimeRobot](https://uptimerobot.com) – ping `https://your-app.onrender.com/health` every 5 minutes.

---

## 📁 Project Structure

```
NumberGuessBot/
├── bot.py              # Main bot code
├── game_core.py        # Game logic
├── app.py              # Flask for Render
├── desktop_app.py      # PyQt6 GUI
├── index.html          # Web/Android version
├── requirements.txt    # Dependencies
├── .env.example        # Sample env
├── README.md           # This file
├── LICENSE             # MIT License
├── users/              # User data (auto-generated)
└── leaderboard.json    # Global scores (auto-generated)
```

---

## 🛠️ Tech Stack

- Python 3.9+
- python-telegram-bot
- PyQt6
- Flask + Gunicorn
- HTML / CSS / JS
- GSAP (animations)
- JSON (storage)
- Git / GitHub
- Render (hosting)

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 👨‍💻 Developer

**Kourosh Hamidi**  
GitHub: [kouroshhamidi92-ship-it](https://github.com/kouroshhamidi92-ship-it)

---

## 💳 Support

If you like this project, you can support development via:

```
5022291532823695 (Shaparak)
```

---

## 📜 License

MIT License – see [LICENSE](LICENSE) file.

---

## ⭐ Star This Project

If you find this useful, please give it a ⭐ on GitHub!

---

**Built with ❤️ by Kourosh Hamidi – Iran**
