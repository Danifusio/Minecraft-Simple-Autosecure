import discord
from discord import ui
from views.modal_one import MyModalOne

class ButtonViewOne(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="persistent:button_one")
    async def button_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.response.is_done():
                print("[WARN] Interacción ya respondida")
                await interaction.followup.send("Esta interacción ya fue procesada. Por favor, intenta de nuevo.", ephemeral=True)
                return
            print("[INFO] Enviando modal MyModalOne")
            await interaction.response.send_modal(MyModalOne())
        except discord.errors.HTTPException as e:
            print(f"[ERROR] Error al enviar modal: {e}")
            await interaction.followup.send("Ocurrió un error al abrir el modal. Por favor, intenta de nuevo.", ephemeral=True)