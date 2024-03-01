#!/bin/bash

#Temps entre cicle i cicle ->  sleep 0,42 ==> 0,0493333

i=0

for (( ; ; ))
do
  echo $i
  sleep $temps_cicle
  cansend can0 030#25.00.30.01
  i=$((i+1))

done

