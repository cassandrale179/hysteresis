# hysteresis
Directory to store tasks related to hysteresis flexibility 

## Task Design

### General Design
- Each task was administered in eight blocks of 80 trials. Each trial was 2.9s long, followed immediately by a 0.1s intertrial interval of a blank white screen. Thus, each block was 4 minutes long. 
- There were three block types: small shapes, big shapes, and switching. The blocks occured in an order such as:
     | Small | Big | Switching| Switching | Small | Big | Switching | Switching
- For each list, Switching was always the last block in the first 1:3 and last 4:6. However, Small and Big were counterbalanced across subjects. 
  - 50% of people received Big first, and 50% received Small first. 
  - If Big was first in the 1:3 blocks, then it was also first in the 4:6 blocks. 
  - The mapping between the stimulus color and big or small was also counterbalanced such that green = big in 50% of subjects, and blue = big in 50% of subjects.
- The trials were sampled along the dimension of ratios such that we had a reasonable number of trials per level within each of the Small, Big, and Switching conditions to estimate median response times. 
- Because there were a total of 160 trials per condition (320 per switching condition), we sampled 16 trials at each of the ratios per condition distributed randomly within each block with the constraint that 8 trials per ratio were administered within each block.


### Ratio
Within the folder blueGlobal, there are 10 folders [0100,1000, 1090, 2080,3070,4060,6040,7030,8020, 9010, 0100,1000]
- 0100 contains purely circles, and 1000 contains all triangles
- For the rest, the first digit denotes number of triangles are there, and the third digit denotes numbers of circles 


## Installation and Requirements
- [Python v3.0](https://www.python.org/downloads/) or higher
- [psychopy](http://www.psychopy.org/):  an open-source application for  neuroscience, psychology and psychophysics experiments 
- [coloredlogs](https://github.com/xolox/python-coloredlogs): enables colored terminal output for Python's logging module 
```
pip install psychopy 
pip install coloredlogs 
> Requirement already satisfied: psychopy in /usr/local/lib/python3.7/site-packages (1.90.3) 
``` 
- If you have two Python versions on computer, use pip3 
