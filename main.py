#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivymd.theming import ThemeManager

class Pykk1App(App):
    theme_cls = ThemeManager()


if __name__ == "__main__":
    Pykk1App().run()