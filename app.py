import os
import random
import time
import json
import datetime
from random import randint
from pyfiglet import figlet_format
from flask import Flask, g, session, redirect, request, url_for, jsonify
from requests_oauthlib import OAuth2Session

OAUTH2_CLIENT_ID = '456608429843283998' #os.environ['OAUTH2_CLIENT_ID']
OAUTH2_CLIENT_SECRET = '03D26-iZchBxx5ncJxN6fjxJkP6k0x-g' #os.environ['OAUTH2_CLIENT_SECRET']
OAUTH2_REDIRECT_URI = 'http://128.1932.254.226:5000/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

quotes = [
        '"The death of one man is a tragedy. The death of millions is a statistic."',
        '"It is enough that the people know there was an election. The people who cast the votes decide nothing. The people who count the votes decide everything."',
        '"Death is the solution to all problems. No man - no problem."'
        '"The only real power comes out of a long rifle."',
        '"Education is a weapon, whose effect depends on who holds it in his hands and at whom it is aimed."',
        '"In the Soviet army it takes more courage to retreat than advance."',
        '"Gaiety is the most outstanding feature of the Soviet Union."',
        '"I trust no one, not even myself."',
        '"The Pope! How many divisions has _he_ got?"',
        '"BENIS"'
        ]

expandList = [
        'cunt',
        'fuck',
        'goddamn',
        'bitch',
        'whore',
        'slut',
        'fortnight',
        'fortnut',
        'fortnite',
        'mixed reality',
        'microsoft',
        'emac',
        'ruby'
        'webscale',
        'web scale',
        'windows',
        'dick'
        ]


import discord

TOKEN = 'NDU2NjA4NDI5ODQzMjgzOTk4.DgNcRw.EviOEVoX7Lwtb1oHcOp3RGzg5L8'


# 0 = none, 1 = lobby phase, 2 = in progress
gameStatus = 0 
host = None
players = [] 
spies = [] 
regulars = [] 
missionsAttempted = 0
missionsFailed = 0
missionsPassed = 0
leader = None
team = [] 
votes = [] 
teamStatus = 0
rejects = 0


spiesPerPlayers = [2, 2, 3, 3, 3, 4]
playersPerMission = [
        [2, 2, 2, 3],
        [3, 3, 3, 4],
        [2, 4, 3, 4],
        [3, 3, 4, 5],
        [3, 4, 4, 5]
        ]


client = discord.Client()
async def say(text, channel):
    global client
    await client.send_message(channel, text)

def gameEnd():
    global gameStatus
    global host
    global spies
    global regulars
    global missionsAttempted
    global missionsFailed
    global missionsPassed
    global leader
    global team
    global votes
    global teamStatus
    global rejects

    gameStatus = 0 # 0 = none, 1 = lobby phase, 2 = in progress
    host = None
    players = []
    spies = [] 
    regulars = [] 
    missionsAttempted = 0
    missionsFailed = 0
    missionsPassed = 0
    leader = None
    team = [] 
    votes = [] 
    teamStatus = 0
    rejects = 0

async def gameBegin():
    global gameStatus
    global host
    global spies
    global regulars
    global missionsAttempted
    global missionsFailed
    global missionsPassed
    global leader
    global team
    global votes
    global teamStatus
    global rejects

    randLeader = randint(0,len(players)-1)
    leader = players[randLeader]
    for p in players:
        regulars.append(p)

    totalSpies = spiesPerPlayers[len(players)-5]

    for x in range(0, totalSpies):
        randSpy = randint(0,len(regulars)-1)
        print(str(randSpy))
        spy = regulars[randSpy]
        print(str(spy))
        regulars.remove(spy)
        spies.append(spy)
    
    spyMessage = ''.join(str(e) for e in spies)

    for p in players:
        if p in spies:
            await say('You are a spy! Your partner(s) in crime are: ' + spyMessage, p)
            #client.send_message(p, 'You are a spy! Your partner(s) in crime are: ' + spyMessage)
        else:
            await say('You are part of the resistance!', p)
            #client.send_message(p, 'You are part of the resistance!')

def checkVotes():
    global gameStatus
    global host
    global spies
    global regulars
    global missionsAttempted
    global missionsFailed
    global missionsPassed
    global leader
    global team
    global votes
    global teamStatus
    global rejects

