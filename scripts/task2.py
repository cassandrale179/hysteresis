# Libraries 
import psychopy.visual
import psychopy.event
import psychopy.misc
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from random import shuffle 
import random
import os
import re 
import sys 
from sys import platform 

# ----------------- ALL GLOBAL VARIABLES GOES HERE -------------- 
experiment_name = 'Hysterisis'   
experiment_info = {'participant':'', 'session':'001','gender':''}
experiment_info['date'] = data.getDateStr(format="%B %d, %Y")  

# Window object screen to display experiemnt slides 
window = visual.Window(fullscr=False, color='white') 
clock = core.Clock()

# Directories to all the four folders within the slide folders 
blue_global_folder = os.path.join("slides", "blue global")  
blue_local_folder = os.path.join("slides", "blue local")  
green_global_folder = os.path.join("slides", "green global")   
green_local_folder = os.path.join("slides", "green local")  

# Blue global folder or green global folder 
cue_blue_global =  { 'small': blue_global_folder, 'big': green_local_folder }
cue_green_global = { 'small': green_global_folder, 'big':  blue_local_folder } 

# Global variables 
small_blocks, big_blocks, switching_blocks = [], [], []  

# Preset designated ratio here 
preset_ratio = []

# --------------- DISPLAY THE INSTRUCTION SLIDES -------------- 
def open_instructions_slide(): 
    instruction_slides = [ os.path.join("instructions", slide) for slide in os.listdir("instructions")]

    # For each slide in instruction slides, draw them 
    for slide in instruction_slides:
        display_slide = True 
        event.clearEvents(eventType='keyboard') 
        stimulus = visual.ImageStim(window, image=slide,mask=None, pos=(0.0,0.0)) 
        stimulus.size = 2 
        stimulus.draw()
        window.flip()

        # Move onto the next slide by awaiting user press key to response 
        while display_slide: 
            keyboard_pressed = event.getKeys()
            display_slide = False if keyboard_pressed else True 


# -------------- CREATE SWITCHING BLOCKS AND SHUFFLE THEM ----------- 
def create_switching_blocks():

    # Global variables goes here 
    global small_blocks; global big_blocks; global switching_blocks
    block_size = 8  

    # Initialize the block list here from either cue_blue_global or cue_green_global 
    general_cue = cue_blue_global 
 
    # True designates ratio is inspected, False designates ratio is not inspected 
    inspected_array = [True, True, True, False, True, True, True, True, False, True]

    # For local or global folder, get array that contain all folders [00]
    for cue, path in general_cue.items():
        local_global_folder = os.path.join(os.getcwd(), path)

        # Filter out if there is a preset ratio here 
        ratios = preset_ratio if preset_ratio != [] else os.listdir(local_global_folder) 
        
        for is_inspected in inspected_array: 
            for ratio in ratios:
                if is_inspected == True: 
                    ratio_folder = os.path.join(local_global_folder, ratio)
                    png_picture = [ os.path.join(ratio_folder, png) for png in os.listdir(ratio_folder) ] 
                    if cue == 'small':
                        random_range = random.sample(range(0, 14), block_size)
                        small_blocks.append([png_picture[i] for i in random_range])
                    if cue == 'big': 
                        random_range = random.sample(range(0, 14), block_size)
                        big_blocks.append([png_picture[i] for i in random_range]) 
                
    # Shuffle the blocks, append in alternative order then take the first half of switching blocks 
    small_blocks = [y for x in small_blocks for y in x]   
    big_blocks = [y for x in big_blocks for y in x] 
    shuffle(big_blocks); shuffle(small_blocks) 
    for i,j in zip(small_blocks,big_blocks):
        switching_blocks.append(i)
        switching_blocks.append(j) 
    switching_blocks = switching_blocks[0:int(len(switching_blocks)/2)] 

# -------- RUN THE TRIAL EXPERIMENT BY CREATING EXPERIMENT BLOCK --------  
def run_trial_experiment():

    # Global variables goes here 
    global small_blocks; global big_blocks; global switching_blocks
    filename = os.getcwd() + os.sep + u'data/%s_%s_%s' % (experiment_info['participant'], experiment_name, experiment_info['date'])   

    # List of local variables (wait time and key)
    experiment_blocks = []                      # can be switching block, small or big block 
    wait_time_response = 10.9                    # time waiting for response 
    wait_time_slides = 10.0                      # time waiting between slides 
    wait_time_blocks = 10.0                       # time waiting between blocks 
    keys = ['m','n']                            # m = circle, n = triangles 
    key_tone = sound.Sound(u'A', secs = .2)

    # Order of the blocks 
    order_directions = {'switching': switching_blocks, 'small': small_blocks, 'big': big_blocks }
    order_array = ['switching', 'big', 'small', 'switching','small', 'big','switching', 'switching'] 

    # For order (small, big, switching) in array 
    for order in order_array:
        experiment_blocks = order_directions[order]  
        this_experiment = data.ExperimentHandler (
            name=experiment_name, version='',
            extraInfo=experiment_info, runtimeInfo=None,
            savePickle=True, saveWideText=True,
            dataFileName=filename +"_" + order 
        )  

        # For each image in experiment block, displayed them 
        for image in experiment_blocks: 
            stimulus = visual.ImageStim(window, image=image)
            stimulus.draw() 
            window.flip()
            clock.reset() 
            response_key = event.waitKeys(maxWait = wait_time_response, keyList=keys, timeStamped=clock) 

            # If user response by pressing m for circles and n for triangles 
            if response_key: 
                key_tone.play() 
                core.wait(wait_time_response - response_key[0][1]) 
                window.flip()
                core.wait(wait_time_slides) 
            else: 
                response_key = [['', '']] 

            # Check if user response correctly 
            check_user_response(image, keys, this_experiment, response_key)
    
        this_experiment.saveAsWideText(filename+ "_" + order[block] +'.csv')
        core.wait(wait_time_blocks) 
    
    # Finish experiment and exit 
    this_experiment.saveAsPickle(filename)
    this_experiment.abort()  
    window.close()
    core.quit()
  
# ------------ GET THE RATIO OF TRIANGLES AND CIRCLE AND CHECK USER RESPONSE ---------- 
def check_user_response(image_path, keys, this_experiment, response_key):

    keyword = 'local/' if 'local/' in image_path else 'global/'
    index = image_path.rfind(keyword) 
    if index != -1:
        ratio = image_path[index+len(keyword):index+len(keyword)+4] 

        this_experiment.addData ('Sample', ratio)      
        this_experiment.addData ('Response', response_key[0][0])
        this_experiment.addData('RT', response_key[0][1]) 
    
        num_of_triangles =  int(ratio[0])
        num_of_circles = int(ratio[2])  

        if response_key[0][0] == keys[0] and num_of_circles >  num_of_triangles: 
            # print ("more circles than triangles")
            this_experiment.addData('Correct', 1) 
        elif response_key[0][0] == keys[1] and num_of_circles < num_of_triangles: 
            # print ("more triangles than circles")
            this_experiment.addData('Correct', 1)  
        else:
            this_experiment.addData('Correct', 0)  
        this_experiment.nextEntry() 

# Call all the functions here 
open_instructions_slide()
create_switching_blocks()
run_trial_experiment()



