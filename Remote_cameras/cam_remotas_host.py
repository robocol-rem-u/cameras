import socket
import cv2
import numpy as np

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = '192.168.0.100'
TCP_PORT = 5010


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)


while True:
	conn, addr = s.accept()

	length = recvall(conn,16)
	stringData = recvall(conn, int(length))
	data = np.fromstring(stringData, dtype='uint8')
	conn.close()

	decimg=cv2.imdecode(data,1)

	rows, cols,a = decimg.shape
	M = cv2.getRotationMatrix2D((cols/2, rows/2),-90,1)
	dst = cv2.warpAffine(decimg, M, (cols,rows))

	cv2.imshow('SERVER',dst)
	cv2.waitKey(1)