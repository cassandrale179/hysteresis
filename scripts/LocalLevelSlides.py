#-----------------------------------------------------------------
#   Description:    Task switching and hysterisis
#   Author:         Hajer Karoui                    Date: 05/01/2018
#   Notes:
#   Revision History: 06/07/2018
#   Name: Hajer Karoui  Date: 05/10/2018


import psychopy.visual
import psychopy.event
import psychopy.misc
import random
from random import shuffle
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
import os

win = psychopy.visual.Window(
    size=[200, 200],
    units="pix",
    fullscr=True,
    color=[1, 1, 1]
)


#script to generate slides
#loop of 10 to go through every ratio
#within each loop, we have different compositions of the ratio



for i in range (11):
    ntriangles = 10 - i
    ncircles = i

    for j in range (15):

        #get the big circle
        pic = random.randint(0,9)
        #change color according to your global cue
        stimulus1 = (os.getcwd() + '/blue/C_blue_5050/'  + str(pic)+".png") 
        stimulus2 = (os.getcwd() + '/blue/T_blue_5050/'+ str(pic)+".png")
        
        pics = [stimulus1 for p in range(ncircles)] + [stimulus2 for p in range(ntriangles)]
        print len(pics)
        shuffle(pics)
        r1 = 0
        #4 on top
        for r1 in range (10):
            st = visual.ImageStim(win, image=pics[r1])
            if r1 < 4 :
                st.pos = [-300 + r1*st.size[0] ,200]
                st.draw()
        
            elif r1 < 6:  
                st.pos = [-900+ (r1%6)*st.size[0] , 0 ]
                st.draw()
                
            else:
                st.pos = [-700 + (r1-4)*st.size[0] ,-200 ]
                st.draw()
                
                
        win.getMovieFrame(buffer="back")
        #core.wait(0.3)
        dir =  (os.getcwd() + '/slides/blue global/%d%d/'% (ntriangles*10,10*ncircles))
        if not os.path.exists(dir):
            os.makedirs(dir)
            
        win.saveMovieFrames(dir+ "%d.png" % j)
        

        #print dir
        win.flip()
        #get the small circle


psychopy.event.waitKeys()

win.getMovieFrame()

win.close()
