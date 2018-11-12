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
import re 
from sys import platform 
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

thisExp = ''


# ------ CREATE INSTRUCTION SLIDES FROM BLUE GLOBAL DIRECTORY  ---------   
def createInstructionSlides(): 
    instrSlidesDir = ""
    if blockdir == cueBlueGlobal :
        instrSlidesDir =   os.getcwd() + "/blueGlobal"
    else:
        instrSlidesDir =   os.getcwd() + "/greenGlobal"
    instrSlides = [ os.path.join(instrSlidesDir, instruction) for instruction in os.listdir(instrSlidesDir) ]
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


# ------ CREATE FBLOCKS TO BE DISPLAYED (CIRCLE / TRIANGLE ) -----   
# @return: an array of file paths which contain .png files of triangle and circle 
def createFblocks(): 
    global thisExp
    fblocks = [] 
    trials1Clock = core.Clock()

    # Create switching, small and big blocks 
    for block in range(len(order)):
        blocks = []     
        if order[block] == 'switching':
            fblocks = switchingBlocks
        elif order[block] == 'small':
            fblocks = smallBlocks
        else:
            fblocks = bigBlocks
        
        # Create experiment object 
        thisExp = data.ExperimentHandler(
            name=expName, version='',
            extraInfo=expInfo, runtimeInfo=None,
            savePickle=True, saveWideText=True,
            dataFileName=filename +"_" + order[block]
        )
    
        # Display images onto the screen 
        displayImages(fblocks,  trials1Clock)  

        # Store data into a csv file 
        thisExp.saveAsWideText(filename+ "_" + order[block] +'.csv')
        core.wait(wait_time_blocks) 
        

# ------ DISPLAY IMAGE OF CIRCLE AND TRIANGLE ONTO THE SCREEN AND GET USER RESPONSE ------ 
def displayImages(fblocks, trials1Clock):
    global thisExp

    # Draw the stimulus onto the screen (the green / blue circle triangle )
    for image in fblocks:
        stimulus = visual.ImageStim(myWin, image=image)
        stimulus.draw() 
        myWin.flip()
        trials1Clock.reset()
        resp_key = event.waitKeys(maxWait = wait_time, keyList=keys_of_interest, timeStamped=trials1Clock)

    
        # If user press m or n, store the data, else leave it black ['', '']
        if resp_key:
            if len(resp_key) > 0:
                keyTone.play()
            core.wait(wait_time - resp_key[0][1])
            myWin.flip()
            core.wait(wait_time_slides)
        else:
            resp_key = [['', '']] 
     

        # Get ratio and store sample, response, and response time 
        ratio = getRatio(fblocks, image)
        thisExp.addData ('Sample', ratio)      
        thisExp.addData ('Response', resp_key[0][0])
        thisExp.addData('RT', resp_key[0][1]) 


        # Number of triangles 
        triangles = int(ratio[0]) 
        circles = int(ratio[2]) 
        

        # If user press n and there are more circles than triangle, that's correct 
        # If user press m and there are less circles than triange, that's correct 
        if resp_key[0][0] == keys_of_interest[0] and circles > triangles:
            thisExp.addData('Correct', 1)
        elif resp_key[0][0] == keys_of_interest[1] and circles < triangles:
            thisExp.addData('Correct', 1)
        else:
            thisExp.addData('Correct', 0)
        thisExp.nextEntry()

    
        # If user want to escape the programs 
        if event.getKeys(keyList=["escape"]):
            thisExp.saveAsWideText(filename+ "_" + order[block] +'.csv')
            thisExp.saveAsPickle(filename)
            thisExp.abort()  # or data files will save again on exit
            myWin.close()
            core.quit()
           
# ------------- THIS FUNCTION CALCUALTE THE RATIO OF TRIANGLE AND CIRCLES BASED ON FILE PATH -----------------
def getRatio(fblocks, imagePath):
    possibleRatios = ['0100','1000', '1090', '2080','3070','4060','6040','7030','8020', '9010', '0100','1000']
    ratio = ''
    if 'local/' in imagePath:
        index = imagePath.rfind('local/')
        ratio = imagePath[index+len('local/'):index+len('local/')+4]
    elif 'global/' in imagePath:
        index = imagePath.rfind('global/') 
        ratio = imagePath[index+len('global/'):index+len('global/')+4]
    if ratio not in possibleRatios:
        logger.critical ("Invalid ratio of triangles and circles ")
    return ratio 


# --------- CALLING ALL THE FUNCTIONS HERE -------- 
createInstructionSlides()  
createSwitchBlocks()
createFblocks() 


# ------- QUITTING THE PROGRAM HERE ------ 
thisExp.saveAsPickle(filename)
thisExp.abort()  
myWin.close()
core.quit()
  