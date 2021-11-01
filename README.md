# RC-CAR_PC-Controller
Basic pc-controller for giving a micro controller (like arduino) input to use for a rc-car.

Use arrow keys as input. Sets up the input in binary data and sends over a serial COM connection to the micro controller.

The data will contain four bits:
			
			0 0 0 0
			| | | |
			| | | UP
			| |DOWN
			|RIGHT
			LEFT
