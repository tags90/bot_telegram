import logging, sys, os, pyautogui, requests
from colorama import Fore
from telegram import Update, ForceReply, KeyboardButton
from telegram.ext import CommandHandler, ContextTypes, Application
from bot_telegram.test_bot_variable import *

logging.basicConfig(level=logging.INFO, format= Fore.BLUE + "%(asctime)s  - %(levelname)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
bot_log = logging.getLogger()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if update.message.from_user.id in USER_BLACK_LIST:
            await update.message.reply_html(f"{update.message.from_user.name} Bạn đã bi chặn", reply_markup=ForceReply(selective=True))
            bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /start")
        elif update.message.from_user.id in USER_ADMIN:
            await update.message.reply_html("Chào mừng bạn đã đến với ...\nBạn hiện tại là ADMIN\n/login để tiến hành đăng nhập\n/help để xem hướng dẫn", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"[ROLE: Admin] Admin: {update.message.from_user.name} ID: {update.message.from_user.id} đã dùng thành công lệnh /start")
        elif update.message.from_user.id in USER_WHITE_LIST:
            await update.message.reply_html("Chào mừng bạn đã đến với ...\nBạn hiện tại là người được ưu tiên\n/login để tiến hành đăng nhập\n/help để xem hướng dẫn", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"[ROLE: Helper] Người dùng: {update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /start")
        elif update.message.from_user.id in USER_ALLOW_LIST:
            await update.message.reply_html("Chào mừng bạn đã đến với ...\nBạn đã xác thực\n/login để tiến hành đăng nhập\n/help để xem hướng dẫn", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"[ROLE: Người dùng] Người dùng: {update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /start")
        else:
            await update.message.reply_html("Không có quyền sử dụng\nVui lòng sử dụng /check để báo lại cho Admin tiến hành sử dụng bot", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"[Người lạ] Người dùng: {update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /start")

    except SyntaxError:
        await update.message.reply_html("Lỗi khi từ khi bắt đầu", reply_markup=ForceReply(selective=True))
        bot_log.info(Fore.GREEN + f"Người dùng: {update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /start")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if USER_LOGIN == False:
            await update.message.reply_html(f"ID hiện tại của bạn là {update.message.from_user.id}\nVui lòng không chia sẻ ID này với bất kỳ ai\nHãy gửi ID này cho Admin tiến hành xác thực", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"{update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /check")
        else:
            await update.message.reply_html(f"Bạn đã xác thực rồi", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"{update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /check")
    except SyntaxError:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /check")

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global USER_LOGIN
    # Kiểm tra tài khoản bị chặn
        if update.message.from_user.id in USER_BLACK_LIST:
            await update.message.reply_html(f"{update.message.from_user.name} - Bạn đã bị chặn", reply_markup=ForceReply(selective=True))
            bot_log.critical(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã bị chặn")    
    # kiểm tra tài khoản
        elif update.message.from_user.id in USER_ADMIN:
            USER_LOGIN = True
            await update.message.reply_html("Sử dụng /help để xem lệnh ADMIN", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.LIGHTMAGENTA_EX + f"{update.message.from_user.id} {update.message.from_user.name} - ADMIN đã đăng Nhập")
        elif update.message.from_user.id in USER_ALLOW_LIST:        
            USER_LOGIN = True
            await update.message.reply_html("Sử dụng /help để biết thêm chi tiết", reply_markup=ForceReply(selective=True))
            bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã đăng Nhập")
        else:
            await update.message.reply_html("Thất bại!\n\nHiện tại bạn chưa đăng kí sử dụng bot.\n Sử dụng /check để báo ADMIN về ID hiện tại của bạn để tiến hành đăng kí", reply_markup=ForceReply(selective=True))
            bot_log.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đang cố đăng nhập")
    except SyntaxError:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /empty")

async def on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global USER_RUNNING
        bot_log.warning(Fore.YELLOW + f"{update.message.from_user.id} {update.message.from_user.name} đã dùng lệnh /on")
        if USER_LOGIN == True:
            USER_RUNNING = True
            if update.message.from_user.id == USER_ALLOW_LIST[0]:
                pyautogui.leftClick(POS1)
                await update.message.reply_html("Sử dụng thành công", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS1}")
            elif update.message.from_user.id == USER_ALLOW_LIST[1]:
                pyautogui.leftClick(POS2)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS2}")
            elif update.message.from_user.id == USER_ALLOW_LIST[2]:
                pyautogui.leftClick(POS3)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS3}")
            elif update.message.from_user.id == USER_ALLOW_LIST[3]:
                pyautogui.leftClick(POS4)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS4}")
            elif update.message.from_user.id == USER_ALLOW_LIST[4]:
                pyautogui.leftClick(POS5)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS5}")
            elif update.message.from_user.id == USER_ALLOW_LIST[5]:
                pyautogui.leftClick(POS6)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS6}")
            else:
                await update.message.reply_html("Lỗi không tìm thấy trong danh sách hiện tại", reply_markup=ForceReply(selective=True))
                bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - sử dụng không thành công vì không nắm trong danh sách")
        else:
            await update.message.reply_html("Không có quyền được truy cập", reply_markup=ForceReply(selective=True))
            bot_log.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} người dùng đã sử dụng /on khi chưa cấp quyền")
    except SyntaxError:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /on")

