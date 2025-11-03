import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update, constants
import json
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from remnawave import RemnawaveSDK, WebhookUtility
from remnawave.models import UsersResponseDto, UserResponseDto, UpdateUserRequestDto


# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_DOMAIN: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')
REMNAWARE_TOKEN: str = os.getenv('REMNA_TOKEN')
REMNAWARE_DOMAIN: str = os.getenv('REMNA_PUBLIC_DOMAIN')
REMNAWARE_KEY: str = os.getenv('REMNA_SECRET_KEY')

# Build the Telegram Bot application
bot_builder = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .updater(None)
    .build()
)

remna = RemnawaveSDK(base_url=REMNAWARE_DOMAIN, token=REMNAWARE_TOKEN)

@asynccontextmanager
async def lifespan(_: FastAPI):
    """ Sets the webhook for the Telegram Bot and manages its lifecycle (start/stop). """
    await bot_builder.bot.setWebhook(url=f"https://{WEBHOOK_DOMAIN}/tghook")
    async with bot_builder:
        await bot_builder.start()
        yield
        await bot_builder.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/remnahook")
async def webhook_processing(request: Request):
    """ Handles incoming remna updates and processes them. """
    body = await request.json()
    request_valid = WebhookUtility.validate_webhook(
        body,
        request.headers.get("X-Remnawave-Signature"),
        REMNAWARE_KEY
    )
    if request_valid:
        if body["event"]=="user.expires_in_24_hours":
            await bot_builder.bot.send_message(
                      chat_id=body["data"]["telegramId"],
                      text="Ваша подписка истекает через сутки, позаботьтесь о продлении подписки.",
                      parse_mode=constants.ParseMode.HTML
                  )


@app.post("/tghook")
async def process_update(request: Request):
    """ Handles incoming Telegram updates and processes them with the bot. """
    message = await request.json()
    update = Update.de_json(data=message, bot=bot_builder.bot)
    await bot_builder.process_update(update)
    return Response(status_code=HTTPStatus.OK)


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """ Handles the /start command by sending a "Hello world!" message in response. """
    await update.message.reply_text("Привет, пришли мне ссылку подписки пожалуйста!")


async def echo(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    short_uid=update.message.text.split("/")[-1]
    user = await remna.users.get_user_by_short_uuid(short_uid)
    await remna.users.update_user(UpdateUserRequestDto(
        telegram_id= int(update.message.from_user.id),
        uuid=user.uuid
    ))
    await update.message.reply_html(f"<b>{update.message.from_user.first_name}</b> вы подписались на уведомления.")


bot_builder.add_handler(CommandHandler(command="start", callback=start))
bot_builder.add_handler(MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=echo))