#!/usr/bin/python3
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import errors
from discord.utils import get
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="_")
@bot.event
async def on_ready():
	print(f'{bot.user.name} connected')
	game = discord.Game("killing jarvis because fun")
	await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command(name="hi")
async def hi(ctx):
	await ctx.send("""
Hi, this is Ultron - the one and only bot that helps maintain order and peace in this discord server. If you're a new admin wondering what to do, I can:
	- start a new contest*
	- say hi
	- innerpeace
	- scream
	- say random things
	- delete rude messages*
	`*`  the `*`s mean that I didn't add those features yet, sorry - Necro
	""")

# Scream
# invoke: _scream
# expected output: AAAAAAAAHHHHH
@bot.command(name="scream")
async def scream(ctx):
	await ctx.send("AAAAAAAAHHHHH")

# Quieting
# invoke: _innerpeace
# output: {slowmode: 30s} everybody calm down
@bot.command(name="innerpeace")
async def innerpeace(ctx):
	# TODO: activate slow mode
	await ctx.send("inner peeeeeeaaaaaacceee")

# Anti-swear
@bot.command(name="eyebleach", count=5)
async def eyebleach(ctx):
	# TODO: delete {count} messages
	await ctx.send("BLEAACCHHH")
#	await ctx.send({kitten images})


@bot.command(name="join")
async def join(ctx, clan: str):
	member = ctx.message.author
	# get clan options
	clan_names = []
	clans = []
	clan_links = {}
	for r in ctx.guild.roles:
		if r.name.startswith("[Clan]"):
			clan_links[r.name.replace("[Clan]", "").replace(" ", "").lower()] = r
			clans.append(r)
			clan_names.append(r.name)
	
	print("[COMMAND]", member.name, "wants to join", clan)
	# check if it's in the options
	if clan not in clan_links.keys():
		print("[INFO]", member.name, "did not choose a valid clan")
		await ctx.send("shut up that's not a valid clan")
		# tell them the valid options
		msg = "valid clans are:"
		for r in clan_names:
			msg += " " + r
		await ctx.send(msg)
		return

	# check if they already have that clan
	if clan_links[clan] in member.roles:
		await ctx.send("omae ou wa, mou shindeiru")
		print("[INFO]", member.name, "already belonged to that clan")
		return
	
	# check if they are already registered to another clan
	for i in clans:
		if i in member.roles:
			await ctx.send("operation lotus has been aborted")
			print("[INFO]", member.name, "was trying to join a clan while being in one")
			return

	# add new role list
	new_roles = member.roles
	new_roles.append(clan_links[clan])
	print("[INFO] passed all the guard checks, continuing..")
	try:
		# update the member's list of roles
		await member.edit(roles=new_roles)
		await ctx.send(member.name+", your clan has been registered - check your roles now.")
	except Exception as e:
		print("[ERROR] in join command:", str(e))
		await ctx.send("internal error - tell necro he sucks")
		await ctx.send("tell him that it's a " + str(type(e)))

# Leave a clan
# Invoke: _leave
# output: {member} has now left the clan {clan}.
@bot.command(name="leave")
async def leave(ctx):
	# get the user who invoked the command
	member = ctx.message.author
	# get a list of the clans (for validation)	
	clans_list = [i for i in ctx.guild.roles if i.name.startswith("[Clan]")]
	# check their roles if they have a clan
	has_clans_in_role_list = [i for i in member.roles if i in clans_list]
	if has_clans_in_role_list is []:
		# tell the user they don't have a clan
		await ctx.send("are you dumb, stupid or dumb?")
		return

	print("[COMMAND]", member.name, "is leaving", has_clans_in_role_list[0].name)
	
	
	# create a list of the member's roles without any mention of the clan
	new_roles = member.roles
	new_roles.remove(has_clans_in_role_list[0])
	
	# update
	try:
		await member.edit(roles=new_roles)
		await ctx.send(member.name+" has now left "+has_clans_in_role_list[0].name)
	except Exception as e:
		print("[ERROR] in leave command:", str(e))
		await ctx.send("internal error - tell necro he sucks")
		await ctx.send("tell him that it's a " + str(type(e)))

# Show non-lurkers and bots
# invoke: _active
# output: {members} are active.
@bot.command(name="active")
async def active(ctx):
	print("[COMMAND]", "listing number of active members")
	active_members = 0
	for member in ctx.guild.members:
		active = True
		for role in member.roles:
			if "Lurker" == role.name:
				active = False
			elif "Robots" == role.name:
				active = False
		if active:
			active_members += 1
	await ctx.send("We have around "+ str(active_members) + " members.")

bot.run(TOKEN)
