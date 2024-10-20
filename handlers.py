from database import add_task_to_db, get_tasks_from_db, find_reminders, update_task_in_db, delete_task_from_db, \
    get_task_from_db
from datetime import datetime
import logging
from telegram import Update
from telegram.ext import ContextTypes

# Enable logging
logging.basicConfig(filename='bot.log',
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Function for command /start'''
    await update.message.reply_text(
        'Welcome to task manager bot! Use command /add, /view, /update, /delete for manage the tasks.')


def is_valid_date(date_str):
    '''Function for check is valid date value'''
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def is_valid_status(status_str):
    '''Function for check is valid status value'''
    try:
        if status_str == "complete" or status_str == "incomplete":
            return True
    except ValueError:
        return False


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Function for command /add '''
    args = context.args
    if len(args) < 2:
        await update.message.reply_text('Use as: /add <description> <date in "DD.MM.YYYY"-format>')
        return
    if is_valid_date(args[-1]):
        due_date = args[-1]
        description = ' '.join(args[:-1])
        add_task_to_db(description, due_date, update.message.from_user.id)
        await update.message.reply_text(f'Task "{description}" added with the date - {due_date}.')
    else:
        await update.message.reply_text(
            'Your date is incorrect, please, put your task again using /add <description> <date in "DD.MM.YYYY"-format>')


async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Function for command /view '''
    tasks = get_tasks_from_db(update.message.from_user.id)
    if not tasks:
        await update.message.reply_text('You have no tasks.')
        return
    response = '\n'.join([f'{task[0]}. {task[1]} - {task[2]} (Status: {task[3]})' for task in tasks])
    await update.message.reply_text(response)


async def update_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Function for command /update '''
    args = context.args
    if args and isinstance(args[0], int):
        if len(args) == 2 and args[1] == "complete":
            task = get_task_from_db(args[0], update.message.from_user.id)
            update_task_in_db(task[0], task[1], task[2], "complete", update.message.from_user.id)
            await update.message.reply_text(f'The task {task[0]} updated.')
        elif len(args) < 4:
            await update.message.reply_text(
                'Use: /update <id> <description> <date in "DD.MM.YYYY"-format> <status> or /update <id> complete')
            return
        else:
            if is_valid_status(args[-1]) and is_valid_date(args[-2]):
                status = args[-1]
                task_id = int(args[0])
                description = ' '.join(args[1:-2])
                due_date = args[-2]
                update_task_in_db(task_id, description, due_date, status, update.message.from_user.id)
                await update.message.reply_text(f'The task {task_id} updated.')
            else:
                await update.message.reply_text(
                    'Your date or status is incorrect, please, update your task again using /update <id> <description> <date in "DD.MM.YYYY"-format> <status>')
                return
    else:
        await update.message.reply_text(
            'The number of task is incorrect, please, update your task again using /update <id> <description> <date in "DD.MM.YYYY"-format> <status>')
        return


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Function for command /delete '''
    args = context.args
    if len(args) != 1:
        await update.message.reply_text('Use: /delete <id>')
        return
    try:
        task_id = int(args[0])
        if delete_task_from_db(task_id, update.message.from_user.id):
            await update.message.reply_text(f'The task {task_id}  was deleted.')
        else:
            await update.message.reply_text(f"The task {task_id}  doesn't exist")
    except ValueError:
        await update.message.reply_text('The number of task is incorrect, please delete it use /delete <id>')


async def execute_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = find_reminders()
    for task in tasks:
        if task[2] == "incomplere":
            context.bot.send_message(chat_id=task[4],
                                     text=f"Attention! The task '{task[1]}' can be done till {task[2]}.")
