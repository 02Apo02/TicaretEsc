import os
from pyrogram import Client, filters
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRX_KEYSTORE = os.getenv("TRX_KEYSTORE")
TRX_PRIVATE_KEY = os.getenv("TRX_PRIVATE_KEY")
TRX_ADDRESS = os.getenv("TRX_ADDRESS")

app = Client("trx_bot", bot_token=BOT_TOKEN)

# /wallet komutu
@app.on_message(filters.command("wallet"))
async def wallet(client, message):
    await message.reply(f"TRX Adresiniz: {TRX_ADDRESS}\nBakiyeniz: 0 TRX (demo)")

# /balance komutu
@app.on_message(filters.command("balance"))
async def balance(client, message):
    await message.reply("TRX Bakiyeniz: 0 TRX (demo)\nTL Bakiyeniz: 0 TL (demo)")

# /ticaret komutu (demo)
@app.on_message(filters.command("ticaret"))
async def ticaret(client, message):
    await message.reply("Ticaret başlatma ekranı (demo)")

# /esc komutu (demo)
@app.on_message(filters.command("esc"))
async def esc(client, message):
    await message.reply("Escrow işlemleri (demo)")

# /onay komutu
@app.on_message(filters.command("onay"))
async def onay(client, message):
    await message.reply("İşlem onaylandı, TRX hak sahibine aktarılacak (demo)")

# /tokat komutu
@app.on_message(filters.command("tokat"))
async def tokat(client, message):
    await message.reply("İşlem başarısız, adminlere bildirildi (demo)")

app.run()
