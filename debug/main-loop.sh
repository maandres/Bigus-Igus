#!/bin/bash

#Temps entre cicle i cicle ->  sleep 0,042 ==> 0,0493333
temps_cicle=0.042
i=0

for (( ; ; ))
do
  echo $i
  sleep $temps_cicle
  cansend can0 050#25.00.30.01
  i=$((i+1))

done
