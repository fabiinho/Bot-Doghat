import asyncio
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class DogHatGroup(app_commands.Group):

    def __init__(self):
        super().__init__(name='doghat', description='Comandos do DogHat')

    @app_commands.command(name='ban', description='Bane um membro do servidor')
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        membro: discord.Member,
        motivo: str = 'Nenhum motivo fornecido',
    ):
        await membro.ban(reason=motivo)
        await interaction.response.send_message(
            'O usuario ' + membro.mention + ' foi banido!\nMotivo: ' + motivo
        )

    @app_commands.command(name='unban', description='Desbane um usuario pelo ID')
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction: discord.Interaction,
        id_usuario: str,
        motivo: str = 'Nenhum motivo fornecido',
    ):
        try:
            user = await bot.fetch_user(int(id_usuario))
            await interaction.guild.unban(user, reason=motivo)
            await interaction.response.send_message(
                'O usuario ' + user.name + ' (' + str(user.id) + ') foi desbanido!'
            )
        except discord.NotFound:
            await interaction.response.send_message(
                'Usuario nao encontrado ou nao esta banido.', ephemeral=True
            )
        except ValueError:
            await interaction.response.send_message(
                'Insira um ID valido contendo apenas numeros.', ephemeral=True
            )

    @ban.error
    @unban.error
    async def permissions_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                'Voce nao tem permissao para usar este comando.', ephemeral=True
            )

bot.tree.add_command(DogHatGroup())

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print('Logged in as ' + str(bot.user) + ' (ID: ' + str(bot.user.id) + ')')
    print('Sincronizados ' + str(len(synced)) + ' comando(s) de barra...')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!deleteme'):
        msg = await message.channel.send('I will delete myself now...')
        await msg.delete()
        await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

    elif message.content.startswith('!editme'):
        msg = await message.channel.send('10')
        await asyncio.sleep(3.0)
        await msg.edit(content='40')

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    msg = str(message.author) + ' deleted the message: ' + message.content
    await message.channel.send(msg)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content != after.content:
        msg = '**' + str(before.author) + '** edited their message:\n' + before.content + ' -> ' + after.content
        await before.channel.send(msg)

bot.run('SEU_TOKEN_AQUI')
