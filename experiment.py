from psychopy import core, event, visual, sound
import random, datetime, csv

class Experiment:
    def __init__(self):
        self.experiment_function = self.color_motor_processing
        # self.experiment_function = self.reaction_time

        self.rand = random.Random()
        self.stopwatch = core.Clock()

        self.setup_window()
        self.menu_page()

    def setup_window(self):
        self.window = visual.Window(color = "grey", fullscr=False) 
        self.window.flip()

        self.background = visual.rect.Rect(self.window, size=2)
        self.background.draw()
        self.set_background_color("#050505")

        self.instructions = visual.TextStim(self.window, "")
        self.instructions.draw()

        self.window.flip()

    def menu_page(self):
        self.instructions.text = "Press the SPACE-key to continue or ESCAPE to exit."
        self.instructions.draw()
        self.window.flip()

        pressed_key = event.waitKeys(keyList = ["space", "escape"])[0]
        if pressed_key == "space":
            self.get_ready()
        else:
            self.window.close()

    def get_ready(self):
        self.set_background_color("purple")
        self.instructions.text = "Get ready"
        self.instructions.draw()

        self.window.flip()

        self.experiment_function()

    def set_background_color(self, color):
        self.background.color = color
        self.background.draw()

    def reaction_time(self):
        self.instructions.text = ""
        core.wait(1 + self.rand.random() * 2) # wait for between 1 and 3 seconds

        self.set_background_color("#3EDE79")
        self.window.flip()

        self.stopwatch.reset()
        key = event.waitKeys(keyList = ["space"])[0] # wait for user pressing SPACE
        time_to_respond = self.stopwatch.getTime()


        self.instructions.text = f"Successful in {round(time_to_respond * 1000)}ms"
        self.instructions.draw()
        self.log_result("reaction", time_to_respond)
        self.window.flip()

        core.wait(2)
        self.menu_page()

    def color_motor_processing(self):
        target_response = self.rand.choice(["left", "right"]) # randomly select which key will be the target key

        self.instructions.text = ""
        core.wait(1 + self.rand.random() * 2) # wait for between 1 and 3 seconds

        self.set_background_color("blue" if target_response == "left" else "red")
        self.window.flip()

        self.stopwatch.reset()
        key = event.waitKeys(keyList = ["left", "right"])[0] # record key-press
        time_to_respond = self.stopwatch.getTime()

        if key == target_response:
            feedback_text = "Successful"
            feedback_color = "#3EDE79"
            self.log_result("reaction_and_decision", time_to_respond)
        else:
            feedback_text = "Failed"
            feedback_color = "grey"

        self.set_background_color(feedback_color)
        self.instructions.text = f"{feedback_text} in {round(time_to_respond * 1000)}ms"
        self.instructions.draw()
        self.window.flip()

        core.wait(2)
        self.menu_page()

    def log_result(self, test_name, score):
        with open("results.csv", "a") as file:
            file.write(f"\n{datetime.datetime.now()},{test_name},{score}")

Experiment()
