## Bot done by Sigma#4652 from Discord ##
## Any questions should go to me ##

import discord
import csv
from student import Student
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import random

client = discord.Client()
room_list = []
student_list = []
token = "insert-token"

@client.event
async def on_ready():
    global student_list
    fp = open('student-file.txt') # Open file on read mode
    lines = fp.read().split("\n")
    for f in lines:
        name_status = f.split(" ")
        name = "{} {}".format(name_status[0],name_status[1])
        student_list.append(Student(name, name_status[2], name_status[3]))
    await client.change_presence(game=discord.Game(name='Trial Music!'))
    print("On")

@client.event
async def on_message(message):
    global room_list
    global student_list
    if message.author == client.user:
        return

    if message.content.startswith('!sendto'):
        if discord.utils.get(message.author.roles, name="Admin") is not None:
            split_channel = message.content[message.content.find("(")+1:message.content.find(")")]
            split_message = message.content[message.content.find("[")+1:message.content.find("]")]
            server_message = message.server
            channel_find = discord.utils.get(server_message.channels, name=split_channel)
            await client.send_message(channel_find, split_message)
    
    if message.content.startswith('!sendtoid'):
        if discord.utils.get(message.author.roles, name="Admin") is not None:
            split_id = message.content[message.content.find("(")+1:message.content.find(")")]
            split_message = message.content[message.content.find("[")+1:message.content.find("]")]
            await client.send_message(client.get_channel(split_id), split_message)

    if message.content.startswith('!ship'):
        random_member = random.choice(list(message.server.members))
        msg = "Your ship is: {} x {}".format(message.author.name,random_member.name)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!add'):
        if discord.utils.get(message.author.roles, name="Admin") is not None:
            room_list.append(message.content[message.content.find("(")+1:message.content.find(")")])
        else:
            await client.send_message(message.channel, "```You have no permission to do this!```")

    if message.content.startswith('!students'):
        if student_list:
            buffer = ""
            for student in student_list:
                name = student.getname()
                status = student.getstatus()
                talent = student.gettalent()
                buffer = "{}{} | {} | {}\n".format(buffer,name,status,talent)
            await client.send_message(message.channel, "```{}```".format(buffer))
        else:
            await client.send_message(message.channel, "No students available!")

    if message.content.startswith('!update'):
        if student_list:
            open('student-file.txt', 'w').close()
            f = open('student-file.txt', 'w')
            studs = []
            for i in range(len(student_list)):
                if i == len(student_list) - 1:
                    studs.append("{} {} {}".format(student_list[i].name,student_list[i].is_alive,student_list[i].talent))
                else:
                    studs.append("{} {} {}\n".format(student_list[i].name,student_list[i].is_alive,student_list[i].talent))
            f.writelines(studs)
            f.close()
        else:
            await client.send_message(message.channel, "No students available!")

    if message.content.startswith('!kill'):
        if student_list:
            split_student = message.content[message.content.find("(")+1:message.content.find(")")]
            for i in range(len(student_list)):
                if student_list[i].name == split_student:
                    student_list[i].kill()
                    await client.send_message(message.channel, "```{} has been killed!```".format(student_list[i].name))
                    break
        else:
            await client.send_message(message.channel, "No students available to kill!")

    if message.content.startswith('!getroom'):
        if discord.utils.get(message.author.roles, name="Admin") is not None:
            if room_list:
                random.shuffle(room_list)
                student_one = room_list.pop()
                student_two = room_list.pop()
                message_to_send = "```{} and {} are roommates now!```".format(student_one, student_two)
                await client.send_message(message.channel, message_to_send)
            else:
                await client.send_message(message.channel, "```There is no one else to pair!```")
        else:
            await client.send_message(message.channel, "```You have no permission to do this!```")

    if message.content.startswith('!nya'):
        split_nya = message.content[message.content.find("(")+1:message.content.find(")")]
        split_message = split_nya.replace(",", "").replace(".", "").split(" ")
        for i in range(len(split_message)):
            split_message[i] = "{}nya".format(split_message[i])
        await client.send_message(message.channel, "```{}```".format(" ".join(split_message)))

    if message.content.startswith('!announcement'):
        if discord.utils.get(message.author.roles, name="Admin") is not None:
            server_message = message.server
            place = message.content[message.content.find("(")+1:message.content.find(")")]
            mentions_c = discord.utils.get(message.server.roles, name="Student").mention
            announce = "{} *Bing Bong Ding Dong! Each student's handbook awakes to a notification from Monokuma.* \"A body has been discovered! Please make your way to {} as soon as possible!\"".format(mentions_c, place)
            channel_find = discord.utils.get(server_message.channels, name="ic-announcements")
            await client.send_message(channel_find, announce)
        else:
            await client.send_message(message.channel, "```You have no permission to do this!```")

    if message.content.startswith('!curse'):
        await client.send_message(message.channel, "```It's been 4 months since an RP has died with Sigma in it!```")

    if message.content.startswith('!public'):
        message_format = "```Name: {0}\nTalent: {1}\nHeight: {2}\nWeight: {3}\nBlood Type: {4}\nLikes: {6}\nDislikes: {7}\n"
        get_student = message.content[message.content.find("(")+1:message.content.find(")")]
        with open('student.csv', 'r',  encoding='utf8') as studentfile:
            spamreader = csv.reader(studentfile, delimiter=';')
            for row in spamreader:
                if row[0] == get_student:
                    public_backstory = row[5].replace("NEWLINE", "\n\n")
                    formatted_message = message_format.format(*row)
                    formatted_message = "{}Public Backstory: {}```".format(formatted_message, public_backstory)
                    await client.send_message(message.channel, formatted_message)  
        
        

        
async def background_loop():
    it_is = " *Bing Bong Ding Dong! Each student's handbook awakes to a notification from Monokuma.* \"It is " ##message
    and_the_current_weather_is = " and the current weather is "
    hours = ["8:00 AM", "13:00 PM", "18:00 PM", "23:00"] ##hours
    messages = ["Sunny", "Cloudy", "Snowy", "Foggy", "Rainy", "Windy", "Stormy"] ##temperatures
    await client.wait_until_ready()
    while not client.is_closed:
        file = open("time-weather.txt","r")
        current_loop = int(file.readlines(1)[0].strip('\n'))
        current_weather = file.readlines(2)[0]
        file.close()
        ##empty file
        open('time-weather.txt', 'w').close()
        server = client.get_server("473310045522755615") ##server that you're currently in
        channel = client.get_channel("475095909412241408") ##channel that you want to post in
        mentions = discord.utils.get(server.roles, name="Student").mention ##role you want to mention
        full_message = it_is + hours[current_loop%4] + and_the_current_weather_is +  current_weather
        current_loop +=1
        if current_loop == 7:
            current_loop = 0
            current_weather = random.choice(messages)
        lines = [str(current_loop)+ '\n', current_weather]
        f = open('time-weather.txt', 'w')
        f.writelines(lines)
        f.close()
        await client.send_message(channel, mentions + full_message + "\"")
        await asyncio.sleep(86400)



client.loop.create_task(background_loop())
client.run(token)
