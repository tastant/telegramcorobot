import os, logging
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8000"))

# Diccionari amb partitures
PARTITURES = {
    "ElCantDelOcells": {"nom":"El cant dels ocells","file_id":""},
    # Afegeix més aquí
}

logging.basicConfig(level=logging.INFO)

async def partitura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if update.effective_chat.type != "private":
        try: await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        except: pass
    if context.args:
        nom = context.args[0]
        part = PARTITURES.get(nom)
        if part and part["file_id"]:
            await context.bot.send_document(chat_id=user_id, document=part["file_id"],
                                            caption=f"Aquí tens la partitura de {part['nom']}")
        else:
            await context.bot.send_message(chat_id=user_id, text="No he trobat aquesta partitura 😕")
    else:
        await context.bot.send_message(chat_id=user_id, text="Fes servir /partitura NomDeLaPartitura")

async def cataleg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    miss = "🎵 *Catàleg de partitures disponibles:*\n\n"
    for clau, p in PARTITURES.items():
        miss += f"• `{clau}` → {p['nom']}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=miss, parse_mode="Markdown")

async def capturar_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.document:
        f = update.message.document; mime=f.mime_type
        tipus = "📄 PDF" if mime=="application/pdf" else f"📦 Alt (MIME:{mime})"
        msg = f"{tipus}\nNom: {f.file_name}\nfile_id: `{f.file_id}`"
    elif update.message.audio:
        f = update.message.audio
        msg = f"🎵 ÀUDIO\nNom: {f.file_name}\nfile_id: `{f.file_id}`"
    elif update.message.photo:
        f = update.message.photo[-1]
        msg = f"🖼️ IMATGE\nfile_id: `{f.file_id}`"
    else:
        msg = "❗ Tipus de fitxer no reconegut."
    await update.message.reply_text(msg, parse_mode="Markdown")

# Endpoint perquè UptimeRobot enviï el ping
app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify(status="ok")

def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("partitura", partitura))
    app_bot.add_handler(CommandHandler("cataleg", cataleg))
    app_bot.add_handler(MessageHandler(filters.Document.ALL | filters.Audio() | filters.PHOTO, capturar_file))
    return app_bot

if __name__ == "__main__":
    bot = run_bot()
    bot_task = bot.run_polling(drop_pending_updates=True)
    app.run(host="0.0.0.0", port=PORT)
