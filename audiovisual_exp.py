#Most of this works
#I need to change: audio file
#unsure of (duration between flashes and beeps)

import random
from expyriment import design, control, stimuli, io, misc

N_TRIALS = 15
MAX_FLASH=4
MAX_BEEPS = 4 # Variable number of auditory beeps
FLASH_DURATION= 17
FLASH_INTERVAL=50
BEEP_INTERVAL= 57
MAX_RESPONSE_DELAY = 2000

beep_num= {
    1: 'beep-1.wav',
    2: 'beep-2.wav',
    3: 'beep-3.wav',
    4: 'beep-4.wav'}

#Calculate the screen coordinates for 5 degrees eccentricity, I used the numbers that ChatGPT provided to me
eccentricity_degrees = 5
pixels_per_degree = 28
viewing_distance_cm = 57

#5 degrees at horizontal eccentricity
eccentricity_pixels = eccentricity_degrees * pixels_per_degree
eccentricity_screen_coordinates = (eccentricity_pixels, 0)  

exp = design.Experiment(name="Audiovisual", text_size=40)
control.set_develop_mode(on=True)

control.initialize(exp)

visual_stimulus = stimuli.Circle(radius=50, position=eccentricity_screen_coordinates, colour=(255, 255, 255))  #stimuli positied according to the eccentricity
blankscreen = stimuli.BlankScreen()

#Instructions for the participants, variables for data file
instructions = stimuli.TextScreen("Instructions",
    f"""You will see a circle accompanied by sound. 
Your task is to report the number of flashes you think you saw after each trial.

There will be {N_TRIALS} trials in total.

Press the spacebar to start.""")

exp.add_data_variable_names(["trial", "beeps", "flashes", "response_flashes"])

#A list of flash and beep combinations, randomized and saved.
combinations = []
for f in range(1, MAX_FLASH + 1):
    for b in range(1, MAX_BEEPS + 1):
        combinations.append((f, b))

combinations.append((1,1))
combinations.append((1,2))
combinations.append((1,3))
combinations.append((1,4))
combinations = combinations * 2

random.seed(42)

random.shuffle(combinations)

#fixation cross added

fixation_cross = stimuli.FixCross()

# Start the experiment
control.start()

# Present visual and audio stimuli according to the pairs in combinations variable
"""for trial, (flashes, beeps) in enumerate(combinations, start=1):
    exp.screen.clear()
    blankscreen.present()
    stimuli.Audio(beep_num[1])
    exp.clock.wait(16)
    visual_stimulus.present()
    exp.clock.wait(FLASH_DURATION)
    if flashes>=2:
        beep_pr=stimuli.Audio(beep_num[beeps])
        beep_pr.play()
        exp.clock.wait(BEEP_INTERVAL)
        flash_pr=stimuli.Circle(combinations[flashes])
        exp.clock.wait(FLASH_DURATION)
        exp.clock.wait(FLASH_INTERVAl)"""
    
for trial, (flashes, beeps) in enumerate(combinations, start=1):
    
    fixation_cross.present()
    exp.clock.wait(1000)  # Display fixation cross for 1 second
    blankscreen.present()

    beep_pr = stimuli.Audio(beep_num[1])
    beep_pr.play()
    exp.clock.wait(16)  # Wait for 16 ms before the first flash
    visual_stimulus.present()
    exp.clock.wait(FLASH_DURATION)
    
 # Present additional flashes and beeps based on the combinations
#I get stuck at this stage, can't figure out how to simultaneously present both after the initial stimuli (first beep and flash)
#also only shows flash once even though it says other numbers in data file. 
    for b in range(beeps):
        beep_pr = stimuli.Audio(beep_num[beeps])
        beep_pr.play() 
        exp.clock.wait(BEEP_INTERVAL)  # Wait for the specified beep interval

    for f in range(flashes):
        visual_stimulus.present()
        exp.clock.wait(FLASH_DURATION)  # Wait for the duration of the flash
        exp.screen.clear()
        visual_stimulus.present()
        exp.clock.wait(FLASH_INTERVAL)  # Wait for the specified flash interval

    exp.screen.clear()
    text_input = io.TextInput("How many flashes did you see?")
    response = text_input.get()
    exp.data.add([trial, beeps, flashes, response])


# End the experiment
control.end()
