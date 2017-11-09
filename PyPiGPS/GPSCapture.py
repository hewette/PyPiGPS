import time
import serial
import serial.tools.list_ports
import string
import sys
from pynmea import nmea
import os
from datetime import datetime, date, timedelta
from time import sleep
from CameraControl import CameraControl 
import logging
from logging.config import fileConfig
from log import setup_custom_logger
from math import radians, cos, sin, asin, sqrt
logger = logging.getLogger('main')  

class GPSCapture:
    @property
    def totalDistance(self):
        return self.__totalDistance
    @property
    def previousLat(self):
        return self.__previousLat
    @property
    def previousLong(self):
        return self.__previousLong
    @property
    def previousDateTime(self):
        return self.__previousDateTime
    @property
    def previousAlt(self):
        return self.__previousAlt
    @property
    def currentLat(self):
        return self.__currentLat
    @property
    def currentLong(self):
        return self.__currentLong
    @property
    def currentDateTime(self):
        return self.__currentDateTime
    @property
    def currentAlt(self):
        return self.__currentAlt

    __future = datetime.now()
    __currentDate = datetime(1900,01,01)
    __previousLat = -99
    __previousLong = -99
    __previousAlt = -99
    __previousDateTime = datetime(1900,01,01)
    __totalDistance = 0
    #logger = logging.getLogger('main')
    
    def __init__(self):
        print('init')
        #logger= setup_custom_logger(__name__)
        logger.debug('Starting %s', 'GPSCapture')

    def saveDataToFile(self,time_stamp,lats,lat_dir, longitude,long_dir,alt, distance, speed):
        logger.debug('saveDataToFile')
        file = open('gpsdata.csv','a') 
        file.write('{},{}{},{}{},{},{},{}\r\n'.format(time_stamp.strftime('%Y-%m-%d %H:%M:%-S.%f'), lats, lat_dir, longitude, long_dir, alt, distance, speed))
        file.close() 
        return

    def haversine(self,lon1, lat1, lon2, lat2):
        # Calculate the great circle distance between two points
        # on the earth (specified in decimal degrees)
        # convert decimal degrees to radians

        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers.  Use 3956 for miles
        self.logger.debug(c * r)
        return c * r

    def calcBearing(lon1, lat1, lon2, lat2):
        bearing = atan2(sin(long2 - long1) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(long2 - long1))
        bearing = degrees(bearing)
        bearing = (bearing + 360) % 360
        return bearing

    def calcSpeed(self,startDate, endDate, distance):
        duration = startDate - endDate
        if duration == 0:
            return 0
        else:
            return distance / duration.total_seconds()

    def gpsdata(self):
        logger.debug('Starting gpsdata')
        self.__future = datetime.now() 
        cameraControl = CameraControl()
        logger.debug("Getting GPS data")
        ser = serial.Serial()
        ser.port = "/dev/ttyUSB0"
        ser.baudrate = 9600
        ser.timeout = 1
        ser.open()
        gpgga = nmea.GPGGA()
        gprmc = nmea.GPRMC()
        foundGPRMC = False
        foundGPGGA = False
        logger.debug('Starting While() to GPS Data')
        while True: # foundGPGGA ==False or foundGPRMC==False:
            data = ser.readline()
            logger.debug(data)
            if data[0:6] == '$GPRMC':
                gprmc.parse(data)
                #print(gprmc.sen_type)
                #print(gprmc.nmea_sentence)
                ##for d in data.split(','):
                #    print('d:' + d)
                ufDate = data.split(',')[9]
                logger.debug('date:' + ufDate)
                logger.debug(str(ufDate)[4:].zfill(2) +'-'+ str(ufDate)[2:4].zfill(2) +'-'+str(ufDate)[0:2].zfill(2) )
                self.__currentDate = datetime(2000+int(str(ufDate)[4:]), int(str(ufDate)[2:4]), int(str(ufDate)[0:2]) ) 
                logger.debug('current date:' + self.__currentDate.strftime("%d %B %Y"))
                foundGPRMC = True
            elif data[0:6] == '$GPGGA':
                ##method for parsing the sentence
                gpgga.parse(data)
                lats = gpgga.latitude
                logger.debug("Latitude values : " + str(lats))

                lat_dir = gpgga.lat_direction
                logger.debug("Latitude direction : " + str(lat_dir))

                longitude = gpgga.longitude
                logger.debug("Longitude values : " + str(longitude))

                long_dir = gpgga.lon_direction
                logger.debug("Longitude direction : " + str(long_dir))

                time_stamp = gpgga.timestamp
                #utctime = str(time_stamp)[0:2].zfill(2) + ':' + str(time_stamp)[2:4].zfill(2) + ':' + str(time_stamp)[4:].zfill(2)
                logger.debug("GPS time stamp : " + str(time_stamp)[0:2].zfill(2) + ':' + str(time_stamp)[2:4].zfill(2) + ':' + str(time_stamp)[4:].zfill(2))
                utctime =  self.__currentDate.replace(hour=int(str(time_stamp)[0:2]), minute=int(str(time_stamp)[2:4]),second=int(str(time_stamp)[4:6])  )
                alt = gpgga.antenna_altitude
                logger.debug("Antenna altitude : " + str(alt))

                #lat_secs = round(float(lats[5:]) * 60 / 10000, 2)
                if datetime.now() > self.__future:
                    self.__future = datetime.now() + timedelta(minutes = 1)
                    self.__currentDateTime = utctime
                    self.__currentLat = lats + lat_dir
                    self.__currentLong = longitude + long_dir
                    self.__currentAlt = alt
                    distance =0
                    #self.haversine(self.__previousLat,self.__previousLong, lats, longitude)
                    self.__totalDistance = self.totalDistance + distance
                    speed = self.calcSpeed(self.__previousDateTime, self.__currentDateTime,self.__totalDistance)
                    self.saveDataToFile(self.__currentDateTime,lats,lat_dir, longitude,long_dir,alt, distance, speed)
                    cameraControl.takeSingle(self.__currentDateTime)
                    foundGPGGA = True

    def findSerial(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            logger.debug(p)
            if 'ttyUSB' in p:
                logger.debug(p)
        logger.info('finished  findserial')
        return  
