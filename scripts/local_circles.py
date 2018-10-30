#-----------------------------------------------------------------
#   Description:    Task switching and hysterisis
#   Author:         Hajer Karoui                    Date: 05/01/2018
#   Notes:
#   Revision History: 05/02/2018
#   Name: Hajer Karoui  Date: 05/10/2018

import psychopy.visual
import psychopy.event
import psychopy.misc
from random import shuffle
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
import os


# Store info about the experiment session
expName = u'test2'  # from the Builder filename that created this script
#2a9e398
expInfo = {'participant':'001', 'Color':'blue', 'Mixture Circles %:':0,'Mixture Triangles %:': 100}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName


win = psychopy.visual.Window(
    size=[200, 160],
    units="pix",
    fullscr=False,
    color=[1, 1, 1]
)

circle = psychopy.visual.Circle(
    win=win,
    units="pix",
    edges=128,
    radius = 10,
    #lineColor ='grey'

)

triangle = psychopy.visual.Polygon(
    win=win,
    units="pix",
    edges=3,
    radius = 13.5,
    #lineColor= 'grey'
    
    
)

# 'test' circles

nElements = 10


ncircles = (expInfo['Mixture Circles %:'])/10
ntriangles = (expInfo['Mixture Triangles %:'])/10
color = expInfo['Color']
#color = [42,158,56]

for j in range(10):
    
    shapeComb = [0 for n in range(ncircles)] + [1 for n in range(ntriangles)]

    shuffle(shapeComb)
    
    test_offset = 0

    # 'surround' circles
    surr_thetas = [i for i in range(0,360,360/(nElements-2))]
    surr_r = 50
    trialComponents = []


    for i_surr in range(len(surr_thetas)):
        
        [surr_pos_x, surr_pos_y] = psychopy.misc.pol2cart(
                surr_thetas[i_surr],
                surr_r
            )

        surr_pos_x = surr_pos_x + test_offset
        
            
        #draw circles if 0
        
        if shapeComb[i_surr] == 0 :
            circle.fillColor = color

            circle.pos = [surr_pos_x, surr_pos_y]
            circle.draw()
            
        else:
            
            triangle.fillColor = color

            triangle.pos = [surr_pos_x, surr_pos_y]
            #circle.radius = 10
            triangle.draw()
            
            


    if shapeComb[nElements-2] == 0 :
        circle.pos = [test_offset, surr_r/3]
        circle.fillColor = color
        circle.draw()
    else:
        triangle.pos = [test_offset, surr_r/3]
        triangle.fillColor = color
        triangle.draw()
        

    if shapeComb[nElements-1] == 0 :
        circle.pos = [test_offset, - surr_r/3]
        circle.fillColor = color
        circle.draw()
    else:
        triangle.pos = [test_offset, - surr_r/3]
        triangle.fillColor = color
        triangle.draw()          
            


    win.getMovieFrame(buffer="back")
    
    dir =  (os.getcwd() + '/blue/C_blue_%d%d/'% (ntriangles*10,ncircles*10))
    print dir
    if not os.path.exists(dir):
        os.makedirs(dir)
    win.saveMovieFrames(dir+ "%d.png" % j)

    win.flip()

win.getMovieFrame()
psychopy.event.waitKeys()

win.close()
