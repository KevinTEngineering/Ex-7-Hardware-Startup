import os

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.uix.slider import Slider
from kivy.uix.image import Image, AsyncImage
from pidev.Joystick import Joystick
from threading import Thread
from time import sleep

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

from datetime import datetime

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'


class ProjectNameGUI(App):

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


# noinspection PyGlobalUndefined
class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    joy = Joystick(0, False)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    trigger = ObjectProperty(DPEAButton)

    def switch(self):
        if self.trigger.text == "On":
            self.trigger.text = "Off"
        elif self.trigger.text == "Off":
            self.trigger.text = "On"

    counter = ObjectProperty(DPEAButton)
    increase = 0

    def counting(self):
        # self.increase += 1
        # self.counter.text = str(self.increase)
        self.counter.text = str(self.joy.get_axis('x'))

    def joy_update(self):
        while True:
            self.image.x += self.joy.get_axis('x')
            self.image.y += self.joy.get_axis('y')            # self.joy_x_val = self.joy.get_axis('x')
            # self.ids.joy_label.x(self.joy_x_val)
            # self.joy_pos_x.text = str(self.joy.get_axis('x'))
            # self.joy_y_val = self.joy.get_axis('y')
            # self.joy_pos_y.text = str(self.joy.get_axis('y'))
            sleep(.01)

    def start_joy_thread(self):
        Thread(target=self.joy_update).start()

    motor = ObjectProperty(DPEAButton)

    def motor_switch(self):

        if self.ids.motor_servant.text == "On":
            self.ids.motor_servant.text = "Off"
        elif self.ids.motor_servant.text == "Off":
            self.ids.motor_servant.text = "On"

    image_check = True
    image = ObjectProperty(None)

    def change_image(self):
        if self.image_check == True:
            print("Yes")
            self.image_check = False
        elif self.image_check == False:
            print("No")
            self.image_check = True

    def animation(self, widget, *args):
        anim = Animation(y=-30) + Animation(y=200)
        anim.start(widget)

    def button_pressed(self):
        pass

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class Screen2(Screen):
    pass


class Screen3(Screen):
    def movement(self, widget, *args):
        anim = Animation(x=-30) + Animation(x=200)
        anim.start(widget)


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name='main'))
SCREEN_MANAGER.add_widget(Screen2(name='second'))
SCREEN_MANAGER.add_widget(Screen3(name='third'))

SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


class MyFloat(Widget):
    def btn(self):
        print("Wah")


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
