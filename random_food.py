import discord
import random
import json
import os


with open("food_list.json", "r", encoding="utf-8") as f:
    food_data = json.load(f)


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.strip() == "!สุ่ม":
        random_food = random.choice(food_data["foods"])
        await message.channel.send(f"ไปหาซื้อ '{random_food}' ซะ แล้วก็ไม่ต้องสุ่มใหม่ล่ะ เหนื่อยจะสุ่มมม")
    elif message.content.strip() == "!ช่วยเหลือ":
        help_text = (
            "**คำสั่งใช้งาน**\n"
            "`!สุ่มอาหาร` - เพื่อให้บอทช่วยสุ่มเมนูอาหาร\n"
            "`!ช่วยเหลือ` - แสดงคำสั่งทั้งหมด"
        )
        await message.channel.send(help_text)

client.run(os.getenv('TOKEN'))