async def off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global USER_RUNNING
        if USER_LOGIN == True:        
            if USER_RUNNING == True:
                USER_RUNNING = False
                if update.message.from_user.id == USER_ALLOW_LIST[0]:
                    pyautogui.leftClick(POS1)
                    await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS1}")             
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS1}")
                elif update.message.from_user.id == USER_ALLOW_LIST[1]:
                    pyautogui.leftClick(POS2)
                    await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS2}")
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS2}")
                elif update.message.from_user.id == USER_ALLOW_LIST[2]:
                    pyautogui.leftClick(POS3)
                    await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS3}")
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS3}")
                elif update.message.from_user.id == USER_ALLOW_LIST[3]:
                    pyautogui.leftClick(POS4)
                    await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS4}")
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS4}")
                elif update.message.from_user.id == USER_ALLOW_LIST[4]:
                    pyautogui.leftClick(POS5)
                    await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS5}")
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS5}")                
                elif update.message.from_user.id == USER_ALLOW_LIST[5]:
                    pyautogui.leftClick(POS6)
                    await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS6}")
                    bot_log.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS6}")
                else:
                    await update.message.reply_html("Lỗi không nằm trong danh sách", reply_markup=ForceReply(selective=True))
                    bot_log.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} sử dụng không thành công vì không nắm trong danh sách")            
            else:
                await update.message.reply_html("Nên bật trước khi tắt", reply_markup=ForceReply(selective=True))
                bot_log.warning(Fore.YELLOW + f"{update.message.from_user.id} {update.message.from_user.name} sử dụng lệnh /off trước khi bật")        
        else:
            await update.message.reply_html("Không có quyền được truy cập", reply_markup=ForceReply(selective=True))
            bot_log.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} người dùng này đã sử dụng /off khi chưa cấp quyền")
    except SyntaxError:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /empty")
 
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        pyautogui.screenshot(region=POS1())
        file = {"photo":open("","rb")}
        r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}", files=file)
        bot_log.info(r.status_code)
    except SyntaxError:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /empty")

async def empty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.info(Fore.GREEN + f"{update.message.from_user.name} {update.message.from_user.id} đã dùng thành công lệnh /empty")
    except SyntaxError:
        await update.message.reply_html("", reply_markup=ForceReply(selective=True))
        bot_log.error(Fore.RED + f"{update.message.from_user.name} {update.message.from_user.id} đã gặp lỗi khi dùng lệnh /empty")
 



def main () -> None:
    bot = Application.builder().token(TOKEN).build()

    
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("check", check))
    bot.add_handler(CommandHandler("login", login))
    bot.add_handler(CommandHandler("on", on))
    bot.add_handler(CommandHandler("off", off))
    bot.add_handler(CommandHandler("exit", exit))
    # bot.add_handler(CommandHandler("empty", empty))

    bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()