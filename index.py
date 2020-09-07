import discord
import challonge
import asyncio 
from discord.ext import commands, tasks #This is for creating commands, used when creating bot instance. Import tasks is for the "now playing" option on discord.
from datetime import datetime
from itertools import cycle #This is also needed for the "now playing" option on discord. Look at the status variable. Cycles through.


#Discord instance variables below
client = commands.Bot(command_prefix = '.') 
status = cycle(['Follow my twitter @gunsinmyarea', 'https://www.twitch.tv/OCEPablo']) 

#Below, write your username on Challonge as well as your API Key. Your API key is located on your settings page. Currently synced 
my_username = 'OCEPablo'
my_api_key = 'nLkPiVktkmvcubNXufqhrJJj2AdcJ4AebL0UnuAl'


#This is for getting the CURRENT LOCAL date and time.
now = datetime.now() #This is for getting today's date and time.
dt_string = now.strftime("%d/%m/%Y %H:%M:%S") #Date time format


@client.event #Event means it's something for the bot
async def on_ready(): #When the bot is ready function
    change_status.start()
    print("Bot is ready.")
    #await client.change_presence(activity=discord.Streaming(name="Follow my stream!", url='https://www.twitch.tv/OCEPablo'))


#Cycling through the bots "in-game status", currently bugged.
@tasks.loop(seconds=10)
async def change_status():
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(next(name=status))) 


@client.command() #A command. The function name is the command name used on discord
async def ping(ctx): #test ping command, returns pong on the server
    await ctx.send('pong')
    await ctx.send(dt_string) #Current date and time formatted
    

@client.command() #Command for the challonge bot
async def ranbat(ctx):
    my_user = await challonge.get_user(my_username, my_api_key)
    my_tournaments = await my_user.get_tournaments()
    for t in my_tournaments:
        if t.notify_users_when_matches_open == True:
            await ctx.send((t.name, t.full_challonge_url, t.game_name, t.start_at, t.notify_users_when_matches_open))


client.run('NzE0MjY1NTcyMTgyOTgyNjY3.XssLVQ.cz3KlqpGEJ1zd24IC83BtYuXBK4')
