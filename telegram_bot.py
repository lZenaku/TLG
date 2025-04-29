from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import platform

# Token del bot (obtenlo de BotFather en Telegram)
TOKEN = "7898746611:AAESOn08A97Pvh3kRnWp0zbLbN34u3G5-lQ"

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English Empower", callback_data="English Empower")],
        [InlineKeyboardButton("American English Empower", callback_data="American English Empower")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Bienvenido, gracias por contactarnos. ¿En qué producto estás interesado?",
        reply_markup=reply_markup
    )

# Función para manejar las selecciones de los botones
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # Si se selecciona un producto
    if data in ["English Empower", "American English Empower"]:
        context.user_data["producto"] = data
        keyboard = [
            [InlineKeyboardButton("A1", callback_data="A1")],
            [InlineKeyboardButton("A2", callback_data="A2")],
            [InlineKeyboardButton("B1", callback_data="B1")],
            [InlineKeyboardButton("B1+", callback_data="B1+")],
            [InlineKeyboardButton("B2", callback_data="B2")],
            [InlineKeyboardButton("C1", callback_data="C1")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            f"¿En qué nivel estás interesado para {data}?",
            reply_markup=reply_markup
        )

    # Si se selecciona un nivel
    elif data in ["A1", "A2", "B1", "B1+", "B2", "C1"]:
        context.user_data["nivel"] = data
        producto = context.user_data["producto"]
        mensaje = (
            f"Has seleccionado {producto} nivel {data}.\n"
            "Características del libro:\n"
            "- Viene con libro de teachers\n"
            "- Viene con el workbook\n\n"
            "¿Deseas obtener este producto?"
        )
        keyboard = [
            [InlineKeyboardButton("Sí", callback_data="Sí")],
            [InlineKeyboardButton("No", callback_data="No")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(mensaje, reply_markup=reply_markup)

    # Si se selecciona Sí o No
    elif data == "Sí":
        await query.message.reply_text(
            "¡Gracias por tu interés! Aquí está la información de pago:\n"
            "Cuenta bancaria: 12456789"
        )
    elif data == "No":
        keyboard = [
            [InlineKeyboardButton("English Empower", callback_data="English Empower")],
            [InlineKeyboardButton("American English Empower", callback_data="American English Empower")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "¿En qué producto estás interesado?",
            reply_markup=reply_markup
        )

# Función para manejar errores
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Función principal para iniciar el bot
async def main():
    # Crear la aplicación
    app = Application.builder().token(TOKEN).build()

    # Añadir manejadores
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_error_handler(error_handler)

    # Iniciar el bot en modo polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Mantener el bot activo
    while True:
        await asyncio.sleep(3600)  # Dormir por 1 hora para evitar consumo innecesario

# Ejecutar el bot
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
