#!/Users/ericandrechek/venv/bin/python
import time
import math
import os
from datetime import datetime, timedelta
from pathlib2 import Path
from guts import SpeedTest

frequencyInt = ""
spanInt = ""
optionInt = ""
timeStart = ""
timeElap = ""


def speedtestrun():
    global timeElap
    timeInt = time.time()
    print("\nBeginning speedtest... This should take about 30 seconds to run depending on your internet speed")
    dt = datetime.now()
    formatdt = datetime.strptime("{}".format(dt), "%Y-%m-%d %H:%M:%S.%f")
    date = "{0:%m}-{0:%d}-{0:%y}".format(formatdt)
    timeCSV = "{0:%I:%M%p}".format(formatdt)
    timeLong = "{0:%c}".format(formatdt)

    errors = False

    s = SpeedTest()
    try:
        downloadBits = s.download()
    except Exception as e:
        downloadBits = 0
        errors = "{}".format(e)
    try:
        uploadBits = s.upload()
    except Exception as e:
        uploadBits = 0
        errors += ", {}".format(e)
    download = downloadBits / 1000000
    try:
        ping = s.ping()
    except Exception as e:
        ping = 0
        errors += ", {}".format(e)
    upload = uploadBits / 1000000

    timeElap = time.time() - timeInt
    timeElapRound = round(timeElap, 2)

    csvName = os.path.join(os.path.expanduser(""), "{}.csv".format(date))
    my_file = Path(os.path.expanduser("{}".format(csvName)))
    if not my_file.is_file():
        csvx = open(csvName, "w")
        csvx.close()
        csvw = open(csvName, "w")
        titleRow = "Time, Download, Upload, Ping, Elapsed Time\n"
        csvw.write(titleRow)
        csvw.close()

    csv = open(csvName, "a")
    dataRow = "{}, {}, {}, {}, {}\n".format(timeCSV, str(round(download, 2)), str(round(upload, 2)),
                                            str(round(ping, 2)),
                                            str(timeElapRound))
    csv.write(dataRow)
    csv.close()

    timeElap = time.time() - timeInt
    timeElapRound = round(timeElap, 2)
    if errors:
        print(
            "\nDatetime = {}\nElapsed Time = {} seconds\nDownload = {} mb/s\nUpload = {} mb/s\nPing = {}\nErrors = {}\n".format(
                timeLong, timeElap, download, upload, ping, errors))
    else:
        print("\nDatetime = {}\nElapsed Time = {} seconds\nDownload = {} mb/s\nUpload = {} mb/s\nPing = {}\n".format(
            timeLong, timeElap, download, upload, ping))


