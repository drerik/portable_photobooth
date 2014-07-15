#!/usr/bin/python

import RPi.GPIO as GPIO
import time, os, subprocess, datetime
import Image
import piggyphoto

### Configs
# Pins
LIGHT=23
BTN=24
#SAVE_DIR="/home/pi/booth-images"
SAVE_DIR="/home/pi/code/portable_photobooth/tmp"

### Funtions

def countdown():
	print "Ok, taking pictures in..."
	print "4...."
	time.sleep(1)
	print "3...."
	time.sleep(1)
	print "2...."
	time.sleep(1)
	print "1...."
	time.sleep(1)
	
def merge_images(img_prefix):
	print "Merging images..."
	img_0 = Image.open(img_prefix+ "_0.jpg")
	
	single_img_width = img_0.size[0]
	single_img_height = img_0.size[1]
	
	combined_image = Image.new("RGB", (single_img_width*2, single_img_height*2) )
	
	print "Adding image 0..."
	combined_image.paste(img_0, (0,0) )
	
	print "Adding image 1..."
	combined_image.paste(Image.open(img_prefix+ "_1.jpg"), (single_img_width, 0) )
	
	print "Adding image 2..."
	combined_image.paste(Image.open(img_prefix+ "_2.jpg"), (0, single_img_height) )
	
	print "Adding image 3..."
	combined_image.paste(Image.open(img_prefix+ "_3.jpg"), (single_img_width, single_img_height) )
	
	print "Resizing and saving combined image..."
	combined_image.resize(img_0.size).save(img_prefix + ".jpg", dpi=[300,300],quality=100)

	print "Saved " + img_prefix + ".jpg"
	#merged_image = Image.new
### Main code
print "Starting portable_booth...."

if not os.path.exists(SAVE_DIR):
	os.makedirs(SAVE_DIR)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


camera = piggyphoto.camera()
print "Found the following camera:"
print camera.abilities

GPIO.setup(LIGHT, GPIO.OUT)
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

LIGHT_STATE=1
while True:
	print "Ready to take pictures. smile! :D"
	while GPIO.input(BTN) == GPIO.HIGH:
		GPIO.output(LIGHT, LIGHT_STATE)
		time.sleep(0.1)
		if LIGHT_STATE == 1:
			#print "LIGHT_STATE => 0"
			LIGHT_STATE = 0
		else:
			#print "LIGHT_STATE => 1"
			LIGHT_STATE = 1
	img_name = SAVE_DIR + "/snap_" + datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
	countdown()
	print "Smile!!!! :D"
	for img_number in range(0, 4):
		print "Taking image nr " + str(img_number) + "..."
		
		camera.capture_image(img_name + "_" + str(img_number) + '.jpg')
		time.sleep(1)
	print "Finished taking image " + img_name + ".jpg"
	merge_images(img_name)
	#time.sleep(5)
GPIO.output(23, 0)
GPIO.cleanup()
