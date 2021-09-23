import os

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
# from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.uix.slider import Slider
from kivy.uix.image import Image, AsyncImage
from pidev.Joystick import Joystick
from threading import Thread

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

import time
import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

spi = spidev.SpiDev()

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
    change_speed = ObjectProperty(None)
    s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                 steps_per_unit=200, speed=8)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    # trigger = ObjectProperty(DPEAButton)

    direction = 0
    On = 0
    clock = 0

    def reverse(self):
        if self.s0.is_busy:
            if self.direction < 1:

                self.s0.go_until_press(0, self.change_speed.value)
                self.direction = 2
                self.clock = 0
            elif self.direction > 1:
                self.s0.go_until_press(1, self.change_speed.value)
                self.direction = 0
                self.clock = 1

    def switch_On(self):

        if not self.s0.is_busy():
            self.s0.go_until_press(self.clock, self.change_speed.value)
        elif self.s0.is_busy():
            self.s0.softStop()

    def slider_speed(self):
        # print(self.change_speed.value)
        if self.s0.is_busy:
            self.s0.go_until_press(self.clock, self.change_speed.value)

    def update_label(self):
        sleep(.3)

        self.s0.start_relative_move(-15)
        while self.s0.is_busy():
            sleep(.5)

        sleep(10)
        self.s0.start_relative_move(-10)
        while self.s0.is_busy():
            sleep(.5)

        sleep(8)
        self.s0.goHome()
        sleep(30)

        self.s0.start_relative_move(100)
        sleep(10)
        self.s0.set_MaxSpeed(200)
        self.s0.goHome()

    def ultra(self):
        Thread(target=self.update_label).start()

    # counter = ObjectProperty(DPEAButton)
    increase = 0

    def counting(self):
        self.increase += 1
        # self.counter.text = str(self.increase)

    # motor = ObjectProperty(DPEAButton)

    def motor_switch(self):

        if self.ids.motor_servant.text == "On":
            self.ids.motor_servant.text = "Off"
        elif self.ids.motor_servant.text == "Off":
            self.ids.motor_servant.text = "On"

    image_check = True

    # image = ObjectProperty(None)

    def button_pressed(self):
        pass

    def admin_action(self):

        SCREEN_MANAGER.current = 'passCode'


class Screen2(Screen):
    pass


class Screen3(Screen):
    def movement(self, widget, *args):
        anim = Animation(x=-30) + Animation(x=200)
        anim.start(widget)


"""
Widget additions
"""

Builder.load_file('stepper.kv')
SCREEN_MANAGER.add_widget(MainScreen(name='main'))
SCREEN_MANAGER.add_widget(Screen2(name='second'))
SCREEN_MANAGER.add_widget(Screen3(name='third'))

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
