import discord
import random
import json
import os
import threading
import asyncio
from flask import Flask

# อ่านข้อมูลจากไฟล์ JSON
with open("food_list.json", "r", encoding="utf-8") as f:
    food_data = json.load(f)

# สร้าง Flask app สำหรับการฟัง HTTP requests
app = Flask(__name__)

@app.route('/')
def index():
    return "Discord bot is running"

# ตั้งค่า Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# สร้าง dictionary สำหรับเก็บจำนวนครั้งที่ผู้ใช้ส่งข้อความ
user_message_count = {}

# ฟังก์ชันสำหรับรีเซ็ตนับจำนวนทุก 5 นาที
async def reset_message_count():
    while True:
        await asyncio.sleep(300)  # รอ 5 นาที
        user_message_count.clear()  # รีเซ็ตจำนวนครั้ง
        print("Reset message count")

# ตั้ง event เมื่อ Discord bot พร้อมใช้งาน
@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

# ตั้ง event เมื่อมีข้อความ
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # ตรวจสอบการนับจำนวนข้อความของผู้ใช้
    user_id = message.author.id
    if user_id not in user_message_count:
        user_message_count[user_id] = 0

    # เพิ่มจำนวนครั้งที่ผู้ใช้ส่งข้อความ
    user_message_count[user_id] += 1
    message_count = user_message_count[user_id]

    # กำหนดข้อความตอบกลับตามจำนวนที่ส่ง
    if message.content.strip() == "!สุ่ม":
        random_food = random.choice(food_data["foods"])
        if message_count == 1:
            await message.channel.send(f"ไปหาซื้อ '{random_food}' ซะ แล้วก็ไม่ต้องสุ่มใหม่ล่ะ อย่าให้มีครั้งที่ 2")
        elif message_count == 2:
            await message.channel.send(f"ไปหาซื้อ '{random_food}' ซะ แล้วก็ไม่ต้องสุ่มใหม่ล่ะ อย่าให้มีครั้งที่ 3 เด็ดขาด")
        elif message_count == 3:
            await message.channel.send(f"ไปหาซื้อ '{random_food}' ซะ ครั้งที่ 4 นี่ไม่ควร")
        elif message_count == 3:
            await message.channel.send(f"ถ้ามีในใจแล้วก็ไม่ต้องสุ่มจ้าา จะล่าแบ้")
        else:
            await message.channel.send(f"ไปหาซื้อ '{random_food}' ซะ แล้วก็ไม่ต้องสุ่มใหม่ล่ะ เหนื่อยจะสุ่มมม")
    elif message.content.strip() == "!ช่วยเหลือ":
        help_text = (
            "**คำสั่งใช้งาน**\n"
            "`!สุ่มอาหาร` - เพื่อให้บอทช่วยสุ่มเมนูอาหาร\n"
            "`!ช่วยเหลือ` - แสดงคำสั่งทั้งหมด"
        )
        await message.channel.send(help_text)

# ฟังก์ชันสำหรับเริ่ม Discord bot ใน thread แยก
def run_discord_bot():
    client.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    # สร้าง thread เพื่อให้ Discord bot รันในขณะที่ Flask app ฟัง HTTP requests
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.start()

    # เริ่มฟังก์ชันรีเซ็ตการนับจำนวนข้อความทุกๆ 5 นาที
    loop = asyncio.get_event_loop()
    loop.create_task(reset_message_count())

    # ฟังพอร์ตที่ Render กำหนด
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
