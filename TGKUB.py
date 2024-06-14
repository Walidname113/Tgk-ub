# TGK UB

from datetime import datetime, timedelta
import json
import asyncio
import os
import random
import telethon
from telethon import TelegramClient, functions, events, utils, Button, types
import time
import sys
import requests
import subprocess
from telethon.tl.types import MessageEntityMention
import platform
import psutil
from telethon.tl.custom import Button
from telegraph import Telegraph
import tempfile
from io import BytesIO
import re
from concurrent.futures import ThreadPoolExecutor
from telethon.errors import FloodWaitError, MessageDeleteForbiddenError
import string
from telethon.tl.functions.messages import DeleteMessagesRequest
import shutil
import telethon.errors
from telethon.tl.functions.users import GetFullUserRequest

adminone = 6892267929
admintwo = 5396017152
ontag_flag = False

admin_ids = [adminone, admintwo]

def input_api_credentials():
    print("\033[95mВведите данные API пользователя.\033[0m")
    api_id = input("\033[95mAPI ID: \033[0m")
    api_hash = input("\033[95mAPI Hash: \033[0m")
    return api_id, api_hash

def save_session_credentials(api_id, api_hash):
    with open('sessioncash.txt', 'w') as file:
        file.write(f"{api_id}\n{api_hash}")

def load_session_credentials():
    try:
        with open('sessioncash.txt', 'r') as file:
            api_id = int(file.readline().strip())
            api_hash = file.readline().strip()
            return api_id, api_hash
    except FileNotFoundError:
        return None, None

api_id, api_hash = load_session_credentials()
if not api_id or not api_hash:
    api_id, api_hash = input_api_credentials()
    save_session_credentials(api_id, api_hash)

session_file = 'ocrestrinatedub.session'
client = TelegramClient(session_file, api_id, api_hash)
        
def load_interval():
    try:
        with open('interval.txt', 'r') as file:
            return float(file.read().strip())
    except Exception as e:
        print(f"Ошибка загрузки интервала: {e}")
        return 10.0

def save_interval(interval):
    with open('interval.txt', 'w') as file:
        file.write(str(interval))
        
