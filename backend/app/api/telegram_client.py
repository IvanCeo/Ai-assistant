from telegram.ext import Application

def create_application(token: str) -> Application:
    return Application.builder().token(token).build()
