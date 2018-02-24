import RPi.GPIO as GPIO
import time
import dropbox
import mysql.connector

cnx = mysql.connector.connect(user='sachinh_project', password='sachin123',
                              host='johnny.heliohost.org',
                              database='sachinh_be_proj')

query = ("select * from analysis")
cursorA = cnx.cursor(buffered = True)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Switches----------------------------------------------
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)#initialize
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)#stop
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)#area1
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)#area2
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_UP)#area3
GPIO.setup(29, GPIO.IN, pull_up_down = GPIO.PUD_UP)#area4
#--------------------------------------------------------

#LEDs----------------------------------------------------
GPIO.setup(3, GPIO.OUT)#metal
GPIO.setup(5, GPIO.OUT)#glass
GPIO.setup(7, GPIO.OUT)#paper
GPIO.setup(11, GPIO.OUT)#plastic
GPIO.setup(12, GPIO.OUT)#initialize
GPIO.setup(13, GPIO.OUT)#stop
GPIO.setup(15, GPIO.OUT)#area1
GPIO.setup(16, GPIO.OUT)#area2
GPIO.setup(18, GPIO.OUT)#area3
GPIO.setup(19, GPIO.OUT)#area4
#--------------------------------------------------------

#Servo PWM-----------------------------------------------
GPIO.setup(31, GPIO.OUT)#main flap
GPIO.setup(32, GPIO.OUT)#small flap 1
GPIO.setup(33, GPIO.OUT)#small flap 2
#--------------------------------------------------------

#Functions Definitions-----------------------------------
def download(file_name,target_name):
    with open(target_name, "wb") as f:
        md,res = dbx.files_download(file_name)
        f.write(res.content)


#--------------------------------------------------------

#Variables-----------------------------------------------s
area1metal = 0
area1paper = 0
area1plastic = 0
area1glass = 0

area2metal = 0
area2paper = 0
area2plastic = 0
area2glass = 0

area3metal = 0
area3paper = 0
area3plastic = 0
area3glass = 0

area4metal = 0
area4paper = 0
area4plastic = 0
area4glass = 0

tosend_metal = 0
tosend_plastic = 0
tosend_paper = 0
tosend_glass = 0

gotfile = 0
#----------------------------------------------------------
mainflap = GPIO.PWM(31, 50)
smallflap1 = GPIO.PWM(32, 50)
smallflap2 = GPIO.PWM(33, 50)
dbx = dropbox.Dropbox('6Xjl6rD5c1QAAAAAAAACL61p6g_XmV7oE3a3nN6SYd64LYw_zAhUbGIW3KZ6xenn')

currentarea = "area1"
GPIO.output(15, True)
#------------------------------------------------------------

def put_metal_in_bin():
	smallflap1.ChangeDutyCycle(5.27)  
	time.sleep(1)
    mainflap.ChangeDutyCycle(5.27)  
	time.sleep(2)
	smallflap1.ChangeDutyCycle(7.5)
	time.sleep(1)
	mainflap.ChangeDutyCycle(7.5)
	time.sleep(1)

def put_plastic_in_bin():
	smallflap1.ChangeDutyCycle(9.72)  
	time.sleep(1)
    mainflap.ChangeDutyCycle(5.27)  
	time.sleep(2)
	smallflap1.ChangeDutyCycle(7.5)
	time.sleep(1)
	mainflap.ChangeDutyCycle(7.5)
	time.sleep(1)

def put_glass_in_bin():
	smallflap1.ChangeDutyCycle(5.27)  
	time.sleep(1)
    mainflap.ChangeDutyCycle(9.72)  
	time.sleep(2)
	smallflap1.ChangeDutyCycle(7.5)
	time.sleep(1)
	mainflap.ChangeDutyCycle(7.5)
	time.sleep(1)

def put_paper_in_bin():
	smallflap1.ChangeDutyCycle(9.72)  
	time.sleep(1)
    mainflap.ChangeDutyCycle(9.72)  
	time.sleep(2)
	smallflap1.ChangeDutyCycle(7.5)
	time.sleep(1)
	mainflap.ChangeDutyCycle(7.5)
	time.sleep(1)

