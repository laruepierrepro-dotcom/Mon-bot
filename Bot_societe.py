import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "8964333587:AAGi8MjFn4RIUPJcoLeYLsWe9mN0tiwFSZs"
ADMIN_ID = 8759565759

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏅 Vouch", callback_data="vouch")],
        [InlineKeyboardButton("📁 Case Proof", callback_data="case_proof")],
        [InlineKeyboardButton("📩 Contact", callback_data="contact")],
        [InlineKeyboardButton("🏢 Création LLC", callback_data="creation_llc")],
        [InlineKeyboardButton("🏛️ Création Société", callback_data="creation_societe")],
    ]
    texte = (
        "👋 *Bienvenue sur notre service de création de société !*\n\n"
        "Nous vous accompagnons dans la création de votre structure juridique "
        "en France et à l'international.\n\n"
        "📌 *Choisissez une option ci-dessous :*"
    )
    msg = update.message or update.callback_query.message
    await msg.reply_text(texte, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour au menu", callback_data="menu")]])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        keyboard = [
            [InlineKeyboardButton("🏅 Vouch", callback_data="vouch")],
            [InlineKeyboardButton("📁 Case Proof", callback_data="case_proof")],
            [InlineKeyboardButton("📩 Contact", callback_data="contact")],
            [InlineKeyboardButton("🏢 Création LLC", callback_data="creation_llc")],
            [InlineKeyboardButton("🏛️ Création Société", callback_data="creation_societe")],
        ]
        await query.edit_message_text(
            "👋 *Bienvenue sur notre service de création de société !*\n\n📌 *Choisissez une option :*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "vouch":
        await query.edit_message_text(
            "🏅 *Nos Avis Clients (Vouch)*\n\n"
            "✅ @client1 — _«Service rapide, société créée en 48h !»_\n"
            "✅ @client2 — _«Très professionnel, je recommande.»_\n"
            "✅ @client3 — _«LLC créée sans problème, merci !»_\n\n"
            "📌 Tous nos avis sont vérifiables sur notre canal public.",
            parse_mode="Markdown", reply_markup=back_button()
        )

    elif data == "case_proof":
        await query.edit_message_text(
            "📁 *Case Proof — Preuves de réalisations*\n\n"
            "🏢 *LLC Delaware* — créée en 72h\n"
            "🏛️ *SASU France* — créée en 5 jours\n"
            "🌍 *LTD UK* — créée en 48h\n\n"
            "📎 Documents disponibles sur demande via Contact.",
            parse_mode="Markdown", reply_markup=back_button()
        )

    elif data == "contact":
        context.user_data["waiting_contact"] = True
        await query.edit_message_text(
            "📩 *Nous Contacter*\n\n"
            "👤 Responsable : @ccolombofficiel\n"
            "⏰ Disponible : Lun–Sam, 9h–20h\n\n"
            "💬 Réponds à ce message pour nous envoyer ta demande.",
            parse_mode="Markdown", reply_markup=back_button()
        )

    elif data == "creation_llc":
        await query.edit_message_text(
            "🏢 *Création de LLC (Delaware - USA)*\n\n"
            "📋 *Inclus :*\n"
            "• Enregistrement officiel\n"
            "• Certificat de formation\n"
            "• Numéro EIN\n"
            "• Adresse enregistrée 1 an\n\n"
            "⏱️ *Délai :* 4 à 7 jours\n"
            "💰 *Tarif :* 599€",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Commander — 199€", callback_data="order_llc")],
                [InlineKeyboardButton("🔙 Retour au menu", callback_data="menu")]
            ])
        )

    elif data == "creation_societe":
        await query.edit_message_text(
            "🏛️ *Création de Société en France*\n\n"
            "📋 *Inclus :*\n"
            "• Rédaction des statuts\n"
            "• Immatriculation au RCS\n"
            "• Numéro SIRET\n"
            "• Publication légale\n"
            "• Kbis officiel\n\n"
            "⏱️ *Délai :* 5 à 7 jours\n\n"
            "Choisis ta structure :",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏛️ SASU — 299€", callback_data="order_sasu")],
                [InlineKeyboardButton("🏛️ EURL — 299€", callback_data="order_eurl")],
                [InlineKeyboardButton("🏛️ SAS — 399€", callback_data="order_sas")],
                [InlineKeyboardButton("🔙 Retour au menu", callback_data="menu")]
            ])
        )

    elif data in ["order_llc", "order_sasu", "order_eurl", "order_sas"]:
        noms = {"order_llc": "LLC Delaware", "order_sasu": "SASU", "order_eurl": "EURL", "order_sas": "SAS"}
        context.user_data["commande"] = noms[data]
        context.user_data["waiting_order"] = True
        await query.edit_message_text(
            f"✅ *Commande : {noms[data]}*\n\n"
            "Envoie-nous :\n"
            "1️⃣ Ton nom complet\n"
            "2️⃣ Le nom souhaité pour la société\n"
            "3️⃣ Ton email",
            parse_mode="Markdown", reply_markup=back_button()
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    texte = update.message.text
    if context.user_data.get("waiting_contact") or context.user_data.get("waiting_order"):
        commande = context.user_data.get("commande", "Contact")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 *Nouveau message*\n\n👤 @{user.username or user.first_name} (ID: {user.id})\n📋 {commande}\n\n💬 {texte}",
            parse_mode="Markdown"
        )
        context.user_data.clear()
        await update.message.reply_text("✅ *Message reçu ! On vous répond très vite.* 🙏", parse_mode="Markdown")
    else:
        await update.message.reply_text("Utilise /start pour accéder au menu. 😊")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("✅ Bot démarré !")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
