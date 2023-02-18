from datetime import datetime

"""
        MODULE này được tạo ra nhằm log tiến trình đang chạy 
        info : thông tin của tiến trình chạy
        warning : thông báo các cảnh báo có thể xảy ra
        error : thông báo lỗi trong quá trình chạy
        high : thông báo kết quả có thể là một lỗi hay lỗ hổng được phát hiện
"""




# NULL
N = '\033[0m'
# White
W = '\033[1;37m'
# Blue
B = '\033[1;34m'
# Màu Tím
M = '\033[1;35m'
# RED
R = '\033[1;31m'
# GREEN
G = '\033[1;32m'
# YELLOW
Y = '\033[1;33m'
# MAU BLUE NHƯNG MÀ NÓ ĐẬM THÊM TẸO
C = '\033[1;36m'


def info(text):
    print("[" + Y + datetime.now().strftime("%H:%M:%S") + N + "] [" + G + "INFO" + N + "] " + text)


def warning(text):
    print("[" + Y + datetime.now().strftime("%H:%M:%S") +
          N + "] [" + Y + "WARNING" + N + "] " + text)


def high(text):
    print("[" + Y + datetime.now().strftime("%H:%M:%S") +
          N + "] [" + R + "CRITICAL" + N + "] " + text)


def error(text):
    print("[" + Y + datetime.now().strftime("%H:%M:%S")
          + N + "] [" + R + "ERROR" + "]" + text)
