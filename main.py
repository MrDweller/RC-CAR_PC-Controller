import serial
import threading
import time
import pygame

# The ImputState Class will hold the current state of the input
class InputState:
    def __init__(self):
        self.state = 0b0000
    
    def getState(self):
        return self.state

    def setState(self, newState):
        self.state = newState

def initSerial():
    # Initialize a serial port at COM3 with 9600 buadrate and a 0.01 timeout timer
    mySerial = serial.Serial()
    mySerial.port = "COM3"
    mySerial.baudrate = 9600
    mySerial.timeout = 0.01
    mySerial.open()
    print(mySerial.name)
    return mySerial
    
def exit(mySerial):
    mySerial.close()


def serial_commands():
    while(True):
        mutex_inputState.acquire()
        data = inputState.getState() # read the current inputState
        mutex_inputState.release()

        mutex.acquire()

        if(0b0000 <= int(data) and int(data) <= 0b1111):
            try:
                mySerial.write(data.to_bytes(1, 'little')) # Write the current inputState to the port
            except:
                print("Cant write to serial port") # Stop if the thread can't write to the port, will happen on exit
                mutex.release()
                break
        mutex.release()


        time.sleep(0.01)

def serial_input():
    while(True):
        mutex.acquire()
        try:
            data = mySerial.readline() # read what the micro controller sent
        except:
            print("Cant read from serial port") # Stop if the port can't be read, will happen on exit
            mutex.release()
            break
        if(data != b''):
            print(data) #
        mutex.release()
        
        time.sleep(0.001)

def window():
    running = True
    while(running):
        # Look for pygame events
        for event in pygame.event.get():
            # Stop the loop if the user cklicked the window close button
            if event.type == pygame.QUIT:
                running = False

            # Check for key events and sets the according data in the inputState object
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state | 0b0001)
                    mutex_inputState.release()
                if event.key == pygame.K_DOWN:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state | 0b0010)
                    mutex_inputState.release()
                if event.key == pygame.K_RIGHT:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state | 0b0100)
                    mutex_inputState.release()
                if event.key == pygame.K_LEFT:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state | 0b1000)
                    mutex_inputState.release()
            
            # Reset the keys inputState if released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state & 0b1110)
                    mutex_inputState.release()
                if event.key == pygame.K_DOWN:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state & 0b1101)
                    mutex_inputState.release()
                if event.key == pygame.K_RIGHT:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state & 0b1011)
                    mutex_inputState.release()
                if event.key == pygame.K_LEFT:
                    mutex_inputState.acquire()
                    state  = inputState.getState()
                    inputState.setState(state & 0b0111)
                    mutex_inputState.release()

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw a solid blue circle in the center
        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Flip the display
        pygame.display.flip()



mySerial = initSerial()
# Lock for the shared serial port
mutex = threading.Lock()

inputState = InputState()
# Lock for the shared inputState object
mutex_inputState = threading.Lock()

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

def main():
    # Setup a thread that writes to the serial port
    thread_command = threading.Thread(target=serial_commands, daemon=True)
    # Setup a thread that read from the serial port
    thread_input = threading.Thread(target=serial_input, daemon=True)

    thread_command.start()
    thread_input.start()

    window()
    
    print("EXIT")

    exit(mySerial)

main()