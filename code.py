import random
from expyriment import design, control, stimuli

N_TRIALS = 20
NUM_FLASHES = 3  # Variable number of visual flashes
NUM_BEEPS = 3  # Variable number of auditory beeps
Visual_interval = 50
Audio_interval = 57
MAX_RESPONSE_DELAY = 2000
aud="beep.wav"

exp = design.Experiment(name="Audiovisual", text_size=40)
#control.set_develop_mode(on=True)
control.initialize(exp)

audio_stimulus = stimuli.Audio(aud)
blankscreen = stimuli.BlankScreen(aud)

visual_stimulus = stimuli.Circle(50, colour=[255,255,255], line_width=0)
blankscreen = stimuli.BlankScreen()


# I tried to use ChatGPT for this part but the whole code doesn't seem to work
trial_list = []
for i in range (NUM_FLASHES):
	trial_list.append(design.Trial())
	trial_list[-1].add_stimulus(visual_stimulus)
	trial_list[-1].set_factor("flash_number", i + 1)

exp.design.randomize.shuffle_list(trial_list)


instructions = stimuli.TextScreen("Instructions",
    f"""From time to time, you will see a circle accompanied by a sound

    Your task is to report the number of flashes after each trial.

    There will be {N_TRIALS} trials in total.

    Press the spacebar to start.""")

# Start the experiment
control.start()

# Present visual and audio stimuli
for trial in trial_list:
    # Present visual stimulus
    trial.stimuli[0].present()
    exp.control.wait(Audio_interval)
    exp.stimuli.BlankScreen().present()
    exp.control.wait(Visual_interval)

    # Present audio stimuli
    for i in range(NUM_BEEPS):
        audio_stimulus.present()
        exp.control.wait(Audio_interval)

# End the experiment
control.end()


