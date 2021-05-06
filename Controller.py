import time
from pyfirmata import Arduino, util
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import screen_brightness_control as sbc
from pynput.keyboard import Key, Controller

board = Arduino('COM5')  # Initialize the board

# Initialize an iterator to get information from the board.
it = util.Iterator(board)
it.start()

digitalInputA = board.get_pin('d:2:i')  # Set digital pin 8 to input.
digitalInputB = board.get_pin('d:4:i')  # Set digital pin 8 to input.
digitalInputC = board.get_pin('d:7:i')  # Set digital pin 8 to input.
digitalInputD = board.get_pin('d:8:i')  # Set digital pin 8 to input.
digitalInputE = board.get_pin('d:12:i')  # Set digital pin 8 to input.

analogInputA = board.get_pin('a:0:i')  # Set analog pin 0 to input.
analogInputB = board.get_pin('a:1:i')  # Set analog pin 1 to input.

# Get a volume object for PC's master volume.
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

keyboard = Controller()  # Initializes a virtual keyboard.


# Function for cleaner code when simulating one key press.
def pressKey(key, kboard=keyboard):
    kboard.press(key)
    kboard.release(key)


time.sleep(1)  # Waits for 1 second to make sure the sensors have given a reading.

dark = False  # Keep track of whether the computer screen is dimmed.

# Keep track of whether the buttons used to be pressed.
wasButtonA = False
wasButtonB = False
wasButtonC = False
wasButtonD = False
wasButtonE = False

# Sensor/Button loop.
while True:
    # Update button digital readings.
    buttonA = digitalInputA.read()
    buttonB = digitalInputB.read()
    buttonC = digitalInputC.read()
    buttonD = digitalInputD.read()
    buttonE = digitalInputE.read()

    # Update sensor analog readings.
    potentiometer = analogInputA.read()
    photoresistor = analogInputB.read()

    # Change volume according to potentiometer reading.
    newV = ((potentiometer*37)-37.0)
    volume.SetMasterVolumeLevel((-37 if newV < -37 else 0 if newV > 0 else newV), None)  # Range from -37 to 0.

    # Change brightness according to photoresistor reading.
    if dark and photoresistor >= 0.25:  # Light on. Turn brightness up.
        sbc.set_brightness(100)
        dark = False
    elif not dark and photoresistor < 0.25:  # Light off. Turn brightness down.
        sbc.set_brightness(0)
        dark = True

    # Executes macro if button A is pressed.
    if wasButtonA != buttonA:
        if buttonA:
            wasButtonA = True

            # Macro A
            pressKey(Key.enter)
            keyboard.type("Let me split, don't fight")
            pressKey(Key.enter)
        else:
            wasButtonA = False

    # Executes macro if button B is pressed.
    if wasButtonB != buttonB:
        if buttonB:
            wasButtonB = True

            # Macro B
            pressKey(Key.enter)
            keyboard.type('Come group with me')
            pressKey(Key.enter)
        else:
            wasButtonB = False

    # Executes macro if button C is pressed.
    if wasButtonC != buttonC:
        if buttonC:
            wasButtonC = True

            # Macro C
            pressKey(Key.enter)
            keyboard.type('Lets get baron')
            pressKey(Key.enter)
        else:
            wasButtonC = False

    # Executes macro if button D is pressed.
    if wasButtonD != buttonD:
        if buttonD:
            wasButtonD = True

            # Macro D
            pressKey(Key.enter)
            keyboard.type('Lets get dragon')
            pressKey(Key.enter)
        else:
            wasButtonD = False

    # Executes macro if button E is pressed.
    if wasButtonE != buttonE:
        if buttonE:
            wasButtonE = True

            # Macro E
            pressKey(Key.enter)
            keyboard.type('Gank please')
            pressKey(Key.enter)
        else:
            wasButtonE = False

    # Print sensor/button values for debugging.
    print("-----------------")
    print("ButtonA:", buttonA)
    print("ButtonB:", buttonB)
    print("ButtonC:", buttonC)
    print("ButtonD:", buttonD)
    print("ButtonE:", buttonE)
    print("Volume:", potentiometer)
    print("Light:", photoresistor)
    time.sleep(0.1)  # .1 second delay after each loop for stability.





