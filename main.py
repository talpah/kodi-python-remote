from kivy.properties import NumericProperty, partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kodi import Kodi


class RootWidget(BoxLayout):
    '''This is the class representing your root widget.
       By default it is inherited from BoxLayout,
       you can use any other layout/widget depending on your usage.
    '''

    xhint = NumericProperty(.15)
    yhint = NumericProperty(.15)
    kodi = Kodi()

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.update_state()
        self.update_volume()
        self.favourites()

    def update_volume(self):
        current_volume = self.kodi.Application.GetProperties(properties=["volume"])
        self.ids.volslider.value = current_volume['result']['volume']

    def update_state(self):
        title = self.kodi.Player.GetItem(playerid=1, properties=['title', ])
        title = ", ".join([value for (key, value) in title['result']['item'].items() if
                           value and key in ['title', 'label']])
        if not title:
            player_speed = 'Stopped'
        else:
            player_speed = self.kodi.Player.GetProperties(playerid=1, properties=['speed', ])
            player_speed = "Playing " if player_speed['result']['speed'] != 0 else "Stopped"
        self.ids.nowplaying.text = "{} {}".format(player_speed, title)

    def set_volume(self):
        volume = int(self.ids.volslider.value)
        self.kodi.Application.SetVolume(volume=volume)
        return True

    def play_pause(self):
        print self.kodi.Player.PlayPause(playerid=1, play="toggle")
        self.update_state()
        return True

    def stop(self):
        print self.kodi.Player.Stop(playerid=1)
        self.update_state()
        return True

    def play_media(self, path, *args):
        self.kodi.Player.Open(item={"file": path})
        self.update_state()

    def favourites(self):
        favs = self.kodi.Favourites.GetFavourites(properties=["window", "path", "thumbnail", "windowparameter"])
        for fav in favs['result']['favourites']:
            if 'path' not in fav:
                continue
            btn = Button(size_hint=(1, None), height=40)
            btn.text = fav['title'][:90] if len(fav['title']) > 90 else fav['title']
            btn.bind(on_release=partial(self.play_media, fav['path']))
            self.ids.favlist.add_widget(btn)


class MainApp(App):
    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::

         app = App.get_running_app()
         print (app.title)

       in kv language::

         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name
       of this class::

         MainApp = main.kv
         MainClass = mainclass.kv

       The App part is auto removed and the whole name is lowercased.
    '''

    def build(self):
        return RootWidget()


if '__main__' == __name__:
    MainApp().run()
