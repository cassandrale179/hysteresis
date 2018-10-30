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
import uuid
import os


# Store info about the experiment session
expName = u'test2'  # from the Builder filename that created this script
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

for i in range (11):
    ntriangles = 10 - i
    ncircles = i


    for j in range(10):
        
        
        shapeComb = [0 for n in range(ncircles)] + [1 for n in range(ntriangles)]

        shuffle(shapeComb)

        row =[]
        #test_offset = -250
        test_offset = 20
        p = 0

        for i_sur in range(4,0,-1):
            
            [surr_pos_x, surr_pos_y] = psychopy.misc.pol2cart(
                60,
                (i_sur*40)-85
            )
            
           
            for i_surr2 in range(i_sur):
                
                if shapeComb[p] == 0 :
                
                    shape = psychopy.visual.Circle(
                        win=win,
                        units="pix",
                        edges=128,
                        radius = 10,
                        #lineColor = 'grey',
                        pos = [surr_pos_x-(i_surr2*40)+test_offset, -surr_pos_y]
                        )
                
                else:
                    shape =psychopy.visual.Polygon(
                        win=win,
                        units="pix",
                        edges=3,
                        radius = 13.5,
                        #lineColor = 'grey',
                        pos = [surr_pos_x-(i_surr2*40)+test_offset, -surr_pos_y-2.5]
                        
                        )
                 
                
                #row.append(triangle)
                shape.fillColor = color
                row.append(shape)
                p = p+1



        for comp in range (len(row)):
            
            #for c in trialComponents[3][comp]:
                #triangle.draw()
                [x,y] = row[comp].pos
                row[comp].fillColor = color
                row[comp].pos = [x,y+15]
                row[comp].draw()          
                


        win.getMovieFrame(buffer="back")
        
        dir =  (os.getcwd() + '/blue/T_blue_%d%d/'% (ntriangles*10,ncircles*10))
        if not os.path.exists(dir):
            os.makedirs(dir)
        win.saveMovieFrames(dir+ "%d.png" % j)

        win.flip()

    win.getMovieFrame()
psychopy.event.waitKeys()

win.close()
