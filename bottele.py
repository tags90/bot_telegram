# THƯ VIỆN ====================================================================================================================================================================================================================
import os, time, sys, logging, colorama
import pyautogui
from colorama import Fore
from telegram import Update, ReplyKeyboardMarkup, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes

# HẰNG SỐ VÀ BIẾN =============================================================================================================================================================================================================
TOKEN = "7203394666:AAF8lmq-rOP0SOngT3C6KnPVShdazq0R5vk"
ADMIN = []
ALLOWED_USER = [1, 2, 3, 4, 5, 6]
BANNED_USER = []

POS1 = (1280, 720)
POS2 = (1280, 740)
POS3 = (1280, 760)
POS4 = (1280, 780)
POS5 = (1280, 800)
POS6 = (1280, 820)

RUNNING = False
LOGIN = False

# TẠO LOG VÀ DANH SÁCH MENU ===================================================================================================================================================================================================
logging.basicConfig(format=Fore.WHITE + "%(asctime)s  - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger()

def get_menu_keyboard() -> None:
    for element in BANNED_USER or ADMIN or ALLOWED_USER:
        if element in BANNED_USER:
            None
        elif element in ADMIN:
            keyboard = [['/start'], ['/help_register'], ['/check_your_ID'], ['/reset']]
            return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        elif element in ALLOWED_USER:
            keyboard = [['/login'], ['/help'], ['/on'], ['/off']] 
            return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        else:
            keyboard = [['/check']]
            return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)        

# LỜI MỞ ĐẦU ==================================================================================================================================================================================================================
# Khởi động con bot kèm thông tin tác giả
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_html("CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI ... CỦA \nSử dụng lệnh /check để kiểm tra thông tin tài khoản", reply_markup=get_menu_keyboard())
        logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} đã khởi động")
    except SyntaxError:
        await update.message.reply_html("Lỗi", reply_markup=get_menu_keyboard())
        logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} Lỗi")

# Check ID Telegram để đăng kí
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info(f"{update.message.from_user.id} {update.message.from_user.name} đang check ID")
        if update.message.from_user.id in BANNED_USER:
            await update.message.reply_html(f"{update.message.from_user.name} à bạn đã bị chặn, vui lòng liên hệ lại để gỡ lệnh cấm", reply_markup=ForceReply(selective=True))
            logger.critical(Fore.RED + f"BAN {update.message.from_user.id} {update.message.from_user.name} đã chặn thành công")
        elif update.message.from_user.id in ADMIN:
            await update.message.reply_html(f"[ROLE: ADMIN] {update.message.from_user.name}, hãy sử dụng /login để bắt đầu công cụ", reply_markup=ForceReply(selective=True))
            logger.info(Fore.LIGHTMAGENTA_EX + f"[ROLE: ADMIN] {update.message.from_user.id} {update.message.from_user.name} đã dùng lệnh /check")
        elif update.message.from_user.id in ALLOWED_USER:
            await update.message.reply_html(f"[ROLE: USERS] {update.message.from_user.name}, Bạn hiện tại có thể đăng nhập, hãy sử dụng /login để bắt đầu công cụ", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"[ROLE: USER] {update.message.from_user.id} {update.message.from_user.name} đã dùng lệnh /check")
        else:
            await update.message.reply_html(f"{update.message.from_user.id} - Bạn vui lòng xác nhận để đăng ký bot", reply_markup=ForceReply(selective=True))
            logger.warning(Fore.YELLOW + f"Người lạ {update.message.from_user.id} {update.message.from_user.name} đã dùng lệnh /check")
    except SyntaxError:
        await update.message.reply_html("Lỗi", reply_markup=get_menu_keyboard())
        logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} Lỗi")

