#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
# The Label widget is for rendering text.
from kivy.uix.label import Label
from kivy.uix.button import Button

# The GridLayout arranges children in a matrix.
# It takes the available space and
# divides it into columns and rows,
# then adds widgets to the resulting “cells”.
from kivy.uix.gridlayout import GridLayout

# to change the kivy default settings we use this module config
from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False

import time
import os
Config.set('graphics', 'resizable', True)

birthdayFile = 'data/bdayfile.dat'

Builder.load_string("""
<UpdatesScreen>
    name: 'updates'
    ScrollView:
        id: scroll
        do_scroll_x: False
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(800)
            padding: dp(15)
            spacing: dp(15)
            Image:
                source: 'img/Realestate.jpeg'
                allow_stretch: True
            MDLabel:
                font_style: 'Body1'
                theme_text_color: 'Secondary'
                text: ut.get_data('texts')['alerts']
""")


class UpdatesScreen(Screen):
    def on_enter(self):
        filename = open(birthdayFile, 'r')
        today = time.strftime('%m%d')
        flag = 0
        for line in filename:
            if today in line:
                line = line.split(' ')
                flag = 1
                # line[1] contains Name and line[2] contains Surname
                msg = line[1] +  "Rent Collection Pending"
                layout = GridLayout(cols=1, padding=10)
                popupLabel = Label(text=msg)
                closeButton = Button(text="Close the pop-up")
                layout.add_widget(popupLabel)
                layout.add_widget(closeButton)
                popup = Popup(title='Alert',
                              content=layout,
                              size_hint=(None, None), size=(500, 600))
                popup.open()
                closeButton.bind(on_press=popup.dismiss)

