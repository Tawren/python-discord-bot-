import discord
from discord import emoji
from discord import reaction
from discord import embeds
from discord.activity import Game
from discord.ext import commands, tasks
import asyncio
import random
import os
import youtube_dl
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType

prefix = '.'
bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), description = "Dev By Tawren", help_command=None)

status = [".help",
        "bot par Tawren",
        "discord server soon"]
ownerid = [841341738358669353]

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# quand le bot est prêt on affiche "print"
@bot.event
async def on_ready():
    print("BOT ON")
    changeStatus.start()

@bot.command()
async def start(ctx, secondes = 5):
    changeStatus.change_interval(seconds = secondes)

@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(activity = game)

# les erreurs
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("**Cette commande n'existe pas.**")
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**Il manque un argument.**")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("**Vous n'avez pas les permissions pour faire cette commande.**")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("**Vous ne pouvez utilisez cette commande.**")
	if isinstance(error.original, discord.Forbidden):
		await ctx.send("**Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande**")


# --------------------
# Les commandes
# --------------------

#---------
# Salut
#---------

# A REFAIRE
@bot.command()
async def salut(ctx, user : discord.User):
    embed = discord.Embed(title =f"{ctx.author.name} vous salut {user.mention}", description ="", color=0xfccf03)
    await ctx.send(embed = embed)

# erreur si il manque un argument
@salut.error
async def coucou_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("**La commande salut prend en paramètre une mention.**")
		await ctx.send("**Veuillez réessayer.**")

#---------------
# Serveurinfo
#---------------

# FAIRE L'EMBED
@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    number_textchannel = len(server.text_channels)
    number_voicechannel = len(server.voice_channels)
    serveurdescription = server.description
    number_members = server.member_count
    serveurname = server.name
    message = f"Le serveur **{serveurname}** contient *{number_members}* membres. \n La description du serveur est {serveurdescription}. \n Ce serveur possède {number_textchannel} salons textuels et {number_voicechannel} salons vocaux. "
    await ctx.send(message)

#-------------
# cmds/help
#-------------

# Rajouter les commandes au fur et à mesure
@bot.command()
async def help(ctx):
	embed = discord.Embed(title = "**Help**", description = "Voici toute les commandes implémenter pour le moment.", color=0xfccf03)
	embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/1739_CMD.png")
	embed.add_field(name = "__Les commandes utilitaire/fun :__", value = ":arrow_down:", inline = False)

	embed.add_field(name = "**help**", value = "Permet de montrer ce message", inline = False)
	embed.add_field(name = "**salut [@mention]**", value = "Permet de saluer la personne mentionné.", inline = False)
	embed.add_field(name = "**serveurinfo**", value = "Donne des informations sur le serveur.", inline = False)
	embed.add_field(name = "**clear [nombre]**", value = "Permet de supprimer le nombre de message indiqué.", inline = False)
	embed.add_field(name = "**say [ce que vous voulez dire]**", value = "Le bot répètera ce que vous avez mis après le say.", inline = False)
	embed.add_field(name = "**inviteme**", value = "Envois un message pour m'inviter dans vos serveurs", inline=False)
	embed.add_field(name = "**invites**", value = "Envois un message avec le nombre de vos invitation", inline=False)
	embed.add_field(name = "**userinfo (@mention)**", value = "Permet de montrer les information de la personne mentionnée", inline=False)
	embed.add_field(name = "**botinfo**", value = "Affiche des information sur le bot", inline = False)
	embed.add_field(name = "**ping**", value = "Affiche le ping du bot", inline = False)
	embed.add_field(name = "**botservers**", value = "Affiche le nombre de serveur sur lesquel je suis", inline = False)
	embed.add_field(name = "**avatar [mention]**", value = "Affiche le photo de profil de la personne mentionné(e)", inline = False)

	embed.add_field(name = "__Les commandes de modération :__", value = ":arrow_down:", inline = False)

	embed.add_field(name = "**ban [@mention] (raison)**", value = "Permet de bannir la personne mentionné.", inline = False)
	embed.add_field(name = "**unban [@mention] (raison)**", value = "Permet de débannir la personne mentionné.", inline = False)

	embed.add_field(name = "**mute [@mention] (raison)**", value = "Permet de réduire au silence la personne mentioné.", inline=False)
	embed.add_field(name = "**unmute [@mention] [chiffre] [s, m, h, d] (raison)**", value = "Permet de redonner la voix à la personne mentioné.", inline=False)
	embed.add_field(name = "**tempmute [@mention] (raison)**", value = "Peret de réduire temporairement au silence la personne mentioné.", inline=False)

	embed.add_field(name = "**kick [@mention] (raison)**", value = "Permet de kick la personne mentionné.", inline = False)

	embed.add_field(name = "**lock**", value = "Vérrouille un salon", inline = False)
	embed.add_field(name = "**unlock**", value = "Dévérouille un salon", inline = False)


	embed.set_footer(text =f"help demandé par {ctx.author}")
	await ctx.send(embed = embed)

