token = "TON TOKEN ICI"
version = "Version 1.0"
name = "Xira-Bot"

import discord
import aiofiles
import random
import asyncio
import json
from discord.ext import commands
intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "!", help_command=None, intents=intents)
bot.welcome_channels = {}
bot.goodbye_channels = {}

@bot.event
async def on_ready():
    print("Bot lancé avec succès ! - " + name)
    await bot.change_presence(activity=discord.Game(name="!help - " + version))
    for file in ["welcome_channels.txt", "goodbye_channels.txt"]:
        async with aiofiles.open(file, mode="a") as temp:
            pass
        
    async with aiofiles.open("welcome_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.welcome_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))

    async with aiofiles.open("goodbye_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.goodbye_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))

    print("Toute les commandes on été chargé avec succès !")

#Event Bienvenue , Aurevoir

@bot.event
async def on_member_join(member):
    for guild_id in bot.welcome_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.welcome_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{message} {member.mention}")
            await bot.get_guild(guild_id).get_channel(channel_id).send("https://images-ext-1.discordapp.net/external/JHqojxkJGrAXq4-CD-vRzWJ-FwR4yRZTeiEhsXam5l0/https/images-ext-2.discordapp.net/external/vEuz33Pr9jxt3-sDda9mCAS9VwdJqZRNf06zZET5xnI/https/media.discordapp.net/attachments/590082530128953405/615816168174911509/welcome3d.gif")
            return

@bot.event
async def on_member_remove(member):
    for guild_id in bot.goodbye_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.goodbye_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{message} {member.mention}")
            return
            
#commande error

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Snif, j'ai chercher partout ! Mais j'ai l'impression que cette commande n'existe pas !")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument a ta commande.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu n'as pas les permissions pour faire cette commande...")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Oups vous ne pouvez utilisez cette commande.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande !")


#commande welcome et goodbye 

@bot.command()
async def set_welcome_channel(ctx, new_channel: discord.TextChannel=None, *, message=None):
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                bot.welcome_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"Le salon de bienvenue a été défini sur le channel : {channel.name} et le message de bienvenue est : {message}")
                await channel.send("Le message de bienvenue a bien été configuré sur ce channel !")
                
                async with aiofiles.open("welcome_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")

                return

        await ctx.channel.send("Impossible de trouver le channel indiquée.")

    else:
        await ctx.channel.send("Vous n'avez pas inclus le nom du channel/salon de bienvenue ou le message de bienvenue. ")

@bot.command()
async def set_goodbye_channel(ctx, new_channel: discord.TextChannel=None, *, message=None):
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                bot.goodbye_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"Le salons de aurevoir a été defini sur le channel : {channel.name} et le message de bienvenue est : {message}")
                await channel.send("Le message d'aurevoir a été défini sur ce channel !")
                
                async with aiofiles.open("goodbye_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")

                return

        await ctx.channel.send("Impossible de trouver le channel indiquée.")

    else:
        await ctx.channel.send("Vous n'avez pas inclus le nom du channel/salon du message d'au revoir ou d'un message d'au revoir.")

#help
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="help/aide" , description="Mon prefix est `!`. \n Fait la commande `!statsbot` pour en savoir plus. \n Fait la commande `!invite` pour invité le bot sur ton serveur discord. \n Fait la commande `!maj` pour voir les nouvelles fonctionnalité ajouté sur le bot." , color=ctx.author.color)
    embed.add_field(name="Commande de modération/administration 👮‍♂️ :", value="``set_welcome_channel <#salons message> `` \n  ``set_goodbye_channel <#salons message> `` \n  ``clear <chiffre entre 1-100>`` \n ``sondage <texte>`` \n ``annonce <texte>``" , inline=False)
    embed.add_field(name="Commande Général 😀:", value="``suggest <texte>`` \n ``makeEmbed <titre description> `` \n ``say <texte> `` \n ``stats`` \n ``météo <ville>``" , inline=False )
    embed.add_field(name="Commande Fun 🤣:", value="``blague`` \n ``coucou`` \n ``kiss <utilisateur>`` \n ``mp`` \n ``chinese <texte> ``" , inline=False )
    embed.add_field(name="Générateur :gift: :", value="``nitro``" , inline=False )   
    embed.set_footer(text="Help • " + name)
    await ctx.send(embed = embed)
    

#commande stats

