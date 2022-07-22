import display
import random
import buttons
import mch22
import urequests
import wifi
import ujson
import time

def reboot(pressed):
  if pressed:
    mch22.exit_python()

buttons.attach(buttons.BTN_A,reboot)

display.drawFill(0xFFFFFF)
display.drawText(30, 80, "Connecting to wifi...", 0x000000)
display.flush()

tries = 0

while not wifi.status() and tries < 5:
    wifi.connect()
    if wifi.wait():
        print("Connected!")
        break
    else:
        display.drawFill(0xFFFFFF)
        display.drawText(30, 80, "Retry wifi... (" + str(tries) + ")", 0x000000)
        display.flush()
    time.sleep(0.2)

if not tries < 5:
    reboot(True) 
        
last_object = ""

def render_url():
    global last_object

    if last_object == "":
        display.drawFill(0xFFFFFF)
        display.drawText(30, 80, "Fetching data...", 0x000000)
        display.flush()

    response = None

    try:
        response = urequests.get('http://dome.bobbycar.cloud/api/timesheet')
    except:
        return

    data = ujson.loads(response.text)

    if response.text == last_object:
        return

    last_object = response.text

    y = 10

    display.drawFill(0xFFFFFF)
    display.flush()

    keys = list(data.keys())
    keys.sort()

    for key in keys:
        day = data[key]
        # display.drawText(10, y, item['title'], 0x000000, "permanentmarker22")
        # y += 26
        # display.drawText(10, y, 'Start: ' + item['start'], 0x000000)
        # y += 12
        # display.drawText(10, y, 'End: ' + item['end'], 0x000000)
        # y += 14
        # display.drawLine(0, y, display.width(), y, 0x000000)
        # y += 2
        display.drawText(5, y, key, 0x000000, "permanentmarker22")
        y += 26
        display.drawLine(0, y, display.width(), y, 0x000000)
        y += 1
        for item in day:
            display.drawText(10, y, item['start'] + ': ' + item['title'], 0x000000, "permanentmarker22")
            y += 26
            display.drawText(10, y, item['start'] + ' - ' + item['end'], 0x000000)
            y += 12
    display.flush()

while True:
    render_url()
    time.sleep(5)