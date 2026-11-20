
#imports built-in python functions for time management and random number generation
import threading
import random
import time

#if i recall, you have to do a pip install pynput to get this library
from pynput import keyboard, mouse


#a class is basically a big grouping of code you can reference with a single variable name
class AutoClicker:
    
    #each class has constructor- this is the block of code that gets ran when the class is created 
    #this is basically where we define what attribuate variables the class will have, and what their starting values will be at the beginning of the program
    def __init__(self, toggle_key='n'): #default the auto-clicking key to 'n' unless othewise specified when the class is created
        
        self.toggle_key = toggle_key #we are in the AutoClicker class, so "self" means "AutoClicker"
        
        self.mouse_controller = mouse.Controller() #the mouse input we imported on line 8 has a built-in Controller class for controlling your mouse 

        self.clicking = False #assume we want to start in a state of not-autoclicking
        
        self.click_thread = None #dont worry about this yet
        
        self.key_held = False #variable that indicates we are starting in a state of the auto-clicking key ('n', in this case) is not being held down at the start of the program

        #creating a "listener", and telling it to use our on_press and on_release functions defined below at lines 
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def click_loop(self): #dont worry about this until you read the "on-release" function 
        #Runs in a separate thread, clicking with a short random delay while active.
        while self.clicking:
            self.mouse_controller.click(mouse.Button.left)
            time.sleep(random.uniform(0, 0.01)) #wait between 0 and .01 seconds- this is because Crush Crush (the game i wrote this for) detects auto-clicking of a certain speed :P
            
    def on_press(self, key): #this block of code gets ran when the button 'n' is pressed and held down.
        if self._matches_toggle_key(key):
            self.key_held = True

    def on_release(self, key): #this block of code is where the magic happens: if we press and release 'n', and we are not clicking, start clicking. if we press and release 'n' while we are autoclicking, then stop. on/off 
        if self._matches_toggle_key(key) and self.key_held:
            self.key_held = False
            self.clicking = not self.clicking

            if self.clicking:
                self.click_thread = threading.Thread(target=self.click_loop, daemon=True) #to start clicking, run our "click_loop" function at line 34
                self.click_thread.start()
            # if just turned off, click_loop exits on its own next iteration

        if key == keyboard.Key.esc:
            return False  # stops the listener if we hit the escape key. can turn this into a variable if wanted

    def _matches_toggle_key(self, key): #tells you if the 'n' button is being presed, or if its another key. dont worry about the try-except stuff yet
        try:
            return key.char == self.toggle_key
        except AttributeError:
            return False

    def run(self):
        print(f"Press and release '{self.toggle_key}' to start autoclicking. "
              f"Press and release it again to stop. Press Esc to quit.")
        with self.listener:
            self.listener.join() #this is just how the Keyboard.Listener class we imported on line 8 wants to start up. idk why they called it "join()" either
           


#this is what we call a "main function" - it's the function that gets ran when your
#program is called from the command line
if __name__ == '__main__':
    clicker = AutoClicker(toggle_key='n') #create an instance of your AutoClicker class- specifying 'n' as the keyboard command to start autoclicking
    clicker.run() #go to the AutoClicker's "run" function 
