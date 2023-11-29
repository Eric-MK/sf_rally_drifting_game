from ursina import *
from ursina import curve
from particles import Particles, TrailRenderer
import json

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)
Text.default_resolution = 1080 * Text.size

class Car(Entity):
    def __init__(self, position = (0, 0, 4), rotation = (0, 0, 0), topspeed = 30, acceleration = 0.35, braking_strength = 30, friction = 0.6, camera_speed = 8, drift_speed = 35):
        super().__init__(
            model = "sports-car.obj",
            texture = "sports-red.png",
            collider = "box",
            position = position,
            rotation = rotation,
        )

        # Rotation parent
        self.rotation_parent = Entity()

        # Controls
        self.controls = "wasd"

        # Car's values
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.steering_amount = 8
        self.topspeed = topspeed
        self.braking_strenth = braking_strength
        self.camera_speed = camera_speed
        self.acceleration = acceleration
        self.friction = friction
        self.drift_speed = drift_speed
        self.drift_amount = 4.5
        self.turning_speed = 5
        self.max_drift_speed = 40
        self.min_drift_speed = 20
        self.pivot_rotation_distance = 1

        # Camera Follow
        self.camera_angle = "top"
        self.camera_offset = (0, 60, -70)
        self.camera_rotation = 40
        self.camera_follow = False
        self.change_camera = False
        self.c_pivot = Entity()
        self.camera_pivot = Entity(parent = self.c_pivot, position = self.camera_offset)

        # Pivot for drifting
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation
        self.drifting = False

        # Car Type
        self.car_type = "sports"

        # Particles
        self.particle_time = 0
        self.particle_amount = 0.07 # The lower, the more
        self.particle_pivot = Entity(parent = self)
        self.particle_pivot.position = (0, -1, -2)

        # TrailRenderer
        self.trail_pivot = Entity(parent = self, position = (0, -1, 2))

        self.trail_renderer1 = TrailRenderer(parent = self.particle_pivot, position = (0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        self.trail_renderer2 = TrailRenderer(parent = self.particle_pivot, position = (-0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        self.trail_renderer3 = TrailRenderer(parent = self.trail_pivot, position = (0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        self.trail_renderer4 = TrailRenderer(parent = self.trail_pivot, position = (-0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        
        self.trails = [self.trail_renderer1, self.trail_renderer2, self.trail_renderer3, self.trail_renderer4]
        self.start_trail = True

        # Audio
        self.audio = True
        self.volume = 1
        self.start_sound = True
        self.start_fall = True
        self.drive_sound = Audio("rally.mp3", loop = True, autoplay = False, volume = 0.5)
        self.dirt_sound = Audio("dirt-skid.mp3", loop = True, autoplay = False, volume = 0.8)
        self.skid_sound = Audio("skid.mp3", loop = True, autoplay = False, volume = 0.5)
        self.hit_sound = Audio("hit.wav", autoplay = False, volume = 0.5)
        self.drift_swush = Audio("unlock.mp3", autoplay = False, volume = 0.8)

        # Collision
        self.copy_normals = False
        self.hitting_wall = False

        # Making tracks accessible in update
        self.sand_track = None
        self.grass_track = None
        self.snow_track = None
        self.forest_track = None
        self.savannah_track = None
        self.lake_track = None

        # Cosmetics
        self.current_cosmetic = "none"
        self.viking_helmet = Entity(model = "viking_helmet.obj", texture = "viking_helmet.png", parent = self)
        self.duck = Entity(model = "duck.obj", parent = self)
        self.banana = Entity(model = "banana.obj", parent = self)
        self.surfinbird = Entity(model = "surfinbird.obj", texture = "surfinbird.png", parent = self)
        self.surfboard = Entity(model = "surfboard.obj", texture = "surfboard.png", parent = self.surfinbird)
        self.cosmetics = [self.viking_helmet, self.duck, self.banana, self.surfinbird]
        self.viking_helmet.disable()
        self.duck.disable()
        self.banana.disable()
        self.surfinbird.disable()

        # Graphics
        self.graphics = "fancy"

        # Stopwatch/Timer
        self.timer_running = False
        self.count = 0.0
        self.highscore_count = None
        self.last_count = self.count
        self.reset_count = 0.0
        self.timer = Text(text = "", origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        self.highscore = Text(text = "", origin = (0, 0), size = 0.05, scale = (0.6, 0.6), position = (-0.7, 0.38))
        self.laps_text = Text(text = "", origin = (0, 0), size = 0.05, scale = (1.1, 1.1), position = (0, 0.43))
        self.reset_count_timer = Text(text = str(round(self.reset_count, 1)), origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        
        self.timer.disable()
        self.highscore.disable()
        self.laps_text.disable()
        self.reset_count_timer.disable()

        self.gamemode = "race"
        self.start_time = False
        self.laps = 0
        self.laps_hs = 0
        self.anti_cheat = 1

        # Drift Gamemode
        self.drift_text = Text(text = "", origin = (0, 0), color = color.white, size = 0.05, scale = (1.1, 1.1), position = (0, 0.43), visible = False)
        self.drift_timer = Text(text = "", origin = (0, 0), size = 0.05, scale = (1, 1), position = (0.7, 0.43))
        self.start_drift = False
        self.drift_score = 0
        self.drift_time = 0
        self.drift_multiplier = 20
        self.get_hundred = False
        self.get_thousand = False
        self.get_fivethousand = False

        # Bools
        self.driving = False
        self.braking = False

        self.ai = False
        self.ai_list = []

        # Multiplayer
        self.multiplayer = False
        self.multiplayer_update = False
        self.server_running = False

        # Shows whether you are connected to a server or not
        self.connected_text = True
        self.disconnected_text = True

        # Camera shake
        self.shake_amount = 0.1
        self.can_shake = False
        self.camera_shake_option = True

        # Get highscore from json file
        path = os.path.dirname(sys.argv[0])
        self.highscore_path = os.path.join(path, "./highscore/highscore.json")
        
        try:
            with open(self.highscore_path, "r") as hs:
                self.highscores = json.load(hs)
        except FileNotFoundError:
            with open(self.highscore_path, "w+") as hs:
                self.reset_highscore()
                self.highscores = json.load(hs)

        self.sand_track_hs = self.highscores["race"]["sand_track"]
        self.grass_track_hs = self.highscores["race"]["grass_track"]
        self.snow_track_hs = self.highscores["race"]["snow_track"]
        self.forest_track_hs = self.highscores["race"]["forest_track"]
        self.savannah_track_hs = self.highscores["race"]["savannah_track"]
        self.lake_track_hs = self.highscores["race"]["lake_track"]

        self.sand_track_laps = self.highscores["time_trial"]["sand_track"]
        self.grass_track_laps = self.highscores["time_trial"]["grass_track"]
        self.snow_track_laps = self.highscores["time_trial"]["snow_track"]
        self.forest_track_laps = self.highscores["time_trial"]["forest_track"]
        self.savannah_track_laps = self.highscores["time_trial"]["savannah_track"]
        self.lake_track_laps = self.highscores["time_trial"]["lake_track"]

        self.sand_track_drift = self.highscores["drift"]["sand_track"]
        self.grass_track_drift = self.highscores["drift"]["grass_track"]
        self.snow_track_drift = self.highscores["drift"]["snow_track"]
        self.forest_track_drift = self.highscores["drift"]["forest_track"]
        self.savannah_track_drift = self.highscores["drift"]["savannah_track"]
        self.lake_track_drift = self.highscores["drift"]["lake_track"]

        self.highscore_count = self.sand_track_hs
        self.highscore_count = float(self.highscore_count)

        self.username_path = os.path.join(path, "./highscore/username.txt")
        with open(self.username_path, "r") as username:
            self.username_text = username.read()

        self.unlocked_json = os.path.join(path, "./highscore/unlocked.json")
        try:
            with open(self.unlocked_json, "r") as u:
                self.unlocked = json.load(u)
        except FileNotFoundError:
            with open(self.unlocked_json, "w+") as u:
                self.save_unlocked()
                self.unlocked = json.load(u)

        self.beat_mandaw_sand_track = False
        self.beat_mandaw_grass_track = False
        self.beat_mandaw_snow_track = False
        self.beat_mandaw_forest_track = False
        self.beat_mandaw_savannah_track = False
        self.beat_mandaw_lake_track = False

        self.model_path = str(self.model).replace("render/scene/car/", "")

        invoke(self.set_unlocked, delay = 1)
        invoke(self.update_model_path, delay = 3)

    def sports_car(self):
        self.car_type = "sports"
        self.model = "sports-car.obj"
        self.texture = "sports-red.png"
        self.drive_sound.clip = "sports.mp3"
        self.topspeed = 30
        self.acceleration = 0.38
        self.drift_amount = 5
        self.turning_speed = 5
        self.min_drift_speed = 18
        self.max_drift_speed = 38
        self.max_rotation_speed = 3
        self.steering_amount = 8
        self.particle_pivot.position = (0, -1, -1.5)
        self.trail_pivot.position = (0, -1, 1.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0

    def muscle_car(self):
        self.car_type = "muscle"
        self.model = "muscle-car.obj"
        self.texture = "muscle-orange.png"
        self.drive_sound.clip = "muscle.mp3"
        self.topspeed = 38
        self.acceleration = 0.32
        self.drift_amount = 6
        self.turning_speed = 10
        self.min_drift_speed = 22
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8.5
        self.particle_pivot.position = (0, -1, -1.8)
        self.trail_pivot.position = (0, -1, 1.8)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0

    def limo(self):
        self.car_type = "limo"
        self.model = "limousine.obj"
        self.texture = "limo-black.png"
        self.drive_sound.clip = "limo.mp3"
        self.topspeed = 30
        self.acceleration = 0.33
        self.drift_amount = 5.5
        self.turning_speed = 8
        self.min_drift_speed = 20
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8
        self.particle_pivot.position = (0, -1, -3.5)
        self.trail_pivot.position = (0, -1, 3.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0.1

    def lorry(self):
        self.car_type = "lorry"
        self.model = "lorry.obj"
        self.texture = "lorry-white.png"
        self.drive_sound.clip = "lorry.mp3"
        self.topspeed = 30
        self.acceleration = 0.3
        self.drift_amount = 7
        self.turning_speed = 7
        self.min_drift_speed = 20
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 7.5
        self.particle_pivot.position = (0, -1, -3.5)
        self.trail_pivot.position = (0, -1, 3.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 1.5

    def hatchback(self):
        self.car_type = "hatchback"
        self.model = "hatchback.obj"
        self.texture = "hatchback-green.png"
        self.drive_sound.clip = "hatchback.mp3"
        self.topspeed = 28
        self.acceleration = 0.43
        self.drift_amount = 6
        self.turning_speed = 15
        self.min_drift_speed = 20
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8.5
        self.particle_pivot.position = (0, -1, -1.5)
        self.trail_pivot.position = (0, -1, 1.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0.4

    def rally_car(self):
        self.car_type = "rally"
        self.model = "rally-car.obj"
        self.texture = "rally-red.png"
        self.drive_sound.clip = "rally.mp3"
        self.topspeed = 34
        self.acceleration = 0.46
        self.drift_amount = 4
        self.turning_speed = 7
        self.min_drift_speed = 22
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8.5
        self.particle_pivot.position = (0, -1, -1.5)
        self.trail_pivot.position = (0, -1, 1.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0.3

    def update(self):
        # Stopwatch/Timer
        # Race Gamemode
        if self.gamemode == "race":
            self.highscore.text = str(round(self.highscore_count, 1))
            self.laps_text.disable()
            if self.timer_running:
                self.count += time.dt
                self.reset_count += time.dt
        # Time Trial Gamemode
        elif self.gamemode == "time trial":
            self.highscore.text = str(self.laps_hs)
            self.laps_text.text = str(self.laps)
            if self.timer_running:
                self.count -= time.dt
                self.reset_count -= time.dt
                if self.count <= 0.0:
                    self.count = 100.0
                    self.reset_count = 100.0
                    self.timer_running = False

                    if self.laps >= self.laps_hs:
                        self.laps_hs = self.laps

                    self.laps = 0

                    if self.sand_track.enabled:
                        self.sand_track_laps = self.laps_hs
                    elif self.grass_track.enabled:
                        self.grass_track_laps = self.laps_hs
                    elif self.snow_track.enabled:
                        self.snow_track_laps = self.laps_hs
                    elif self.forest_track.enabled:
                        self.forest_track_laps = self.laps_hs
                    elif self.savannah_track.enabled:
                        self.savannah_track_laps = self.laps_hs
                    elif self.lake_track.enabled:
                        self.lake_track_laps = self.laps_hs

                    self.start_time = False

                    self.save_highscore()
                    self.reset_car()
        # Drift Gamemode
        elif self.gamemode == "drift":
            self.timer.text = str(int(self.drift_score))
            self.drift_text.text = str(int(self.count))
            self.drift_timer.text = str(float(round(self.drift_time, 1)))
            self.laps_text.disable()
            if self.timer_running:
                self.drift_time -= time.dt
                if self.drifting and held_keys["w"]:
                    self.count += self.drift_multiplier * time.dt
                    self.drift_multiplier += time.dt * 10
                    self.start_drift = True
                    self.drift_text.visible = True
                    self.drift_text.x = 0

                    if abs(100 - self.count) <= 5 or abs(200 - self.count) <= 20:
                        if not self.get_hundred:
                            self.animate_text(self.drift_text, 1.7, 1.1)