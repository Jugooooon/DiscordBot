import discord
from discord import app_commands

import random
import matplotlib.pyplot as plt
import os
from PIL import Image

import openai
import BotToken

TOKEN = BotToken.token
openai.api_key = BotToken.OpenAI
RiotAPIKey = BotToken.RiotAPI

#初期設定
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Botのアクティビティを設定する
activity = discord.Game(name="Sample Bot")
client.activity = activity

@client.event
async def on_ready():
    print("Botが起動しました")
    await tree.sync()#スラッシュコマンドを同期

async def on_message(message: discord.Message):
    # メッセージ送信者がBot(自分を含む)だった場合は無視する
    if message.author.bot:
        return

    # メッセージが"hello"だった場合、"Hello!"と返信する
    if message.content == 'hello':
        await message.reply("Hello!")

#ChatGPT model gpt3
@tree.command(name="gpt",description="OpenAI-ChatGPT")
async def chatgpt_command(interaction: discord.Interaction, text: str):

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system", "content":"語尾に「にゃ」をつけて話してください" }, #content以降に設定を付けられる
            {"role":"user", "content":text },
        ],
        max_tokens = 1024,
        n = 1,
        temperature = 1,
    )

    chatgpt_response = response.choices[0].message.content
    await interaction.response.send_message(chatgpt_response)

#ChatGPT engine davinci
@tree.command(name="chat",description="OpenAI-davinci")
async def chatdvc_command(interaction: discord.Interaction, text: str):

    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = text,
        max_tokens = 1024,
        n = 1,
        temperature = 0.5,
    )

    chatgpt_response = response.choices[0].text.strip()
    await interaction.response.send_message(chatgpt_response)

@tree.command(name="rou", description="ルーレット。\n入力例:A B C")
async def roulette_command(interaction: discord.Interaction, text: str):

    try:
        Text = text.replace('　', ' ')
        Roulette_Title = Text.split()
        Roulette_Title_Len = len(Roulette_Title)
        N = random.randint(0, Roulette_Title_Len)
        await interaction.response.send_message(f'{Roulette_Title[N]}!!!')

        fig = plt.figure()
        mov = []
        #create PIE
        Value = 100 // Roulette_Title_Len
        Roulette_Value = [Value] * Roulette_Title_Len
        textprops={"weight":"bold", "color":"white", "size":"large"}
        for i in range(100):
            img = plt.pie(Roulette_Value, labels=Roulette_Title, labeldistance=0.3, textprops=textprops, counterclock=False, startangle=90 + (i * 10))
            plt.savefig(f'D:\Works\Discordbot\DiscordBot\pics\Roulette{i}.png')
            plt.clf()
        
        #Create Gif from imgs
        gif = []
        for i in range(100):
            img = Image.open(f'D:\Works\Discordbot\DiscordBot\pics\Roulette{i}.png')
            gif.append(img)

        gif[0].save('Roulette.gif',save_all=True, append_images=gif[1:], optimize=True, duration=0, loop=0)
        await interaction.channel.send(file=discord.File('D:\Works\Discordbot\DiscordBot\Roulette.gif'))
        
        #Delete All imgs
        img.close()
        
        for i in range(100):
            os.remove(f'D:\Works\Discordbot\DiscordBot\pics\Roulette{i}.png')
        os.remove('D:\Works\Discordbot\DiscordBot\Roulette.gif')
        


    except IndexError:
        await interaction.response.send_message('もう一度やり直してください。')
    



client.run(TOKEN)
