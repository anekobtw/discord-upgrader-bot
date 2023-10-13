import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'We\'ve logged in as {client.user}')

@client.command()
async def improve_channels(ctx):
    """An asynchronous function that improves the names of channels in a guild by adding emojis or prompting for emoji suggestions."""
    guild = ctx.guild
    user = ctx.author

    if user.id != guild.owner_id:
        await ctx.send("You must be the owner of the guild to use this command.")
        return

    for channel in guild.channels:
        embed = discord.Embed(
            title="Suggest an emoji",
            description=f"Please send an emoji for the channel/category: `{channel.name}`",
            colour=0x7289da,
        )

        embed.set_footer(
            text="Upgrader bot",
            icon_url="https://media.discordapp.net/attachments/1160586888017612892/1160973085667770578/improve.png?ex=65369b71&is=65242671&hm=3c37ccd450bfd9c34ba5b3092451846a609f8829ddb5c1de8ff1b5a741356a28&=&width=625&height=625",
        )

        await ctx.send(embed=embed)

        try:
            suggestion = await client.wait_for(
                'message',
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel,
                timeout=25,
            )
        except asyncio.TimeoutError:
            await ctx.send("You took too long to provide a suggestion. Skipping this channel.")
            continue

        await channel.edit(name=f'〈{suggestion.content}〉{channel.name}')

    await ctx.send(embed=discord.Embed(title="Done!", colour=0x028000))

client.run('YOUR_BOT_TOKEN')
