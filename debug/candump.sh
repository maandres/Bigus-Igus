#!/bin/bash

#Setup can0 and can1 ports
sudo ip link set can0 up type can bitrate 500000 dbitrate 8000000 restart-ms 1000 berr-reporting on fd on 
sudo ip link set can1 up type can bitrate 500000 dbitrate 8000000 restart-ms 1000 berr-reporting on fd on 

#Enable can0 and can1 ports
sudo ifconfig can0 txqueuelen 65536 
sudo ifconfig can1 txqueuelen 65536

#Dump can0 data on terminal 
candump can0
