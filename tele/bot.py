from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from pathlib import Path
import os

from database.db import save_user, get_bot_user
from src.auth import login_user, validate_otp, get_user_info

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR.parent / ".env")

print("Starting the bot...")

def get_tele_id(update: Update):
    tele_id = update._effective_user.id
    return tele_id

async def send_msg(update: Update, message: str):
    await update.message.reply_text(message)
    return
            
    

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_msg(update, "Welcome to SITogether!\nUse the /login command to get started!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_msg(update, update.message.text)

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tele_id = get_tele_id(update)

    if len(context.args) != 1:
        await send_msg(update, "Usage: /login <student_id>")
        return

    student_id = context.args[0]
    # Call the login_user function from auth.py
    response = await login_user(student_id)
    if response == 400:
        await send_msg(update, "Invalid student ID. Please try again.")
    elif response == 500:
        await send_msg(update, "Error occurred while sending OTP. Please try again later.")
    else:
        save_user(tele_id=tele_id, student_id=student_id)
        await send_msg(update, "An OTP has been sent to your email. Please check your inbox. \nEnter OTP using the /otp command:\n/otp <student_id> <otp>")

async def otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await send_msg(update, "Usage: /otp <student_id> <otp>")
        return

    student_id = context.args[0]
    otp = context.args[1]

    result = validate_otp(student_id=student_id, otp=otp)
    print(f"opt res {result}")
    if result == 200:
        await send_msg(update, "OTP verified!")
        return
    if result == 201:
        await send_msg(update, "Account Created!")
        return
    if result == 400:
        await send_msg(update, "Invalid student ID. Please try again.")
    elif result == 403:
        await send_msg(update, "Invalid OTP!")
        return
    elif result == 404:
        await send_msg(update, "Error! OTP not found")
        return
    elif result == 500:
        await send_msg(update, "A server error! Contact @nmd_002 for help")
        return
    else:
        await send_msg(update, "An unknown error! Contact @nmd_002 for help")
        return

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tele_id = get_tele_id(update)
    user = get_bot_user(tele_id)

    if user is None:
        await send_msg(update, "You are not logged in! Log in using the /login command")
        return

    try:
      student_id = user["student_id"]
      if student_id is None:
          await send_msg(update, "Student ID not found!")
          return
      print("Getting user info")
      user_result = get_user_info(student_id)
      print(f'User res {user_result}')
      if user_result is None or user_result.get("status") == 404:
          await send_msg(update, "Error! User details not found")
      user_details = user_result["user"]
      reply = "User Details:\n"
      for key, value in user_details.items():
          reply += f"{key}: {value}\n"
      await send_msg(update, reply)
    except Exception as e:
        print(f"Error with /profile: {e}")
        await send_msg(update, "An Error occurred, contact nmd_002")

      
          
  


app = ApplicationBuilder().token(os.environ.get("TELE_API_KEY")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("login", login))
app.add_handler(CommandHandler("otp", otp))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()