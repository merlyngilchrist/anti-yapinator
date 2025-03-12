# 🤐 Anti-Yapinator: The Ultimate Interruption Bot

Tired of people talking too much in voice chat? **Anti-Yapinator** is here to help! This silly Discord bot lurks in voice channels and **rudely interrupts** a chosen target whenever they dare to speak. A perfect tool for *absolute chaos* or just some harmless fun.  

## 🎤 What Does It Do?
- **Joins a voice channel** and spies (uh, I mean… listens).  
- **Plays a loud, obnoxious sound** whenever the target user talks.  
- **Automatically disconnects** if nobody is around to be annoyed.  
- **Customizable access** so only authorized users can wield its disruptive power.  

## ⚠️ Warning  
Use responsibly. Or don’t. I’m not your boss.  

---

## 🛠️ Setup Guide
### Requirements
Before you let the **Anti-Yapinator** loose, make sure you have:
- **Python 3.8+** (because we’re civilized here).  
- **[FFmpeg](https://ffmpeg.org/download.html)** (needed to make noise).  
- A **Discord bot token** from [Discord Developer Portal](https://discord.com/developers/applications).  

### Installation
1. Clone this nonsense to your machine:
   ```sh
   git clone https://github.com/yourusername/anti-yapinator.git
   cd anti-yapinator

2. Install the necessary ~~black magic~~ dependencies:
   ```sh
   pip install -r requirements.txt

3. Create a .env file and add your bot token like so:
   ```sh
   DISCORD_BOT_TOKEN=your_super_secret_token

4. Run the bot and let the chaos begin:
   ```sh
   python bot.py

### 🔥 Commands (a.k.a. Ways to Annoy Your Friends) 

|           Command           |                   What It Does                  |
|:----------------------------|------------------------------------------------:|
| `!set_allowed_role @role`   | Grants a role the power to control the bot.     |
| `!show_allowed_roles`       | Shows who's in on the joke.                     |
| `!target @user`             | Selects the unlucky soul who will be _shut up_. |
| `!remove_target`            | Removes the current target (booo!)              |
| `!help_commands`            | Display all the ways you can cause mischief.    |

### 🚀 Deploying to Render (Because Keeping a PC On is Lame)

1. Got to [Render](Render.com) and create a **new Web Service**.

2. Link your Gethub repo.

3. Set the **Start Command**:
   ```sh
   python bot.py

4. Add you **Eviroment Variables**:
   -  `DISCORD_BOT_TOKEN`

5. Deploy and sit back as your bot wreaks havoc.

---

## 🤝 Contributing

Have a hilarious idea? Found a bug that ruins the fun? Submit a pull request or open an issue! Just don't ask me to make this bot _less_ annoying—it's against its very nature.

## 📜 License

Do whatever you want with this. Just don't blame me when your friends get mad.

---

This will display correctly on GitHub with all the formatting intact. Just update the GitHub repo link (`yourusername/anti-yapinator`) to match your actual repo. 🚀