@client.event
async def on_message(message):
    global gameStatus
    global host
    global spies
    global regulars
    global missionsAttempted
    global missionsFailed
    global missionsPassed
    global leader
    global team
    global votes
    global teamStatus
    global rejects
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    print(message.content)
    #text = message.content.split(' ')[1]
    text = ' '.join(message.content.split()[1:])
    #text2 = ' '.join(message.content.split()[2:])

    message.content = message.content.lower()

    f = open('log.txt', 'a')
    curTime = datetime.datetime.utcnow().isoformat() + '|' + '{:30.30}'.format(message.author.name) + '|' + message.author.id + '|' + message.content + '\n'

    f.write(curTime)



    if(message.channel.id == '360125095043268608'):
        return
    if(message.channel.id == '364919001434030101'):
        return

    for word in expandList:
        if word in message.content:
            msg = 'Expand your vocabulary.'
            await client.send_message(message.channel, msg)
            break


    if message.content.startswith('_help'):
        msg = 'Commands: _help, _guidance, _big, _pig, _soviet, _avatar'
        await client.send_message(message.channel, msg)


    if message.content.startswith('_roll'):
        print('text: ' + text)
        sides = int(text)
        if sides:
            num = randint(1, sides)
            comment = ''
            if(num == 1 and sides != 1):
                comment = 'The universe has deathed you, have fun kiddo.'
            elif(num == sides):
                comment = 'Hot diggety dice-eyes, nice roll partner!'
            elif(num > (sides/2)):
                comment = 'Not bad.'
            elif(num <= (sides/2)):
                comment = 'Could be better.'
            msg = str(sides) + ' sided die result: `' + str(num) + '`\n' + comment
            await client.send_message(message.channel, msg)

    if message.content.startswith('_resist host'):
        if message.channel.type != discord.ChannelType.text:
            await client.send_message(message.channel, 'This must be in a guild channel.')
            print(message.channel.type.id)
            return
        if gameStatus != 0:
            await client.send_message(message.channel, 'A game is currently in progress.')
            return
        host = message.author
        players.append(message.author)
        votes.append(-1)
        gameStatus = 1
        await client.send_message(message.channel, 'A resistance lobby is now being hosted.')

    if message.content.startswith('_resist start'):
        if message.channel.type != discord.ChannelType.text:
            await client.send_message(message.channel, 'This must be in a guild channel.')
            return
        if gameStatus != 1:
            await client.send_message(message.channel, 'You are not hosting a lobby')
            return
        if message.author != host:
            await client.send_message(message.channel, 'You are not the host')
            return
        if len(players) < 5:
            await client.send_message(message.channel, 'You need at least 5 players to play.')
            return
            await client.send_message(message.channel, 'The game has begun')
        await gameBegin()
        
    if message.content.startswith('_resist close'):
        if message.channel.type != discord.ChannelType.text:
            await client.send_message(message.channel, 'This must be in a guild channel.')
            return
        if message.author != host:
            await client.send_message(message.channel, 'You are not the host.')
            return
        gameEnd()

    if message.content.startswith('_resist pick'):
        if message.channel.type != discord.ChannelType.private:
            await client.send_message(message.channel, 'This must be in a DM.')
            return 
        if message.author not in players:
            await say('You are not playing', message.channel)
            return
        if message.author != leader:
            await say('You are not the mission leader.', message.channel)
            return
        if len(agents) != 0:
            await say('Agents have already been assigned.', message.channel)
            return
        index = len(players) - 5
        if index > 2:
            index = 3;
        if len(message.mentions) != playersPerMission[missionsAttempted][index]:
            await say('You must assign exactly ' + playersPerMission[missionsAttempted][index] + ' agents.', message.channel)
            return
        for agent in message.mentions:
            agents.append(agent)

    if message.content.startswith('_resist approve'):
        if message.channel.type != discord.ChannelType.private:
            await client.send_message(message.channel, 'This must be in a DM.')
            return
        if message.author not in players:
            await say('You are not playing.', message.channel)
            return
        if teamStatus != 0:
            await say('Team must be forming.', message.channel)
            return
        index = players.index(message.author)
        votes[index] = 1
        checkVotes()

    if message.content.startswith('_resist reject'):
        if message.channel.type != discord.ChannelType.private:
            await client.send_message(message.channel, 'This must be in a DM.')
            return
        if message.author not in players:
            await say('You are not playing.', message.channel)
            return
        if teamStatus != 0:
            await say('Team must be forming.', message.channel)
            return
        index = players.index(message.author)
        votes[index] = 0
        checkVotes()

    if message.content.startswith('_resist pass'):
        if message.channel.type != discord.ChannelType.priate:
            await client.send_message(message.channel, 'This must be in a DM.')
            return
        if message.author not in players:
            await say('You are not playing.', message.channel)
            return
        if teamStatus != 1:
            await say('Team must be approved.', message.channel)
            return
        if message.author not in agents:
            await say('You are not on the team.', message.channel)
        index = players.index(message.author)
        votes[index] = 1
        checkVotes()

    if message.content.startswith('_resist fail'):
        if message.channel.type != discord.ChannelType.private:
            await client.send_message(message.channel, 'This must be in a DM.')
            return
        if message.author not in players:
            await say('You are not playing.', message.channel)
            return
        if teamStatus != 1:
            await say('Team must be approved.', message.channel)
            return
        if message.author not in agents:
            await say('You are not on the team.', message.channel)
        index = players.index(message.author)
        votes[index] = 0
        checkVotes()

    if message.content.startswith('_resist join'):
        if message.channel.type != discord.ChannelType.text:
            await client.send_message(message.channel, 'This must be in a guild channel.')
            return
        if len(players) >= 10:
            await client.end_message(message.channel, 'Game full.')
            return
        if message.author in players:
            await client.send_message(message.channel, 'You are already in this game.')
            return
        players.append(message.author)
        votes.append(-1)


    if message.content.startswith('_resist leave'):
        if message.channel.type != discord.ChannelType.text:
            await client.send_message(message.channel, 'This must be in a guild channel.')
            return
        if message.author not in players:
            await client.send_message(message.channel, 'You cannot leave a game you aren\'t in.')
            return
        
        if message.author == host:
            gameEnd()
        elif gameStatus == 1:
            players.remove(message.author)
            votes.pop(0)
        elif gameStatus == 2:
            gameEnd()
    
    if message.content.startswith('_resist players'):
        if message.channel.type != discord.ChannelType.text:
            await client.send_message(message.channel, 'This must be in a guild channel.')
            return
        msg = ''.join(str(e) for e in players)
        await client.send_message(message.channel, msg)



    if message.content.startswith('_guidance'):
        #msg = 'Hello {0.author.mention}'.format(message)
        msg = random.choice(quotes) 
        await client.send_message(message.channel, msg)
    '''
    if message.content.startswith('_death'):
        target = message.mentions
        if target:
            if target[0]:
                targ = target[0]
                currentTime = datetime.datetime.utcnow()
                delta 
                with open('death.json', 'r') as read_file:
                    data = json.load(read_file)
                    entry = data[message.author.id]
                    allow = True
                    if entry:
                        death = entry['death']
                        life = entry['life']
                        if death:
                            delta = (currentTime - death).days
                        else:
                            delta = (currentTime - life).days
                        if(delta < 1):
                            msg = 'You have to wait a whole day'
                        else:



                    


                
                msg = '{0.author.mention}'.format(message) + ' has ***DEATHED*** ' + targ.mention
                data = {}
                
                with open('death.json', 'w') as write_file:
                    json.dump(data, write_file)
                await client.send_message(message.channel, msg)
    '''


    if message.content.startswith('_big'):
        msg = '```' + figlet_format(text, width=160) + '```'
        await client.send_message(message.channel, msg)

    if message.content.startswith('_soviet'):
        #msg = '`This message is from the capitalist pigs at OSU:`\n\n' + text
        msg = '`Capitalist pig` <' + message.author.name + '> ' + text
        await client.send_message(client.get_channel('456665509555994624'), msg)
    
    if message.content.startswith('_pig'):
        #msg = '`This message is from the soviet scum in the Clubhaus:`\n\n' + text
        msg = '`Soviet scum` <' + message.author.name + '> ' + text 
        await client.send_message(client.get_channel('456716843407638529'), msg)

    if message.content.startswith('_avatar'):
        msg = message.mentions[0].avatar_url
        await client.send_message(message.channel, msg)

    if client.user in message.mentions:
        msg = 'Da'
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('vvvv')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='with capitalist pigs'))
    
    print('^^^^')

client.run(TOKEN)
if __name__ == '__main__':
   app.run()

