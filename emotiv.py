import os
import sys

import csv
import socket

HOST = "127.0.0.1" 
PORT = 6868 # port for emotiv
outfile_csv = 'emotiv_out.csv'

if __name__ == "__main__":

    out_f = open(outfile_csv, 'w')
    emotiv_writer = csv.writer(out_f)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)

        print(f"Received {data!r}") # DEBUG
        emotiv_writer.writerow(data)

    out_f.close()
    sys.exit()