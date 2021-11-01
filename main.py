import serial
import threading
import time
import pygame

class InputState:
    def __init__(self):
        self.state = 0b0000
    
    def getState(self):
        return self.state

    def setState(self, newState):
        self.state = newState

def initSerial():
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
        data = inputState.getState()
        mutex_inputState.release()

        mutex.acquire()

        if(0b0000 <= int(data) and int(data) <= 0b1111):
            mySerial.write(data.to_bytes(1, 'little'))
        mutex.release()


        time.sleep(0.01)

def serial_input():
    while(True):
        mutex.acquire()
        data = mySerial.readline()
        if(data != b''):
            print(data)
        mutex.release()
        
        time.sleep(0.001)


mySerial = initSerial()
mutex = threading.Lock()

inputState = InputState()
mutex_inputState = threading.Lock()

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

def main():

    thread_command = threading.Thread(target=serial_commands, daemon=True)
    thread_input = threading.Thread(target=serial_input, daemon=True)

    thread_command.start()
    thread_input.start()

    running = True
    while(running):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

    print("EXIT")

    #exit(mySerial)

main()