while True:
    init_button = GPIO.input(21)
    stop_button = GPIO.input(22)
    area1_button = GPIO.input(23)
    area2_button = GPIO.input(24)
    area3_button = GPIO.input(26)
    area4_button = GPIO.input(29)

    for entry in dbx.files_list_folder('/be_proj').entries:
        print(entry.name)
        if 'prediction.txt' in entry.name:
            download('/be_proj/prediction.txt','output.txt')
            dbx.files_delete('/be_proj/prediction.txt')
            gotfile = 1

    
    if init_button == False:
        GPIO.output(12, True)
        print("Init button preseed")
        time.sleep(0.2)
        mainflap.start(7.5)
        smallflap1.start(7.5)
        smallflap2.start(7.5)
        GPIO.output(12, False)
        continue

    elif stop_button == False:
        GPIO.output(13, True)
        time.sleep(0.2)
        GPIO.output(13, False)
        break

    elif area1_button == False:
        currentarea = "area1"
        GPIO.output(15, True)
        GPIO.output(16, False)
        GPIO.output(18, False)
        GPIO.output(19, False)
        continue 

    elif area2_button == False:
        currentarea = "area2"
        GPIO.output(15, False)
        GPIO.output(16, True)
        GPIO.output(18, False)
        GPIO.output(19, False)
        continue

    elif area3_button == False:
        currentarea = "area3"
        GPIO.output(15, False)
        GPIO.output(16, False)
        GPIO.output(18, True)
        GPIO.output(19, False)
        continue

    elif area4_button == False:
        currentarea = "area4"
        GPIO.output(15, False)
        GPIO.output(16, False)
        GPIO.output(18, False)
        GPIO.output(19, True)
        continue

    if gotfile == 1:
        file1 = open("output.txt","r")
        t = file1.read()
        f = int(t)
        #####################################You've to write flap code here in each if statements############################################
        if f == 0:
            if currentarea == "area1":
                area1metal += 1
                GPIO.output(3, True)
                put_metal_in_bin()
                GPIO.output(3, False)
            elif currentarea == "area2":
                area2metal += 1
                GPIO.output(3, True)
                put_metal_in_bin()
                GPIO.output(3, False)              
            elif currentarea == "area3":
                area3metal += 1
                GPIO.output(3, True)
                put_metal_in_bin()
                GPIO.output(3, False)
            elif currentarea == "area4":
                area4metal += 1
                GPIO.output(3, True)
                put_metal_in_bin()
                GPIO.output(3, False)
        elif f == 1:
            if currentarea == "area1":
                area1plastic += 1
                GPIO.output(11, True)
                put_plastic_in_bin()
                GPIO.output(11, False)
            elif currentarea == "area2":
                area2plastic += 1
                GPIO.output(11, True)
                put_plastic_in_bin()
                GPIO.output(11, False)
            elif currentarea == "area3":
                area3plastic += 1
                GPIO.output(11, True)
                put_plastic_in_bin()
                GPIO.output(11, False)
            elif currentarea == "area4":
                area4plastic += 1
                GPIO.output(11, True)
                put_plastic_in_bin()
                GPIO.output(11, False)
        elif f == 2:
            if currentarea == "area1":
                area1paper += 1
                GPIO.output(7, True)
                put_paper_in_bin()
                GPIO.output(7, False)
            elif currentarea == "area2":
                area2paper += 1
                GPIO.output(7, True)
                put_paper_in_bin()
                GPIO.output(7, False)
            elif currentarea == "area3":
                area3paper += 1
                GPIO.output(7, True)
                put_paper_in_bin()
                GPIO.output(7, False)
            elif currentarea == "area4":
                area4paper += 1
                GPIO.output(7, True)
                put_paper_in_bin()
                GPIO.output(7, False)

        elif f == 3:
            if currentarea == "area1":
                area1glass += 1
                GPIO.output(5, True)
                put_glass_in_bin()
                GPIO.output(5, False)
            elif currentarea == "area2":
                area2glass += 1
                GPIO.output(5, True)
                put_glass_in_bin()
                GPIO.output(5, False)
            elif currentarea == "area3":
                area3glass += 1
                GPIO.output(5, True)
                put_glass_in_bin()
                GPIO.output(5, False)
            elif currentarea == "area4":
                area4glass += 1
                GPIO.output(5, True)
                put_glass_in_bin()
                GPIO.output(5, False)

        os.remove('output.txt')
        gotfile = 0


    if currentarea == "area1":
        tosend_metal = area1metal
        tosend_glass = area1glass
        tosend_paper = area1paper
        tosend_plastic = area1plastic

    elif currentarea == "area2":
        tosend_metal = area2metal
        tosend_glass = area2glass
        tosend_paper = area2paper
        tosend_plastic = area2plastic

    elif currentarea == "area3":
        tosend_metal = area3metal
        tosend_glass = area3glass
        tosend_paper = area3paper
        tosend_plastic = area3plastic

    elif currentarea == "area4":
        tosend_metal = area4metal
        tosend_glass = area4glass
        tosend_paper = area4paper
        tosend_plastic = area4plastic