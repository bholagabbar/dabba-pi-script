#The code here will integrate "Pi Code.py" and Telegram API in a single file
from multiprocessing import Process, Lock, Value
import PiCode as pc
import telegram_api as ta

if __name__ == '__main__':

	lock = Lock()
	distance = Value('d', 0.0)
	# URL = Value('s')

	telegram = ta.telegram()
	pi = pc.Pi()

	proc_1 = Process(target=pi.loop)
	proc_2 = Process(target=telegram.poll)

	proc_1.start()
	proc_2.start()