from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Define states
SELECT_PURCHASE_TYPE, WAIT_FOR_PAYMENT, SELECT_ACCOUNT = range(3)

ADMIN_ID = 7521166281  # Replace with your Telegram ID

# Accounts categorized by year with availability
ACCOUNTS = {
    "2012 (with posts) (Gmail Domain)": {"price": 10, "details": ["""New Instagram Hit by @pmroh
— — — — — — — — — — — — —
          - Email Or Reset -
- Hit : 1
- Email : iloveazpower@gmail.com
- Reset : i*******r@gmail.com
- Followers : 33
- Following : 47
- Posts : 13
- Username : iloveazpower
- Date : 2012
— — — — — — — — — — — — —"""]},
    "2012 (without posts) (Gmail Domain)": {"price": 10, "details": ["""New Instagram Hit by @pmroh
— — — — — — — — — — — — —
- Hit : 1
- Email : renitachise@gmail.com
- Reset : r*******e@gmail.com
- Followers : 0
- Following : 0
- Posts : 0
- Username : renitachise
- Date : 2012
— — — — — — — — — — — — —""", """New Instagram Hit by @pmroh
— — — — — — — — — — — — —
          - Email Or Reset -
- Hit : 2
- Email : jadatiberi49@gmail.com
- Reset : j*******9@gmail.com
- Followers : 1
- Following : 0
- Posts : 0
- Username : jadatiberi49
- Date : 2012
— — — — — — — — — — — — —""", """New Instagram Hit by @pmroh
— — — — — — — — — — — — —
          - Email Or Reset -
- Hit : 3
- Email : emmalinese46@gmail.com
- Reset : e*******6@gmail.com
- Followers : 0
- Following : 0
- Posts : 0
- Username : emmalinese46
- Date : 2012

— — — — — — — — — — — — —""", """New Instagram Hit by @pmroh
— — — — — — — — — — — — —
          - Email Or Reset -
- Hit : 4
- Email : rowenapilkix@gmail.com
- Reset : r*******x@gmail.com
- Followers : 0
- Following : 0
- Posts : 0
- Username : rowenapilkix
- Date : 2012

— — — — — — — — — — — — —"""]},
    "2012 (with posts) (Hotmail Domain)": {"price": 8, "details": ["""- Good Account Instagram
— — — — — — — — — — — — —
- Name : 
- Username : deandina86
- Email : deandina86@hotmail.com
- Followers : 4
- Following : 54
- Id : 246593682
- Date : 2012
- Posts : 17
- Reset : d*******6@hotmail.com
— — — — — — — — — — — — —""", """====================
Account Name : : DigestMiny
Account Username : digestminy
Account Email : digestminy@hotmail.com
Total Followers : 0
Total Following : 7
Account ID :  257157320
Account Date : 2012
Total Posts  : 4
Rest Mail  : d*******y@hotmail.com
====================""", """====================
Account Name : : 
Account Username : celestjee
Account Email : celestjee@hotmail.com
Total Followers : 0
Total Following : 2
Account ID :  227278432
Account Date : 2012
Total Posts  : 1
Rest Mail  : c*******e@hotmail.com
===================="""]},
    "2012 (without posts) (Hotmail Domain)": {"price": 8, "details": ["""- Good Account Instagram
— — — — — — — — — — — — —
- Name : 
- Username : rachaelwallskm
- Email : rachaelwallskm@hotmail.com
- Followers : 0
- Following : 0
- Id : 256664370
- Date : 2012
- Posts : 0
- Reset : r*******m@hotmail.com
— — — — — — — — — — — — —""", """- Good Account Instagram
— — — — — — — — — — — — —
- Name : Stacey
- Username : barnerst91
- Email : barnerst91@hotmail.com
- Followers : 0
- Following : 0
- Id : 271787461
- Date : 2012
- Posts : 0
- Reset : b*******1@hotmail.com
— — — — — — — — — — — — —""", """- Good Account Instagram
— — — — — — — — — — — — —
- Name : 
- Username : masonryseattlem_775
- Email : masonryseattlem_775@hotmail.com
- Followers : 0
- Following : 6
- Id : 204015004
- Date : 2012
- Posts : 0
- Reset : m*******5@hotmail.com
— — — — — — — — — — — — —""", """- Good Account Instagram
— — — — — — — — — — — — —
- Name : swaggmuddy
- Username : swaggmuddyo
- Email : swaggmuddyo@hotmail.com
- Followers : 0
- Following : 0
- Id : 253048361
- Date : 2012
- Posts : 0
- Reset : s*******o@hotmail.com
— — — — — — — — — — — — —""", """- Good Account Instagram
— — — — — — — — — — — — —
- Name : 
- Username : katherinas49
- Email : katherinas49@hotmail.com
- Followers : 0
- Following : 0
- Id : 244337161
- Date : 2012
- Posts : 0
- Reset : k*******9@hotmail.com
— — — — — — — — — — — — —"""]},
    "2013 (with posts) (Gmail Domain)": {"price": 8, "details": ["""New Instagram Hit by @pmroh
— — — — — — — — — — — — —
          - Email Or Reset -
- Hit : 2
- Email : jaedynfinch@gmail.com
- Reset : j*******h@gmail.com
- Followers : 0
- Following : 0
- Posts : 1
- Username : jaedynfinch
- Date : 2013
— — — — — — — — — — — — —""", """• 𝗡𝗲𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 :
• 𝗗𝗼𝗺𝗮𝗶𝗻 𝗧𝘆𝗽𝗲 :  gmail.com 
— — — — — — — — — — — — —
• 📝 𝗛𝗶𝘁 : 36
• 🔍 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 : ketlywallis
• 📧 𝗘𝗺𝗮𝗶𝗹 : ketlywallis@gmail.com
• 📋 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : 0
• 📕 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : 0
• 🗳 𝗣𝗼𝘀𝘁𝘀 : 5
• 📆 𝗗𝗮𝘁𝗲 : 2013
• 🎴 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗 : 372605333
• ⚙ 𝗥𝗲𝘀𝘁 : k*******s@gmail.com
• 📖 𝗟𝗶𝗻𝗸 :https://www.instagram.com/ketlywallis""", """• 𝗡𝗲𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 :
• 𝗗𝗼𝗺𝗮𝗶𝗻 𝗧𝘆𝗽𝗲 :  gmail.com 
— — — — — — — — — — — — —
• 📝 𝗛𝗶𝘁 : 51
• 🔍 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 : yaanarner
• 📧 𝗘𝗺𝗮𝗶𝗹 : yaanarner@gmail.com
• 📋 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : 0
• 📕 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : 0
• 🗳 𝗣𝗼𝘀𝘁𝘀 : 3
• 📆 𝗗𝗮𝘁𝗲 : 2013
• 🎴 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗 : 450252826
• ⚙ 𝗥𝗲𝘀𝘁 : y*******r@gmail.com
• 📖 𝗟𝗶𝗻𝗸 :https://www.instagram.com/yaanarner"""]},
    "2013 (without posts) (Gmail Domain)": {"price": 8, "details": ["""• 𝗡𝗲𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 :
• 𝗗𝗼𝗺𝗮𝗶𝗻 𝗧𝘆𝗽𝗲 :  gmail.com 
— — — — — — — — — — — — —
• 📝 𝗛𝗶𝘁 : 110
• 🔍 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 : fashionna32264
• 📧 𝗘𝗺𝗮𝗶𝗹 : fashionna32264@gmail.com
• 📋 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : 0
• 📕 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : 0
• 🗳 𝗣𝗼𝘀𝘁𝘀 : 3
• 📆 𝗗𝗮𝘁𝗲 : 2013
• 🎴 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗 : 317232518
• ⚙ 𝗥𝗲𝘀𝘁 : f*******4@gmail.com
• 📖 𝗟𝗶𝗻𝗸 :https://www.instagram.com/fashionna32264""", """• 𝗡𝗲𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 :
• 𝗗𝗼𝗺𝗮𝗶𝗻 𝗧𝘆𝗽𝗲 :  gmail.com 
— — — — — — — — — — — — —
• 📝 𝗛𝗶𝘁 : 80
• 🔍 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 : fliprnesto
• 📧 𝗘𝗺𝗮𝗶𝗹 : fliprnesto@gmail.com
• 📋 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : 1
• 📕 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : 0
• 🗳 𝗣𝗼𝘀𝘁𝘀 : 0
• 📆 𝗗𝗮𝘁𝗲 : 2013
• 🎴 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗 : 525897430
• ⚙ 𝗥𝗲𝘀𝘁 : f*******o@gmail.com
• 📖 𝗟𝗶𝗻𝗸 :https://www.instagram.com/fliprnesto""", """• 𝗡𝗲𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 :
• 𝗗𝗼𝗺𝗮𝗶𝗻 𝗧𝘆𝗽𝗲 :  gmail.com 
— — — — — — — — — — — — —
• 📝 𝗛𝗶𝘁 : 75
• 🔍 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 : aarronbrody8
• 📧 𝗘𝗺𝗮𝗶𝗹 : aarronbrody8@gmail.com
• 📋 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : 2
• 📕 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : 11
• 🗳 𝗣𝗼𝘀𝘁𝘀 : 0
• 📆 𝗗𝗮𝘁𝗲 : 2013
• 🎴 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗 : 639568913
• ⚙ 𝗥𝗲𝘀𝘁 : a*******8@gmail.com
• 📖 𝗟𝗶𝗻𝗸 :https://www.instagram.com/aarronbrody8""", """• 𝗡𝗲𝘄 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 :
• 𝗗𝗼𝗺𝗮𝗶𝗻 𝗧𝘆𝗽𝗲 :  gmail.com 
— — — — — — — — — — — — —
• 📝 𝗛𝗶𝘁 : 59
• 🔍 𝗨𝘀𝗲𝗿𝗡𝗮𝗺𝗲 : valariemixrh
• 📧 𝗘𝗺𝗮𝗶𝗹 : valariemixrh@gmail.com
• 📋 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 : 0
• 📕 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 : 0
• 🗳 𝗣𝗼𝘀𝘁𝘀 : 0
• 📆 𝗗𝗮𝘁𝗲 : 2013
• 🎴 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗜𝗗 : 283750487
• ⚙ 𝗥𝗲𝘀𝘁 : v*******h@gmail.com
• 📖 𝗟𝗶𝗻𝗸 :https://www.instagram.com/valariemixrh"""]},
    "2013 (with posts) (Hotmail Domain)": {"price": 6, "details": ["""====================
Account Name : : James
Account Username : james8efpemb
Account Email : james8efpemb@hotmail.com
Total Followers : 0
Total Following : 0
Account ID :  309353727
Account Date : 2013
Total Posts  : 2
Rest Mail  : j*******b@hotmail.com
====================""", """====================
Account Name : : Anonymous
Account Username : sahs_couples
Account Email : sahs_couples@hotmail.com
Total Followers : 21
Total Following : 86
Account ID :  451321959
Account Date : 2013
Total Posts  : 11
Rest Mail  : s*******s@hotmail.com
====================""", """====================
Account Name : : N
Account Username : nouraalsul
Account Email : nouraalsul@hotmail.com
Total Followers : 22
Total Following : 34
Account ID :  477819511
Account Date : 2013
Total Posts  : 27
Rest Mail  : n*******l@hotmail.com
====================""", """====================
Account Name : : Mysara
Account Username : maisii76
Account Email : maisii76@hotmail.com
Total Followers : 0
Total Following : 2
Account ID :  355699371
Account Date : 2013
Total Posts  : 11
Rest Mail  : m******6@hotmail.com
===================="""]},
    "2013 (without posts) (Hotmail Domain)": {"price": 6, "details": ["""====================
Account Name : : 
Account Username : evamatten
Account Email : evamatten@hotmail.com
Total Followers : 0
Total Following : 0
Account ID :  282226521
Account Date : 2013
Total Posts  : 0
Rest Mail  : e*******n@hotmail.com
====================""", """====================
Account Name : : Tresa
Account Username : tresabeb1joh
Account Email : tresabeb1joh@hotmail.com
Total Followers : 0
Total Following : 3
Account ID :  339908457
Account Date : 2013
Total Posts  : 0
Rest Mail  : t*******h@hotmail.com
====================""", """====================
Account Name : : 
Account Username : ladonna3x
Account Email : ladonna3x@hotmail.com
Total Followers : 0
Total Following : 0
Account ID :  304827067
Account Date : 2013
Total Posts  : 0
Rest Mail  : l*******x@hotmail.com
====================""", """====================
Account Name : : فيصل الجبوري
Account Username : fasalalgbory
Account Email : fasalalgbory@hotmail.com
Total Followers : 7
Total Following : 0
Account ID :  345779110
Account Date : 2013
Total Posts  : 0
Rest Mail  : f*******y@hotmail.com
===================="""]},
    "2014 (with posts) (Gmail Domain)": {"price": 6, "details": ["user9:pass9", "user10:pass10"]},
    "2014 (without posts) (Gmail Domain)": {"price": 6, "details": ["user11:pass11", "user12:pass12"]},
    "2014 (with posts) (Hotmail Domain)": {"price": 6, "details": ["user9:pass9", "user10:pass10"]},
    "2014 (without posts) (Hotmail Domain)": {"price": 6, "details": ["user11:pass11", "user12:pass12"]},
    "2015 (with posts) (Gmail Domain)": {"price": 5, "details": ["user9:pass9", "user10:pass10"]},
    "2015 (without posts) (Gmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2015 (with posts) (Hotmail Domain)": {"price": 5, "details": ["user9:pass9", "user10:pass10"]},
    "2015 (without posts) (Hotmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2016 (with posts) (Gmail Domain)": {"price": 5, "details": ["user9:pass9", "user10:pass10"]},
    "2016 (without posts) (Gmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2016 (with posts) (Hotmail Domain)": {"price": 5, "details": ["user9:pass9", "user10:pass10"]},
    "2016 (without posts) (Hotmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2017 (with posts) (Gmail Domain)": {"price": 5, "details": ["user9:pass9", "user10:pass10"]},
    "2017 (without posts) (Gmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2017 (with posts) (Hotmail Domain)": {"price": 5, "details": ["user9:pass9", "user10:pass10"]},
    "2017 (without posts) (Hotmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2018 (without posts) (Gmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2018 (without posts) (Gmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2018 (without posts) (Hotmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    "2018 (without posts) (Hotmail Domain)": {"price": 5, "details": ["user11:pass11", "user12:pass12"]},
    
}

