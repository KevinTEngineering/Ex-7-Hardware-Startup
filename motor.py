from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
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

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

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
    # change_speed = ObjectProperty(None)
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
    side = 0

    # while True:
    #     if (cyprus.read_gpio() & 0b0001):
    #         sleep(.2)
    #         if (cyprus.read_gpio() & 0b0001):
    #             cyprus.set_servo_position(1, 0)
    #     else:
    #         cyprus.set_servo_position(1, 1)
    #         sleep(.2)

    def talon(self):
        cyprus.initialize()
        cyprus.setup_servo(1)
        cyprus.set_servo_position(1, 0.52)
        sleep(4.2)
        cyprus.set_servo_position(1, 0.6)
        sleep(4.2)
        cyprus.set_servo_position(1, 0.66)
        sleep(4.2)
        cyprus.set_servo_position(1, 0.72)
        sleep(4.2)
        cyprus.set_servo_position(1, 0.78)
        sleep(4.2)
        cyprus.set_servo_position(1, 0.84)
        sleep(4.2)
        cyprus.set_servo_position(1, .9)
        sleep(4.2)
        cyprus.set_servo_position(1, .96)
        sleep(4.2)
        cyprus.set_servo_position(1, 1)
        sleep(5)
        cyprus.set_servo_position(1, 0.5)
        sleep(5)

    def cyt(self):
        cyprus.initialize()
        while True:
            if cyprus.read_gpio() & 0b0010:  # binary bitwise AND of the value returned from read.gpio()
                sleep(.5)
                if (cyprus.read_gpio() & 0b0010):
                    cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            else:
                cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
                sleep(.5)

        # cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        # cyprus.initialize()
        # cyprus.set_pwm_values(1, period_value=100000, compare_value=100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        # sleep(4)
        # cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        # sleep(5)
        # cyprus.set_pwm_values(1, period_value=100000, compare_value=-100000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
        # sleep(4)
        # cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)

    # count = 0
    # while count <= 5:
    #     cyprus.set_servo_position(1, .52)
    #     sleep(5)
    #     cyprus.set_servo_position(1, 0.5)
    #     sleep(5)
    #     cyprus.set_servo_position(1, .48)
    #     sleep(5)
    #     cyprus.set_servo_position(1, 0.5)
    #     sleep(3)
    #     count+=1

    def servos(self):
        cyprus.initialize()
        cyprus.setup_servo(1)
        if self.side < 1:
            print("GPIO on port P6 is LOW")
            self.side = 3
        elif self.side > 2:
            cyprus.set_servo_position(1, 1)
            self.side = 0

    # while True:
    #    if cyprus.read_gpio() & 0b0001:
    #       sleep(.5)
    #       if cyprus.read_gpio() & 0b0001:
    #            self.cyprus.set_servo_position(1, 0)

    #   else:
    #       self.cyprus.set_servo_position(1, 1)
    #       sleep(.5)

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
