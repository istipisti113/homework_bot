import discord
import asyncio
from months import month_days
import pickle
import dill
from discord.ext import commands
import threading
import time
import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "!", intents = intents)

esemenyek = list(map(lambda x: x.strip(), open("esemenyek.txt").readlines()))
guilds = set()

#@bot.command()
#async def ping(channel):
#    await channel.send("pong")

@bot.event
async def on_ready():
    print('Ready!')

@bot.event
async def on_message(message):
    guilds.add(message.guild)
    if message.author == "homework!8822":
        return
    else:
        if message.content[0] != "!": return
        print(f"{message.author} said '{message.content}' at {message.guild}:{message.channel}({message.channel.id})")
        if message.guild.name in ["public ip bot", "10D angol"]:
            match message.content.split()[0][1::] :
                case "ping" : 
                    print(f"{message.author} wants to be pinged")
                    await message.author.add_roles(list(filter(lambda x: x.name == "ping", message.guild.roles))[0])
                    await message.channel.send(f"{message.author} will receive notifications from now on!")
                case "remove" :
                    print(f"{message.author} does not want to be pinged")
                    await message.author.remove_roles(list(filter(lambda x: x.name == "ping", message.guild.roles))[0])
                    await message.channel.send(f"{message.author} will not receive notifications from now on!")
                    # print(message.guild.roles)
                case "házi":
                    print("new homework")
                    month = message.content.split()[1]
                    day = message.content.split()[2]
                    hazi = " ".join(message.content.split()[3::])
                    file = open("esemenyek.txt", "a")
                    file.write(f"{message.guild.name}%{month}%{day}%{hazi}\n")
                    file.close()
                # case "add_guild":
                #     # with open("guild", "wb") as outp:
                #     #     dill.dump(message.guild, outp)
                #     # check_for_homework()
                #     # dill.dump_module()
                case "h":
                    await check_for_homework()
                case "help" :
                    await message.channel.send(f"All command must start with '!' \nThe list of available commands: \n  !ping -- you will be granted the permission to view the channel the homework notification is being sent to\n  !remove -- removes you from that channel\n  !házi 'month' 'date' 'the actual homework' -- adds a new homework to the list.\n  !h -- makes a search for homework at that moment. Other than that there will be an automated one evety day at 7pm. \n\nThis will be available on my github at: www.github.com/istipisti113/homework_bot ")
                case _:
                    print(message.content.split()[0][1::])
        else:
            print(f"'{message.guild.name}'")


def sleeper():
    print("sleeper thread started, see you at 7!")
    while True:
        current_time = time.time()
        current_hour = time.localtime(current_time).tm_hour
        current_minute = time.localtime(current_time).tm_min
        current_second = time.localtime(current_time).tm_sec
        # print(current_hour, current_minute, current_second)
        sleeping_seconds = 60-current_second
        sleeping_minutes = 60-current_minute-1
        sleeping_hours = 0
        if current_hour > 19:
            hours_left = 24-current_hour
            sleeping_hours += hours_left+19-1
        else:
            sleeping_hours = 19-current_hour-2
        sleeping_seconds += 60*sleeping_minutes + 3600*sleeping_hours
        print(sleeping_seconds)
        asyncio.run(check_for_homework())
        time.sleep(sleeping_seconds)

async def check_for_homework():
        now = datetime.datetime.now()
        homeworks = list(map(lambda x: x.strip().split("%"), open("esemenyek.txt").readlines()))
        print(homeworks)
        #guild%month%day%hazi
        for i in homeworks:
            if len(i) < 4:
                continue

            date_in_days = datetime.datetime(2024, int(i[1]), int(i[2]))
                # date_in_days -= datetime.datetime(year=2024, month=0, day=1) # so that it checkes the day before and not on the same day
                # print(date_in_days-now)
            diff = date_in_days-now
            if diff.days < 2 and diff.days > -1:
                if len(guilds) == 0:
                    continue
                guild = list(filter(lambda x: x.name == i[0], guilds))[0]
                match guild.name:
                    case "public ip bot" :
                        await list(filter(lambda x: x.id == 1099788473189273640, guild.channels))[0].send(f"{i[3]}")
                    case "1.0.D" :
                        # THIS NEEDS TO BE UPDATED!!!
                        await list(filter(lambda x: x.id == 1099788473189273640, guild.channels))[0].send(f"{i[3]}")


checker_thread = threading.Thread(target=sleeper)
checker_thread.start()

key = open("../key.txt").readlines()[0].strip()
#print(f"key: \n\n\n\n\ni   asdfasfa sd {key}")
bot.run(key)