PAYMENT_METHODS = {
    "Binance": "Binance ID: your_binance_id",
    "JazzCash": "JazzCash Number: 0300-XXXXXXX",
    "GPay": "GPay ID: your_gpay_id",
    "Google Pay": "Google Pay ID: your_googlepay_id",
}

# User points data (Replace with a database for production)
USER_POINTS = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    USER_POINTS.setdefault(user_id, 0)  # Initialize user points
    keyboard = [
        [InlineKeyboardButton("Buy Points", callback_data="buy_points")],
        [InlineKeyboardButton("Use Points", callback_data="use_points")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Welcome! You have {USER_POINTS[user_id]} points.\nWhat would you like to do?",
        reply_markup=reply_markup,
    )
    return SELECT_PURCHASE_TYPE

async def handle_purchase_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "buy_points":
        keyboard = [[InlineKeyboardButton(method, callback_data=method)] for method in PAYMENT_METHODS.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Please select your preferred payment method to buy points:",
            reply_markup=reply_markup,
        )
        return WAIT_FOR_PAYMENT
    elif query.data == "use_points":
        user_id = query.from_user.id

        # Show available accounts with total counts
        account_summary = "Available accounts:\n"
        for account_type, data in ACCOUNTS.items():
            account_summary += f"{account_type}: {len(data['details'])} available (Price: {data['price']} points)\n"

        keyboard = [
            [InlineKeyboardButton(account, callback_data=account)]
            for account in ACCOUNTS.keys()
            if ACCOUNTS[account]["details"]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"You have {USER_POINTS[user_id]} points.\n{account_summary}\nSelect an account type to purchase:",
            reply_markup=reply_markup,
        )
        return SELECT_ACCOUNT

async def payment_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    payment_method = query.data
    payment_details = PAYMENT_METHODS.get(payment_method, "Unknown")
    await query.edit_message_text(
        f"You selected {payment_method}.\nPlease send your payment to the following details:\n\n"
        f"{payment_details}\n\n"
        "After completing the payment, upload the screenshot here."
    )
    return WAIT_FOR_PAYMENT

async def payment_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        user_id = update.message.from_user.id
        photo = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=(
                f"Payment screenshot received for user {user_id}.\n"
                "Approve or reject the payment and manually add points."
            ),
        )
        await update.message.reply_text(
            "Your payment screenshot has been sent to the admin for review. Please wait for points to be added."
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please upload a valid payment screenshot.")
        return WAIT_FOR_PAYMENT

async def confirm_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    selected_account = query.data

    if selected_account not in ACCOUNTS:
        await query.edit_message_text("Invalid account type. Please select a valid account.")
        return SELECT_ACCOUNT

    account_data = ACCOUNTS[selected_account]
    account_cost = account_data["price"]

    if USER_POINTS[user_id] >= account_cost:
        if account_data["details"]:
            USER_POINTS[user_id] -= account_cost
            account_info = account_data["details"].pop(0)  # Remove the first account
            await query.edit_message_text(
                f"Purchase successful! You bought {selected_account}.\n"
                f"Account details: {account_info}\n\n"
                f"Remaining points: {USER_POINTS[user_id]}."
            )
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"User {user_id} purchased {selected_account}. Delivered account: {account_info}."
            )
        else:
            await query.edit_message_text("Sorry, no accounts are available for this category.")
    else:
        await query.edit_message_text(
            f"Insufficient points! You need {account_cost} points but only have {USER_POINTS[user_id]} points."
        )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Process has been canceled. Thank you!")
    return ConversationHandler.END

# Add Points Command (Admin Only)
async def add_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("Usage: /addpoints <user_id> <points>")
            return

        user_id = int(args[0])
        points_to_add = int(args[1])

        USER_POINTS.setdefault(user_id, 0)  # Ensure user exists
        USER_POINTS[user_id] += points_to_add

        await update.message.reply_text(f"Successfully added {points_to_add} points to user {user_id}.")
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Your payment has been verified! {points_to_add} points have been added to your account. You now have {USER_POINTS[user_id]} points."
        )
    except ValueError:
        await update.message.reply_text("Invalid input. Provide user_id and points as numbers.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# Main Function
def main():
    print("Bot is running...")

    application = Application.builder().token("8032741891:AAGVchF4PZCXh_9f_WpHrjeFZ3Rn_WsHoEU").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_PURCHASE_TYPE: [CallbackQueryHandler(handle_purchase_type)],
            WAIT_FOR_PAYMENT: [
                CallbackQueryHandler(payment_details),
                MessageHandler(filters.PHOTO, payment_screenshot),
            ],
            SELECT_ACCOUNT: [CallbackQueryHandler(confirm_purchase)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_chat=True,  # Avoid warning
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('addpoints', add_points))

    application.run_polling()

if __name__ == '__main__':
    main()