import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='a!')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Streaming(name='discord.gg/ckFHCRC', url='https://twitch.tv/abdouplayz1'))
	print("Bot is ready.")

@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount + 1)

@client.command()
async def kick(ctx, member: discord.Member, *, reason='No reason given.'):
	await member.kick(reason=reason)
	await ctx.send("***Successfully kicked {}. {}***".format(member, reason))

@client.command()
async def ban(ctx, member: discord.Member, *, reason='No reason given.'):
	await member.ban(reason=reason)
	await ctx.send("***Successfully banned {}. {}***".format(member, reason))

@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split("#")

	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			return

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ.get('TOKEN'))
