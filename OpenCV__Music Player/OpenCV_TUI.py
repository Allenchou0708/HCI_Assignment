import cv2
from playsound import playsound
import numpy as np
import multiprocessing
import time


def play_music(song):
    playsound(song)

if __name__ == '__main__':

    video=cv2.VideoCapture(0)
    frame_height=480
    frame_width=640
    button_height=50
    button_width=100
    height_space=30
    width_space=70
    reflect_width=(frame_width-4*button_width-3*width_space)//2


    thread=200000   #200000
    persist=9 #12 #9
    render_rate=120

    accu1=0
    accu2=0
    accu3=0
    accu4=0

    time_stamp=0
    
    reserve_button1=[]
    reserve_button2=[]
    reserve_button3=[]
    reserve_button4=[]

    play_or_not=0
    count=0
    not_re_render=0


    while True:
            
        result,frame=video.read()
        front=cv2.flip(frame,1)

        if not_re_render==0:
            frame=cv2.flip(frame,1)     #use as background
        else:
            if time.perf_counter()-time_stamp>=1.5:  # in case the user click too fast
                not_re_render=0
        
        #front-ground drawing
        cv2.rectangle(front,(reflect_width,height_space),(reflect_width+button_width,height_space+button_height),(83,49,0),cv2.FILLED)
        cv2.putText(front,"Music 1",(8+reflect_width,height_space+button_height*3//5),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255))
        cv2.rectangle(front,(reflect_width+(button_width+width_space),height_space),(reflect_width+button_width+(width_space+button_width),height_space+button_height),(83,49,0),cv2.FILLED)
        cv2.putText(front,"Music 2",(8+reflect_width+(button_width+width_space),height_space+button_height*3//5),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255))
        cv2.rectangle(front,(reflect_width+2*(button_width+width_space),height_space),(reflect_width+button_width+2*(width_space+button_width),height_space+button_height),(83,49,0),cv2.FILLED)
        cv2.putText(front,"Music 3",(8+reflect_width+2*(button_width+width_space),height_space+button_height*3//5),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255))
        cv2.rectangle(front,(reflect_width+3*(button_width+width_space),height_space),(reflect_width+button_width+3*(width_space+button_width),height_space+button_height),(83,49,0),cv2.FILLED)
        cv2.putText(front,"Music 4",(8+reflect_width+3*(button_width+width_space),height_space+button_height*3//5),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255))
        


        if not_re_render==1:    #if lock(click too fast), then continue
            cv2.imshow("Me",front)
            if cv2.waitKey(render_rate)==ord("q"):
                break
            continue

        if count==0:    #first data
            reserve_button1=frame[height_space:height_space+button_height,reflect_width:reflect_width+button_width].astype("int16")
            reserve_button2=frame[height_space:height_space+button_height,reflect_width+(button_width+width_space):reflect_width+button_width+(width_space+button_width)].astype("int16")
            reserve_button3=frame[height_space:height_space+button_height,reflect_width+2*(button_width+width_space):reflect_width+button_width+2*(width_space+button_width)].astype("int16")
            reserve_button4=frame[height_space:height_space+button_height,reflect_width+3*(button_width+width_space):reflect_width+button_width+3*(width_space+button_width)].astype("int16")
 
            count+=1
        
        else:
            diff1=np.sum(np.abs(frame[height_space:height_space+button_height,reflect_width:reflect_width+button_width].astype("int16")-reserve_button1))
            diff2=np.sum(np.abs(frame[height_space:height_space+button_height,reflect_width+(button_width+width_space):reflect_width+button_width+(width_space+button_width)].astype("int16")-reserve_button2))
            diff3=np.sum(np.abs(frame[height_space:height_space+button_height,reflect_width+2*(button_width+width_space):reflect_width+button_width+2*(width_space+button_width)].astype("int16")-reserve_button3))
            diff4=np.sum(np.abs(frame[height_space:height_space+button_height,reflect_width+3*(button_width+width_space):reflect_width+button_width+3*(width_space+button_width)].astype("int16")-reserve_button4))

            reserve_button1=frame[height_space:height_space+button_height,reflect_width:reflect_width+button_width].astype("int16")
            reserve_button2=frame[height_space:height_space+button_height,reflect_width+(button_width+width_space):reflect_width+button_width+(width_space+button_width)].astype("int16")
            reserve_button3=frame[height_space:height_space+button_height,reflect_width+2*(button_width+width_space):reflect_width+button_width+2*(width_space+button_width)].astype("int16")
            reserve_button4=frame[height_space:height_space+button_height,reflect_width+3*(button_width+width_space):reflect_width+button_width+3*(width_space+button_width)].astype("int16")
            
            #calculate the different and save it
      

            if diff1>thread:
                accu1+=1
                if accu1==persist:
                    if play_or_not==1:
                        now_thread.terminate()
                    else: play_or_not=1
                    now_thread=multiprocessing.Process(target=play_music,args=("Ereve.mp3",))
                    now_thread.start()
                    print("activate button 1")
                    accu1=-5
                    time_stamp=time.perf_counter()
                    not_re_render=1
            else: 
                accu1=0

            if diff2>thread:
                accu2+=1
                if accu2==persist:
                    if play_or_not==1:
                        now_thread.terminate()
                    else: play_or_not=1
                    now_thread=multiprocessing.Process(target=play_music,args=("Ludi.mp3",))
                    now_thread.start()

                    print("activate button 2")
                    accu2=-5
                    time_stamp=time.perf_counter()
                    not_re_render=1
            else: accu2=0

            if diff3>thread:
                accu3+=1
                if accu3==persist:
                    if play_or_not==1:
                        now_thread.terminate()
                    else: play_or_not=1
                    now_thread=multiprocessing.Process(target=play_music,args=("Orbis.mp3",))
                    now_thread.start()
                    print("activate button 3")
                    accu3=-5
                    time_stamp=time.perf_counter()
                    not_re_render=1
            else: accu3=0

            if diff4>thread:
                accu4+=1
                if accu4==persist:
                    if play_or_not==1:
                        now_thread.terminate()
                    else: play_or_not=1
                    now_thread=multiprocessing.Process(target=play_music,args=("Aqua.mp3",))
                    now_thread.start()
                    print("activate button 4")
                    accu4=-5
                    time_stamp=time.perf_counter()
                    not_re_render=1
            else: accu4=0
        
            count+=1


        cv2.imshow("Me",front)
        if cv2.waitKey(render_rate)==ord("q"):
            break

    video.release()
    cv2.destroyAllWindows
    if play_or_not==1:
        now_thread.terminate()
