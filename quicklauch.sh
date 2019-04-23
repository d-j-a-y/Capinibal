#!/bin/bash

pipename="/tmp/plop"

rm ${pipename}
./capinibal.py -p ${pipename} &
sleep 2
mpv ${pipename}

