import cv2
import time
from itertools import izip
import Image
import smtplib
 
# Camera 0 is the integrated web cam on my netbook
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
 
# Captures a single image from the camera and returns it in PIL format
def get_image():
	global camera
 	# read is the easiest way to get a full image out of a VideoCapture object.
 	retval, im = camera.read()
 	return im

def take_image(image_name):
	global camera
	global ramp_frames
	# Ramp the camera - these frames will be discarded and are only used to allow v4l2
	# to adjust light levels, if necessary
	for i in xrange(ramp_frames):
	 temp = get_image()
	print("Taking image...")
	# Take the actual image we want to keep
	camera_capture = get_image()
	file = image_name;
	# A nice feature of the imwrite method is that it will automatically choose the
	# correct format based on the file extension you provide. Convenient!
	cv2.imwrite(file, camera_capture)
	 
	# You'll want to release the camera, otherwise you won't be able to create a new
	# capture object until your script exits
	#del(camera)

def compare():
	i1 = Image.open("security_a.png")
	i2 = Image.open("security_b.png")
	assert i1.mode == i2.mode, "Different kinds of images."
	assert i1.size == i2.size, "Different sizes."
	 
	pairs = izip(i1.getdata(), i2.getdata())
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	 
	ncomponents = i1.size[0] * i1.size[1] * 3
	return (dif / 255.0 * 100) / ncomponents

def send_email():
	to = 'nvaughan84@gmail.com'
	gmail_user = 'nvaughan84@gmail.com'
	gmail_pwd = '******'
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:House Security \n'
	print header
	msg = header + '\n There is someone in your house \n\n'
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done!'
	smtpserver.close()


def loop():
	#take image 1
	take_image('security_a.png')
	time.sleep(2)
	take_image('security_b.png')
	#compare images. If different, output 'different'. If same, output 'same'
	time.sleep(2)
	diff = compare()
	print diff
	if(diff>20.00):
		send_email()


while True:
	loop()