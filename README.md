# hysteresis
Directory to store tasks related to hysteresis flexibility 

## Task Design
- Each task was administered in eight blocks of 80 trials. Each trial was 2.9s long, followed immediately by a 0.1s intertrial interval of a blank white screen. Thus, each block was 4 minutes long. 
- There were three block types: small shapes, big shapes, and switching. The blocks occured in an order such as:
     | Small | Big | Switching| Switching | Small | Big | Switching | Switching
- For each list, Switching was always the last block in the first 1:3 and last 4:6. However, Small and Big were counterbalanced across subjects. 
  - 50% of people received Big first, and 50% received Small first. 
  - If Big was first in the 1:3 blocks, then it was also first in the 4:6 blocks. 
  - The mapping between the stimulus color and big or small was also counterbalanced such that green = big in 50% of subjects, and blue = big in 50% of subjects.
- The trials were sampled along the dimension of ratios such that we had a reasonable number of trials per level within each of the Small, Big, and Switching conditions to estimate median response times. 
- Because there were a total of 160 trials per condition (320 per switching condition), we sampled 16 trials at each of the ratios per condition distributed randomly within each block with the constraint that 8 trials per ratio were administered within each block.


## Installation
- Make sure psychopy is installed on computer. Currently this is compatible with Python v3.7 
```
sudo pip3 install psychopy 
> Requirement already satisfied: psychopy in /usr/local/lib/python3.7/site-packages (1.90.3) 
``` 

