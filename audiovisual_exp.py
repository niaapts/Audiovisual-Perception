#Most of this works
#I need to change: audio file
#unsure of (duration between flashes and beeps)

import random
from expyriment import design, control, stimuli, io 

N_TRIALS = 10
NUM_FLASH=3
NUM_BEEPS = 5  # Variable number of auditory beeps
FLASH_DURATION= 50
BEEP_INTERVAL= 57
MAX_RESPONSE_DELAY = 2000
aud="click.wav" #I used your audio file, the one I had before didn't play

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

audio_stimulus = stimuli.Audio(aud)
visual_stimulus = stimuli.Circle(radius=50, position=eccentricity_screen_coordinates, colour=(255, 255, 255))  #stimuli positied according to the eccentricity
blankscreen = stimuli.BlankScreen()

#Instructions for the participants, variables for data file
instructions = stimuli.TextScreen("Instructions",
    f"""You will see a circle accompanied by sound. 
Your task is to report the number of flashes you think you saw after each trial.

There will be {N_TRIALS} trials in total.

Press the spacebar to start.""")

exp.add_data_variable_names(["trial", "reported_flashes"])

# Start the experiment
control.start()

# Present visual and audio stimuli N times


# First display visual stimuli random amount of times in each trial
for trial in range(N_TRIALS):
    rand_flash=random.randint(1, NUM_FLASH)
    rand_beeps=random.randint(1, NUM_BEEPS)
    for f in range(rand_flash):
        exp.screen.clear()
        blankscreen.present()
        visual_stimulus.present()
        exp.clock.wait(FLASH_DURATION)

# Present audio stimuli after each flash, with randomized number of beeps between 1 and 5
        for i in range(rand_beeps):
            audio_stimulus.present()
            exp.clock.wait(BEEP_INTERVAL)

 
# Get and record number of flashes from the participant as an integer (I used ChatGPT for this as well)
    exp.screen.clear()
    text_input = io.TextInput("How many flashes did you see?")
    response = text_input.get()
    exp.data.add([trial, response])


# End the experiment
control.end()


