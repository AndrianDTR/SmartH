#! /bin/bash
sudo modprobe w1-therm
sudo mount --bind ../devices /sys/bus/w1/devices
