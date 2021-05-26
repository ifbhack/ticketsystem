#-------------#
#setup the bot#
#-------------#

import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)

#---------------#
#create an issue#
#---------------#


#1. read the command
#2. get the users info
#3. create the ticket based off that info
#4. send the ticket to the database