#!/usr/bin/env python
# Work with Python 3.6
# Cool
import random
import asyncio
import aiohttp
import json
import requests
from discord import Game
from discord.ext.commands import Bot

from DiscordSQLLite import find_discord_id_balance, adduser
from DiscordSQLLite import find_user_exists

BOT_PREFIX = ("?", "!")
TOKEN = "NjExNzU5NDk2Njc4ODY2OTY5.XVYfiA.9NJG-8QdvgckcnHxNZzuVW-PqIg"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Pong"))
    print("Logged in as " + client.user.name)


@client.command()
async def roll():
    player_roll = random.randrange(1, 7)
    computer_roll = random.randrange(1, 7)
    if player_roll > computer_roll:
        response = ("Player rolled: " + str(player_roll) + ". Computer rolled: " + str(
            computer_roll) + ". Player Wins! Hurrah!")
    elif computer_roll > player_roll:
        response = ("Player rolled: " + str(player_roll) + ". Computer rolled: " + str(
            computer_roll) + ". Computer Wins. :(")
    else:
        response = ("It was a tie!")
    await client.say(response)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['temp']['humidity'][''])


@client.command()
async def weather(zip):
    # api_token = 'd32530925739e01e4a83912ce05d8209'
    def get_weather():
        url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip,
                                                                                                    'd32530925739e01e4a83912ce05d8209')
        r = requests.get(url)
        return r.json()

    x = get_weather()
    y = x["main"]
    current_temp = y["temp"]
    current_temp_f = 9 / 5 * current_temp + 32
    await client.say("Current Temp is: " + str(current_temp_f))


userbalances = [["Marley#4366"], [101]]


@client.command(name='userbalance',
                description="Provides users with their accounts balance.",
                brief="Account Balances",
                aliases=['ub', 'mybalance', 'balance'],
                pass_context=True)
async def user_balance(context):
    name = str(context.message.author)
    if find_user_exists():
        await client.say(name + " your balance is: " + find_discord_id_balance(name))
    else:
        await client.say(name + " you do not have an account. Please use !new_account")

@client.command(name='addbalance',
                description='adds 10 credits to balance.',
                brief='Adds 10 Credits',
                aliases=['ab'],
                pass_context=True)


async def add_account(context):
    name = str(context.message.author)
    if find_user_exists():
        await client.say(name + " you already have an account. Try !userbalance")
    else:
        adduser(name)


async def add_balance(context):
    name = str(context.message.author)
    if name in userbalances[0]:
        i = userbalances[0].index(name)
        userbalances[1][i] = userbalances[1][i] + 10
        await client.say(name + " your balance is: " + str(userbalances[1][i]))
        return userbalances
    else:
        await client.say(name + " you do not have an open account, please use !ub to create one.")
        return userbalances


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(10)


client.loop.create_task(list_servers())
client.run(TOKEN)
