#The code here will integrate "Pi Code.py" and Telegram API in a single file
import PiCode as Pi
import telegram_api as ta

if __name__ == '__main__':
	#add multiprocessing
	ta.poll()
	pi = Pi()
	pi.loop()