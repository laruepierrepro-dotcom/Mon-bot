import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
)

TOKEN = "8964333587:AAFhLpPN3OsgNcMdvRyb0dHWPKYoooNdJ3w"
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
    reply_markup = InlineKeyboardMarkup(keyboard)
    texte = (
        "👋 *Bienvenue sur notre service de création de société !*\n\n"
        "Nous vous accompagnons dans la création de votre structure juridique "
        "en France et à l'international.\n\n"
        "📌 *Choisissez une option ci-dessous :*"
    )
    if update.message:
        await update.message.reply_text(texte, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text(texte, parse_mode="Markdown", reply_markup=reply_markup)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Retour au menu", callback_data="menu")]])

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await start(update, context)

    elif data == "vouch":
        texte = (
            "🏅 *Nos Avis Clients (Vouch)*\n\n"
            "✅ @client1 — _«Service rapide, société créée en 48h !»_\n"
            "✅ @client2 — _«Très professionnel, je recommande.»_\n"
            "✅ @client3 — _«LLC créée sans problème, merci !»_\n\n"
            "📌 Tous nos avis sont vérifiables sur notre canal public."
        )
        await query.edit_message_text(texte, parse_mode="Markdown", reply_markup=back_button())

    elif data == "case_proof":
        texte = (
            "📁 *Case Proof — Preuves de réalisations*\n\n"
            "Voici quelques exemples de sociétés créées pour nos clients :\n\n"
            "🏢 *LLC Delaware* — créée en 72h\n"
            "🏛️ *SASU France* — créée en 5 jours\n"
            "🌍 *LTD UK* — créée en 48h\n\n"
            "📎 Les documents officiels sont disponibles sur demande via Contact."
        )
        await query.edit_message_text(texte, parse_mode="Markdown", reply_markup=back_button())

    elif data == "contact":
        texte = (
            "📩 *Nous Contacter*\n\n"
            "Pour toute question ou commande, contacte-nous directement :\n\n"
            "👤 Responsable : @ccolombofficiel\n"
            "⏰ Disponible : Lun–Sam, 9h–20h\n\n"
            "💬 Réponds à ce message pour nous envoyer ta demande."
        )
        context.user_data["waiting_contact"] = True
        await query.edit_message_text(texte, parse_mode="Markdown", reply_markup=back_button())

    elif data == "creation_llc":
        keyboard = [
            [InlineKeyboardButton("💳 Commander une LLC — 199€", callback_data="order_llc")],
            [InlineKeyboardButton("🔙 Retour au menu", callback_data="menu")],
        ]
        texte = (
            "🏢 *Création de LLC (Limited Liability Company)*\n\n"
            "🇺🇸 *État : Delaware (USA)*\n\n"
            "📋 *Ce qui est inclus :*\n"
            "• Enregistrement officiel\n"
            "• Certificat de formation\n"
            "• Numéro EIN (équivalent SIRET)\n"
            "• Adresse enregistrée 1 an\n\n"
            "⏱️ *Délai :* 4 à 7 jours\n"
            "💰 *Tarif :* 599€\n\n"
            "✅ Idéal pour Stripe, PayPal, business en ligne, Revolut business, Wise Business."
        )
        await query.edit_message_text(texte, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "creation_societe":
        keyboard = [
            [InlineKeyboardButton("🏛️ SASU — 299€", callback_data="order_sasu")],
            [InlineKeyboardButton("🏛️ EURL — 299€", callback_data="order_eurl")],
            [InlineKeyboardButton("🏛️ SAS — 399€", callback_data="order_sas")],
            [InlineKeyboardButton("🔙 Retour au menu", callback_data="menu")],
        ]
        texte = (
            "🏛️ *Création de Société en France*\n\n"
            "📋 *Ce qui est inclus :*\n"
            "• Rédaction des statuts\n"
            "• Immatriculation au RCS\n"
            "• Numéro SIRET\n"
            "• Publication légale\n"
            "• Kbis officiel\n\n"
            "⏱️ *Délai :* 5 à 7 jours ouvrés\n\n"
            "Choisis ta structure :"
        )
        await query.edit_message_text(texte, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif data in ["order_llc", "order_sasu", "order_eurl", "order_sas"]:
        noms = {
            "order_llc": "LLC Delaware",
            "order_sasu": "SASU",
            "order_eurl": "EURL",
            "order_sas": "SAS",
        }
        nom = noms[data]
        context.user_data["commande"] = nom
        context.user_data["waiting_order"] = True
        texte = (
            f"✅ *Commande : {nom}*\n\n"
            f"Pour finaliser, envoie-nous :\n"
            f"1️⃣ Ton nom complet\n"
            f"2️⃣ Le nom souhaité pour la société\n"
            f"3️⃣ Ton email\n\n"
            f"💬 Réponds directement à ce message."
        )
        await query.edit_message_text(texte, parse_mode="Markdown", reply_markup=back_button())

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    texte = update.message.text

    if context.user_data.get("waiting_contact") or context.user_data.get("waiting_order"):
        commande = context.user_data.get("commande", "Contact")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📩 *Nouveau message*\n\n"
                f"👤 De : @{user.username or user.first_name} (ID: {user.id})\n"
                f"📋 Type : {commande}\n\n"
                f"💬 Message :\n{texte}"
            ),
            parse_mode="Markdown"
        )
        context.user_data["waiting_contact"] = False
        context.user_data["waiting_order"] = False
        context.user_data["commande"] = None
        await update.message.reply_text(
            "✅ *Message reçu !*\nNous vous répondrons dans les plus brefs délais. 🙏",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Utilise /start pour accéder au menu. 😊")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("✅ Bot démarré !")
    app.run_polling()

if __name__ == "__main__":
    main()