#-------
# say
#-------

# Faire dire au bot ce que l'on veux
@bot.command()
@commands.has_permissions(administrator = True)
async def say(ctx, *texte):
    await ctx.message.delete()
    await ctx.send(" ".join(texte))

# Erreur si il manque un argument
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande say prend en paramètre du texte.")
        await ctx.send("Veuillez réessayer.")

#------------
# analyser
#------------

# C'est juste un embed fun qui envoit un résultat aléatoire

#--------
# Ping
#--------

# Affiche le ping du bot
@bot.command(name="ping")
async def ping(ctx: commands.Context):
    embed = discord.Embed(title =f":ping_pong:Pong ! {round(bot.latency * 1000)}ms", description ="", color=0x009E09)
    await ctx.send(embed = embed)

#--------
# Clear
#--------

# Clear, Supprime le nombre de message voulu puis supprime le message de confirmation au bout de 5s
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in messages:
        await message.delete()
    await ctx.send(f"**{nombre} messages ont été supprimé.**")   
    await asyncio.sleep(5)
    aaa = await ctx.channel.history(limit = 1).flatten()
    for message in aaa:
        await message.delete()

#----------------------------
# Mute/tempmute/unmute
#----------------------------

# Tempmute, Membre mention + chiffre + time
@bot.command()
@commands.has_permissions(administrator = True)
async def tempmute(ctx, member: discord.Member, time: int, d, reason="Aucune"):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)

            embed = discord.Embed(title="Mute !", description=f"{member.mention} à été tempmute ", colour=discord.Colour.red())
            embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/1558_muted.gif")
            embed.add_field(name="raison:", value=reason, inline=False)
            embed.add_field(name="temps restant du mute :", value=f"{time}{d}", inline=False)
            embed.set_footer(text = "Bot par adan_")
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="unmute (temp) ", description=f"unmute -{member.mention} ", colour=discord.Colour.red())
            embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/4991-unmute.png")
            embed.set_footer(text = "Bot par adan_")
            await ctx.send(embed=embed)

            return

# Création du rôle : "Muted"
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des personne.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

# Mute, donne le rôle mute à membrer mention
@bot.command()
@commands.has_permissions(administrator = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = "**Mute**", description = "Un membre a été mute", color=0xFF0000)
    embed.add_field(name = "__Raison__", value = reason, inline = False)
    embed.add_field(name = "__Membre__", value = member.mention, inline = False)
    embed.set_footer(text = "Bot par adan_")

    await ctx.send(embed = embed)

# Erreur si il manque un argument
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande mute prend en paramètre une mention.")
        await ctx.send("Veuillez réessayer.")

# Unmute, enleve le rôle muted et envoit l'embed
@bot.command()
@commands.has_permissions(administrator = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = "**Unmute**", description = "Un membre a été unmute", color=0xFF0000)
    embed.add_field(name = "__Raison__", value = reason, inline = False)
    embed.add_field(name = "__Membre__", value = member.mention, inline = False)
    embed.set_footer(text = "Bot par adan_")

    await ctx.send(embed = embed)

# Erreur, si il manque un argument
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("La commande unmute prend en paramètre une mention.")
        await ctx.send("Veuillez réessayer.")

