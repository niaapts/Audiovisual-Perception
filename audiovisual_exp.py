#Most of this works
#I need to change: audio file
#unsure of (duration between flashes and beeps)

import random
from expyriment import design, control, stimuli, io, misc

N_TRIALS = 15
MAX_FLASH=4
MAX_BEEPS = 4 # Variable number of auditory beeps
FLASH_DURATION= 17
FLASH_INTERVAL=55
MAX_RESPONSE_DELAY = 2000


#Calculate the screen coordinates for 5 degrees eccentricity, I used the numbers that ChatGPT provided to me
eccentricity_degrees = 5
pixels_per_degree = 28
viewing_distance_cm = 57

#5 degrees at horizontal eccentricity
eccentricity_pixels = eccentricity_degrees * pixels_per_degree
eccentricity_screen_coordinates = (eccentricity_pixels, 0)  

exp = design.Experiment(name="Audiovisual", text_size=40)
control.set_develop_mode(on=True)
#expyriment.control.default.window_mode=True

control.initialize(exp)

beeps= {
    1: stimuli.Audio('beep-1.wav'),
    2: stimuli.Audio('beep-2.wav'),
    3: stimuli.Audio('beep-3.wav'),
    4: stimuli.Audio('beep-4.wav')}


visual_stimulus = stimuli.Circle(radius=50, position=eccentricity_screen_coordinates, colour=(255, 255, 255))  #stimuli positied according to the eccentricity
blankscreen = stimuli.BlankScreen()

#Instructions for the participants, variables for data file
instructions = stimuli.TextScreen("Instructions",
    f"""You will see a circle accompanied by sound. 
Your task is to report the number of flashes you think you saw after each trial.

There will be {N_TRIALS} trials in total.

Press the spacebar to start.""")

exp.add_data_variable_names(["trial", "nflashes", "nbeeps", "response_flashes"])

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
print(combinations)

#fixation cross added

fixation_cross = stimuli.FixCross()

# Start the experiment
control.start()

old_tf= exp.clock.time
for trial, (n_flashes, n_beeps) in enumerate(combinations, start=1):

    fixation_cross.present()
    exp.clock.wait(1000)  # Display fixation cross for 1 second
    blankscreen.present()

    beeps[n_beeps].present()
    exp.clock.wait(16)  # Wait for 16 ms before the first flash
    for f in range(n_flashes):
        visual_stimulus.present(log_event_tag=True)
        tf = exp.clock.time
        print(tf - old_tf)
        old_tf = tf
        blankscreen.present(log_event_tag=True)
        exp.clock.wait(FLASH_INTERVAL)

    exp.clock.wait(1000)
    text_input = io.TextInput("How many flashes did you see?")
    response = text_input.get()
    exp.data.add([trial, n_flashes, n_beeps, response])


# End the experiment
control.end()
