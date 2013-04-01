#!/usr/bin/env python

import time

## Generate filename from date and time
class DateTimeFileName():
	__filename = ""

	def __init__(self):
		self.createFileName()

	def createFileName(self):
		lt = time.localtime(time.time())

		hours = str(lt.tm_hour)
		if int(hours) < 10:
			hours = "0" + hours

		minutes = str(lt.tm_min)
		if int(minutes) < 10:
			minutes = "0" + minutes

		seconds = str(lt.tm_sec)
		if int(seconds) < 10:
			seconds = "0" + seconds

		month = str(lt.tm_mon)
		if int(month) < 10:
			month = "0" + str(month)

		day = str(lt.tm_mday)
		if int(day) < 10:
			day = "0" + str(day)

		date = str(lt.tm_year) + month + day

		self.__filename = str(lt.tm_year) + month + day + "-" + hours + "-" + minutes + "-" + seconds + ".log"

	def fileName(self):
		return self.__filename