# Chính =======================================================================================================================================================================================================================
# Bắt đầu sử dụng
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global LOGIN
    # Kiểm tra tài khoản bị chặn
    if update.message.from_user.id in BANNED_USER:
        await update.message.reply_html(f"{update.message.from_user.name} - Bạn đã bị chặn", reply_markup=ForceReply(selective=True))
        logger.critical(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã bị chặn")    
    # kiểm tra tài khoản
    elif update.message.from_user.id in ADMIN:
        LOGIN = True
        await update.message.reply_html("Sử dụng /help để xem lệnh ADMIN", reply_markup=ForceReply(selective=True))
        logger.info(Fore.LIGHTMAGENTA_EX + f"{update.message.from_user.id} {update.message.from_user.name} - ADMIN đã đăng Nhập")
    elif update.message.from_user.id in ALLOWED_USER:        
        LOGIN = True
        await update.message.reply_html("Sử dụng /help để biết thêm chi tiết", reply_markup=ForceReply(selective=True))
        logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã đăng Nhập")
    else:
        await update.message.reply_html("Thất bại!\n\nHiện tại bạn chưa đăng kí sử dụng bot.\n Sử dụng /check để báo ADMIN về ID hiện tại của bạn để tiến hành đăng kí", reply_markup=ForceReply(selective=True))
        logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đang cố đăng nhập")

# Dev Phụ Của ADMIN

# reset bot
# delete history chat

# Hướng dẫn
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if LOGIN == True:
        if update.message.from_user.id in ADMIN:
            await update.message.reply_html("Thành Công ADMIN", reply_markup=ForceReply(selective=True))
            logger.info(Fore.LIGHTMAGENTA_EX + f"{update.message.from_user.id} {update.message.from_user.name} - ADMIN đã dùng lệnh /check")
        else:
            await update.message.reply_html("Thành Công USERs", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã dùng lệnh /help")            
    else:
        await update.message.reply_html("Bạn vui lòng xác nhận để đăng ký bot", reply_markup=ForceReply(selective=True))
        logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đang cố dùng lệnh /help")

# Bật Tools
async def on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global RUNNING
    logger.warning(Fore.YELLOW + f"{update.message.from_user.id} {update.message.from_user.name} đã dùng lệnh /on")
    if LOGIN == True:
        RUNNING = True
        if update.message.from_user.id == ALLOWED_USER[0]:
            pyautogui.leftClick(POS1)
            await update.message.reply_html("Sử dụng thành công", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS1}")
        elif update.message.from_user.id == ALLOWED_USER[1]:
            pyautogui.leftClick(POS2)
            await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS2}")
        elif update.message.from_user.id == ALLOWED_USER[2]:
            pyautogui.leftClick(POS3)
            await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS3}")
        elif update.message.from_user.id == ALLOWED_USER[3]:
            pyautogui.leftClick(POS4)
            await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS4}")
        elif update.message.from_user.id == ALLOWED_USER[4]:
            pyautogui.leftClick(POS5)
            await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS5}")
        elif update.message.from_user.id == ALLOWED_USER[5]:
            pyautogui.leftClick(POS6)
            await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã bật tại vị trí {POS6}")
        else:
            await update.message.reply_html("Lỗi không tìm thấy trong danh sách hiện tại", reply_markup=ForceReply(selective=True))
            logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - sử dụng không thành công vì không nắm trong danh sách")
    else:
        await update.message.reply_html("Không có quyền được truy cập", reply_markup=ForceReply(selective=True))
        logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} người dùng đã sử dụng /on khi chưa cấp quyền")

async def off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global RUNNING
    if LOGIN == True:        
        if RUNNING == True:
            RUNNING = False
            if update.message.from_user.id == ALLOWED_USER[0]:
                pyautogui.leftClick(POS1)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS1}")             
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS1}")
            elif update.message.from_user.id == ALLOWED_USER[1]:
                pyautogui.leftClick(POS2)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS2}")
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS2}")
            elif update.message.from_user.id == ALLOWED_USER[2]:
                pyautogui.leftClick(POS3)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS3}")
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS3}")
            elif update.message.from_user.id == ALLOWED_USER[3]:
                pyautogui.leftClick(POS4)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS4}")
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS4}")
            elif update.message.from_user.id == ALLOWED_USER[4]:
                pyautogui.leftClick(POS5)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS5}")
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS5}")                
            elif update.message.from_user.id == ALLOWED_USER[5]:
                pyautogui.leftClick(POS6)
                await update.message.reply_html("Sử dụng lệnh thành công", reply_markup=ForceReply(selective=True))
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - đã tắt tại vị trí {POS6}")
                logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Tắt thành công {POS6}")
            else:
                await update.message.reply_html("Lỗi không nằm trong danh sách", reply_markup=ForceReply(selective=True))
                logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} sử dụng không thành công vì không nắm trong danh sách")            
        else:
            await update.message.reply_html("Nên bật trước khi tắt", reply_markup=ForceReply(selective=True))
            logger.warning(Fore.YELLOW + f"{update.message.from_user.id} {update.message.from_user.name} sử dụng lệnh /off trước khi bật")        
    else:
        await update.message.reply_html("Không có quyền được truy cập", reply_markup=ForceReply(selective=True))
        logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} người dùng này đã sử dụng /off khi chưa cấp quyền")
    


# logger.info(Fore.LIGHTYELLOW_EX + f"{update.message.from_user.id} {update.message.from_user.name} - ADMIN đã dùng lệnh")
# logger.info(Fore.GREEN + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã dùng lệnh")
# logger.warning(Fore.YELLOW + f"{update.message.from_user.id} {update.message.from_user.name} - Người lạ đã dùng lệnh")
# logger.error(Fore.RED + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đang cố dùng lệnh")
# logger.critical(Fore.LIGHTMAGENTA_EX + f"{update.message.from_user.id} {update.message.from_user.name} - Người dùng đã bị chặn")

# MAIN CHÍNH ==================================================================================================================================================================================================================

def main() -> None:
    
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("login", login))     
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("on", on))
    app.add_handler(CommandHandler("off", off))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()