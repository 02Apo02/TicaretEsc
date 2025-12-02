import os
from pyrogram import Client, filters
from dotenv import load_dotenv
from escrow import EscrowManager

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRX_ADDRESS = os.getenv("TRX_ADDRESS")
COMMISSION_PERCENT = int(os.getenv("COMMISSION_PERCENT", 10))

app = Client("trx_bot", bot_token=BOT_TOKEN)
escrow_mgr = EscrowManager(COMMISSION_PERCENT)

@app.on_message(filters.command("wallet"))
async def wallet(client, message):
    balance = escrow_mgr.get_balance(message.from_user.id)
    await message.reply(f"TRX Adresiniz: {TRX_ADDRESS}\nBakiyeniz: {balance} TRX")

@app.on_message(filters.command("balance"))
async def balance(client, message):
    balance = escrow_mgr.get_balance(message.from_user.id)
    await message.reply(f"Bakiyeniz: {balance} TRX")

@app.on_message(filters.command("ticaret"))
async def ticaret(client, message):
    escrow_id = escrow_mgr.create_escrow(message.from_user.id, 100)  # demo 100 TRX
    await message.reply(f"Ticaret ilanı oluşturuldu. Escrow ID: {escrow_id}\nAlıcı bekleniyor...")

@app.on_message(filters.command("buy"))
async def buy(client, message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply("Kullanım: /buy ESCROW_ID")
        return
    escrow_id = int(parts[1])
    try:
        escrow_mgr.assign_buyer(escrow_id, message.from_user.id)
        await message.reply(f"Escrow #{escrow_id} ile işlem başlatıldı. Ödeme escrow hesabına alındı.")
    except Exception as e:
        await message.reply(str(e))

@app.on_message(filters.command("onay"))
async def onay(client, message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply("Kullanım: /onay ESCROW_ID")
        return
    escrow_id = int(parts[1])
    try:
        net_amount, commission = escrow_mgr.approve(escrow_id, message.from_user.id)
        await message.reply(f"İşlem onaylandı.\nSatıcıya aktarılacak: {net_amount} TRX\nKomisyon: {commission} TRX")
    except Exception as e:
        await message.reply(str(e))

@app.on_message(filters.command("tokat"))
async def tokat(client, message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply("Kullanım: /tokat ESCROW_ID")
        return
    escrow_id = int(parts[1])
    try:
        escrow_mgr.dispute(escrow_id, message.from_user.id)
        await message.reply("İşlemde sorun bildirildi. Adminler haklı olana TRX’i aktaracak.")
    except Exception as e:
        await message.reply(str(e))

app.run()
