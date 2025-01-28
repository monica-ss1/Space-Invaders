import pygame as pg
import time

class Sound:
    def __init__(self):
        pg.mixer.init()  # Initialize the mixer
        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover2.mp3')
        self.faster = pg.mixer.Sound('sounds/Running.mp3')

        # Set volume for each sound
        self.pickup.set_volume(0.1)
        self.gameover.set_volume(0.1)
        self.faster.set_volume(0.1)

        # Load background music
        pg.mixer.music.load('sounds/Megalovonia.mp3')
        pg.mixer.music.set_volume(0.2)
        
        self.music_playing = False  # Tracks if music is currently playing
        self.music_position = 0     # Keeps track of where the music was stopped
    
    # Play background music, resuming from the last position if stopped
    def play_background(self):
        self.stop_all_sounds()  # Ensure no other sound is playing
        print(self.music_position)
        if self.music_position > 0:
            # Resume from the saved position if music was previously playing
            print(f'started music at {self.music_position}')
            pg.mixer.music.play(-1, self.music_position / 1000.0)  # Convert milliseconds to seconds
        else:
            # Start from the beginning if no position has been saved or if music wasn't playing
            pg.mixer.music.play(-1, 0.0)
        
        self.music_playing = True
    
    # Play faster sound (and stop background music)
    def play_faster(self):
        self.stop_all_sounds()  # Ensure no other sound is playing
        self.faster.play()  # Play the faster sound
    
    # Stop the faster sound
    def stop_faster(self):
        self.faster.stop()
    
    # Play pickup sound (without stopping background music)
    def play_pickup(self):
        self.pickup.play()  # Pickup sound doesn't stop background music
    
    # Play game over sound and stop other music/sounds
    def play_gameover(self):
        self.stop_all_sounds()  # Ensure no other sound is playing
        self.gameover.play()  # Play the gameover sound
        time.sleep(2.0)  # Optional: Sleep for the duration of the sound if you want to wait
    
    # Toggle background music on/off
    def toggle_background(self):
        if self.music_playing:
            self.stop_background()  # Stop if music is playing
        else:
            self.play_background()  # Start if no music is playing
    
    # Stop background music and save the position
    def stop_background(self):
        if self.music_playing:
            self.music_position = pg.mixer.music.get_pos()  # Save current position
            print(f"Music stopped at: {self.music_position} ms")
            pg.mixer.music.stop()
            self.music_playing = False
    
    # Stop all sounds and music
    def stop_all_sounds(self):
        if pg.mixer.music.get_busy():
            self.music_position = pg.mixer.music.get_pos()  # Save current position
            print(f"Music stopped at: {self.music_position} ms")
        pg.mixer.music.stop()
        self.pickup.stop()     # Stop pickup sound if playing
        self.faster.stop()     # Stop faster sound if playing
        self.gameover.stop()   # Stop gameover sound if playing
        self.music_playing = False
