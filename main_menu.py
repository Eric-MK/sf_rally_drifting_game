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
                
            camera.world_rotation_y = self.car.rotation_y
            self.car.speed = 0
            self.car.anti_cheat = 1
            self.car.velocity_y = 0
            if self.car.gamemode == "race":
                self.car.count = 0.0
                self.car.reset_count = 0.0
                self.car.timer_running = False
            elif self.car.gamemode == "time trial":
                self.count = 100.0
                self.reset_count = 100.0
                self.laps = 0
                self.timer_running = False
                self.start_time = False
            elif self.car.gamemode == "drift":
                self.car.timer_running = False
                self.car.reset_drift_score()
            for trail in self.car.trails:
                if trail.trailing:
                    trail.end_trail(True)
            self.car.start_trail = True
            self.car.start_sound = True
            if self.car.audio:
                if self.car.skid_sound.playing:
                    self.car.skid_sound.stop(False)
                if self.car.dirt_sound.playing:
                    self.car.dirt_sound.stop(False)

        def main_menu():
            self.car.position = (0, 0, 4)
            self.car.visible = False
            self.car.rotation = (0, 65, 0)
            self.car.speed = 0
            self.car.velocity_y = 0
            self.car.count = 0.0
            self.car.last_count = 0.0
            self.car.reset_count = 0.0
            self.car.laps = 0
            self.car.drift_score = 0
            self.car.reset_drift_score()
            self.car.gamemode = "race"
            self.car.start_time = False
            self.car.reset_count_timer.disable()
            self.car.timer_running = False
            self.car.anti_cheat = 1
            self.main_menu.enable()
            self.pause_menu.disable()
            for track in self.tracks:
                track.disable()
                track.alpha = 255
                for i in track.track:
                    if track != self.grass_track:
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
            
            for trail in self.car.trails:
                if trail.trailing:
                    trail.end_trail(True)
            self.car.start_trail = True
            self.car.start_sound = True
            if self.car.audio:
                if self.car.skid_sound.playing:
                    self.car.skid_sound.stop(False)
                if self.car.dirt_sound.playing:
                    self.car.dirt_sound.stop(False)
                
        p_resume_button = Button(text = "Resume", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.11, parent = self.pause_menu)
        p_respawn_button = Button(text = "Respawn", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.01, parent = self.pause_menu)
        p_mainmenu_button = Button(text = "Main Menu", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.13, parent = self.pause_menu)
        p_mainmenu_button.on_click = Func(main_menu)
        p_respawn_button.on_click = Func(respawn)
        p_resume_button.on_click = Func(resume)

        # Garage

        def back_garage():
            self.garage_menu.disable()
            self.main_menu.enable()
            self.car.position = (0, 0, 4)
            self.car.camera_offset = (20, 40, -50)
            camera.rotation = (35, -20, 0)
            self.car.visible = False
            grass_track.enable()
            sand_track.disable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
                for i in track.details:
                    i.disable()
            for track in self.grass_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in grass_track.details:
                    detail.enable()
            if self.car.graphics == "fast":
                grass_track.grass.disable()

            self.car.highscore_count = float(self.car.grass_track_hs)

        def garage_button_func():
            self.garage_menu.enable()
            self.main_menu.disable()
            self.cars_menu.enable()
            self.cosmetics_menu.disable()
            self.colours_menu.disable()
            self.car.visible = True
            self.car.position = (-105, -50, -59)
            grass_track.disable()
            sand_track.enable()
            for track in self.tracks:
                for i in track.track:
                    i.disable()
                for i in track.details:
                    i.disable()
            for track in self.sand_track.track:
                track.enable()
            if self.car.graphics != "ultra fast":
                for detail in sand_track.details:
                    detail.enable()

        def cars_menu():
            self.cars_menu.enable()
            self.colours_menu.disable()
            self.cosmetics_menu.disable()

        def colours_menu():
            self.cars_menu.disable()
            self.colours_menu.enable()
            self.cosmetics_menu.disable()

        def cosmetics_menu():
            self.cars_menu.disable()
            self.colours_menu.disable()
            self.cosmetics_menu.enable()

        def sports_car():
            self.car.sports_car()
            self.car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            self.car.viking_helmet.disable()
            self.car.duck.disable()
            self.car.banana.disable()
            self.car.surfinbird.disable()

        def muscle_car():
            self.car.muscle_car()
            self.car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            self.car.viking_helmet.disable()
            self.car.duck.disable()
            self.car.banana.disable()
            self.car.surfinbird.disable()

        def limo():
            self.car.limo()
            self.car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            self.car.viking_helmet.disable()
            self.car.duck.disable()
            self.car.banana.disable()
            self.car.surfinbird.disable()
        def lorry():
            self.car.lorry()
            self.car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            self.car.viking_helmet.disable()
            self.car.duck.disable()
            self.car.banana.disable()
            self.car.surfinbird.disable()
        def hatchback():
            self.car.hatchback()
            self.car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            self.car.viking_helmet.disable()
            self.car.duck.disable()
            self.car.banana.disable()
            self.car.surfinbird.disable()

        def rally():
            self.car.rally_car()
            self.car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            self.car.viking_helmet.disable()
            self.car.duck.disable()
            self.car.banana.disable()
            self.car.surfinbird.disable()

        def sports_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Sports Car"

        def muscle_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Muscle Car"

        def limo_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Limo"
        
        def lorry_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Lorry"

        def hatchback_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Hatchback"

        def rally_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Rally Car"

        def change_colour(colour):
            """
            Changes the car color to the selected color after a small animation.
            """
            if colour == "red":
                if self.car.car_type == "muscle":
                    return
                elif self.car.car_type == "limo":
                    return
                elif self.car.car_type == "lorry":
                    return
                elif self.car.car_type == "hatchback":
                    return
                car.texture = f"{self.car.car_type}-red.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "blue":
                if self.car.car_type == "muscle":
                    return
                elif self.car.car_type == "limo":
                    return
                elif self.car.car_type == "lorry":
                    return
                elif self.car.car_type == "hatchback":
                    return
                elif self.car.car_type == "rally":
                    return
                car.texture = f"{self.car.car_type}-blue.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "green":
                if self.car.car_type == "sports":
                    return
                elif self.car.car_type == "muscle":
                     return
                elif self.car.car_type == "limo":
                    return
                elif self.car.car_type == "lorry":
                    return
                elif self.car.car_type == "rally":
                    return
                car.texture = f"{self.car.car_type}-green.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "orange":
                if self.car.car_type == "sports":
                    return
                elif self.car.car_type == "limo":
                    return
                elif self.car.car_type == "lorry":
                    return
                elif self.car.car_type == "hatchback":
                    return
                elif self.car.car_type == "rally":
                    return
                car.texture = f"{self.car.car_type}-orange.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "black":
                if self.car.car_type == "sports":
                    return
                elif self.car.car_type == "muscle":
                    return
                elif self.car.car_type == "lorry":
                    return
                elif self.car.car_type == "hatchback":
                    return
                elif self.car.car_type == "rally":
                    return
                car.texture = f"{self.car.car_type}-black.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            if colour == "white":
                if self.car.car_type == "sports":
                    return
                elif self.car.car_type == "muscle":
                    return
                elif self.car.car_type == "limo":
                    return
                elif self.car.car_type == "hatchback":
                    return
                elif self.car.car_type == "rally":
                    return
                car.texture = f"{self.car.car_type}-white.png"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)

        def viking_helmet():
                self.car.current_cosmetic = "viking"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.viking_helmet.enabled = not car.viking_helmet.enabled
                car.duck.disable()
                car.banana.disable()
                car.surfinbird.disable()

        def duck():
                self.car.current_cosmetic = "duck"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.duck.enabled = not car.duck.enabled
                car.viking_helmet.disable()
                car.banana.disable()
                car.surfinbird.disable()

        def banana():
                self.car.current_cosmetic = "banana"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.banana.enabled = not car.banana.enabled
                car.duck.disable()
                car.viking_helmet.disable()
                car.surfinbird.disable()

        def surfinbird():
                self.car.current_cosmetic = "surfinbird"
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
                car.surfinbird.enabled = not car.surfinbird.enabled
                car.viking_helmet.disable()
                car.duck.disable()
                car.banana.disable()

        def viking_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Viking Helmet"

        def duck_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Duck"

        def banana_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Banana"
        
        def surfinbird_hover():
            self.garage_name_text.enable()
            self.garage_name_text.text = "Surfin Bird"

        self.start_spin = True

        garage_button = Button(text = "Garage", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)

        back_button_garage = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.garage_menu)
        
        cars_menu_button = Button(text = "Cars", color = color.black, scale_y = 0.1, scale_x = 0.15, x = -0.7, y = -0.3, parent = self.garage_menu)
        colours_menu_button = Button(text = "Colours", color = color.black, scale_y = 0.1, scale_x = 0.15, x = -0.5, y = -0.3, parent = self.garage_menu)
        cosmetics_menu_button = Button(text = "Cosmetics", color = color.black, scale_y = 0.1, scale_x = 0.15, x = -0.3, y = -0.3, parent = self.garage_menu)

        sports_car_button = Button(texture = "sports-car-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.7, alpha = 255, parent = self.cars_menu)
        muscle_car_button = Button(texture = "muscle-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.5, alpha = 255, parent = self.cars_menu)
        limo_button = Button(texture = "limo-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.3, alpha = 255, parent = self.cars_menu)
        lorry_button = Button(texture = "lorry-icon.png", color = color.white, scale = (0.16, 0.1), y = -0.1, x = -0.7, alpha = 255, parent = self.cars_menu)
        hatchback_button = Button(texture = "hatchback-icon.png", color = color.white, scale = (0.16, 0.1), y = -0.1, x = -0.5, alpha = 255, parent = self.cars_menu)
        rally_car_button = Button(texture = "rally-icon.png", color = color.white, scale = (0.16, 0.1), y = -0.1, x = -0.3, alpha = 255, parent = self.cars_menu)

        red_button = Button(color = color.red, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.7, parent = self.colours_menu)
        blue_button = Button(color = color.cyan, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.5, parent = self.colours_menu)
        green_button = Button(color = color.lime, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.3, parent = self.colours_menu)
        orange_button = Button(color = color.orange, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.7, parent = self.colours_menu)
        black_button = Button(color = color.black, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.5, parent = self.colours_menu)
        white_button = Button(color = color.white, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.3, parent = self.colours_menu)

        viking_helmet_button = Button(texture = "viking_helmet-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.7, alpha = 255, parent = self.cosmetics_menu)
        duck_button = Button(texture = "duck-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.5, alpha = 255, parent = self.cosmetics_menu)
        banana_button = Button(texture = "banana-icon.png", color = color.white, scale = (0.16, 0.1), y = 0.1, x = -0.3, alpha = 255, parent = self.cosmetics_menu)
        surfinbird_button = Button(texture = "surfinbird-icon.png", color = color.white, scale = (0.16, 0.1), y = -0.1, x = -0.7, alpha = 255, parent = self.cosmetics_menu)

        self.garage_name_text = Text("Surfin Bird", scale = 1.5, color = color.white, line_height = 2, origin = 0, x = -0.5, y = -0.4, parent = self.garage_menu)
        self.garage_name_text.disable()

        self.garage_unlocked_text = Text("Beat Mandaw in Every Track", scale = 1.5, color = color.orange, line_height = 2, origin = 0, y = 0.3, parent = self.garage_menu)
        self.garage_unlocked_text.disable()

        garage_button.on_click = Func(garage_button_func)
        cars_menu_button.on_click = Func(cars_menu)
        colours_menu_button.on_click = Func(colours_menu)
        cosmetics_menu_button.on_click = Func(cosmetics_menu)

        back_button_garage.on_click = Func(back_garage)
        
        sports_car_button.on_click = Func(sports_car)
        muscle_car_button.on_click = Func(muscle_car)
        limo_button.on_click = Func(limo)
        lorry_button.on_click = Func(lorry)
        hatchback_button.on_click = Func(hatchback)
        rally_car_button.on_click = Func(rally)

        sports_car_button.on_mouse_enter = Func(sports_hover)
        sports_car_button.on_mouse_exit = Func(self.garage_name_text.disable)
        muscle_car_button.on_mouse_enter = Func(muscle_hover)
        muscle_car_button.on_mouse_exit = Func(self.garage_name_text.disable)
        limo_button.on_mouse_enter = Func(limo_hover)
        limo_button.on_mouse_exit = Func(self.garage_name_text.disable)
        lorry_button.on_mouse_enter = Func(lorry_hover)
        lorry_button.on_mouse_exit = Func(self.garage_name_text.disable)
        hatchback_button.on_mouse_enter = Func(hatchback_hover)
        hatchback_button.on_mouse_exit = Func(self.garage_name_text.disable)
        rally_car_button.on_mouse_enter = Func(rally_hover)
        rally_car_button.on_mouse_exit = Func(self.garage_name_text.disable)

        red_button.on_click = Func(change_colour, "red")
        blue_button.on_click = Func(change_colour, "blue")
        green_button.on_click = Func(change_colour, "green")
        orange_button.on_click = Func(change_colour, "orange")
        black_button.on_click = Func(change_colour, "black")
        white_button.on_click = Func(change_colour, "white")

        viking_helmet_button.on_click = Func(viking_helmet)
        duck_button.on_click = Func(duck)
        banana_button.on_click = Func(banana)
        surfinbird_button.on_click = Func(surfinbird)

        viking_helmet_button.on_mouse_enter = Func(viking_hover)
        viking_helmet_button.on_mouse_exit = Func(self.garage_name_text.disable)
        duck_button.on_mouse_enter = Func(duck_hover)
        duck_button.on_mouse_exit = Func(self.garage_name_text.disable)
        banana_button.on_mouse_enter = Func(banana_hover)
        banana_button.on_mouse_exit = Func(self.garage_name_text.disable)
        surfinbird_button.on_mouse_enter = Func(surfinbird_hover)
        surfinbird_button.on_mouse_exit = Func(self.garage_name_text.disable)

        

    def garage_locked_text(self, warning):
        self.garage_unlocked_text.enable()
        self.garage_unlocked_text.text = warning
        self.garage_unlocked_text.shake()
        invoke(self.garage_unlocked_text.disable, delay = 1)

    def update(self):
        if not self.start_menu.enabled and not self.main_menu.enabled and not self.settings_menu.enabled and not self.race_menu.enabled and not self.maps_menu.enabled and not self.settings_menu.enabled and not self.garage_menu.enabled and not self.controls_menu.enabled and not self.host_menu.enabled and not self.server_menu.enabled and not self.created_server_menu.enabled and not self.video_menu.enabled and not self.gameplay_menu.enabled and not self.audio_menu.enabled and not self.quit_menu.enabled:
            self.car.camera_follow = True
        else:
            self.car.camera_follow = False

       
            

        # Set the camera's position and make the car rotate
        if self.start_menu.enabled or self.host_menu.enabled or self.garage_menu.enabled or self.server_menu.enabled or self.quit_menu.enabled:
            if not held_keys["right mouse"]:
                if self.start_spin:
                    self.car.rotation_y += 15 * time.dt
            else:
                self.car.rotation_y = mouse.x * 200

            camera.position = lerp(camera.position, self.car.position + self.car.camera_offset, time.dt * self.car.camera_speed)

            if self.start_menu.enabled or self.quit_menu.enabled:
                self.car.camera_offset = (-25, 4, 0)
                camera.rotation = (5, 90, 0)
            elif self.host_menu.enabled:
                self.car.camera_offset = (-25, 8, 0)
                camera.rotation = (14, 90, 0)
            else:
                self.car.camera_offset = (-25, 6, 5)
                camera.rotation = (10, 90, 0)
        else:
            if not self.car.camera_follow:
                camera.rotation = (35, -20, 0)
                camera.position = lerp(camera.position, self.car.position + (20, 40, -50), time.dt * self.car.camera_speed)

        # If the host menu or server menu is enabled, save username
        if self.host_menu.enabled or self.server_menu.enabled or self.created_server_menu.enabled:
            with open(self.car.username_path, "w") as user:
                if self.created_server_menu.enabled:
                    user.write(self.username_created_server.text)
                else:
                    user.write(self.car.username.text)

        # If multiplayer, start leaderboard
        if self.car.multiplayer_update:
            for menu in self.menus:
                if menu.enabled == False:
                    if self.sand_track.enabled or self.grass_track.enabled or self.snow_track.enabled or self.forest_track.enabled or self.savannah_track.enabled:
                        invoke(self.start_leaderboard, delay = 0.1)
                else:
                    for l in self.leaderboard_texts:
                        l.disable()
        else:
            for l in self.leaderboard_texts:
                l.disable()
            
    def start_leaderboard(self):
        for l in self.leaderboard_texts:
            l.enable()

        self.leaderboard_01.text = str(self.car.leaderboard_01)
        self.leaderboard_02.text = str(self.car.leaderboard_02)
        self.leaderboard_03.text = str(self.car.leaderboard_03)
        self.leaderboard_04.text = str(self.car.leaderboard_04)
        self.leaderboard_05.text = str(self.car.leaderboard_05)
    
    def input(self, key):
        # Pause menu
        if not self.start_menu.enabled and not self.main_menu.enabled and not self.server_menu.enabled and not self.settings_menu.enabled and not self.race_menu.enabled and not self.maps_menu.enabled and not self.settings_menu.enabled and not self.garage_menu.enabled and not self.audio_menu.enabled and not self.controls_menu.enabled and not self.host_menu.enabled and not self.created_server_menu.enabled and not self.video_menu.enabled and not self.gameplay_menu.enabled and not self.quit_menu.enabled:
            if key == "escape":
                self.pause_menu.enabled = not self.pause_menu.enabled
                mouse.locked = not mouse.locked

            self.start_spin = False

            if self.car.reset_count_timer.enabled == False:
                self.car.timer.enable()
            else:
                self.car.timer.disable()
             
            self.car.highscore.enable()
            if self.car.gamemode == "time trial":
                self.car.laps_text.enable()
            elif self.car.gamemode == "drift":
                self.car.drift_text.enable()
                self.car.drift_timer.enable()
        else:
            self.car.timer.disable()
            self.car.reset_count_timer.disable()
            self.car.highscore.disable()
            self.car.laps_text.disable()
            self.car.drift_text.disable()
            self.car.drift_timer.disable()
            self.car.camera_speed = 8
            self.start_spin = True

        # Audio
        if self.car.audio:
            for menu in self.menus:
                if menu.enabled:
                    for i, e in enumerate(menu.children):
                        if e.hovered and key == "left mouse down":
                            self.click.volume = self.car.volume * 5
                            self.click.play()
        
        if self.audio_menu.enabled:
            self.car.volume = self.volume.value

        # Quit Menu
        if self.start_menu.enabled or self.quit_menu.enabled:
            if key == "escape":
                self.quit_menu.enabled = not self.quit_menu.enabled
                self.start_menu.enabled = not self.start_menu.enabled

        # Settings Menu
        if key == "escape":
            if self.settings_menu.enabled:
                self.settings_menu.disable()
                self.main_menu.enable()
            elif self.video_menu.enabled:
                self.video_menu.disable()
                self.settings_menu.enable()
            elif self.controls_menu.enabled:
                self.controls_menu.disable()
                self.settings_menu.enable()
            elif self.gameplay_menu.enabled:
                self.gameplay_menu.disable()
                self.settings_menu.enable()
            elif self.audio_menu.enabled:
                self.audio_menu.disable()
                self.settings_menu.enable()

        if self.start_spin:
            self.car.copy_normals = False
        else:
            self.car.copy_normals = True