from ursina import *
from direct.stdpy import thread

from car import Car


from main_menu import MainMenu

from sun import SunLight

from tracks.sand_track import SandTrack
from tracks.grass_track import GrassTrack

Text.default_font = "./assets/Roboto.ttf"
Text.default_resolution = 1080 * Text.size

# Window

app = Ursina()
window.title = "Rally"
window.borderless = False
window.show_ursina_splash = True
window.cog_button.disable()
window.fps_counter.disable()
window.exit_button.disable()

if sys.platform != "darwin":
    window.fullscreen = True
else:
    window.size = window.fullscreen_size
    window.position = Vec2(
        int((window.screen_resolution[0] - window.fullscreen_size[0]) / 2),
        int((window.screen_resolution[1] - window.fullscreen_size[1]) / 2)
    )

# Starting new thread for assets

def load_assets():
    models_to_load = [
        # Cars
        "sports-car.obj", 
        # Tracks
        "sand_track.obj", "grass_track.obj",  "particles.obj",
        # Track Bounds
        "sand_track_bounds.obj", "grass_track_bounds.obj", 
        # Track Details
        "rocks-sand.obj", "cacti-sand.obj", "trees-grass.obj", "thintrees-grass.obj", "rocks-grass.obj", "grass-grass_track.obj", "trees-snow.obj", 
        "thintrees-snow.obj", "rocks-snow.obj", "trees-forest.obj", "thintrees-forest.obj", "rocks-savannah.obj", "trees-savannah.obj",
        "trees-lake.obj", "thintrees-lake.obj", "rocks-lake.obj", "bigrocks-lake.obj", "grass-lake.obj", "lake_bounds.obj",
       
    ]

    textures_to_load = [
        # Car Textures
        # Sports Car
        "sports-red.png",
        # Track Textures
        "sand_track.png", "grass_track.png", 
        # Track Detail Textures
        "rock-sand.png", "cactus-sand.png", "tree-grass.png", "thintree-grass.png", "rock-grass.png", "grass-grass_track.png",
        # Particle Textures
        "particle_sand_track.png", "particle_grass_track.png"
        
    ]

    for i, m in enumerate(models_to_load):
        load_model(m)

    for i, t in enumerate(textures_to_load):
        load_texture(t)

try:
    thread.start_new_thread(function = load_assets, args = "")
except Exception as e:
    print("error starting thread", e)

# Car
car = Car()
car.sports_car()

# Tracks
sand_track = SandTrack(car)
grass_track = GrassTrack(car)

car.sand_track = sand_track
car.grass_track = grass_track



# Main menu
main_menu = MainMenu(car, sand_track, grass_track)

# Lighting + shadows
sun = SunLight(direction = (-0.7, -0.9, 0.5), resolution = 3072, car = car)
ambient = AmbientLight(color = Vec4(0.5, 0.55, 0.66, 0) * 0.75)

render.setShaderAuto()

main_menu.sun = sun

# Sky
Sky(texture = "sky")


app.run()