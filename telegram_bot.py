from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
import platform

# Token del bot (obtenlo de BotFather en Telegram)
TOKEN = "TU_TOKEN_AQUÍ"

# ID del usuario de Telegram para redirigir información de pago
ADMIN_ID = 842996224

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cambridge English Empower", callback_data="Cambridge English Empower")],
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

    # Selección de producto
    if data == "Cambridge English Empower":
        context.user_data["producto"] = data
        keyboard = [
            [InlineKeyboardButton("1st Edition", callback_data="1st Edition")],
            [InlineKeyboardButton("2nd Edition", callback_data="2nd Edition")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "¿Te interesa la 1ª edición o la 2ª edición de Cambridge English Empower?",
            reply_markup=reply_markup
        )

    elif data == "American English Empower":
        await query.message.reply_text(
            "Para American English Empower, consulta la información completa aquí: "
            "https://sites.google.com/view/netzek/libros/american-empower\n"
            "Disponible: Teacher's Book y Class Audio Files."
        )

    # Selección de edición para Cambridge English Empower
    elif data == "1st Edition":
        context.user_data["edicion"] = data
        mensaje = (
            "Cambridge English Empower - 1ª Edición\n"
            "Incluye todos los niveles (A1 al C1) con los siguientes contenidos:\n"
            "✅ Student's Book\n✅ Teacher's Book\n✅ Workbook with Answers (No online)\n"
            "✅ Class Audios\n✅ Class Videos\n✅ Workbook Audios\n✅ Presentation Plus\n"
            "✅ Progress Tests\n✅ Competency Tests\n✅ Reading Plus\n\n"
            "Costo: S/5 (Perú) o $2 (otros países)\n\n"
            "¿Deseas adquirir la 1ª edición?"
        )
        keyboard = [
            [InlineKeyboardButton("Sí", callback_data="Sí_1st")],
            [InlineKeyboardButton("No", callback_data="No")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(mensaje, reply_markup=reply_markup)

    elif data == "2nd Edition":
        context.user_data["edicion"] = data
        keyboard = [
            [InlineKeyboardButton("A2", callback_data="A2_2nd")],
            [InlineKeyboardButton("B1", callback_data="B1_2nd")],
            [InlineKeyboardButton("C1", callback_data="C1_2nd")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "Para la 2ª edición de Cambridge English Empower, solo están disponibles los paquetes A2, B1 y C1. "
            "¿Cuál deseas?",
            reply_markup=reply_markup
        )

    # Selección de nivel para 2nd Edition
    elif data in ["A2_2nd", "B1_2nd", "C1_2nd"]:
        context.user_data["nivel"] = data.split("_")[0]
        if data == "A2_2nd":
            mensaje = (
                "Cambridge English Empower - 2ª Edición, Nivel A2\n"
                "El paquete incluye:\n"
                "✅ Student’s Book PDF\n✅ Workbook with Answers PDF\n✅ Teacher’s Book PDF\n"
                "✅ Audio Files and Captions, Audio Scripts\n✅ Class Video\n"
                "✅ Academic Skills + Reading Plus\n✅ Photocopiable + Teacher’s notes\n"
                "✅ ESOL resources\n✅ Unit Progress Tests\n\n"
                "Costo: S/8\n\n"
                "¿Deseas adquirir este paquete?"
            )
            costo = "S/8"
        elif data == "B1_2nd":
            mensaje = (
                "Cambridge English Empower - 2ª Edición, Nivel B1\n"
                "El paquete incluye:\n"
                "✅ Student’s Book PDF\n✅ Workbook with Answers PDF\n✅ Teacher’s Book PDF\n"
                "✅ Audio Files and Captions, Audio Scripts\n✅ Class Video\n"
                "✅ Academic Skills + Reading Plus\n✅ Photocopiable + Teacher’s notes\n"
                "✅ ESOL resources\n✅ Unit Progress Tests\n✅ Competency Tests\n\n"
                "Costo: S/10\n\n"
                "¿Deseas adquirir este paquete?"
            )
            costo = "S/10"
        else:  # C1_2nd
            mensaje = (
                "Cambridge English Empower - 2ª Edición, Nivel C1\n"
                "El paquete incluye:\n"
                "✅ Student’s Book PDF\n✅ Teacher’s Book PDF\n"
                "✅ Audio Files and Captions, Audio Scripts\n✅ Class Video\n"
                "✅ Photocopiable + Teacher’s notes\n✅ Academic Skills + Reading Plus\n"
                "✅ ESOL resources\n✅ Academic Skills\n"
                "No incluye: Workbook, Tests (UPT, CT)\n\n"
                "Costo: S/5\n\n"
                "¿Deseas adquirir este paquete?"
            )
            costo = "S/5"
        context.user_data["costo"] = costo
        keyboard = [
            [InlineKeyboardButton("Sí", callback_data=f"Sí_2nd_{context.user_data['nivel']}")],
            [InlineKeyboardButton("No", callback_data="No")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(mensaje, reply_markup=reply_markup)

    # Proceso de compra para 1st Edition
    elif data == "Sí_1st":
        keyboard = [
            [InlineKeyboardButton("Perú", callback_data="Perú_1st")],
            [InlineKeyboardButton("Otro país", callback_data="Otro_1st")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "¿Eres de Perú o de otro país?",
            reply_markup=reply_markup
        )

    # Proceso de compra para 2nd Edition
    elif data.startswith("Sí_2nd"):
        nivel = data.split("_")[2]
        context.user_data["nivel"] = nivel
        keyboard = [
            [InlineKeyboardButton("Perú", callback_data=f"Perú_2nd_{nivel}")],
            [InlineKeyboardButton("Otro país", callback_data=f"Otro_2nd_{nivel}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "¿Eres de Perú o de otro país?",
            reply_markup=reply_markup
        )

    # Manejo de país para 1st Edition
    elif data in ["Perú_1st", "Otro_1st"]:
        context.user_data["pais"] = "Perú" if data == "Perú_1st" else "Otro país"
        costo = "S/5" if data == "Perú_1st" else "$2"
        context.user_data["costo"] = costo
        mensaje = (
            f"Información de pago para Cambridge English Empower - 1ª Edición ({context.user_data['pais']}):\n"
            f"Costo: {costo}\n"
        )
        if data == "Perú_1st":
            mensaje += "Por favor, realiza el pago usando la información en: https://acortar.link/BgRLVu\n"
        else:
            mensaje += "Contacta con @lZenaku para detalles de pago internacional.\n"
        mensaje += "¿Has realizado el pago?"
        keyboard = [
            [InlineKeyboardButton("Sí, ya he pagado", callback_data="Pagado_1st")],
            [InlineKeyboardButton("No, volver al inicio", callback_data="No")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(mensaje, reply_markup=reply_markup)

    # Manejo de país para 2nd Edition
    elif data.startswith("Perú_2nd") or data.startswith("Otro_2nd"):
        nivel = data.split("_")[2]
        context.user_data["pais"] = "Perú" if data.startswith("Perú") else "Otro país"
        mensaje = (
            f"Información de pago para Cambridge English Empower - 2ª Edición, Nivel {nivel} ({context.user_data['pais']}):\n"
            f"Costo: {context.user_data['costo']}\n"
        )
        if data.startswith("Perú"):
            mensaje += "Por favor, realiza el pago usando la información en: https://acortar.link/BgRLVu\n"
        else:
            mensaje += "Contacta con @lZenaku para detalles de pago internacional.\n"
        mensaje += "¿Has realizado el pago?"
        keyboard = [
            [InlineKeyboardButton("Sí, ya he pagado", callback_data=f"Pagado_2nd_{nivel}")],
            [InlineKeyboardButton("No, volver al inicio", callback_data="No")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(mensaje, reply_markup=reply_markup)

    # Confirmación de pago para 1st Edition
    elif data == "Pagado_1st":
        context.user_data["esperando_operacion"] = "1st"
        await query.message.reply_text(
            "Por favor, envía el número de operación del pago."
        )

    # Confirmación de pago para 2nd Edition
    elif data.startswith("Pagado_2nd"):
        nivel = data.split("_")[2]
        context.user_data["esperando_operacion"] = f"2nd_{nivel}"
        await query.message.reply_text(
            "Por favor, envía el número de operación del pago."
        )

    # Volver al inicio
    elif data == "No":
        keyboard = [
            [InlineKeyboardButton("Cambridge English Empower", callback_data="Cambridge English Empower")],
            [InlineKeyboardButton("American English Empower", callback_data="American English Empower")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "¿En qué producto estás interesado?",
            reply_markup=reply_markup
        )

# Manejar el número de operación
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "esperando_operacion" in context.user_data:
        context.user_data["numero_operacion"] = update.message.text
        context.user_data["esperando_correo"] = context.user_data["esperando_operacion"]
        del context.user_data["esperando_operacion"]
        await update.message.reply_text(
            "Por favor, envía el correo Gmail al que se enviarán los productos."
        )
    elif "esperando_correo" in context.user_data:
        correo = update.message.text
        edicion = context.user_data["esperando_correo"].split("_")[0]
        nivel = context.user_data["nivel"] if "nivel" in context.user_data else "Todos los niveles"
        mensaje_admin = (
            f"Nueva compra:\n"
            f"Producto: Cambridge English Empower - {edicion} Edición\n"
            f"Nivel: {nivel}\n"
            f"País: {context.user_data['pais']}\n"
            f"Costo: {context.user_data['costo']}\n"
            f"Número de operación: {context.user_data['numero_operacion']}\n"
            f"Correo Gmail: {correo}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=mensaje_admin)
        await update.message.reply_text(
            "Gracias por tu compra. Espera unos momentos para confirmar tu pago (máximo 15 minutos). "
            "De lo contrario, contáctate con @lZenaku."
        )
        context.user_data.clear()  # Limpiar datos del usuario

# Función para manejar errores
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Función principal para iniciar el bot
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    while True:
        await asyncio.sleep(3600)

# Ejecutar el bot
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
