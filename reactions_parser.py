import os
import pandas as pd
from pyrogram import Client
import csv
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

app = Client("my_account", api_id=api_id, api_hash=api_hash)

chats_id = ["readovkanews", "rt_russian", "uranews", "rbc_news", "pravdadirty", "chtddd", "ru2ch", "novosti_efir", "tele_eve",
            "ssigny", "shot_shot", "Cbpub", "nemorgenshtern", "tvrain", "novaya_pishet", "truekpru", "oldlentach", "kommersant",
            "rgrunews", "SuperRu", "lentadnya", "infomoscow24", "ntvnews", "nwsru"]

message_limit = 15000

temp_data_path = os.getenv('temp_data_path')
for chat_id in chats_id:
    csv_file = f"{temp_data_path}/reactions_{chat_id}.csv"

    with app:
        chat = app.get_chat(chat_id)
        chat_title = chat.title or chat.username or chat_id
        chat_link = f"https://t.me/{chat.username}" if chat.username else f"https://t.me/c/{chat.id}"

        messages = app.get_chat_history(chat_id, limit=message_limit)

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["channel_name", "channel_link", "post", "post_link", "reactions"])

            for message in messages:
                text = message.text or ""
                if text:
                    text = text.strip()

                caption = message.caption or ""

                post_link = message.link if message.link else ""

                reactions = ""
                if hasattr(message, "reactions") and message.reactions is not None:
                    reactions = ", ".join([f"{r.emoji}: {r.count}" for r in message.reactions.reactions])

                writer.writerow([chat_title, chat_link, text + caption, post_link, reactions])


files = os.listdir(temp_data_path)
df = pd.DataFrame()

for file in files:
    if 'ipynb' not in file:
        df_file = pd.read_csv(temp_data_path + fr'/{file}')
        df = pd.concat([df, df_file], ignore_index=True)

data_path = os.getenv('data_path')
dataset_name = os.getenv('dataset_name')

df.to_csv(f'{data_path}/{dataset_name}.csv', encoding='utf-8', index=False)