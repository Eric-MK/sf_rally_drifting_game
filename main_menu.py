from ursina import *
from ursina import curve
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, car, sand_track, grass_track):
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
        
        self.sun = None

        self.click = Audio("click.wav", False, False, volume = 10)

        self.tracks = [
            self.sand_track, self.grass_track]

        # Animate the menu
        for menu in (self.start_menu, self.main_menu, self.race_menu, self.maps_menu,  self.gameplay_menu,  self.pause_menu, self.quit_menu):
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

        singleplayer_button = Button(text = "LETS GO", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = 0.05, parent = self.start_menu)
        
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

          # Main Menu

        def back_singleplayer():
            self.car.position = (-80, -42, 18.8)
            self.car.rotation = (0, 90, 0)
            self.car.visible = True
            self.grass_track.enable()
            self.start_menu.enable()
            self.main_menu.disable()
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

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        back_button_singleplayer = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.34, parent = self.main_menu)
        back_button_singleplayer.on_click = Func(back_singleplayer)

        # Maps Menu

        def start():
            self.main_menu.disable()
            if self.car:
                self.maps_menu.enable()
            else:
                self.race_menu.enable()

        def back():
            self.maps_menu.disable()
            if self.car:
                self.main_menu.enable()
            else:
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
            if sand_track.unlocked:
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
            if grass_track_button:
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
                highscore_text.text = "Highscore: " + str(round(self.car.sand_track_hs, 2)) + "\n Kevin: 15.55" + "\n Moses: 17.10" + "\n David: 18.30"+ "\n Adrian: 20.10" + "\n Eric: 21.30"

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
            
            if self.car.gamemode == "race":
                    highscore_text.enable()
                    highscore_text.text = "Highscore: " + str(round(self.car.grass_track_hs, 2)) 
                    highscore_text.text = "Highscore: " + str(round(self.car.grass_track_hs, 2)) + "\n Kevin: 15.55" + "\n Moses: 17.10" + "\n David: 18.30"+ "\n Adrian: 20.10" + "\n Eric: 21.30"
            unlocked_text.disable()
            grass_track.alpha = 255

        
            

        start_button = Button(text = "Start Game", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        sand_track_button = Button(text = "Safari", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "Grass Plain", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        back_button = Button(text = "<- Back", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.maps_menu)
        
        unlocked_text = Text("Get Less Than 20 seconds on Safari to Unlock Grass Plain", scale = 1.5, color = color.orange, line_height = 2, origin = 0, y = -0.1, parent = self.maps_menu)
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

        start_button.on_click = Func(start)
        sand_track_button.on_click = Func(sand_track_func)
        grass_track_button.on_click = Func(grass_track_func)
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
            self.car.ai = False

        def drift_func():
            if self.car.drift_unlocked:
                self.race_menu.disable()
                self.maps_menu.enable()
                self.car.gamemode = "drift"
                self.car.count = 0.0
                self.car.reset_count = 0.0
                self.car.ai = False
            else:
                unlocked_text.parent = self.race_menu
                unlocked_text.y = -0.3
                unlocked_text.enable()
                unlocked_text.shake()
                unlocked_text.text = "Unlock Every Track to play Drift Gamemode"
                invoke(setattr, unlocked_text, "parent", self.maps_menu, delay = 1.5)
                invoke(setattr, unlocked_text, "y", -0.1, delay = 1.6)

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
        p_respawn_button = Button(text = "Restart", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.01, parent = self.pause_menu)
        p_mainmenu_button = Button(text = "Main Menu", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.13, parent = self.pause_menu)
        p_mainmenu_button.on_click = Func(main_menu)
        p_respawn_button.on_click = Func(respawn)
        p_resume_button.on_click = Func(resume)


    def update(self):
        if not self.start_menu.enabled and not self.main_menu.enabled and not self.settings_menu.enabled and not self.race_menu.enabled and not self.maps_menu.enabled and not self.settings_menu.enabled and not self.garage_menu.enabled and not self.controls_menu.enabled and not self.host_menu.enabled and not self.server_menu.enabled and not self.created_server_menu.enabled and not self.video_menu.enabled and not self.gameplay_menu.enabled and not self.audio_menu.enabled and not self.quit_menu.enabled:
            self.car.camera_follow = True
        else:
            self.car.camera_follow = False

        
    
    def input(self, key):
        # Pause menu
        if not self.start_menu.enabled and not self.main_menu.enabled  and not self.settings_menu.enabled and not self.race_menu.enabled and not self.maps_menu.enabled and not self.settings_menu.enabled  and not self.audio_menu.enabled and not self.controls_menu.enabled and not self.host_menu.enabled  and not self.video_menu.enabled and not self.gameplay_menu.enabled and not self.quit_menu.enabled:
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