""" stds-sample-code-for-object-detection.py


    USAGE: 
    $ python stds-sample-code-for-object-detection.py --video_file football-field-cropped-video.mp4 --frame_resize_percentage 30

"""

# -----------------------  Import standard libraries ----------------------- #
from __future__ import print_function
import cv2 
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d



# ------------------------- Define utility functions ----------------------- #
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)


# ------------------ Define and initialise variables ---------------------- #
max_value = 255
max_value_H = 360//2
low_H = 80
low_S = 35
low_V = 0
high_H = 165
high_S =250
high_V =max_value
window_capture_name = 'Input video'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

#declaring arrays
distance_in_x=list()
distance_in_y=list()
distance_in_z=list()
measurements=list()
measures_o_center_in_x=list()
measures_o_center_in_y=list()
measures_o_center_in_z=list()


# ------------------ Parse data from the command line terminal ------------- #
parser = argparse.ArgumentParser(description='Vision-based object detection')
parser.add_argument('--video_file', type=str, default='camera', help='Video file used for the object detection process')
parser.add_argument('--frame_resize_percentage', type=float )
args = parser.parse_args()

# ------------------ Read video sequence file ------------------------------ #
cap = cv2.VideoCapture(args.video_file)

# ------------- Create two new windows for visualisation purposes ---------- #
cv2.namedWindow(window_capture_name, cv2.WINDOW_NORMAL)
cv2.namedWindow(window_detection_name,cv2.WINDOW_NORMAL)

#define start time of the video (18 seg) in miliseconds
start_time=18
cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

#define end time (2:57, 177 seg) in miliseconds
end_time=177

frame_rate = cap.get(cv2.CAP_PROP_FPS)
frames_selected_time=int((end_time-start_time)*frame_rate)

x_list=[]
y_list=[]
z_list=[]
cx=1920
cy=1080
f=1723.72
Z=50

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def get_real_coordinates(x_obtained,y_obtained):
        coor_x,coor_y=x_obtained,y_obtained

        u=coor_x-cx
        v=cy-coor_y

        x_global=float((u/f)*Z)
        y_global=float((-v/f)*Z)  
        z_global=50

        return x_global,y_global,z_global
    
def plot_x_y_z(x_global,y_global,z_global):
    ax.plot(x_global, y_global, z_global,marker='o',color='blue')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.pause(0.1)

def get_acumulated_coordinates(x_global,y_global,z_global):
    x_list.append(x_global)
    y_list.append(y_global)
    z_list.append(z_global)

    return x_list,y_list,z_list

def draw_rectangle(contour):
    perimeter=cv2.arcLength(contour,True)
    polynomio=cv2.approxPolyDP(contour,0.02*perimeter,True)
    x_,y_,w,h=cv2.boundingRect(polynomio)
    
    return x_,y_,w,h




# def get_distance_between_points(x_list,y_list,z_list):
#     #Append all the coordinates based on the center in lists x and y separately
#     distance_in_x=x_list
#     distance_in_y=y_list
#     distance_in_z=z_list

#     substraction_iteration=np.arange(0,frames_selected_time-1,-1)

#     print(substraction_iteration)
    # if len(distance_in_x)==1:
    #Create a for loop to  substract the measurements and get the distance   
        # for j in substraction_iteration:
        #         # print(len(distance_in_x))
        #     substraction_in_x=distance_in_x[j]-distance_in_x[j-1]
        #     measures_o_center_in_x.append(substraction_in_x)
            
#         substraction_in_y=distance_in_y[j]-distance_in_y[j-1]
#         measures_o_center_in_y.append(substraction_in_y)

#         substraction_in_z=distance_in_z[j]-distance_in_z[j-1]
#         measures_o_center_in_z.append(substraction_in_z)

# #Create a for loop to calculare the magnitude
#     for h in range(frames_selected_time):
#         magnitude=np.sqrt(np.square(measures_o_center_in_x[h-1])+np.square(measures_o_center_in_y[h-1]))
#         measurements.append(magnitude)
    
    # return measures_o_center_in_x



# ------- Main loop --------------- #
for frames in range(frames_selected_time):
    # Read current frame
    ret, frame = cap.read()

    # Check if the image was correctly captured
    if frame is None:
        break
   
    # Convert the current frame from BGR to HSV
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Apply a threshold to the HSV image
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    # Convert the current frame from BGR to Gray
    framem = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
    # Filter out the grassy re+gion from current frame and keep the moving object only
    bitwise_AND = cv2.bitwise_and(frame, frame, mask=frame_threshold)
    contours, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area=cv2.contourArea(contour)
        max_value=np.max(bitwise_AND[:,:,1])
        if area>420:
            ax.clear
            x_,y_,w,h=draw_rectangle(contour)
            cv2.rectangle(bitwise_AND,(x_-40,y_-40),(x_+100,y_+100),(0,255,0),1)

            if frames % (30) == 0:
                x_global,y_global,z_global=get_real_coordinates(x_,y_)
                x_list,y_list,z_list=get_acumulated_coordinates(x_global,y_global,z_global)
                plot_x_y_z(x_list,y_list,z_list)
            
                if len(x_list)>=2:
                    #getting the measurement in x
                    substraction_in_x=x_list[-1]-x_list[-2]
                    measures_o_center_in_x.append(substraction_in_x)
                    print(measures_o_center_in_x)
                
                

    # Visualise both the input video and the object detection windows
    # Create a new window for visualisation purposes
    cv2.imshow(window_capture_name, frame)
    cv2.imshow(window_detection_name, bitwise_AND)

    # The program finishes if the key 'q' is pressed
    key = cv2.waitKey(5)
    if key == ord('q') or key == 27:
        print("Programm finished, mate!")
        break

# Destroy all visualisation windows
cv2.destroyAllWindows()

# Destroy 'VideoCapture' object
cap.release()