def load_words():
    try:
        with open('words.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_words(words):
    with open('words.json', 'w') as file:
        json.dump(words, file)
        
def save_command_prefix(prefix):
    with open('command_prefix.txt', 'w') as file:
        file.write(prefix)

def load_command_prefix():
    try:
        with open('command_prefix.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        return "."

def load_tagger_status():
    try:
        with open('tagger_status.txt', 'r') as file:
            return file.readline().strip() == 'on'
    except FileNotFoundError:
        return False

def save_tagger_status(status):
    with open('tagger_status.txt', 'w') as file:
        file.write('on' if status else 'off')

async def send_random_message(username_or_user_id, shablon, chat_id, shapka):
    try:
        with open(shablon, 'r') as file:
            words = json.load(file)
    except Exception as e:
        print(f"Ошибка загрузки JSON файла: {e}")
        return
    
    while ontag_flag:
        word = random.choice(words)
        mention = await format_mention(username_or_user_id, shapka, word)
        await client.send_message(chat_id, mention, parse_mode='HTML')
        
        interval = load_interval()
        await asyncio.sleep(interval)

async def format_mention(username_or_user_id, shapka, word):
    try:
        user = await client.get_entity(username_or_user_id)
    except ValueError:
        try:
            user = await client.get_entity(int(username_or_user_id))
        except Exception as e:
            print(f"Ошибка при получении информации о пользователе: {e}")
            user = None
    except Exception as e:
        print(f"Ошибка при получении информации о пользователе: {e}")
        user = None
    
    if user:
        if isinstance(user, types.User):
            if user.username and shapka:
                mention = f"<a href='tg://openmessage?user_id={user.id}'>{shapka} | {word}</a>"
            else:
                mention = f"<a href='tg://openmessage?user_id={user.id}'>{word}</a>"
        elif isinstance(user, types.UserFull):
            mention = f"<a href='tg://openmessage?user_id={user.user.id}'>{word}</a>"
        else:
            mention = f"<a href='tg://openmessage?user_id={username_or_user_id}'>{word}</a>"
    else:
        mention = f"<a href='tg://openmessage?user_id={username_or_user_id}'>{word}</a>"
    
    return mention

@client.on(events.NewMessage(outgoing=True))
async def handle_commands(event):
    global ontag_flag
    command_prefix = load_command_prefix()
    command = event.message.message
    if not command.startswith(command_prefix):
        return
    command = command[len(command_prefix):].strip()
    chat_id = event.chat_id                       
    if command.startswith('setprefix'):
        if event.sender_id not in admin_ids:
            return await event.edit("<b><i>Нет прав доступа</i></b>", parse_mode='HTML')
        new_prefix = command[len('setprefix'):].strip()
        if new_prefix and len(new_prefix) == 1 and not new_prefix.isspace() and not new_prefix.isalpha():
            save_command_prefix(new_prefix)
            await event.delete()
            await event.client.send_message(event.to_id, f'<i><b>Префикс успешно изменён на {new_prefix}</b></i>', parse_mode='HTML')
        else:
            await event.message.edit('❌️ <i><b>Неверный формат префикса</b></i>', parse_mode='HTML')
            
    elif command.startswith('help'):
        if event.sender_id not in admin_ids:
            return await event.edit("<b><i>Нет прав доступа</i></b>", parse_mode='HTML')
        vidos = ["https://t.me/Mrakozniyfile/55", "https://t.me/Mrakozniyfile/37", "https://t.me/Mrakozniyfile/32", "https://t.me/Mrakozniyfile/50", "https://t.me/Mrakozniyfile/54", "https://t.me/Mrakozniyfile/56", "https://t.me/Mrakozniyfile/57"]
        vidos = list(filter(None, vidos))
        random_video = random.choice(vidos)
        await asyncio.sleep(0.1)
        prefix = load_command_prefix()
        user_id_or_username = "{user_id_or_username}"
        shablon = "{shablon}"
        chat_id = "{chat_id}"
        shapka = "{shapka}"
        await event.delete()
        await event.client.send_file(event.to_id, random_video, caption=f"<i><b>🎃 TGK USERBOT 🎃\n\n<code>{prefix}cid</code> — ПОЛУЧАЕТ АЙДИ КОНФЕРЕНЦИИ.\n<code>uid</code> — ПОЛУЧАЕТ ИНФУ О ЮЗЕРЕ ПО РЕПЛАЮ.\n<code>{prefix}ontag</code> — ВРУБАЕТ ТЕГГЕР. Аргументы: <code>{prefix}ontag</code> {user_id_or_username} {shablon} {chat_id}(этот аргумент использовать если вы используете команду не в нужном вам чате в котором нужно врубить теггер) {shapka}(необязательно)\n<code>{prefix}offtag</code> — ВЫРУБАЕТ ТЕГГЕР.\n<code>{prefix}setprefix</code> — МЕНЯЕТ ПРЕФИКС КОМАНДЫ НА УКАЗАННЫЙ ВАМИ.\n<code>{prefix}help</code> — ХЕЛПА.\n\nПРЕФИКС КОМАНДЫ — <code>{prefix}</code>.</b></i>", parse_mode='HTML', supports_streaming=True)
        
    elif command.startswith('cid'):
        if event.sender_id not in admin_ids:
            return await event.edit("<b><i>Нет прав доступа</i></b>", parse_mode='HTML')
        if event.is_private:
            await event.edit("❌️ <b><i>Эту команду можно использовать только в чатах.</b></i>", parse_mode='HTML')
            await asyncio.sleep(5)
            await event.delete()
        else:
            chat_id = event.chat_id 
            await event.delete()
            await event.client.send_message(event.to_id, f"<b><i>Conference ID:</b></i> <code>{chat_id}</code>", parse_mode='HTML')
            
    elif command.startswith('uid'):
        if event.sender_id not in admin_ids:
            return await event.edit("<b><i>Нет прав доступа</i></b>", parse_mode='HTML')    	
        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message:
                user_id = reply_message.sender_id
                user = await client.get_entity(user_id)
                username = user.username if user.username else "Юзернейм отсутствует"
                
                await event.edit(f"📋 <b>Информация о пользователе:</b>\n"
                                 f"🔹 <b>ID:</b> <code>{user_id}</code>\n"
                                 f"🔹 <b>Юзернейм:</b> @{username}" if user.username else "Юзернейм отсутствует",
                                 parse_mode='HTML')
            else:
                await event.edit("❌ <b>Не удалось получить информацию о пользователе.</b>", parse_mode='HTML')
        else:
            await event.edit("❌ <b>Используйте эту команду в ответ на сообщение.</b>", parse_mode='HTML')

    elif command.startswith('ontag'):
        if event.sender_id not in admin_ids:
            return await event.edit("<b><i>Нет прав доступа</i></b>", parse_mode='HTML')
        
        ontag_flag = True
        
        command_args = command.split(maxsplit=4)
        if len(command_args) < 3:
            await event.edit("❌ <i><b>Пожалуйста, укажите как минимум {username or user_id}, {shablon} и {chat_id} или используйте команду в чате.</i></b>", parse_mode='HTML')
            return

        username_or_user_id = command_args[1]
        shablon = command_args[2]
        
        if command_args[3].lstrip('-').isdigit():
            chat_id = int(command_args[3])
            shapka = command_args[4].strip() if len(command_args) > 4 else ""
        else:
            shapka = " ".join(command_args[3:])
        try:
            with open(shablon, 'r') as file:
                json.load(file)
        except FileNotFoundError:
            await event.edit(f"❌ <i><b>Файл {shablon} не найден.</b></i>", parse_mode='HTML')
            return
        except json.JSONDecodeError:
            await event.edit(f"❌ <i><b>Файл {shablon} содержит некорректные данные JSON.</b></i>", parse_mode='HTML')
            return
        except Exception as e:
            await event.edit(f"❌ <i><b>Ошибка загрузки JSON файла: {e}</b></i>", parse_mode='HTML')
            return
        
        await event.edit(f"<i><b>Сохранено как: {username_or_user_id} в чате {chat_id} с шаблоном {shablon}.</b></i>", parse_mode='HTML')
        await send_random_message(username_or_user_id, shablon, chat_id, shapka)

    elif command.startswith('offtag'):
        if event.sender_id not in admin_ids:
            return await event.edit("<b><i>Нет прав доступа</i></b>", parse_mode='HTML')

        ontag_flag = False
        await event.edit("<i><b>Отправка остановлена.</b></i>", parse_mode='HTML')
        
client.start()
print('\033[0;32mUserbot successfully launched!\033[0m')
client.run_until_disconnected()

# UB NH200C1 V1