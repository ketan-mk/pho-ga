#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivymd.tabs import MDTab
from kivymd.list import MDList, TwoLineIconListItem, ILeftBodyTouch
from kivymd.button import MDIconButton, MDRaisedButton
from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from utils import get_data


base_listing_screen = '''
<{class_name}>
    name: '{screen_name}'
{widgets}
'''

common_widgets = '''
    MDSpinner:
        id: spinner
        active: True
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    MDTabbedPanel:
        id: schedule_tabs
        tab_display_mode: 'text'
'''


Builder.load_string(base_listing_screen.format(class_name='NlistingScreen', screen_name='nlisting', widgets=common_widgets))
Builder.load_string(base_listing_screen.format(class_name='SlistingScreen', screen_name='slisting', widgets=common_widgets))
Builder.load_string(base_listing_screen.format(class_name='OlistingScreen', screen_name='olisting', widgets=common_widgets))


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class Track(TwoLineIconListItem):

    colors = {
            # rgb(241, 194, 65)
            'Sala Aventurine e Alexandrite': [0.94, 0.76, 0.25, .4],
            # rgb(87, 193, 219)
            'Sala Amethyst': [0.34, 0.75, 0.85, .4],
            # rgb(86, 184, 103)
            'Sala Crystal': [0.33, 0.72, 0.4, .4],
            'default': [0.5, 0.5, 0.5, .4],
    }

    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info')
        kwargs['type'] = 'three-line'
        kwargs['text'] = self.info['time']
        kwargs['secondary_text'] = self.info['title'].upper()

        super(Track, self).__init__()

        icon = IconLeftSampleWidget(icon=self.info.get('icon', 'bulletin-board'))
        color = self.colors['default']

        if 'place' in self.info:
            label = self.ids._lbl_primary
            place = self.info['place'].replace('Sala', '')
            label.text += ' - {}'.format(place)
            color = self.colors.get(self.info['place'], color)

        icon.ids.content.color = color
        self.add_widget(icon)


    def on_release(self):
        if not self.info.get('speaker'):
            return
        print(" i am here on release")
        box = BoxLayout(height=dp(500), orientation='vertical',
                        spacing=dp(10), size_hint_y=None)

        # adding avatar widget
        if self.info['speaker'].get('avatar'):
            image = AsyncImage(source=self.info['speaker']['avatar'],
                               allow_stretch=True)
            box.add_widget(image)

        # adding place widget
        if self.info.get('place'):
            place = MDRaisedButton(text=self.info['place'], elevation_normal=2,
                                   opposite_colors=True,
                                   pos_hint={'center_x': .5, 'center_y': .4})
            box.add_widget(place)

        # adding description widget
        label = MDLabel(font_style='Body1', theme_text_color='Primary',
                        text=self._parse_text(), size_hint_y=None)
        label.bind(texture_size=label.setter('size'))

        box.add_widget(label)
        self.dialog = MDDialog(title=self.info['speaker']['name'],
                               content=box,
                               size_hint=(1, None),
                               height=dp(500),
                               auto_dismiss=False)

        self.dialog.add_action_button('Close',
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def _parse_text(self):
        text = self.info['about']
        if len(text) >= 1000:
            text = u'{}...'.format(text[:1000])
        return text


class ListingScreen(Screen):
    schedule_range = tuple()
    base_tab_name = '{:02d}_10_2017'

    def __init__(self, *args, **kwargs):
        super(ListingScreen, self).__init__(*args, **kwargs)
        self.tracks = get_data('tracks')

    def on_enter(self):
        # schedules already populated
        if self.ids.schedule_tabs.ids.tab_manager.screens:
            return

        current_date = datetime.datetime.now().strftime('%d_%m_%Y')
        track_names = []
        # populating schedules
        for i in range(*self.schedule_range):
            track_name = self.base_tab_name.format(i)
            track_names.append(track_name)
            track_day = str(i)

            tab = MDTab(id=track_day, name=track_name,
                        text='{} Out'.format(track_day))
            # tab schedule
            sv = ScrollView(id='tab_{}'.format(track_name), do_scroll_x=False)
            l = MDList()

            for track in self.tracks[track_day]:
                item = Track(info=track)
                l.add_widget(item)

            sv.add_widget(l)
            tab.add_widget(sv)
            self.ids.schedule_tabs.add_widget(tab)

        # not really sure if this is the way to select a tab
        if current_date in track_names:
            self.ids.schedule_tabs.current = current_date

        self.ids.spinner.active = False


class NlistingScreen(ListingScreen):
    schedule_range = (6, 9)


class SlistingScreen(ListingScreen):
    schedule_range = (9, 11)


class OlistingScreen(ListingScreen):
    schedule_range = (11, 12)