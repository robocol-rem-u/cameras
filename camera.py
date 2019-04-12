import cv2
import urllib.request
import numpy as np
from pynput.keyboard import Key, Listener

DIR_CAM0 = "http://192.168.0.103:57055"
DIR_CAM1 = "rtsp://192.168.0.110:554"

vcap1 = cv2.VideoCapture(DIR_CAM1)
vcap2 = cv2.VideoCapture(DIR_CAM0+"/video.cgi?user=alegis&pwd=alegis")

global selected
selected = -1

def enviar_comando_cam0(comando):
	result = urllib.request.urlopen(DIR_CAM0+"/decoder_control.cgi?command="+str(comando)+"&user=alegis&pwd=alegis").read()

def on_press(key):
	if selected == 0:
		if key==Key.up:
			enviar_comando_cam0(0)
		elif key==Key.down:
			enviar_comando_cam0(2)
		elif key==Key.left:
			enviar_comando_cam0(6)
		elif key==Key.right:
			enviar_comando_cam0(4)
		elif key.char=="i":
			enviar_comando_cam0(95)
		elif key.char=="o":
			enviar_comando_cam0(94)

def on_release(key):
	if selected == 0:
		if key==Key.up:
			enviar_comando_cam0(1)
		elif key==Key.down:
			enviar_comando_cam0(3)
		elif key==Key.left:
			enviar_comando_cam0(5)
		elif key==Key.right:
			enviar_comando_cam0(7)


def click(event, x, y, flags, param):
	global selected
	if event == cv2.EVENT_LBUTTONDOWN:
		if x>800 and selected!=0:
			selected = 0
		elif x>800 and selected==0:
			selected = -1
		else:
			selected = -1

cv2.namedWindow('ROBOCOL - Camaras Ucumari')
cv2.setMouseCallback('ROBOCOL - Camaras Ucumari', click)

Listener(on_press=on_press,on_release=on_release).start()

while True:

	_,frame1 = vcap1.read()

	_,frame2 = vcap2.read()

	if frame1.__class__ != None.__class__:
		rows, cols,a = frame1.shape
		M = cv2.getRotationMatrix2D((cols/2, rows/2),-180,1)
		frame1 = cv2.warpAffine(frame1, M, (cols,rows))




	if frame1.__class__ != None.__class__ and frame2.__class__ != None.__class__ :
		if selected == 0:
			shape=frame2.shape
			w=shape[1]
			h=shape[0]
			base_size=h,w,3
			base=np.zeros(base_size,dtype=np.uint8)
			cv2.rectangle(base,(0,0),(w,h),(0,0,255),10)
			base[5:h-5,5:w-5]=frame2[5:h-5,5:w-5]
		else:
			base = frame2
		a = np.hstack([cv2.resize(frame1, (800,480)),base])
	elif frame1.__class__ != None.__class__:
		a = frame1
	elif frame2.__class__ != None.__class__:
		if selected == 0:
			shape=frame2.shape
			w=shape[1]
			h=shape[0]
			base_size=h,w,3
			base=np.zeros(base_size,dtype=np.uint8)
			cv2.rectangle(base,(0,0),(w,h),(0,0,255),10)
			base[5:h-5,5:w-5]=frame2[5:h-5,5:w-5]
		else:
			base = frame2
		a = base
	else:
		print("ERROR")
	cv2.imshow('ROBOCOL - Camaras Ucumari', a)
	cv2.waitKey(1) & 0xFF

