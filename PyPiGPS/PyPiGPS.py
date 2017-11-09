#!  /usr/bin/python
from GPSCapture import GPSCapture
#from kivy.app import App
#from kivy.uix.widget import Widget
#from kivy.uix.label import Label
#from kivy.properties import StringProperty
import sys
import logging
from logging.config import fileConfig
from log import setup_custom_logger
#logger = setup_custom_logger('main')

#class MainControl(Widget):
#    gpsCapture = GPSCapture()
#    currentLat = StringProperty()
#    currentLong = StringProperty()
#    currentDateTime= StringProperty()
#    currentAlt = StringProperty()

#    def update(self, dt):
#        self.gpsCapture.findSerial()
#        self.gpsCapture.gpsdata()
#        currentLat = self.gpsCapture.currentLat
#        currentLong = self.gpsCapture.currentLong
#        currentDateTime=self.gpsCapture.currentDateTime
#        currentAlt=self.gpsCapture.currentAlt

#class PyPiGPSMain(App):
#    def build(self):
#        mainControl = MainControl()
#        Clock.schedule_interval(mainControl.update, 1.0/60.0)
#        return mainControl

def main():
    #PyPiGPSMain().run()
    logger.info('Starting main')
    gpsCapture = GPSCapture()
    gpsCapture.findSerial()
    gpsCapture.gpsdata()


if __name__ == "__main__":
    logger= setup_custom_logger(__name__)
    logger.info('Starting init')
    sys.exit(int(main() or 0))


