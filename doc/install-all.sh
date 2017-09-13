#!/bin/bash

# This script is used to install the required packages and source code on a fresh raspberry-pi.
# It is recommended to execute this script by copying and pasting each command separately.
# Executing it as a standalone script has not been tested and will surely fail!

# based on
# http://www.pyimagesearch.com/2015/10/26/how-to-install-opencv-3-on-raspbian-jessie/
# https://www.ics.com/blog/raspberry-pi-camera-module#.VJFhbyvF-b8

# latest firmware
sudo rpi-update

# install normal people tools
sudo apt-get install vlc emacs ne tmux bc

mkdir -p ~/src/geekcon-2017
cd ~/src/geekcon-2017

git clone https://github.com/adikarol/the_ass.git
cd ~

# follow instructions on http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
# - note we are using a different home folder for sources
# - using version opencv 3.3 and not 3.1

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev

sudo apt-get install libgtk2.0-dev

sudo apt-get install libatlas-base-dev gfortran

sudo apt-get install python2.7-dev python3-dev

# my addition, just in case should already be installed by now
sudo apt-get install libavdevice-dev x264 libx264-148 ffmpeg libavcodec57 libavcodec-extra libavdevice57 libavutil-dev libavutil55 libresample1 libresample1-dev
sudo apt-get install ccache libavresample-dev libavresample3 libgphoto2-dev libgphoto2-6 libgstreamer1.0-dev gstreamer1.0-libav libdc1394-22-dev doxygen

mkdir -p ~/src/3rdParty
cd ~/src/3rdParty

wget -O opencv-3.3.0.zip https://github.com/opencv/opencv/archive/3.3.0.zip
unzip opencv-3.3.0.zip

wget -O opencv_contrib-3.3.0.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
unzip opencv_contrib-3.3.0.zip

# we have settled on python-2.7
# the instructions say do the following but that is already installed
# wget https://bootstrap.pypa.io/get-pip.py
# sudo python get-pip.py

sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

source ~/.profile

mkvirtualenv cv -p python2
# in case of python3
# mkvirtualenv cv -p python3

source ~/.profile
# workon cv

pip install numpy
# I like having this one too, not mandatory for now, takes a while to install
pip install ipython
# pip install scipy

pip install reportlab
pip install Pillow

cd ~/src/3rdParty/opencv-3.3.0
mkdir build
cd build

# note enable precomipled headers must be added since there is a bug in gcc
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/src/3rdParty/opencv_contrib-3.3.0/modules \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D BUILD_EXAMPLES=ON ..

# this takes a while (~1h) make sure your pi is *properly* cooled
make -j4

sudo make install
sudo ldconfig

cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so

# load the camera module
sudo modprobe bcm2835-v4l2

# sample aruco markers
python aruco_show.py 11 12 13 14 15 16 17 18 19 20 21 22 -o markers_4x4_50.pdf --labels --length 70
