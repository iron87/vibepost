import logging
from abc import ABC, abstractmethod
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext
from telegram.error import TelegramError
from ports.driven_port import NotificationSenderPort

class TelegramSenderAdapter(NotificationSenderPort):
    """Adapter for sending post previews to Telegram and handling user approval."""

    def __init__(self, bot_token: str):
        """
        Initializes the Telegram bot.
        
        :param bot_token: The API token for the Telegram bot.
        """
        self.bot = Bot(token=bot_token)
       # self.updater = Updater(token=bot_token, use_context=True)
       # self.dispatcher = self.updater.dispatcher

        # Register a handler for user responses
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_approval_response))

        logging.basicConfig(level=logging.INFO)

    def send_post_preview(self, post_content: str, business_contact: str, image_url: str = None):
        """
        Sends a post preview to a Telegram user/group with approval buttons.

        :param post_content: The text content of the post.
        :param business_contact: The Telegram chat ID of the recipient.
        :param image_url: (Optional) URL of an image to attach.
        """
        try:
            # Create approval buttons
            keyboard = [
                [InlineKeyboardButton("✅ Approve", callback_data="approve"),
                 InlineKeyboardButton("❌ Reject", callback_data="reject")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if image_url:
                # Send an image with caption and approval buttons
                self.bot.send_photo(chat_id=business_contact, photo=image_url, caption=post_content, reply_markup=reply_markup)
            else:
                # Send a text-only message with approval buttons
                message = self.bot.send_message(chat_id=business_contact, text=post_content, reply_markup=reply_markup)

            logging.info(f"Post preview sent to {business_contact}")

        except TelegramError as e:
            logging.error(f"Error sending Telegram message: {e}")

    def handle_approval_response(self, update: Update, context: CallbackContext):
        """
        Handles user responses to approve or reject a post.

        :param update: The update received from Telegram.
        :param context: The bot context.
        """
        query = update.callback_query
        query.answer()

        user_response = query.data
        chat_id = query.message.chat_id

        if user_response == "approve":
            response_message = "✅ The post has been approved!"
        else:
            response_message = "❌ The post has been rejected!"

        # Remove buttons after user interaction
        query.edit_message_reply_markup(reply_markup=None)
        query.message.reply_text(response_message)

        logging.info(f"Response received from {chat_id}: {user_response}")

    def start_polling(self):
        """Starts the bot in polling mode to listen for user responses."""
        self.updater.start_polling()
        logging.info("Bot is now listening for approval responses...")
