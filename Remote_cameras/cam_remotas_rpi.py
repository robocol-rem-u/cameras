import socket
import cv2
import numpy as np
import time

TCP_IP = '192.168.0.104'
TCP_PORT = 5001
IMG_QUALITY = 20

capture = cv2.VideoCapture(1)

while True:
	try:
		sock = socket.socket()
		sock.connect((TCP_IP, TCP_PORT))

		_, frame = capture.read()
		frame = cv2.resize(frame, (800,480))

		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), IMG_QUALITY]
		_, imgencode = cv2.imencode('.jpg', frame, encode_param)
		data = np.array(imgencode)
		stringData = data.tostring()

		sock.send( str(len(stringData)).ljust(16).encode());
		sock.send( stringData );
		sock.close()
	except:
		time.sleep(1)
