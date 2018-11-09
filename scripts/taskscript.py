# ------ IMPORTED LIBRARIES--------   
import psychopy.visual
import psychopy.event
import psychopy.misc
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from random import shuffle 
import random
import os
import coloredlogs
import logging 
coloredlogs.install() 


# ------ EXPERIMENT INFORMATION -------- 
expName = 'Hysterisis'   
expInfo = {'participant':'', 'session':'001','gender':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
expInfo['date'] = data.getDateStr(format="%B %d, %Y") 
expInfo['expName'] = expName

# ------ IF USER QUIT THE PROGRAM --------  
if dlg.OK == False:
    core.quit() 

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = os.getcwd() + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
keyTone = sound.Sound(u'A', secs = .2)


# ------ SET UP THE WIDNOW --------   
myWin = visual.Window(fullscr=False, color='white')

#| Small | Big | Switching| Switching | Small | Big | Switching | Switching
order = ['switching', 'big', 'small', 'switching','small', 'big','switching', 'switching']
cueBlueGlobal =  {'small':"/slides/blue global", 'big': "/slides/green local"}
cueGreenGlobal = {'small':"\\slides\\green global", 'big': "\\slides\\blue local"}

# ------- SMALL BLOCK AND BIG BLOCK ARRAY -------  
blockdir = cueBlueGlobal
blocks = []
switchingBlocks = []
smallBlocks = []
bigBlocks = []
fblocks = []
responses = []

#keys used by the user for resposne
#by convention first key is for circles, second key is for triangles
keys_of_interest = ['m','n']
#max waiting time for response
wait_time = 2.9
#time between slides
wait_time_slides = 0.1
#time between blocks
wait_time_blocks = 10
#number of slides per ratio (block size is blocksz*10 )
blocksz = 8 

#ratios [0100,1000, 1090, 2080,3070,4060,6040,7030,8020, 9010, 0100,1000]
#1 designates ratio is inspected, 0 designates ratio is not inspected
ratios = [1,1,1,0,1,1,1,1,0,1]

#design block for every element in order, and call it?
#for each block get randomized ratios (8 of each ratio)
#blue cue: focus on small
#green cue : focus on big


# ------ CREATE INSTRUCTION SLIDES FROM BLUE GLOBAL DIRECTORY  ---------   
def createInstructionSlides(): 
    instrSlidesDir = ""
    if blockdir == cueBlueGlobal :
        instrSlidesDir =   os.getcwd() + "/blueGlobal"
    else:
        instrSlidesDir =   os.getcwd() + "/greenGlobal"
    instrSlides = [  os.path.join(instrSlidesDir, instruction) for instruction in os.listdir(instrSlidesDir) ]
    continueRoutine = True

    # ---- Print out instructions on the slides ---- 
    for instrPath in instrSlides:
        if os.path.exists(instrPath):  
            continueRoutine = True
            event.clearEvents(eventType='keyboard')
            stimulus = visual.ImageStim(myWin, image=instrPath,mask=None, pos=(0.0,0.0))
            stimulus.size = 2   # size to display the instructions 
            stimulus.draw()
            myWin.flip()

            # ----- Press enter to move onto next slide ---- 
            while continueRoutine:
                theseKeys = event.getKeys()
                if theseKeys:
                    continueRoutine = False
        else:
            logger.critical("Unable to find the instruction path. There should be a folder name Blue Global within scripts")

# ------ CREATE SWITCH BLOCKS  ---------  
def createSwitchBlocks(): 
    global bigBlocks; global smallBlocks; global switchingBlocks; 
    for cue in blockdir:
        directory = os.getcwd() + blockdir[cue]
        i = 0
        for folder in os.listdir(directory):
            if (ratios[i] == 1 ):
                ratio = os.path.join(directory, folder) 
                ratiosamples = [ os.path.join(ratio, sample) for sample in os.listdir(ratio) ]
                if cue == 'small':
                    rs = random.sample(range(0, 14), blocksz)
                    smallBlocks.append([ratiosamples[f] for f in rs ])
                if cue == 'big':
                    rb = random.sample(range(0, 14), blocksz)
                    bigBlocks.append([ratiosamples[f] for f in rb ])
            i = i + 1


    # ------ Shuffle the slides -------  
    smallBlocks = [y for x in smallBlocks for y in x]   
    bigBlocks = [y for x in bigBlocks for y in x] 
    shuffle(bigBlocks)
    shuffle(smallBlocks)
    for i,j in zip(smallBlocks,bigBlocks):
        switchingBlocks.append(i)
        switchingBlocks.append(j)

    # ------- Slice the blocks --------- 
    if len(switchingBlocks) > 0: 
        half_len = int(len(switchingBlocks)/2) 
        switchingBlocks = switchingBlocks[0:half_len]
    else:
        logger.critical("Unable to get switching blogs")


# --------- CALLING ALL THE FUNCTIONS HERE -------- 
createInstructionSlides()
createSwitchBlocks()

#directory = os.getcwd() + '\\slides\\blue global'
#for every ratio get 8 slides
trials1Clock = core.Clock()


for block in range(len(order)):
    blocks = []    
    if order[block] == 'switching':
        fblocks = switchingBlocks
    elif order[block] == 'small':
        fblocks = smallBlocks
    else:
        fblocks = bigBlocks
    
    
    thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename +"_" + order[block])
   

    for el in range(len(fblocks)):

        stim = fblocks[el]
        stimulus = visual.ImageStim(myWin, image=stim)
        
        stimulus.draw()
        #reset response timer
        myWin.flip()
        trials1Clock.reset()
        
        #resp_time_start = core.getTime() 
        resp_key = event.waitKeys(maxWait = wait_time, keyList=keys_of_interest, timeStamped=trials1Clock)
        #print resp_key , len(resp_key)
        
        if resp_key:
            if len(resp_key) > 0:
                keyTone.play()
                
            core.wait(wait_time - resp_key[0][1])
            myWin.flip()
            core.wait(wait_time_slides)
            
        else:
            resp_key = [['', '']]

        print (resp_key)
        r = fblocks[el].rfind('\\')

        triangle_ratio = fblocks[el][r-4:r][:2]
        circle_ratio = fblocks[el][r-4:r][2:]

        thisExp.addData ('Sample', fblocks[el][r-4:r])      
        thisExp.addData ('Response', resp_key[0][0])
        thisExp.addData('RT', resp_key[0][1])

        # print ("Triangle ratio", triangle_ratio..rstrip('.'))
        # print ("Circle ratio", circle_ratio)
        
        # print(type(triangle_ratio)) 
        # print(type(circle_ratio))  

            
        if resp_key[0][0] == keys_of_interest[0] and int(circle_ratio.rstrip('.')) > int(triangle_ratio.rstrip('.')):
            #if response was majority is circles and it's correct
            thisExp.addData('Correct', 1)
        elif resp_key[0][0] == keys_of_interest[1] and int(circle_ratio.rstrip('.')) < int(triangle_ratio.rstrip('.')):
            #if response was majority is triangles and it's correct
            thisExp.addData('Correct', 1)
        else:
            thisExp.addData('Correct', 0)

        
        
#         thisExp.nextEntry()
        
   
#         #thisExp.addData ( 'RT', resp_time1)

#             # check for quit (the Esc key)
#         if event.getKeys(keyList=["escape"]):
#             thisExp.saveAsWideText(filename+ "_" + order[block] +'.csv')
#             thisExp.saveAsPickle(filename)
#             thisExp.abort()  # or data files will save again on exit
#             myWin.close()
#             core.quit()
#             #break

#     thisExp.saveAsWideText(filename+ "_" + order[block] +'.csv')
#     core.wait(wait_time_blocks)
    
    


# thisExp.saveAsPickle(filename)
# # make sure everything is closed down
# thisExp.abort()  # or data files will save again on exit
# myWin.close()
# core.quit()
 
 
 #https://groups.google.com/forum/#!topic/python-excel/s8uO999EDU0