def autorun():
    def freq():
        global frequencyInt
        frequency = raw_input("\nAt what intervals (in minutes) would you like your internet speed to be tested and "
                              "recorded? (15 minutes is recommended)")
        try:
            frequencyInt = float(frequency)
        except ValueError:
            print("\nError setting frequency to \'{}\' minute intervals. Please try again and only type the number of "
                  "minutes between each test, for example if you desire 15 minutes between each test, type \'15\' not "
                  "\'fifteen\' or \'15 minutes\' etc.".format(frequency))
            freq()

        if frequencyInt != "":
            if frequencyInt >= 1:
                return frequencyInt
            else:
                print("\nInterval time must be greater than or equal to 1 minute.")
                freq()

    intFreq = freq()
    if intFreq is None:
        intFreq = frequencyInt

    def spanfunc():
        global spanInt
        span = raw_input("\nHow long would you like this program to run for? (in hours) (ie 24 hours (1 day) or 168 "
                         "hours (1 week))")
        try:
            spanInt = float(span)
        except ValueError:
            print("\nError setting span to \'{}\' hours. Please try again and only type the number of hours for the "
                  "program to run, for example if you desire results from 1 full day, type \'24\' not \'twenty-four\' "
                  "or \'24 hours\' etc.".format(span))
            spanfunc()

        if spanInt != "":
            if spanInt >= (intFreq / 60):
                return spanInt
            else:
                print("\nTesting time span must be greater than or equal to the interval time.")
                spanfunc()

    intSpan = spanfunc()
    if intSpan is None:
        intSpan = spanInt

    def startTime():
        global timeStart
        startq = raw_input("\nWould you like to set a time for this program to start? (\'yes\' or \'no\')")
        if startq == "yes":
            timein = raw_input("\nWhat time would you like this program to start (in year-month-day "
                               "hour:minutes:seconds.milliseconds format (ex: {}))".format(datetime.now()))
            try:
                timeStart = datetime.strptime(timein, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                print("Inputted time does not match the format. Try again and follow the format.")
                startTime()

            timeq = raw_input("Is this the time you wanted: {}? \'yes\' or \'no\'".format(timeStart))
            if timeq == "yes":
                if timeStart != "":
                    if timeStart > (datetime.now() + timedelta(seconds=5)):
                        print("Beginning speedtests at {}".format(timeStart))
                        return timeStart
                    else:
                        print("\nStart time must be at least 5 seconds from now.")
                        startTime()
                else:
                    print("\nError\ processing start time. Please try again. If the error persists, save all text in "
                          "terminal and report the glitch.")
                    startTime()
            else:
                print("\nPlease be sure to type your times in the proper format.")
                startTime()
        elif startq == "no":
            timeStart = "no"
            return "no"
        else:
            print("\n{} not recognized as \'yes\' or \'no\', please try again and type either \'yes\' or "
                  "\'no\'.".format(startq))
            startTime()

    def runLoop():
        print("\nRunning speedtests... Speedtest results will appear in the terminal every {} minutes for {} "
              "hours".format(intFreq, intSpan))
        intSpanMin = intSpan * 60
        runNumb = int(math.ceil(intSpanMin / intFreq))
        speedtestrun()
        for x in xrange(0, runNumb):
            minutesDelay = intFreq - (float(timeElap) / 60)
            now_plus_2 = datetime.now() + timedelta(minutes=minutesDelay)
            print("Next test running in {} minutes at about {}...".format(minutesDelay,
                                                                          now_plus_2))
            time.sleep((intFreq * 60) - float(timeElap))
            speedtestrun()

    startT = startTime()
    if startT is None:
        startT = timeStart

    if startT != "no":
        deltatime = startT - datetime.now()
        print("Executing first test in {} seconds...".format(deltatime.total_seconds()))
        time.sleep(deltatime.total_seconds())
        runLoop()
    else:
        runLoop()


def opt():
    global optionInt
    option = raw_input("\nWould you like to run one speedtest (\'1\') or setup a speedtest to run at designated "
                       "intervals for a designated time period (\'2\'). (Please type \'1\' for option 1 or "
                       "\'2\' for option 2)")
    try:
        optionInt = int(option)
    except ValueError:
        print("\nError choosing option {}. Please type either \'1\' or \'2\'.".format(option))
        opt()

    if optionInt != "":
        if optionInt == 1 or optionInt == 2:
            return optionInt
        else:
            print("\nChoose only \'1\' or \'2\'. The program was unable to find an option {}".format(optionInt))
            opt()


print("\nWelcome to speedtester! This python script gets all the data you could possibly want about your internet "
      "speed. The program can run 1 speedtest, or schedule periodic speedtests so you can map the fast and slow "
      "internet times during the day. This program, when finished running the speedtest, will output some speed "
      "info into the terminal, add some easier to read formatted speed data into a .csv for easy graphing, dump "
      "all raw data into a json file for you to see the guts of the un-formatted data if you so desire (note that "
      "the date and time data in the json file are occassionaly off. This is due an error in the server but is "
      "fixed for the console and csv outputs) and lastly it will download a very easy to see and understand .png "
      "with the basic speedtest specs for easy sharing (again the date and time for this are occasionally off). "
      "Enjoy your speedtesting!")
intOpt = opt()
if intOpt is None:
    intOpt = optionInt

if intOpt == 1:
    speedtestrun()
elif intOpt == 2:
    autorun()
else:
    print("\nAn unknown error occurred. Please execute this script again and choose only option \'1\' or \'2\'.")