#----------------------
# Tempban/ban/unban
#----------------------

# Banni member mention
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason = "Aucune raison n'a été donné"):
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "Un membre à été banni !", color=0xff0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url,)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/9005-abanhammer.gif")
    embed.add_field(name = "Membre banni", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Bot par adan_")

    await ctx.send(embed = embed)

# Unban
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user, reason = reason)

#--------
# Warn
#--------

# Warn A FAIRE MARCHER
@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, server, member:discord.Member, *, raison = None):
    user = member.mention
    serveurnom = server.name
    embed = discord.Embed(title="Warn : ", color=0xf40000)
    embed.add_field(name="Warn : ", value=f'Raison : {raison}', inline=False)
    embed.add_field(name="User warn: ", value=f'{member.mention}', inline=False)
    embed.add_field(name="Warn par : ", value=f'{ctx.author}', inline=False)
    embed.set_footer(text = "Bot par adan_")
    
    await user.send(f'Vous avez été warn sur le serveur {serveurnom} pour **{raison}**!')
    await ctx.send(embed=embed)

#--------
# Kick
#--------

# Kick
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, reason = "Aucune raison n'a été donné"):
    await ctx.guild.kick(user, reason = reason)
    embed = discord.Embed(title = "**Kick**", description = "Un membre à été kick !", color=0xff0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url,)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/7783-discordkickicon.png")
    embed.add_field(name = "Membre kick", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Bot par adan_")

    await ctx.send(embed = embed)

#-----------------
# AVATAR
#-----------------

@bot.command
async def avatar(ctx, member = discord.Member == None):
	if member == None:
		member = ctx.author


	memberAvatar = member.avatar_url

	avaEmbed = discord.Embed(title = f"{member.name}'s avatar")
	avaEmbed.set_image(url = memberAvatar)

	await ctx.send(embed = avaEmbed)

#-----------------
# 
#-----------------

@bot.command()
async def userinfo(ctx, *, user: discord.User = None):
    if user is None:
        user = ctx.author
    voice_state = None if not user.voice else user.voice.channel
    date_format = "%a %d %b %Y %H:%M "
    if isinstance(user, discord.Member):
                role = user.top_role.name
                if role == "@everyone":
                    role = "N/A"
    embed = discord.Embed(color=0xfccf03, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="A rejoint", value=user.joined_at.strftime(date_format), inline=False)
    embed.add_field(name="Création du compte", value=user.created_at.strftime(date_format), inline=False)
    embed.add_field(name='Surnom', value=user.nick, inline=True)
    embed.add_field(name='Status', value=user.status, inline=True)   
    embed.add_field(name='Jeux', value=user.activity, inline=True)
    embed.add_field(name='En vocal', value=voice_state, inline=True)
    embed.add_field(name='Plus au rôle', value=role, inline=True)
    embed.set_footer(text='ID: ' + str(user.id))
    
    await ctx.send(embed=embed)

#--------------------
# Botservers/botinfo
#--------------------

@bot.command()
async def botservers(ctx):
    embed = discord.Embed(title ="**Je suis sur __" + str(len(bot.guilds)) + "__ serveurs**", description ="", color=0xfccf03)

    await ctx.send(embed = embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(title = "__Nom du bot__ : ", color=0xfccf03)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name = "__ID du bot__ : ", value = bot.user.id, inline=False)
    embed.add_field(name = "Créateur du bot : ", value = "Tawren", inline=False)
    embed.set_footer(text =f"botinfo demandé par {ctx.author}")

    await ctx.send(embed = embed)

#---------------
# Lock/Unlock
#---------------

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    perms = ctx.channel.overwrites_for(ctx.guild.default_role)
    perms.send_messages=False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
    embed = discord.Embed(title = ":lock:Lock", description = "Ce channel est vérouillé", color=0xff0000)
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    perms = ctx.channel.overwrites_for(ctx.guild.default_role)
    perms.send_messages=True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)
    embed = discord.Embed(title = ":unlock:Unlock", description = "Ce channel est dévérouillé", color=0xff0000)
    await ctx.send(embed = embed)

bot.run("bottoken")