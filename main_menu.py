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
                        i.disable()
                    else:
                        i.enable()
                if self.car.graphics != "ultra fast":
                    for i in track.details:
                        if track != sand_track:
                            i.disable()
                        else:
                            i.enable()
            sand_track.enable()
            self.car.position = (-40, 30, -175)
            unlocked_text.disable()
            if self.car.gamemode == "race":
                highscore_text.enable()
                highscore_text.text = "Highscore: " + str(round(self.car.sand_track_hs, 2)) 

        def grass_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != grass_track:
                        i.disable()
                    else:
                        i.enable()
                if self.car.graphics != "ultra fast":
                    for i in track.details:
                        if track != grass_track:
                            i.disable()
                        else:
                            i.enable()
                if self.car.graphics == "fast":
                    grass_track.grass.disable()
            grass_track.enable()
            self.car.position = (20, 30, -100)
            if grass_track.unlocked == False:
                grass_track.alpha = 200
                highscore_text.disable()
                for i in grass_track.track:
                    i.alpha = 200
                for i in grass_track.details:
                    i.alpha = 200
            else:
                if self.car.gamemode == "race":
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.grass_track_hs, 2))
                unlocked_text.disable()
                grass_track.alpha = 255

        def snow_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != snow_track:
                        i.disable()
                    else:
                        i.enable()
                if self.car.graphics != "ultra fast":
                    for i in track.details:
                        if track != snow_track:
                            i.disable()
                        else:
                            i.enable()
            snow_track.enable()
            self.car.position = (20, 30, -80)
            if snow_track.unlocked == False:
                snow_track.alpha = 200
                highscore_text.disable()
                for i in snow_track.track:
                    i.alpha = 200
                for i in snow_track.details:
                    i.alpha = 200
            else:
                if self.car.gamemode == "race":
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.snow_track_hs, 2))
                unlocked_text.disable()
                snow_track.alpha = 255
        
        def forest_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != forest_track:
                        i.disable()
                    else:
                        i.enable()
                if self.car.graphics != "ultra fast":
                    for i in track.details:
                        if track != forest_track:
                            i.disable()
                        else:
                            i.enable()
            forest_track.enable()
            self.car.position = (50, 30, -100)
            if forest_track.unlocked == False:
                forest_track.alpha = 200
                highscore_text.disable()
                for i in forest_track.track:
                    i.alpha = 200
                for i in forest_track.details:
                    i.alpha = 200
            else:
                if self.car.gamemode == "race":
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.forest_track_hs, 2))
                unlocked_text.disable()
                forest_track.alpha = 255

        def savannah_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != savannah_track:
                        i.disable()
                    else:
                        i.enable()
                if self.car.graphics != "ultra fast":
                    for i in track.details:
                        if track != savannah_track:
                            i.disable()
                        else:
                            i.enable()
            savannah_track.enable()
            self.car.position = (25, 30, -130)
            if savannah_track.unlocked == False:
                savannah_track.alpha = 200
                highscore_text.disable()
                for i in savannah_track.track:
                    i.alpha = 200
                for i in savannah_track.details:
                    i.alpha = 200
            else:
                if self.car.gamemode == "race":
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.savannah_track_hs, 2))
                unlocked_text.disable()
                savannah_track.alpha = 255

        def lake_track_hover():
            for track in self.tracks:
                track.disable()
                for i in track.track:
                    if track != lake_track:
                        i.disable()
                    else:
                        i.enable()
                if self.car.graphics != "ultra fast":
                    for i in track.details:
                        if track != lake_track:
                            i.disable()
                        else:
                            i.enable()
                if self.car.graphics == "fast":
                    lake_track.grass.disable()
                    lake_track.rocks.disable()
            lake_track.enable()
            self.car.position = (140, 200, -350)
            if lake_track.unlocked == False:
                lake_track.alpha = 200
                highscore_text.disable()
                for i in lake_track.track:
                    i.alpha = 200
                for i in lake_track.details:
                    i.alpha = 200
            else:
                if self.car.gamemode == "race":
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.lake_track_hs, 2))
                unlocked_text.disable()
                lake_track.alpha = 255

        start_button = Button(text = "Start Game", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        sand_track_button = Button(text = "Safari", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "Grass Plain", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        snow_track_button = Button(text = "Snow Grounds", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0.5, parent = self.maps_menu)
        forest_track_button = Button(text = "Forest", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.1, x = -0.5, parent = self.maps_menu)
        savannah_track_button = Button(text = "Savannah Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.1, x = 0, parent = self.maps_menu)
        lake_track_button = Button(text = "Lake Track", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.1, x = 0.5, parent = self.maps_menu)
        back_button = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.maps_menu)
        
        unlocked_text = Text("", scale = 1.5, color = color.orange, line_height = 2, origin = 0, y = -0.1, parent = self.maps_menu)
        unlocked_text.disable()

        highscore_text = Text("", scale = 1.2, color = color.white, line_height = 2, origin = 0, y = -0.07, parent = self.maps_menu)
        highscore_text.disable()

        

        self.leaderboard_background = Entity(model = "quad", color = color.hex("0099ff"), alpha = 100, scale = (0.4, 0.42), position = Vec2(0.6, 0.25), parent = camera.ui)
        self.leaderboard_title = Text("Leaderboard", color = color.gold, scale = 5, line_height = 2, origin = 0, y = 0.4, parent = self.leaderboard_background)
        
        self.leaderboard_01 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0.2, parent = self.leaderboard_background)
        self.leaderboard_02 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0.1, parent = self.leaderboard_background)
        self.leaderboard_03 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0, parent = self.leaderboard_background)
        self.leaderboard_04 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = -0.1, parent = self.leaderboard_background)
        self.leaderboard_05 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = -0.2, parent = self.leaderboard_background)
        
        self.leaderboard_texts = [self.leaderboard_background, self.leaderboard_title, self.leaderboard_01, self.leaderboard_02, self.leaderboard_03, self.leaderboard_04, self.leaderboard_05]

        self.leaderboard_background.disable()
        self.leaderboard_title.disable()

        sand_track_button.on_mouse_enter = Func(sand_track_hover)
        grass_track_button.on_mouse_enter = Func(grass_track_hover)
        snow_track_button.on_mouse_enter = Func(snow_track_hover)
        forest_track_button.on_mouse_enter = Func(forest_track_hover)
        savannah_track_button.on_mouse_enter = Func(savannah_track_hover)
        lake_track_button.on_mouse_enter = Func(lake_track_hover)

        start_button.on_click = Func(start)
        sand_track_button.on_click = Func(sand_track_func)
        grass_track_button.on_click = Func(grass_track_func)
        snow_track_button.on_click = Func(snow_track_func)
        forest_track_button.on_click = Func(forest_track_func)
        savannah_track_button.on_click = Func(savannah_track_func)
        lake_track_button.on_click = Func(lake_track_func)
        back_button.on_click = Func(back)

        # Race Menu

        def race_button_func():
            self.race_menu.disable()
            self.maps_menu.enable()
            self.car.gamemode = "race"
            self.car.count = 0.0
            self.car.reset_count = 0.0

        def time_trial_func():
            self.race_menu.disable()
            self.maps_menu.enable()
            self.car.gamemode = "time trial"
            self.car.count = 100.0
            self.car.reset_count = 100.0

        def drift_func():
            self.race_menu.disable()
            self.maps_menu.enable()
            self.car.gamemode = "drift"
            self.car.count = 0.0
            self.car.reset_count = 0.0
            

        def back_race():
            self.race_menu.disable()
            self.main_menu.enable()

        race_button = Button(text = "Race", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.race_menu)
        time_trial_button = Button(text = "Time Trial", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.race_menu)
        drift_button = Button(text = "Drift", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.race_menu)
        back_button_race = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.race_menu)

        race_button.on_click = Func(race_button_func)
        time_trial_button.on_click = Func(time_trial_func)
        drift_button.on_click = Func(drift_func)
        back_button_race.on_click = Func(back_race)

        # Settings

        def settings():
            self.main_menu.disable()
            self.settings_menu.enable()

        def video():
            self.settings_menu.disable()
            self.video_menu.enable()

        def gameplay():
            self.settings_menu.disable()
            self.gameplay_menu.enable()

        def audio():
            self.settings_menu.disable()
            self.audio_menu.enable()

        def controls():
            self.settings_menu.disable()
            self.controls_menu.enable()

        def back_settings():
            self.settings_menu.disable()
            self.main_menu.enable()

        settings_button = Button(text = "Settings", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        
        video_button = Button(text = "Video", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.24, parent = self.settings_menu)
        gameplay_button = Button(text = "Gameplay", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.settings_menu)
        audio_button = Button(text = "Audio", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.settings_menu)
        controls_button = Button(text = "Controls", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.settings_menu)

        back_button_settings = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.24, parent = self.settings_menu)

        settings_button.on_click = Func(settings) 
        video_button.on_click = Func(video)
        gameplay_button.on_click = Func(gameplay)
        audio_button.on_click = Func(audio)
        controls_button.on_click = Func(controls)
        back_button_settings.on_click = Func(back_settings)

        # Gameplay Menu

        def graphics():
            if self.car.graphics == "fancy":
                self.car.graphics = "fast"
                self.car.particle_amount = 0.085
                graphics_button.text = "Graphics: Fast"
                for track in self.tracks:
                    if track.enabled:
                        for detail in track.details:
                            detail.enable()
                        grass_track.grass.disable()
                self.sun.resolution = 2048
            elif self.car.graphics == "fast":
                self.car.graphics = "ultra fast"
                self.car.particle_amount = 0.1
                graphics_button.text = "Graphics: Ultra Fast"
                for track in self.tracks:
                    if track.enabled:
                        for detail in track.details:
                            detail.disable()
                self.sun.resolution = 1024
            elif self.car.graphics == "ultra fast":
                self.car.graphics = "fancy"
                self.car.particle_amount = 0.07
                graphics_button.text = "Graphics: Fancy"
                for track in self.tracks:
                    if track.enabled:
                        for detail in track.details:
                            detail.enable()
                self.sun.resolution = 3072
            self.sun.update_resolution()

        def camera_angle():
            if self.car.camera_angle == "top":
                self.car.camera_angle = "side"
                camera_angle_button.text = "Camera Angle: Side"
            elif self.car.camera_angle == "side":
                self.car.camera_angle = "behind"
                camera_angle_button.text = "Camera Angle: Behind"
            elif self.car.camera_angle == "behind":
                self.car.camera_angle = "first-person"
                camera_angle_button.text = "Camera Angle: First-Person"
            elif self.car.camera_angle == "first-person":
                self.car.camera_angle = "top"
                camera_angle_button.text = "Camera Angle: Top"
            self.car.change_camera = True

        def camera_shake():
            self.car.camera_shake_option = not self.car.camera_shake_option
            if self.car.camera_shake_option:
                camera_shake_button.text = "Camera Shake: On"
            elif self.car.camera_shake_option == False:
                camera_shake_button.text = "Camera Shake: Off"

        def back_gameplay():
            self.gameplay_menu.disable()
            self.settings_menu.enable()

        graphics_button = Button("Graphics: Fancy", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.24, parent = self.gameplay_menu)
        camera_angle_button = Button("Camera Angle: Top", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.gameplay_menu)
        camera_shake_button = Button("Camera Shake: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.gameplay_menu)
        reset_highsore_button = Button(text = "Reset Highscore", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.gameplay_menu)
        back_button_gameplay = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.24, parent = self.gameplay_menu)

        graphics_button.on_click = Func(graphics)
        camera_angle_button.on_click = Func(camera_angle)
        camera_shake_button.on_click = Func(camera_shake)
        reset_highsore_button.on_click = Func(self.car.reset_highscore)
        back_button_gameplay.on_click = Func(back_gameplay)

        # Video Menu

        def fullscreen():
            window.fullscreen = not window.fullscreen
            if window.fullscreen:
                fullscreen_button.text = "Fullscreen: On"
            elif window.fullscreen == False:
                fullscreen_button.text = "Fullscreen: Off"

        def borderless():
            window.borderless = not window.borderless
            if window.borderless:
                borderless_button.text = "Borderless: On"
            elif window.borderless == False:
                borderless_button.text = "Borderless: Off"
            window.exit_button.enable()

        def fps():
            window.fps_counter.enabled = not window.fps_counter.enabled
            if window.fps_counter.enabled:
                fps_button.text = "FPS: On"
            elif window.fps_counter.enabled == False:
                fps_button.text = "FPS: Off"

        def exit_button_func():
            window.exit_button.enabled = not window.exit_button.enabled
            if window.exit_button.enabled:
                exit_button.text = "Exit Button: On"
            elif window.exit_button.enabled == False:
                exit_button.text = "Exit Button: Off"

        def back_video():
            self.video_menu.disable()
            self.settings_menu.enable()

        fullscreen_button = Button("Fullscreen: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.24, parent = self.video_menu)
        borderless_button = Button("Borderless: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.video_menu)
        fps_button = Button("FPS: Off", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.video_menu)
        exit_button = Button("Exit Button: Off", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.video_menu)
        back_button_video = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.24, parent = self.video_menu)

        fullscreen_button.on_click = Func(fullscreen)
        borderless_button.on_click = Func(borderless)
        fps_button.on_click = Func(fps)
        exit_button.on_click = Func(exit_button_func)
        back_button_video.on_click = Func(back_video)

        # Audio Menu

        def audio_func():
            if self.car.audio:
                audio_button.text = "Audio: Off"
                self.volume.value = 0
            elif not self.car.audio:
                audio_button.text = "Audio: On"
                self.volume.value = 1
            self.car.audio = not self.car.audio
        
        def back_audio():
            self.audio_menu.disable()
            self.settings_menu.enable()

        audio_button = Button("Audio: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.audio_menu)
        back_button_audio = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.audio_menu)
        
        self.volume = Slider(min = 0, max = 1, default = 1, text = "Volume", y = 0.2, x = -0.3, scale = 1.3, parent = self.audio_menu, dynamic = True)
        self.volume.step = 0.1

        audio_button.on_click = Func(audio_func)
        back_button_audio.on_click = Func(back_audio)

        # Controls

        def back_controls():
            self.controls_menu.disable()
            self.settings_menu.enable()

        def controls_settings():
            if self.car.controls == "wasd":
                self.car.controls = "zqsd"
                controls_settings_button.text = "Controls: ZQSD"
                drive_controls_text.text = "Drive: Z"
                steering_controls_text.text = "Steering: Q D"
            elif self.car.controls == "zqsd":
                self.car.controls = "wasd"
                controls_settings_button.text = "Controls: WASD"
                drive_controls_text.text = "Drive: W"
                steering_controls_text.text = "Steering: A D"
        
        drive_controls_text = Button("Drive: W", color = color.black, scale_y = 0.1, scale_x = 0.3, x = -0.5, y = 0.3, parent = self.controls_menu)
        steering_controls_text = Button("Steering: A D", color = color.black, scale_y = 0.1, scale_x = 0.3, x = 0, y = 0.3, parent = self.controls_menu)
        braking_controls_text = Button("Braking: S", color = color.black, scale_y = 0.1, scale_x = 0.3, x = 0.5, y = 0.3, parent = self.controls_menu)
        handbraking_controls_text = Button("Hand Brake: SPACE", color = color.black, scale_y = 0.1, scale_x = 0.3, x = -0.5, y = 0.1, parent = self.controls_menu)
        respawn_controls_text = Button("Respawn: G", color = color.black, scale_y = 0.1, scale_x = 0.3, x = 0, y = 0.1, parent = self.controls_menu)
        controls_settings_button = Button("Controls: WASD", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.2, parent = self.controls_menu)
        back_button_controls = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.32, parent = self.controls_menu)

        back_button_controls.on_click = Func(back_controls)
        controls_settings_button.on_click = Func(controls_settings)

        # Pause Menu

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

        def respawn():
            if sand_track.enabled:
                self.car.position = (-63, -40, -7)
                self.car.rotation = (0, 90, 0)
                
            elif grass_track.enabled:
                self.car.position = (-80, -30, 18.5)
                self.car.rotation = (0, 90, 0)
                
            elif snow_track.enabled:
                self.car.position = (-5, -35, 93)
                self.car.rotation = (0, 90, 0)
                
            elif forest_track.enabled:
                self.car.position = (12, -35, 76)
                self.car.rotation = (0, 90, 0)
                
            elif savannah_track.enabled:
                self.car.position = (-14, -35, 42)
                self.car.rotation = (0, 90, 0)
                
            elif self.lake_track.enabled:
                self.car.position = (-121, -40, 158)
                self.car.rotation = (0, 90, 0)