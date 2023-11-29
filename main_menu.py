from ursina import *
from ursina import curve
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, car, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track):
        super().__init__(
            parent = camera.ui
        )

        # The different menus
        self.start_menu = Entity(parent = self, enabled = True)
        self.host_menu = Entity(parent = self, enabled = False)
        self.created_server_menu = Entity(parent = self, enabled = False)
        self.server_menu = Entity(parent = self, enabled = False)
        self.main_menu = Entity(parent = self, enabled = False)
        self.race_menu = Entity(parent = self, enabled = False)
        self.maps_menu = Entity(parent = self, enabled = False)
        self.settings_menu = Entity(parent = self, enabled = False)
        self.video_menu = Entity(parent = self, enabled = False)
        self.gameplay_menu = Entity(parent = self, enabled = False)
        self.audio_menu = Entity(parent = self, enabled = False)
        self.controls_menu = Entity(parent = self, enabled = False)
        self.garage_menu = Entity(parent = self, enabled = False)
        self.cars_menu = Entity(parent = self.garage_menu, enabled = False)
        self.colours_menu = Entity(parent = self.garage_menu, enabled = False)
        self.cosmetics_menu = Entity(parent = self.garage_menu, enabled = False)
        self.pause_menu = Entity(parent = self, enabled = False)
        self.quit_menu = Entity(parent = self, enabled = False)

        self.menus = [
            self.start_menu, self.host_menu, self.created_server_menu, self.server_menu,
            self.main_menu, self.race_menu, self.maps_menu, self.settings_menu, self.video_menu, self.gameplay_menu,
            self.audio_menu, self.controls_menu, self.garage_menu, self.pause_menu, self.quit_menu
        ]
        
        self.car = car
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forest_track = forest_track
        self.savannah_track = savannah_track
        self.lake_track = lake_track
        self.sun = None

        self.click = Audio("click.wav", False, False, volume = 10)

        self.tracks = [
            self.sand_track, self.grass_track, self.snow_track, self.forest_track, self.savannah_track, self.lake_track
        ]

        # Animate the menu
        for menu in (self.start_menu, self.main_menu, self.race_menu, self.maps_menu, self.settings_menu, self.video_menu, self.gameplay_menu, self.audio_menu, self.controls_menu, self.pause_menu, self.quit_menu, self.garage_menu):
            def animate_in_menu(menu = menu):
                for i, e in enumerate(menu.children):
                    e.original_scale = e.scale
                    e.scale -= 0.01
                    e.animate_scale(e.original_scale, delay = i * 0.05, duration = 0.1, curve = curve.out_quad)

                    e.alpha = 0
                    e.animate("alpha", 0.7, delay = i * 0.05, duration = 0.1, curve = curve.out_quad)

                    if hasattr(e, "text_entity"):
                        e.text_entity.alpha = 0
                        e.text_entity.animate("alpha", 1, delay = i * 0.05, duration = 0.1)

            menu.on_enable = animate_in_menu

        # Start Menu

        self.car.position = (-80, -42, 18.8)
        self.car.visible = True
        self.grass_track.enable()
        for track in self.grass_track.track:
            track.enable()
        for detail in self.grass_track.details:
            detail.enable()

        def singleplayer():
            self.start_menu.disable()
            self.main_menu.enable()
            grass_track.enable()
            self.car.position = (0, 0, 4)
            self.car.visible = False
            for track in self.tracks:
                for i in track.track:
                    i.disable()
                for i in track.details:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in self.grass_track.details:
                    detail.enable()
            if self.car.graphics == "fast":
                self.grass_track.grass.disable()

        def quit():
            application.quit()
            os._exit(0)

        start_title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.start_menu, y = 0.3)

        singleplayer_button = Button(text = "Lets Go", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = 0.05, parent = self.start_menu)
        singleplayer_button.on_click = Func(singleplayer)

        # Quit Menu

        def quit():
            application.quit()
            os._exit(0)

        def dont_quit():
            self.quit_menu.disable()
            self.start_menu.enable()

        quit_text = Text("Are you sure you want to quit?", scale = 1.5, line_height = 2, x = 0, origin = 0, y = 0.2, parent = self.quit_menu)
        quit_yes = Button(text = "Yes", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.05, parent = self.quit_menu)
        quit_no = Button(text = "No", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.07, parent = self.quit_menu)

        quit_yes.on_click = Func(quit)
        quit_no.on_click = Func(dont_quit)

        # Host Server Menu

        def create_server():
            if str(self.car.host_ip.text) != "IP" and str(self.car.host_port) != "PORT":
                self.car.server = Server(car.host_ip, car.host_port)
                self.car.server_running = True
                self.car.server.start_server = True
                self.host_menu.disable()
                self.created_server_menu.enable()
                self.car.visible = True
                self.car.position = (-63, -40, -7)
                self.car.rotation = (0, 90, 0)
                snow_track.disable()
                sand_track.enable()
                back_button_server.disable()
                for track in self.tracks:
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()
                for track in self.sand_track.track:
                    track.enable()
                if self.car.graphics != "ultra fast":
                    for detail in self.sand_track.details:
                        detail.enable()

        def join_server_func():
            self.host_menu.disable()
            self.server_menu.enable()
            self.car.visible = True
            self.car.position = (-105, -50, -59)
            snow_track.disable()
            sand_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
                for i in track.details:
                    i.disable()
            for track in self.sand_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in self.sand_track.details:
                    detail.enable()

        def back_host():
            self.host_menu.disable()
            self.start_menu.enable()
            self.car.position = (-80, -42, 18.8)
            self.car.rotation = (0, 90, 0)
            self.car.visible = True
            self.grass_track.enable()
            self.snow_track.disable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
                for i in track.details:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in self.grass_track.details:
                    detail.enable()
            if self.car.graphics == "fast":
                self.grass_track.grass.disable()
        
        self.car.host_ip = InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.host_menu)
        self.car.host_port = InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.host_menu)

        create_server_button = Button(text = "Create Server", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.host_menu)
        join_server_button = Button(text = "Join Server", color = color.hex("0097F5"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.host_menu)
        back_button_host = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.host_menu)

        create_server_button.on_click = Func(create_server)
        join_server_button.on_click = Func(join_server_func)
        back_button_host.on_click = Func(back_host)


        def back_singleplayer():
            self.car.position = (-80, -42, 18.8)
            self.car.rotation = (0, 90, 0)
            self.car.visible = True
            self.grass_track.enable()
            self.start_menu.enable()
            self.main_menu.disable()
            
            for track in self.grass_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in self.grass_track.details:
                    detail.enable()
            if self.car.graphics == "fast":
                self.grass_track.grass.disable()

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        back_button_singleplayer = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.34, parent = self.main_menu)
        back_button_singleplayer.on_click = Func(back_singleplayer)

        # Maps Menu

        def start():
            self.main_menu.disable()
            self.race_menu.enable()

        def back():
            self.maps_menu.disable()
            self.race_menu.enable()
                
            self.car.position = (0, 0, 4)
            unlocked_text.disable()
            for track in self.tracks:
                track.alpha = 255
                track.disable()
                for i in track.track:
                    i.disable()
                for i in track.details:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in self.grass_track.details:
                    detail.enable()
            if self.car.graphics == "fast":
                self.grass_track.grass.disable()
            grass_track.enable()

        def sand_track_func():
            if sand_track:
                self.car.visible = True
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-63, -30, -7)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()
                        
                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()

                sand_track.enable()
                sand_track.played = True

                for s in sand_track.track:
                    s.enable()
                    s.alpha = 255
                if self.car.graphics != "ultra fast":
                    for detail in sand_track.details:
                        detail.enable()
                        detail.alpha = 255

                

                if self.car.gamemode == "race":
                    self.car.highscore_count = float(self.car.sand_track_hs)
                elif self.car.gamemode == "time trial":
                    self.car.highscore_count = float(self.car.sand_track_laps)
                elif self.car.gamemode == "drift":
                    self.car.drift_time = 25
                    self.car.highscore_count = float(self.car.sand_track_drift)
                    self.car.highscore.text = str(int(self.car.highscore_count))
            else:
                unlocked_text.shake()

        def grass_track_func():
            if grass_track:
                self.car.visible = True
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-80, -30, 18.5)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()

                grass_track.enable()
                grass_track.played = True

                for g in grass_track.track:
                    g.enable()
                    g.alpha = 255
                if self.car.graphics != "ultra fast":
                    for detail in grass_track.details:
                        detail.enable()
                        detail.alpha = 255
                if self.car.graphics == "fast":
                    grass_track.grass.disable()

                

                if self.car.gamemode == "race":
                    self.car.highscore_count = float(self.car.grass_track_hs)
                elif self.car.gamemode == "time trial":
                    self.car.highscore_count = float(self.car.grass_track_laps)
                elif self.car.gamemode == "drift":
                    self.car.drift_time = 30
                    self.car.highscore_count = float(self.car.grass_track_drift)
                    self.car.highscore.text = str(int(self.car.highscore_count))
            else:
                unlocked_text.shake()

        def snow_track_func():
            if snow_track:
                self.car.visible = True
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-5, -35, 93)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()
                        
                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()

                snow_track.enable()
                snow_track.played = True

                for s in snow_track.track:
                    s.enable()
                    s.alpha = 255
                if self.car.graphics != "ultra fast":
                    for detail in snow_track.details:
                        detail.enable()
                        detail.alpha = 255

                

                if self.car.gamemode == "race":
                    self.car.highscore_count = float(self.car.snow_track_hs)
                elif self.car.gamemode == "time trial":
                    self.car.highscore_count = float(self.car.snow_track_laps)
                elif self.car.gamemode == "drift":
                    self.car.drift_time = 50
                    self.car.highscore_count = float(self.car.snow_track_drift)
                    self.car.highscore.text = str(int(self.car.highscore_count))
            else:
                unlocked_text.shake()

        def forest_track_func():
            if forest_track:
                self.car.visible = True
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (12, -35, 76)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()

                forest_track.enable()
                forest_track.played = True
                
                for f in forest_track.track:
                    f.enable()
                    f.alpha = 255
                if self.car.graphics != "ultra fast":
                    for detail in forest_track.details:
                        detail.enable()
                        detail.alpha = 255

                

                if self.car.gamemode == "race":
                    self.car.highscore_count = float(self.car.forest_track_hs)
                elif self.car.gamemode == "time trial":
                    self.car.highscore_count = float(self.car.forest_track_laps)
                elif self.car.gamemode == "drift":
                    self.car.drift_time = 40
                    self.car.highscore_count = float(self.car.forest_track_drift)
                    self.car.highscore.text = str(int(self.car.highscore_count))
            else:
                unlocked_text.shake()

        def savannah_track_func():
            if savannah_track:
                self.car.visible = True
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-14, -35, 42)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()

                savannah_track.enable()
                savannah_track.played = True

                for s in savannah_track.track:
                    s.enable()
                    s.alpha = 255
                if self.car.graphics != "ultra fast":
                    for detail in savannah_track.details:
                        detail.enable()
                        detail.alpha = 255

                

                if self.car.gamemode == "race":
                    self.car.highscore_count = float(self.car.savannah_track_hs)
                elif self.car.gamemode == "time trial":
                    self.car.highscore_count = float(self.car.savannah_track_laps)
                elif self.car.gamemode == "drift":
                    self.car.drift_time = 25
                    self.car.highscore_count = float(self.car.savannah_track_drift)
                    self.car.highscore.text = str(int(self.car.highscore_count))
            else:
                unlocked_text.shake()
            
        def lake_track_func():
            if lake_track:
                self.car.visible = True
                mouse.locked = True
                self.maps_menu.disable()
                self.car.position = (-121, -40, 158)
                self.car.rotation = (0, 90, 0)
                self.car.reset_count_timer.enable()

                for track in self.tracks:
                    track.disable()
                    for i in track.track:
                        i.disable()
                    for i in track.details:
                        i.disable()

                lake_track.enable()
                lake_track.played = True

                for l in lake_track.track:
                    l.enable()
                    l.alpha = 255
                if self.car.graphics != "ultra fast":
                    for detail in lake_track.details:
                        detail.enable()
                        detail.alpha = 255
                if self.car.graphics == "fast":
                    lake_track.grass.disable()
                    lake_track.rocks.disable()


                if self.car.gamemode == "race":
                    self.car.highscore_count = float(self.car.lake_track_hs)
                elif self.car.gamemode == "time trial":
                    self.car.highscore_count = float(self.car.lake_track_laps)
                elif self.car.gamemode == "drift":
                    self.car.drift_time = 75
                    self.car.highscore_count = float(self.car.lake_track_drift)
                    self.car.highscore.text = str(int(self.car.highscore_count))
            else:
                unlocked_text.shake()

        def sand_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != sand_track: