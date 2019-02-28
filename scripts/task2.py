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
from glob import glob 
from sys import platform 

# Experiment name and information 
experiment_name = 'Hysterisis'   
experiment_info = {
    'participant':'', 
    'session':'001',
    'gender':'', 
    'experiment_name': experiment_name, 
    'date': data.getDateStr(format="%B %d, %Y")  
}

# Open dialogue to ask participant information (gender, participant name)
dialogue = gui.DlgFromDict(dictionary=experiment_info, title=experiment_name) 

# Window object screen to display the slides 
window = visual.Window(fullscr=False, color='white') 

# Clock to count time of response and movement between slides 
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

# Preset conditions (whether to run preset parameters or random slides)
preset_conditions = True

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


# ----------- CREATE SWITCHING BLOCKS BASED ON PRESET CONDITIONS ------- 
    # 35 blue of randomize low / high contrast, 35 green of randomize low / high contrast
    # 35 switches of blue / green image (blue-green-blue-green-blue-green is fixed, but ratio is random)
 
def create_preset_blocks():
    experiment_blocks = []
    

    # Set either (blue global, green local) or (green global, blue local)
    general_cue = cue_blue_global 

    # Preset designated ratio for low contrast and high contrast here 
    low_contrast = ['4060', '6040']   
    high_contrast = ['2080', '8020'] 
    blues = []                              # containing all slides in 4060, 6040, 2080, 8020 for blue 
    greens = []                             # containing all slides in 4060, 6040, 2080, 8020 for green  

    for ratio in (low_contrast + high_contrast):
        blue_path = os.path.join(blue_global_folder, ratio)
        green_path = os.path.join(green_local_folder, ratio)
        blues.append(blue_path)
        greens.append(green_path)

    # Store all the image path from all 8 folders   
    all_slides = []                          
    for slide_path in (blues + greens):
       path_sub_arr = glob(os.path.join(slide_path, '*'))
       all_slides += path_sub_arr

    # Pick number of slides to run experiment here 
    number_of_slides = 10   

    # Generate a random slide (either blue of random contrast, or green of random contrast)
    def generate_random_slides(color):
        slides_container = []
        for i in range(0, number_of_slides): 
            if color == 'blue':
                slides = [slide for slide in all_slides if 'blue' in slide]
            else:
                slides = [slide for slide in all_slides if 'green' in slide]  
            random_slide = random.choice(slides)  
            slides_container.append(random_slide)
        return slides_container
        

    # Return an array containing X amount of random switching slides
    # It will present a blue slide then green slide then blue slide then green slide ... 
    # But the ratio [high_contrast, low_contrast] is randomize 
    def generate_switching_slide():
        blue_slides = [slide for slide in all_slides if 'blue' in slide] 
        green_slides = [slide for slide in all_slides if 'green' in slide]
        slides_container = []
        for i in range(0, number_of_slides): 
            if i % 2 == 0: 
                random_slide = random.choice(blue_slides)
            else:
                random_slide = random.choice(green_slides)
            slides_container.append(random_slide)
        return slides_container
            
    # An array contain both high contrast + low contrast slides that are blue 
    blue_experiment_slides = generate_random_slides('blue')
 
    # An array contain both high contrast + low contrast slides that are green 
    green_experiment_slides = generate_random_slides('green')

    # Switching slides 
    switching_slides = generate_switching_slide()
     
     # Run Trial Experiment Here 
    order_directions = {
        'blue_experiment_slides': blue_experiment_slides, 
        'green_experiment_slides': green_experiment_slides, 
        'switching_slides': switching_slides  
    }

    # Set the order of the array for the experiment 
    order_array = ['blue_experiment_slides', 'green_experiment_slides', 'switching_slides'] 
    run_trial_experiment(order_directions, order_array)


# Add a blank 100 ms white screen 


# -------------- CREATE SWITCHING BLOCKS AND SHUFFLE THEM ----------- 
def create_random_blocks():

    # Global variables goes here 
    global small_blocks; global big_blocks; global switching_blocks
    block_size = 8  

    # Initialize the block list here from either cue_blue_global or cue_green_global 
    general_cue = cue_blue_global 
 
    # True designates ratio is inspected, False designates ratio is not inspected 
    inspected_array = [True, True, True, False, True, True, True, True, False, True]

    # For local or global folder, get array that contain all folders [1090]
    for cue, path in general_cue.items():
        local_global_folder = os.path.join(os.getcwd(), path)

        # Get pictures from all kind of ratios 
        ratios = os.listdir(local_global_folder) 
        for is_inspected in inspected_array: 
            for ratio in ratios:
                if is_inspected == True: 
                    ratio_folder = os.path.join(local_global_folder, ratio)
                    png_picture = [ os.path.join(ratio_folder, png) for png in os.listdir(ratio_folder) ] 

                    # Generate 8 (block_size) random number betweeen 0 and 14 
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


    # Call Run Trial Experiment Here 
    order_directions = {'switching': switching_blocks, 'small': small_blocks, 'big': big_blocks }
    order_array = ['switching', 'big', 'small', 'switching','small', 'big','switching', 'switching'] 
    run_trial_experiment(order_directions, order_array)


# -------- RUN THE TRIAL EXPERIMENT  --------  
def run_trial_experiment(order_directions, order_array):

    # Global variables
    global small_blocks; global big_blocks; global switching_blocks; 
    global experiment_name; global experiment_info   

    # Local variables 
    experiment_blocks = []                          # can be switching block, small or big block 
    wait_time_response = 2.5                        # time waiting for response 
    wait_time_slides = 0.1                          # time waiting between slides 
    wait_time_blocks = 10.0                         # time waiting between blocks 
    keys = ['c','t']                                # m = circle, n = triangles 
    key_tone = sound.Sound(u'A', secs = .2)         # key sound 

    # Set the file name for the output that contains the participant's infromation 
    filename = os.getcwd() + os.sep + u'data/%s_%s_%s' % (experiment_info['participant'], experiment_name, experiment_info['date'])  

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
            check_user_response(image, keys, this_experiment, response_key, wait_time_response)
        
        # Save each session at the experiment after finishing 
        this_experiment.saveAsWideText(filename+ "_" + order +'.csv')
        core.wait(wait_time_blocks) 
    
    # Finish experiment and exit 
    this_experiment.saveAsPickle(filename)
    this_experiment.abort()  
    window.close()
    core.quit()
  
# ------------ GET THE RATIO OF TRIANGLES AND CIRCLE AND CHECK USER RESPONSE ---------- 
def check_user_response(image_path, keys, this_experiment, response_key, wait_time_response):
    keyword = 'local/' if 'local/' in image_path else 'global/'
    index = image_path.rfind(keyword) 

    # Find the ratio number [1090, 2080...etc.] from the image path 
    if index != -1:
        ratio = image_path[index+len(keyword):index+len(keyword)+4] 
        this_experiment.addData ('Sample', ratio)      
        this_experiment.addData ('Response', response_key[0][0])
        if response_key[0][1] == '':
            this_experiment.addData('RT', wait_time_response)
        else: 
            this_experiment.addData('RT', response_key[0][1]) 
       

        # Get the number of triangles and circles displayed in picture 
        num_of_triangles =  int(ratio[0]); num_of_circles = int(ratio[2])  

        # Check if user response correctly by press m for more circles and n for more triangles  
        if response_key[0][0] == keys[0] and num_of_circles >  num_of_triangles: 
            this_experiment.addData('Correct', 1) 
        elif response_key[0][0] == keys[1] and num_of_circles < num_of_triangles: 
            this_experiment.addData('Correct', 1)  
        else:
            this_experiment.addData('Correct', 0)  
        this_experiment.nextEntry() 



# ------------- CALL ALL THE MAIN FUNCTIONS DOWN HERE -------------- 
# Create instruction slids and displayed on screen 

open_instructions_slide()

# Randomly create switching blocks or preset them based on conditions 
if preset_conditions == True: 
    create_preset_blocks()
else: 
    create_random_blocks()



# Have a instruction slide for user to press when ready 
# Put the maximum time in the slot (2.5 second for recorded time)
# Take the experiment data 



# Okay I take two folder (2080 and 4060) so number of circles always more than triangle
# Do I mix (2080 + 8020 + 4060 + 6040) together??? 