welcomeClock# -------------
# begin experiment
import serial
from datetime import datetime
from threading import Lock, Thread, Event
import time

gustato_port = '/dev/cu.wchusbserial1410'

try:
    gustato_com = serial.Serial(gustato_port, baudrate=115200)
    print("Serial: Found serial interface, using it.")
except serial.SerialException:
    print("Serial: Couldnt find serial interface. Using port = None.")
    trigger = None




# -------------
# begin routine
def trigger_logging_thread(gustato_com, thisExp, blocks, logging):

    while True:
        current_line = str(gustato_com.readline())
        if '+++' in current_line:
            blocks.addData('gustato_trigger_unixtime', '%.3f' %time.time())
            logging.log(level=logging.EXP, msg= 'gustato_trigger_unixtime: ' + '%.3f' %time.time())

            blocks.addData('gustato_trigger_time', datetime.now().strftime("%H:%M:%S.%f"))
            logging.log(level=logging.EXP, msg= 'gustato_trigger_time: ' + datetime.now().strftime("%H:%M:%S.%f"))

            start_time = welcomeClock.getTime()
            blocks.addData('gustato_trigger_clock', start_time)
            logging.log(level=logging.EXP, msg= 'gustato_trigger_clock: %.2f' %start_time)

            next_line = str(gustato_com.readline());
            next_line = str(gustato_com.readline());
            counter = next_line[6:-5]
            blocks.addData('gustato_counter', counter)
            logging.log(level=logging.EXP, msg= 'gustato_counter: ' + counter)

            next_line = str(gustato_com.readline());
            voltage = next_line[11:-6]
            blocks.addData('gustato_voltage', voltage)
            logging.log(level=logging.EXP, msg= 'gustato_voltage: ' + voltage)

        elif '---' in current_line:
            next_line = str(gustato_com.readline());
            next_line = str(gustato_com.readline());
            elapsed_time = next_line[8:-7]
            blocks.addData('gustato_trigger_elapsed_time', elapsed_time)
            logging.log(level=logging.EXP, msg= 'gustato_trigger_elapsed_time: ' + elapsed_time)

        elif 'KILL trigger thread.' in current_line:
            break;

    print("Exiting trigger thread ...")

    #thisExp.nextEntry()



if gustato_com:
    trigger_thread = Thread(target=trigger_logging_thread, args=[gustato_com, thisExp, blocks, logging])
    trigger_thread.start()




# -------------
# end routine
# starting gustatometer by setting the trigger_in port to high
if gustato_com:
    print("Serial: Sending 'START'")
    gustato_com.write(b'START')

    blocks.addData('gustato_init_unixtime', '%.3f' %time.time())
    logging.log(level=logging.EXP, msg= 'gustato_init_unixtime: ' + '%.3f' %time.time())

    blocks.addData('gustato_init_time', datetime.now().strftime("%H:%M:%S.%f"))
    logging.log(level=logging.EXP, msg= 'gustato_init_time: ' + datetime.now().strftime("%H:%M:%S.%f"))

    start_time = expClock.getTime()
    blocks.addData('gustato_init_clock', start_time)
    logging.log(level=logging.EXP, msg= 'gustato_init_clock: %.2f' %start_time)

    time.sleep(2)
    print("Serial: Sending 'STOP'")
    gustato_com.write(b'STOP')






# -------------
# end experiment
if gustato_com:
    print("Serial: Sending 'KILL'")
    gustato_com.write(b'KILL')
    trigger_thread.join() 

if gustato_com:
    gustato_com.close()
