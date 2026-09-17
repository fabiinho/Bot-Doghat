import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class DogHatGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="doghat", description="Comandos do DogHat")

    @app_commands.command(name="ban", description="Bane um membro do servidor")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, membro: discord.Member, motivo: str = "Nenhum motivo fornecido"):
        await membro.ban(reason=motivo)
        await interaction.response.send_message(f'🔨 O usuário {membro.mention} foi banido!\n**Motivo:** {motivo}')

    @app_commands.command(name="unban", description="Desbane um usuário pelo ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, id_usuario: str, motivo: str = "Nenhum motivo fornecido"):
        try:
            user = await bot.fetch_user(int(id_usuario))
            await interaction.guild.unban(user, reason=motivo)
            await interaction.response.send_message(f'🔓 O usuário **{user.name}** ({user.id}) foi desbanido!')
        except discord.NotFound:
            await interaction.response.send_message("❌ Usuário não encontrado ou não está banido.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Insira um ID válido contendo apenas números.", ephemeral=True)

    @ban.error
    @unban.error
    async def permissions_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ Você não tem permissão para usar este comando.", ephemeral=True)

bot.tree.add_command(DogHatGroup())

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'Bot {bot.user} está online!')
    print(f'Sincronizados {len(synced)} comando(s) globalmente.')

bot.run("token")
