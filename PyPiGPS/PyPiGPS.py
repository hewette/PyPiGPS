#!  /usr/bin/python
from GPSCapture import GPSCapture

import sys
import logging
from logging.config import fileConfig
from log import setup_custom_logger
from Tkinter import *
import tkFont
#logger = setup_custom_logger('main')

class PyPiGPSMain():
    def  exitProgram(self):
        self.win.quit()

    def build(self):
        self.win = Tk()
        self.myfont = tkFont.Font(family='Helvetic', size = 35, weight ='bold')
        self.gpsCapture = GPSCapture()        
        self.win.title("Pi GPS")
        self.win.geometry('800x480')
        Label(self.win, text= "Hello", bg = "black", fg = "white", font = "none 12 bold").grid(row=0, column=0,sticky=W)
        exitButton = Button(self.win, text = 'Exit', font = self.myfont, command = self.exitProgram()).grid(row=3, column=0,sticky=W)
        #gpsCapture.findSerial()
        #gpsCapture.gpsdata()

        self.win.mainloop()




def main():
    main =  PyPiGPSMain()
    main.build()
    logger.info('Starting main')



if __name__ == "__main__":
    logger= setup_custom_logger(__name__)
    logger.info('Starting init')
    sys.exit(int(main() or 0))


