import sys, bluetooth

bd_addr = "00:06:66:48:97:57" # RN-42 address
port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))