@bot.command()
async def stats(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    numberOfPerson = server.member_count
    numberOfEmoji = len(server.emojis)
    serverName = server.name
    serverId = server.id
    serverOwner = server.owner
    serverRegion = server.region
    serverIcon = server.icon_url
    serverRole = len(server.roles)
    embed = discord.Embed(title="**Voilà des informations sur le serveur  :**",color=ctx.author.color)



    embed.add_field(name="\nNom du serveur :", value=server.name, inline=False)
    embed.add_field(name="\nID :", value=server.id, inline=False)
    embed.add_field(name="\nRégion :", value=server.region, inline=False)
    embed.add_field(name="\nMembres :", value= server.member_count, inline=True)
    embed.add_field(name="\nTextuelles :", value=len(server.text_channels), inline=True)
    embed.add_field(name="\nVocaux :", value=len(server.voice_channels), inline=True)
    embed.add_field(name="\nNombre d'émojis :", value=len(server.emojis), inline=True)
    embed.add_field(name="\nNombre de rôles :", value=len(server.roles), inline=True)
    embed.set_thumbnail(url=server.icon_url)
    embed.set_footer(text=" \n informations serveurs • " + name)

    await ctx.send(embed=embed)

#commande statsbot

@bot.command()
async def statsbot(ctx):
    embed = discord.Embed(title=f"{ctx.message.author} voici les informations de Xira-Bot 🤖 " , description=f"Je suis dans {len(bot.guilds)} serveurs !" ,color=ctx.author.color)
    embed.add_field(name="Créateur 👑 : ", value="``Zeyox``", inline=True)

    await ctx.send(embed=embed)

#commande blague	

@bot.command()
async def blague(ctx):
    responses = ["Quel est l'animal le plus connecté ?  ||Le porc USB||",
                 "Monsieur et madame Tiole ont une fille. Comment s’appelle-t-elle ? ||Bess||",
                 "C’est l’histoire d’un mec qui rentre chez un antiquaire et qui dit Bonjour, quoi de neuf ? ",
                 "Que crie une lampe lorsqu’elle se fait agresser ? ||A l’aide ! (à les)||",
                 "Hier j’ai vu une mouche écrasée sur un mur. Elle devait voler super vite.",
                 "Qu’est qu’un cochon qui rit ? || Un porc tout gai. ||",
                 "Quel est le comble pour un rugbyman ? ||C’est de se faire plaquer par sa copine||",
                 "Qu’est-ce qu’un chameau à trois bosses ? ||Un chameau qui s’est cogné…||",
                 "Pourquoi l’idiot se frappe la tête sur le mur ? ||Parce que ça lui fait du bien quand il arrête.||",
                 "Pour ne plus puer de la gueule… *Faut-il arrêter de dire de la merde ?*",
                 "– Docteur, je ne suis pas malade. - Ca tombe bien, je ne suis pas docteur !",
                 "Quel animal peut lire l’avenir ? ||La poule de cristal !||",
                 "Une mouette mange un sandwich. Une autre arrive : On fait mouette-mouette ?",
                 "Qu’est-ce qu’un éléphant dit à un homme tout nu ? « Et tu arrives à attraper des cacahuètes avec ça ? »",
                 "Un jour, Dieu demanda à David de guetter -Et David guetta.",
                 "Comment appelle-t-on un indien qui regarde de la pornographie ? ||Un cochon d’inde.||",
                 "Quel est le repas préféré de Dracula ? ||Le croc monsieur !||",
                 "Comment fait-on pour savoir si on est atteint de la maladie de la vache folle ? ||C’est quand on commence à tuer les mouches avec sa queue.||",
                 "Qu’est ce qu’une baguette avec une boussole ? ||Du pain perdu||",
                 "Que dit Frodon devant sa maison ? C’est là que j’hobbit… *ref*",
                 "Qu’est-ce que 2 canards qui se battent? ||Un conflit de canard||",
                 "Les ciseaux à bois, les chiens aussi.",
                 "Si deux sourds se battent, ca doit ||être sûrement un malentendu.||",
                 "Qu’est-ce qui n’est pas un steak ? ||Une pastèque||",
                 "Un piano à un autre : « Hey, ça va ? » L’autre : « Non, j’ai mal au do ! »",
                 "A quoi servent les archipels ? ||A faire des archi-trous !||",
                 "Comment appelle-t-on un chat tout-terrain ? ||Un Cat-cat||",
                 "Quel est le comble pour un policier ? ||De manger des amendes !||",
                 "Que fait une fraise sur un cheval ? ||Tagada Tagada Tagada||",
                 "C’est quoi le fruit préféré des militaires ? ||La grenad||",
                 "Comment appelle-t-on une personne agréable à Paris ? ||Un touriste.||",
                 "C’est l’histoire d’une girafe qui va dans un bar, pour boire un coup",
                 "Dans quel parc les gens tremblent ?  ||Au parkinson||",
                 "40% des accidents sont provoqués par l’alcool… Donc, 60% des accidents sont provoqués par des buveurs d’eau. C’est énorme !",
                 "Qu’est-ce qu’un nain qui fait du tir à l’arc ? ||Un Indien||",
                 "Qui s’occupe de la décoration à l’Elysée ? ||Le ministère de l’intérieur||",
                 "Où se cache Mozart ? ||Dans le frigo….Car Mozzarella…||",
                 "Pourquoi les indiens mettent-ils la main au dessus des yeux pour regarder au loin ? ||Parce que s’ils mettent la main devant les yeux, ils ne verraient plus rien.||",
                 "Moi je connait une chanson qui énervent les gens, Moi je connait une chanson qui énervent les gens, Moi je connait une chanson qui énervent les gens, ...",
                 "Ce matin, un calepin a tué un classeur",
                 "– Docteur, j’ai besoin de lunettes. – Oui certainement. Ici c’est une banque",
                 "Tu connais la blague du chauffeur de bus ? Moi non plus, j’étais à l’arrière…",
                 "Quelle est la différence entre tintin et milou ?  ||Milou n’a pas de chien…||",
                 "Que fait un crocodile lorsqu’il rencontre une crocodile ? ||Il l’accoste !||",
                 "Pourquoi un chasseur emmène-t-il son fusil aux toilettes ?  ||Pour tirer la chasse.||",
                 "Qu’est-ce qu’un nem avec des écouteurs ? ||Un NemP3…||",
                 "Deux puces vont se promener – On part à pied ou on prend un chien ?",
                 "Que font 2 squelettes le soir de leur mariage ? ||La nuit de noces||",
                 "Qu’est-ce qu’un chalumeau ?? ||C’est un drolumadaire à deux bosse !!||",
                 "Pourquoi les vieux font-ils des bains de boue? ||Pour s’habituer à la terre…||",
                 "Quel est le sport le plus silencieux ?  ||Le parachhhhhhuuuuutt !||",
                 "Pourquoi les français marchent sur les tuyaux d’arrosage ? ||Pour avoir de l’eau plate !||",
                 "Deux femmes discutent : »Mon mari, il est en or ! » – Le mien il est en tôle !",
                 "tu connais la blague du pouce ? elle est comme sa :thumbsup:",
                 "C’est l’histoire d’un pingouin qui respire par les fesses. Un jour il s’assoit, et il meurt…"]
    embed = discord.Embed(title=f"Blague aléatoire ``😊`` " , description=f"{random.choice(responses)}", color=ctx.author.color)
    embed.set_footer(text="Blague • " + name)
    caca = await ctx.send(embed=embed)
    await caca.add_reaction("\U0001F923")

#coucou

@bot.command()
async def coucou(ctx):
    responses = ["Salut !",
                 "Hey !",
                 "Coucou"]
    embed = discord.Embed(title=f"{random.choice(responses)} {ctx.message.author}", color=ctx.author.color)
    embed.set_footer(text="coucou • " + name)
    caca = await ctx.send(embed=embed)

#chinese

@bot.command()
async def chinese(ctx, *text):
	chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
	chineseText = []
	for word in text:
		for char in word:
			if char.isalpha():
				index = ord(char) - ord("a")
				transformed = chineseChar[index]
				chineseText.append(transformed)
			else:
				chineseText.append(char)
		chineseText.append(" ")
	await ctx.send("".join(chineseText))

#ping

@bot.command()
async def ping(ctx):

    embed = discord.Embed(title=" :ping_pong:  •  Pong !", description=f"{round(bot.latency * 1000)}ms", color=ctx.author.color)
    embed.set_footer(text="Ping • " + name)
    await ctx.send(embed=embed)

#commande sondage


@bot.command()
@commands.has_permissions(manage_messages=True)
async def sondage(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(title=":newspaper: Sondage", color=ctx.author.color)
    embed.add_field(name=f"{message}", value=":white_check_mark: Pour :x: Contre", inline=True)
    embed.set_footer(text=f"Sondage • Proposer par : {ctx.message.author}" )
    caca = await ctx.send(embed=embed)
    await caca.add_reaction("\U00002705")
    await caca.add_reaction("\U0000274C")

#commande suggest 

@bot.command()
async def suggest(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(title=":newspaper:Suggestion", color=ctx.author.color)
    embed.add_field(name=f"{message}", value=":white_check_mark: Pour :x: Contre \U0001F914 Bof", inline=True)
    embed.set_footer(text=f"Suggestion • Proposer par : {ctx.message.author}" )
    caca = await ctx.send(embed=embed)
    await caca.add_reaction("\U00002705")
    await caca.add_reaction("\U0001F914")
    await caca.add_reaction("\U0000274C")
    
#commande annonce
  
@bot.command()
@commands.has_permissions(manage_messages=True)
async def annonce(ctx , *, message):
    await ctx.message.delete()
    embed = discord.Embed(title="Annonce 🚨", color=ctx.author.color)
    embed.add_field(name=f" {message} " , value=" @everyone ", inline=True)
    embed.set_footer(text=f"Annonce • Proposer par : {ctx.message.author} ")
    await ctx.send(embed = embed)   
  
#commande say

@bot.command()
async def say(ctx, *, message):
	await ctx.send(f" {message} ")


#commande clear

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

#command MP

@bot.command()
async def mp(ctx):
    author = ctx.message.author
    embed = discord.Embed(title="Message en MP" , description=f'Message envoyé avec succès a {ctx.message.author}',color=ctx.author.color)
    await ctx.send(embed = embed)
    await author.send('Beh alors tu veux parlé avec moi ?')

#kiss 

@bot.command()
async def kiss(ctx, *, user : discord.User):
    embed = discord.Embed(title="Kiss ❤️" , description=f'``{ctx.message.author} a fait un bisous a {user}``' , color=ctx.author.color)
    embed.set_image(url="https://images-ext-1.discordapp.net/external/8YpN43gIiJQIzJjQfj62OKYGoyrwBWlnIOF0H2m3_80/https/media.giphy.com/media/wOtkVwroA6yzK/giphy.gif")
    await ctx.send(embed=embed)

#embed

@bot.command()
async def makeEmbed(ctx, title: str, *, message):
    embed = discord.Embed(title=title, description=message, color=ctx.author.color)
    embed.set_footer(text="Embed • " + name)
    await ctx.send(embed=embed)
  
#invite

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Lien d'invitation de " + name , description="https://discord.com/api/oauth2/authorize?client_id=821730871224172586&permissions=8&scope=bot" , color=ctx.author.color)
    embed.set_footer(text="Lien d'invitation • " + name)
    await ctx.send(embed=embed)

#commande MAJ

@bot.command()
async def maj(ctx):
    embed = discord.Embed(title="Dernières mises-à-jours - Version 1.0 😀 ",color=ctx.author.color)
    embed.add_field(name="1", value="Ajout des blagues 🤣" , inline=False)
    embed.add_field(name="2", value="Ajout des sondages 📰" , inline=False)
    embed.add_field(name="2", value="Ajout de la commande makeEmbed qui permet de faire un embed 💜" , inline=False)
    await ctx.send(embed=embed)

#commande Nitro 

@bot.command()
async def nitro(ctx):
    responses = ["http://discord.gift/PXmx2vin9Dpwfyot",
                 "http://discord.gift/Lb3JluAnxFWFR4ct",
                 "http://discord.gift/lSznbHYShes6qzOd",
                 "http://discord.gift/uqqj8lVNBSt6ao65",
                 "http://discord.gift/i5dULIwH48B4GijY",
                 "http://discord.gift/T4zK4ezhX8eAg50o",
                 "http://discord.gift/XSXbx6gqAkRiFyrW",
                 "http://discord.gift/8MzzksOwAIAQCj1B",
                 "http://discord.gift/QiuSZw1VKpTqY4Gm",
                 "http://discord.gift/KZAKkg4O6rs9pAcX",
                 "http://discord.gift/FJCOxH1B8Hi67c43",
                 "http://discord.gift/1BZveYRvydaktAoG",
                 "http://discord.gift/5NGA41TQS8w1sFU5",
                 "http://discord.gift/GDVYkelxtGTnU7l9",
                 "http://discord.gift/GM4JzjH2IzurgfEY"]
    author = ctx.message.author
    embed = discord.Embed(title=f"Check t'est MP le nitro t'a été envoyer ! {ctx.message.author} 🎁 ", color=ctx.author.color)
    embed.set_footer(text="nitro • " + name)
    await ctx.send(embed=embed)
    em = discord.Embed(title=f"{random.choice(responses)}" , description="Attention il faut avoir de la chance pour tomber sur un code valide ! " , color=ctx.author.color)
    await author.send(embed=em)


#commande météo

@bot.command()
async def météo(ctx, *, message):
    await ctx.send(f"Voici le temps actuel a {message}.")
    await ctx.send(f"https://api.cool-img-api.ml/weather-card?location={message}&background=https://aysdiscord.com/img/discord_dark.png")

bot.run(token)

# https://unicode.org/emoji/charts/full-emoji-list.html