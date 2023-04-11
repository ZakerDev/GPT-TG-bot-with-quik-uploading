import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json


openai.api_key='' #openai token
bot=Bot('')  #tg bot token
dp= Dispatcher(bot)

dp=Dispatcher(bot)


messages=[
    { "role":"system","content":"You are a bot Zaker."},
    {"role":"user","content":"I am a person who needs your help  "},
    {"role":"assistant","content":"How can I help you?"},
]
def distribute_text(messages, book_file):

    with open(book_file, 'r', encoding='utf-8') as file:
        book = file.read()
        tokens = book.split()
        chunk_size = 500
        for i in range(0, len(tokens), chunk_size):
            chunk = ' '.join(tokens[i:i+chunk_size])
            messages.append({"role": "user", "content": chunk})
            messages.append({"role": "system", "content": "I understand and have processed this information"})
    return messages


def update(messages, role ,content):
    messages.append({"role": role ,"content": content})
    return messages


@dp.message_handler()
async def send(message:types.Message):
    bot_info=await message.bot.get_me()

    update(messages,"user",message.text)
    await message.answer('Я думаю!')
    response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
    )
    await message.answer(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    distribute_text(messages, 'book.txt')
    executor.start_polling(dp,skip_updates=True)