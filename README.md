# Sound-Induced Flash Illusion
## Audiovisual-Perception
[Webpage](https://niaapts.github.io/Audiovisual-Perception)

Based on: Shams, L., Kamitani, Y., & Shimojo, S. (2002). Visual illusion induced by sound. Brain research. Cognitive brain research, 14(1), 147–152. (https://doi.org/10.1016/s0926-6410(02)00069-1)

The Sound-Induced Flash Illusion (SIFI) is the first visual illusion caused by a non-visual cue - demonstrating that the visual perception can be dramatically altered by sound. This is proven by the experiment  designed by Ladan Shams, in which the presentation of a visual stimulus (circle) as a rapid single flash accompanied with two beeps results in the perception of two flashes.

## **Hypothesis:**
Visual ilusion induced by sound - auditory information can qualitatively alter the perception of an unambiguous visual stimulus to create a striking visual illusion.
The illusion is strongest when the flash is in the periphery
but also works in the fovea. 
 
In this project for [PROG 201: Programming Experiments for Psychology or Neuroscience](https://docs.google.com/document/d/1-6AzSP1wuRjMQlASjc1o72xaUmhyvhu2U054vK4Q164/edit) class, we designed the experiment to demonstrate this illusion. 

## **The Experiment**
#### **Part 1:**  perception of a single visual flash when accompanied by multiple auditory beeps
*Stimuli:* Flashing a uniform white disk (at 5 degrees eccentricity) for a variable number of times (1-4) - 17ms long flashes, 50 ms apart on a black background. Flashes were accompanied by a variable number of beeps (1-4), 7ms long, spaced 57 milliseconds apart.

*Data:* Answers of each participant after each trial is recorded and saved as a csv file in a folder called "data".

*Result:* Observers consistently and incorrectly reported seeing multiple flashes whenever a single flash was accompanied by more than one beep.

## **Code**
#### **Libraries and variables:**

```
import random
from expyriment import design, control, stimuli, io, misc

#All the needed variables
MAX_FLASH=4
MAX_BEEPS = 4 
WAIT_AFTER_FIRST_BEEP=16
FLASH_INTERVAL=55
MAX_RESPONSE_DELAY = 2000
WHITE=(255,255,255)
```

#### **Stimuli:**
*Visual Stimulus*

```
#Screen coordinates for 5 degrees eccentricity (ChatGPT)

eccentricity_degrees = 5
pixels_per_degree = 28
viewing_distance_cm = 57

#horizontal eccentricity at 5 degrees

eccentricity_pixels = eccentricity_degrees * pixels_per_degree
eccentricity_screen_coordinates = (eccentricity_pixels, 0)  

#visual stimulus

visual_stimulus = stimuli.Circle(radius=50, colour=WHITE, position=eccentricity_screen_coordinates)  

```
*Audio Stimuli:*

```
#pre-recorded audio stimuli with 1-4 beeps
beeps= {
    1: stimuli.Audio('beep-1.wav'),
    2: stimuli.Audio('beep-2.wav'),
    3: stimuli.Audio('beep-3.wav'),
    4: stimuli.Audio('beep-4.wav')}
```
*Flash-beep combinations*
```
combinations = []
for f in range(1, MAX_FLASH + 1):
    for b in range(1, MAX_BEEPS + 1):
        combinations.append((f, b))

#added several where there's 1 flash and 1-4 beeps
for b in range(1, 5):
    combinations.append((1, b))

combinations = combinations * 2

#randomized the flash-beep combinations
random.seed(32)
random.shuffle(combinations)

#number of trials
N_TRIALS = len(combinations)
```

#### **Experimental design:**
```
exp = design.Experiment(name="Audiovisual", text_size=40)
control.set_develop_mode(on=True)

control.initialize(exp)

#fixation cross added
fixation_cross = stimuli.FixCross(size=(24,24), colour=WHITE)

#blankscreen added
blankscreen = stimuli.BlankScreen()

#Instructions for the participants, variables for data file

instructions = stimuli.TextScreen("Instructions",
    f"""You will see a circle accompanied by sound. 
Your task is to report the number of flashes you saw after each trial.

There will be {N_TRIALS} trials in total.

Press the spacebar to start.""", heading_font="freesans", text_font="freesans", 
heading_bold=True, heading_size=55, text_size=36, text_italic=True, text_colour=(255,255,255))

exp.add_data_variable_names(["trial", "nflashes", "nbeeps", "response_flashes"])

```
#### **The Experiment**
*Running the experiment and recording responses.*
```
# Start of the experiment
control.start()
instructions.present()
exp.keyboard.wait()

#looping through flashes and beeps 
#Starting with the beeps and adjusting the wait time before the first flash

for trial, (n_flashes, n_beeps) in enumerate(combinations, start=1):

    fixation_cross.present()
    exp.clock.wait(1000)  # Display fixation cross for 1 second
    blankscreen.present()

    beeps[n_beeps].present()
    exp.clock.wait(WAIT_AFTER_FIRST_BEEP)  # Waiting for 16 ms before the first flash
    #loop for flashes 
    for f in range(n_flashes):
        visual_stimulus.present(log_event_tag=True)
        blankscreen.present(log_event_tag=True)
        exp.clock.wait(FLASH_INTERVAL)

    exp.clock.wait(500) #wait after stimuli for half a second

    #getting participant's answer
    text_input = io.TextInput("How many flashes did you see?", message_colour=WHITE, user_text_colour= WHITE)
    response = text_input.get()
    exp.data.add([trial, n_flashes, n_beeps, response])


# End the experiment
control.end()
```
