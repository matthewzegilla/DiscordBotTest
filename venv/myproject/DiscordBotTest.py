#!/usr/bin/env python
# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import requests
from discord import Game
from discord.ext.commands import Bot
from DiscordSQLLite import find_discord_id_balance, adduser, find_user_exists, add_to_balance


BOT_PREFIX = ("?", "!")
TOKEN = "NjExNzU5NDk2Njc4ODY2OTY5.XVYfiA.9NJG-8QdvgckcnHxNZzuVW-PqIg"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')


@client.command(name='help_me',
                description='lists commands',
                aliases=['commands', 'readme'],
                pass_context=False)
async def help_me():
    commands = """  
                    
!roll           -   plays a simple dice game.
!bitcoin        -   displays the price of bitcoin in USD.
!weather (zip)  -   displays temperature at zip code entered, don't put ( ).
!userbalance    -   checks your credit balance.
!addaccount     -   makes you a credit account if you are a new user.
                                                                                                    """
    await client.say(commands)


@client.command(name='roll',
                description="plays a dice game",
                brief="dice",
                aliases=['rolldice'],
                pass_context=True)
async def roll(context):
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


@client.command(name='bitcoin',
                description='find the price of btc/usd',
                brief='btc price',
                aliases=['btc'],
                pass_context=False)
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        btc_price = response['bpi']['USD']['rate']
        await client.say("Bitcoin price is: $" + btc_price)


@client.command(name='weather',
                description='finds the temperature of a zip code.',
                pass_context=True)
async def weather(context, zip):
    api_token = 'd32530925739e01e4a83912ce05d8209'
    def get_weather():
        url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=metric&appid={}".format(zip,api_token)
        r = requests.get(url)
        return r.json()

    name = str(context.message.author)
    w = get_weather()
    w_main = w["main"]
    current_temp = w_main["temp"]
    current_temp_f = round(9 / 5 * current_temp + 32,1)
    await client.say(name + ", current temp is: " + str(current_temp_f) + "° in " + str(zip))


@client.command(name='userbalance',
                description="Provides users with their accounts balance.",
                brief="Account Balances",
                aliases=['ub', 'mybalance', 'balance'],
                pass_context=True)
async def user_balance(context):
    name = str(context.message.author)
    if find_user_exists(name):
        await client.say(name + ", your balance is: " + str(find_discord_id_balance(name)))
    else:
        await client.say(name + ", you do not have an account. Please use !addaccount")


@client.command(name='addaccount',
                description='Adds a new user to the database if they dont exist',
                aliases=['newaccount'],
                pass_context=True)
async def add_account(context):
    name = str(context.message.author)
    if find_user_exists(name):
        await client.say(name + ", you already have an account. Try !userbalance")
    else:
        adduser(name)
        await client.say(name + ", your account has been created. have fun!")

@client.command(name='addbalance',
                description='Adds money to a users account',
                aliases=['addmoney','ab'],
                pass_context=True)
async def add_balance(context, ammount):
    name = str(context.message.author)
    int_ammount = int(ammount)
    if find_user_exists(name):
        add_to_balance(name, int_ammount)
        await client.say(name + " " + ammount + " credits have been added to your account. Your new total is: " +
                                                                                    str(find_discord_id_balance(name)))
    else:
        await client.say(name + ", I cannot find an account for you. Try !addaccount")


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
