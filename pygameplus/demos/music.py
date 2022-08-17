
import code
from importlib import resources
from pygameplus import *


def main ():
    # Set up the screen
    screen = Screen(640, 360, "PyGame Plus")
    screen.open()
    
    # Populate the music stream
    for x in range(3, 16, 3):
        with resources.path("pygameplus.demos.audio", f"sample-{x}s.mp3") as audio_path:
            music_stream.add_tracks(audio_path)

    music_stream.repeat = False
    music_stream.repeat_one = False

    def play_music ():
        music_stream.play()

    def stop_music ():
        music_stream.stop()

    def pause_music ():
        music_stream.pause()

    def fade_in_music ():
        music_stream.play(2)

    def fade_out_music ():
        music_stream.stop(3)

    def skip_to_next_track ():
        music_stream.skip_to_next(1)

    def skip_to_prev_track ():
        music_stream.skip_to_previous(1)

    def skip_to_first_track ():
        music_stream.skip_to_first(1)

    def create_skip_to_index_track (index):
        def skip_to_index_track ():
            music_stream.skip_to_index(index, 1)
        return skip_to_index_track

    def add_track ():
        with resources.path("pygameplus.demos.audio", f"hampster-march.mp3") as audio_path:
            music_stream.add_tracks(audio_path)

    def insert_track ():
        with resources.path("pygameplus.demos.audio", f"hampster-march.mp3") as audio_path:
            music_stream.insert_track(3, audio_path)

    def remove_track ():
        with resources.path("pygameplus.demos.audio", f"hampster-march.mp3") as audio_path:
            music_stream.remove_track(audio_path)

    def pop_track ():
        music_stream.pop_track(3)

    def pop_last_track ():
        music_stream.pop_track()

    def clear_tracks ():
        music_stream.clear_tracks()

    def toggle_repeat ():
        music_stream.repeat = not music_stream.repeat

    def toggle_repeat_one ():
        music_stream.repeat_one = not music_stream.repeat_one
            

    screen.on_key_press(play_music, 'return')
    screen.on_key_press(stop_music, 'backspace')
    screen.on_key_press(pause_music, 'space')
    screen.on_key_press(fade_in_music, 'f')
    screen.on_key_press(fade_out_music, 'g')
    screen.on_key_press(skip_to_next_track, 'right')
    screen.on_key_press(skip_to_prev_track, 'left')
    screen.on_key_press(skip_to_first_track, 'up')
    for i in range(5):
        screen.on_key_press(create_skip_to_index_track(i), str(i))
    screen.on_key_press(add_track, 'a')
    screen.on_key_press(insert_track, 'i')
    screen.on_key_press(remove_track, 'd')
    screen.on_key_press(pop_track, 'p')
    screen.on_key_press(pop_last_track, 'l')
    screen.on_key_press(clear_tracks, 'c')
    screen.on_key_press(toggle_repeat, 'r')
    screen.on_key_press(toggle_repeat_one, 'o')


    def handle_track_done (index, track):
        print(f"DONE TRACK {index}: {track}")

    def handle_queue_done ():
        print(f"DONE QUEUE")

    music_stream.on_done_track(handle_track_done)
    music_stream.on_done_queue(handle_queue_done)
    

    main_vars = globals()
    main_vars.update(locals())
    
    def interact ():
        code.interact(local=main_vars)
    
    screen.on_key_press(interact, "escape")

    start_game()


# Call the "main" function if running this script
if __name__ == "__main__":
    main()
