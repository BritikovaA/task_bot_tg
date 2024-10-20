from telegram import Update
from telegram.ext import CommandHandler, Application
from handlers import start, add_task, view_tasks, update_task, delete_task,execute_reminders
from database import init_db
import asyncio
import schedule

async def run_schedule():
    while True:
        schedule.run_pending()

def main() -> None:
    init_db()

    application = Application.builder().token("TOKEN").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add_task))
    application.add_handler(CommandHandler('view', view_tasks))
    application.add_handler(CommandHandler('update', update_task))
    application.add_handler(CommandHandler('delete', delete_task))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    schedule.every().day.at("23:00").do(execute_reminders(application.bot))
    asyncio.create_task(run_schedule())


if __name__ == "__main__":
    main()
