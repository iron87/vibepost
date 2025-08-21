from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram.request import HTTPXRequest
from models.business import Business
from models.post import Post
from ports.driven_port import DatabasePort
from ports.driver_port import PostCreationPort
from settings import settings
import httpx


class TelegramBotAdapter:

    def __init__(self, db_port: DatabasePort, post_creator: PostCreationPort):
        self.db_port = db_port
        self.post_service = post_creator
        API_BASE_URL = "https://telegram-http-proxy-737748161943.europe-west1.run.app/bot"
        self.application = (
            Application.builder()
            .token(settings.TELEGRAM_BOT_TOKEN)
            .base_url(API_BASE_URL)
            .build()
        )
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("post", self.create_post))
        self.application.add_handler(CallbackQueryHandler(self.button_callback))

    def get_business_from_username(self, username: str):
        """Retrieve business ID from Telegram username."""
        owner: Business = self.db_port.get_business_by_telegram_id(username);
        return owner.id if owner else None

    async def start(self, update: Update, context: CallbackContext):
        """Handles /start command and checks registration."""
        username = update.message.from_user.username
        business_id = self.get_business_from_username(username)

        if business_id:
            update.message.reply_text("✅ Sei già registrato! Puoi iniziare a creare post con `/create_post`")
        else:
            update.message.reply_text("❌ Non sei registrato! Contatta il supporto per registrare il tuo business.")

    async def create_post(self, update: Update, context: CallbackContext):
        """Handles /create_post <text> command - Generates a post preview."""
        username = update.message.from_user.username
        business_id = self.get_business_from_username(username)

        if not business_id:
            update.message.reply_text("❌ Non sei registrato. Contatta il supporto per registrarti.")
            return

        user_input = " ".join(context.args)
        if not user_input:
            update.message.reply_text("❌ Usa il comando così: `/create_post Nuovo menu disponibile! 🍽️`", parse_mode="Markdown")
            return

        # Generate Post using LLM
        post: Post  = self.post_service.create_post(business_id, user_input)
        
        # Save in context for approval
        context.user_data["pending_post"] = post

        # Send preview with approval buttons
        keyboard = [
            [InlineKeyboardButton("✅ Approva", callback_data="approve"),
             InlineKeyboardButton("❌ Rifiuta", callback_data="reject")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(f"📢 **Anteprima del Post:**\n\n{post.content}", reply_markup=reply_markup, parse_mode="Markdown")

    def button_callback(self, update: Update, context: CallbackContext):
        """Handles button clicks (Approve/Reject)."""
        query = update.callback_query
        query.answer()
        
        username = query.from_user.username
        business_id = self.get_business_from_username(username)

        if not business_id:
            query.message.reply_text("❌ Non sei registrato!")
            return

        if query.data == "approve":
            post: Post = context.user_data.get("pending_post")
            if post:
                #self.post_service.approve_post(post.content, username, post.get("image_url"))
                query.edit_message_text("✅ Post approvato e pubblicato!")
            else:
                query.edit_message_text("❌ Nessun post in attesa di approvazione.")

        elif query.data == "reject":
            query.edit_message_text("❌ Post rifiutato.")

    def run(self):
        """Start the bot polling."""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)