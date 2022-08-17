# Copyright 2022 Casey Devet
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("always")

import pygame
from . import pgputils

# Create an event type for the end of a track
MUSIC_END = pygame.event.custom_type()
pygame.mixer.music.set_endevent(MUSIC_END)


class MusicStreamException (Exception):
    pass

class MusicStreamWarning (Warning):
    pass
    

class MusicStream (object):
    '''
    A MusicStream is a queue that manages a collection of music to
    be streamed during the game.  Music is loaded in chunks for
    efficiency and the next track is pre-loaded for a seemless
    transition.

    You will not be able to create your own MusicStream.  Instead,
    you should use the `music_stream` variable, included in this
    module, which contains the single possible MusicStream object.

    Note that the music stream will only be able to work properly
    when the game loop is running.
    '''

    # Used to enforce this as a singleton class
    __the_music_stream = None

    def __init__ (self):
        '''
        Creates the single MusicStream object.  DO NOT USE!
        The `music_stream` variable holds the single possible
        MusicStream.
        '''

        # Throw an error if the singleton has already been created.
        if MusicStream.__the_music_stream is not None:
            raise Exception('The music stream has already been created!')
        MusicStream.__the_music_stream = self

        # Initialize with no files and stopped
        self._files = []
        self._in_use = False
        self._paused = False
        self._track_index = None
        self._loaded_index = None
        self._queued_index = None
        self._repeat = False
        self._repeat_one = False

        # Holds any user-defined event handlers
        self._done_track_func = None
        self._done_queue_func = None

        # Stores whether or not any errors are block
        self._suppress_errors = False


    def __str__ (self):
        if self._track_index is None:
            return f'<MusicStream({self.status}, no tracks)'
        return f'<MusicStream({self.status}, track index {self._track_index} of {len(self._files)}: {self.current_track})'

    def __repr__ (self):
        return self.__str__()


    def _load_track (self, index=None):
        '''
        Helper function that loads the track with the given index
        into the pygame music stream.  By default, load the current
        track.
        '''
        if index is None:
            index = self._track_index
        try:
            pygame.mixer.music.load(self._files[index])
            self._loaded_index = index
        except:
            self._error(f'Could not load track: {self._files[0]}')
            pygame.mixer.music.unload()
            self._loaded_index = None


    def _queue_track (self, index=None):
        '''
        Helper function that queues the track with the given index
        into the pygame music stream.  By default, queue the current
        track.
        '''
        if index is None:
            index = self._track_number
        try:
            pygame.mixer.music.queue(self._files[index])
            self._queued_index = index
        except:
            self._error(f'Could not queue track: {self._files[0]}')
            self._queued_index = None


    def _queue_next (self):
        '''
        Helper function that queues the next track to play in the
        pygame music stream.
        '''

        # Only queue the next track is the music is playing/paused
        if self._in_use:
            # If repeating one track, queue it
            if self._repeat_one:
                self._queue_track()

            # If not currently on the last track, queue the next one
            elif self._track_index < len(self._files) - 1:
                self._queue_track(self._track_index + 1)

            # If on the last track and repeating the queue, queue the
            # first track.
            elif self._repeat:
                self._queue_track(0)

    
    def _handle_end_event (self):
        '''
        Helper function that is called by the game loop when a
        track is completed.
        '''

        # Nothing to do if not playing/paused
        if not self._in_use:
            return

        # If there is a done track handler, call it
        if self._done_track_func is not None:
            pgputils.call_with_args(self._done_track_func,
                                    index=self._track_index,
                                    track=self._files[self._track_index])

        # Update the track index if necessary
        if not music_stream.repeat_one:
            music_stream._track_index += 1
            if music_stream._track_index == music_stream.size:
                music_stream._track_index = 0

                # If just finished the last track and not repeating,
                # ensure that any queued track is stopped and set
                # up the stream to play from the start again
                if not music_stream.repeat:
                    pygame.mixer.music.stop()
                    self._load_track()
                    self._in_use = False

                    # If there is a done queue handler, call it
                    if self._done_queue_func is not None:
                        pgputils.call_with_args(self._done_queue_func)

                    # End the method
                    return

        # Switch queued track to loaded track.  If none was queued
        # try loading it and playing it.
        self._loaded_index = self._queued_index
        if self._loaded_index is None:
            self._in_use = False
            self._load_track()
            self.play()

        # Otherwise, queue up the next track
        else:
            self._queue_next()


    def _error (self, message):
        if self._suppress_errors:
            warnings.warn(message, MusicStreamWarning, 2)
        else:
            raise MusicStreamException(message) from None


    ### STREAM CONTROLS ###
    
    def play (self, fade_in=None):
        '''
        Play the music stream.

        If stopped, playback starts at the beginning of the current
        track.  If paused, playback resumes at the point it was passed.

        Optionally, you can provide a `fade_in` time, in seconds.  This
        will be ignored when unpausing the stream.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - No tracks in the stream
        - The music is already playing
        - An invalid `fade_in` time
        - The music track can't be played
        '''

        # Error if no tracks in the stream
        if not self._files:
            self._error('There are no music files in the queue!')
            return

        # If the stream is not stopped
        if self._in_use:
            # If stream is paused, unpause it
            if self._paused:
                pygame.mixer.music.unpause()
                self._paused = False

            # Otherwise, the music is already playing
            else:
                self._error('The music stream is already playing!')
                return

        # Otherwise, the stream is stopped.  Start at the current track.
        else:
            try:
                fade_ms = 0 if fade_in is None else int(fade_in * 1000)
            except:
                self._error(f'Invalid fade in time: {fade_in}')
                fade_ms = 0
            self._in_use = True
            try:
                pygame.mixer.music.play(fade_ms=fade_ms)
                self._queue_next()
            except:
                self._error(f'Could not play track: {self._files[self._track_index]}')
                self.skip_to_next()


    def pause (self):
        '''
        Pause the music stream so it can be continued at the current
        position.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The music is stopped
        - The music is already paused
        '''

        # Errors if music is not playing
        if not self._in_use:
            self._error('The music is not playing!')
            return
        if self._paused:
            self._error('The music is already paused!')

        # Pause the stream
        self._paused = True
        pygame.mixer.music.pause()


    def stop (self, fade_out=None):
        '''
        Stop the music stream and return to the beginning.

        Optionally, you can provide a `fade_out` time, in seconds.
        This method will block until the fade is complete.
        
        Unless errors have been suppressed, the following will cause
        exceptions:
        - The music is already stopped
        - An invalid `fade_out` time
        '''

        # Error if already stopped
        if not self._in_use:
            raise RuntimeError('The music is already stopped!')

        # Stop the music
        self._in_use = False
        if fade_out and not self._paused:
            try:
                fade_ms = int(fade_out * 1000)
            except:
                raise ValueError(f'Invalid fade out time: {fade_out}')
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()

        # Set up the stream to start again at the beginning
        self._track_index = 0
        self._load_track()


    def skip_to_next (self, fade_in=None):
        '''
        Skip to the next track in the stream.

        If the stream is playing/paused, the next track will 
        start playing immediately.  If the stream is stopped, a
        call to `play()` will start the stream at the new track
        position.

        If previously playing the last track, the stream will be 
        stopped, unless the `repeat` property is set, in which case
        stream will loop back to the first track.

        Optionally, you can provide a `fade_in` time, in seconds,
        that will be used if the next track plays immediately.
        It will be ignored if the stream is stopped.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The next music track can't be played
        '''

        # Update the stream's attributes
        self._paused = False
        if self._track_index < len(self._files) - 1:
            self._track_index += 1
        else:
            self._track_index = 0
            if not self._repeat:
                self._in_use = False

        # Load and, if necessary, play the new track
        self._load_track()
        if self._in_use:
            self._in_use = False
            self.play(fade_in)
            

    def skip_to_previous (self, fade_in=None):
        '''
        Skip to the previous track in the stream.

        If the stream is playing/paused, the previous track will 
        start playing immediately.  If the stream is stopped, a
        call to `play()` will start the stream at the new track
        position.

        If previously playing the first track, the stream will be 
        stopped, unless the `repeat` property is set, in which case
        stream will loop to the last track.  If stopped, the
        last track will become the current track as well.

        Optionally, you can provide a `fade_in` time, in seconds,
        that will be used if the previous track plays immediately.
        It will be ignored if the stream is stopped.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The previous music track can't be played
        '''

        # Update the stream's attributes
        self._paused = False
        if self._track_index > 0:
            self._track_index -= 1
        else:
            self._track_index = len(self._files) - 1
            if not self._repeat:
                self._in_use = False

        # Load and, if necessary, play the new track
        self._load_track()
        if self._in_use:
            self._in_use = False
            self.play(fade_in)


    def skip_to_first (self, fade_in=None):
        '''
        Skip to the first track in the stream.

        If the stream is playing/paused, the first track will 
        start playing immediately.  If the stream is stopped, a
        call to `play()` will start the stream at the beginning.

        Optionally, you can provide a `fade_in` time, in seconds,
        that will be used if the previous track plays immediately.
        It will be ignored if the stream is stopped.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The first music track can't be played
        '''

        # Update the stream's attributes
        self._paused = False
        self._track_index = 0

        # Load and, if necessary, play the new track
        self._load_track()
        if self._in_use:
            self._in_use = False
            self.play(fade_in)


    def skip_to_index (self, index, fade_in=None):
        '''
        Skip to the given track index in the stream.

        Track indices start at 0 for the first track.  If a 
        negative index is given, the method skips to the track that
        far from the end.

        If the stream is playing/paused, the new track will 
        start playing immediately.  If the stream is stopped, a
        call to `play()` will start the stream at the new track.

        Optionally, you can provide a `fade_in` time, in seconds,
        that will be used if the new track plays immediately.
        It will be ignored if the stream is stopped.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The index is not an integer
        - The index is out of bounds
        - The given music track can't be played
        '''

        # Update the stream's attributes.
        # Error for invalid indices
        self._paused = False
        if not isinstance(index, int):
            raise TypeError(f'The track index must be an integer! (given {index}')
        size = len(self._files)
        if index < -size or index >= size:
            raise ValueError(f'Invalid track number for a queue of size {size}: {index}')
        if index < 0:
            index += size
        self._track_index = index

        # Load and, if necessary, play the new track
        self._load_track()
        if self._in_use:
            self._in_use = False
            self.play(fade_in)


    ### STREAM TRACK MANAGEMENT ###

    def add_track (self, music_file):
        '''
        Add a single music track to the end of the stream.

        The argument should be a music filename, including its file
        type (e.g. '.mp3', '.ogg', '.wav').

        Adding a track to the stream will not play the stream.
        Use the `play()` method to start the stream after tracks
        have been added.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - A track is loaded into an empty stream and it can't be loaded
        '''

        # Add the track to the files list
        old_size = len(self._files)
        self._files.append(music_file)

        # If the stream was previously empty, load the first track
        # in preparation for playback
        if self._track_index is None:
            self._track_index = 0
            self._load_track()

        # If the next track to be played is one of the new ones,
        # queue it
        if self._track_index == old_size - 1 and not self._repeat_one:
            self._queue_next()
            

    def add_tracks (self, *music_files):
        '''
        Add one or more music tracks to the end of the stream.

        The arguments should be music filenames, including its file
        type (e.g. '.mp3', '.ogg', '.wav').  The argument can also
        be a list of music filenames.

        Adding tracks to the stream will not play the stream.
        Use the `play()` method to start the stream after tracks
        have been added.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - A track is loaded into an empty stream and it can't be loaded
        '''

        # Add the tracks to the files list recursively
        for music_file in music_files:
            if isinstance(music_file, list):
                self.add_tracks(*music_file)
            else:
                self.add_track(music_file)


    def insert_track (self, index, music_file):
        '''
        Add a single music track to the stream before the track 
        with the given index.

        Track indices start at 0 for the first track.  If a 
        negative index is given, the method skips to the track that
        far from the end.

        The second argument should be a music filenames, 
        including its file type (e.g. '.mp3', '.ogg', '.wav').
        '''

        # Insert the track into the file list
        old_size = len(self._files)
        self._files.insert(index, music_file)

        # If inserted before the current track, update the track index
        if index < 0:
            index += old_size
            if index < 0:
                index = 0
        elif index > old_size:
            index = old_size
        if index <= self._track_index:
            self._track_index += 1

        # If the next track to be played is one of the new ones,
        # queue it
        if self._track_index == index - 1 and not self._repeat_one:
            self._queue_next()


    def find_track_index (self, music_file, start=0, end=-1):
        '''
        Get the index of the first occurrense of a music track in
        the stream.

        Track indices start at 0 for the first track.

        Use the `start` and `end` arguments to search a slice of the
        stream.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The music file is not in the stream (or slice of the stream)
        '''
        
        try:
            return self._files.index(music_file, start, end)
        except ValueError:
            self._error(f'Track not in the queue: {music_file}')


    def remove_track (self, music_file):
        '''
        Remove the first occurrence of a music track from the stream.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The music file is not in the stream (or slice of the stream)
        '''
        try:
            index = self.find_track_index(music_file)
            self.pop_track(index)
        except ValueError:
            self._error(f'Track not in the queue: {music_file}')


    def pop_track (self, index=None):
        '''
        Remove and return the music track at the given index.

        Track indices start at 0 for the first track.  If a 
        negative index is given, the method pops the track that
        far from the end.

        If no index is given, the last track will be popped.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - The index is out of bounds
        '''

        # If not index, use last index
        if index is None:
            index = len(self._files) - 1

        # If playing the track to be popped, skip to the next one
        if index == self._track_index:
            self.skip_to_next()

        # Pop the track and give and error if our of bounds.
        try:
            track = self._files.pop(index)
        except:
            self._error(f'Index out of bounds: {index}')
            return
        if index <= self._track_index:
            self._track_index -= 1

        # If the next track to be played was the removed track,
        # queue a new one
        if index == self._track_index + 1 and not self._repeat_one:
            self._queue_next()

        # Return the removed track
        return track


    def clear_tracks (self):
        '''
        Clear all tracks from the music stream.

        This will stop the music stream.
        '''
        
        self._files.clear()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self._track_index = None
        self._in_use = False
        self._paused = False


    ### PROPERTIES ###
    
    @property
    def status (self):
        '''
        *Readonly.*  The current status of the music stream.

        Will be only of `'stopped'`, `'paused'` or `'playing'`.
        '''
        
        if not self._in_use:
            return 'stopped'
        elif self._paused:
            return 'paused'
        else:
            return 'playing'


    @property
    def playing (self):
        '''
        *Readonly.*  Whether or not the stream is currently playing.

        This will be false when the stream is stopped or paused.
        '''
        
        return self._in_use and not self._paused


    @property
    def paused (self):
        '''
        *Readonly.*  Whether or not the stream is currently paused.

        This will be false when the stream is stopped or playing.
        '''
        
        return self._paused


    @property
    def volume (self):
        '''
        The volume of the stream.

        This will be a number between 0 (mute) and 1 (full volume).

        Unless errors have been suppressed, the following will cause
        exceptions:
        - Setting to and invalid value (see above)
        '''
        
        return pygame.mixer.music.get_volume()

    @volume.setter
    def volume (self, new_value):
        try:
            pygame.mixer.music.set_volume(float(new_value))
        except ValueError:
            self._error(f'Invalid volume: {new_value!r}')


    @property
    def size (self):
        '''
        *Readonly.*  The number of tracks in the stream.
        '''
        
        return len(self._files)


    @property
    def track_index (self):
        '''
        The index of the current track.

        This will be an integer between 0 (first track) and one less
        than the size of the stream.

        Unless errors have been suppressed, the following will cause
        exceptions:
        - Setting to an invalid value (see above)
        - Setting to a music track can't be played
        '''
        
        return self._track_index

    @track_index.setter
    def track_index (self, new_value):
        self.skip_to_index(new_value)


    @property
    def current_track (self):
        '''
        *Readonly.*  The filename of the current track.

        If the stream is empty, this will be None.
        '''
        
        if self._track_index is None:
            return None
        return self._files[self._track_index]


    @property
    def repeat (self):
        '''
        Whether or not the stream repeats when it reaches its end.
        '''
        return self._repeat

    @repeat.setter
    def repeat (self, new_value):
        self._repeat = bool(new_value)

        # If set to True and the current track is the last one,
        # queue the first track
        if new_value and self._track_index == len(self._files) - 1 and not self._repeat_one:
            self._queue_next()


    @property
    def repeat_one (self):
        '''
        Whether or not the current track will be repeated when it
        reaches its end.
        '''
        return self._repeat_one

    @repeat_one.setter
    def repeat_one (self, new_value):
        self._repeat_one = bool(new_value)
        
        # When this changes, the queued song likely needs 
        # to change too
        self._queue_next()


    @property
    def suppress_errors (self):
        '''
        Whether or not errors are suppressed.

        If this is `True`, all non-breaking errors are warned
        and the stream will skip the track that's not working.

        If this is `False`, all errors are treated as exceptions.
        '''

        return self._suppress_errors

    @suppress_errors.setter
    def suppress_errors (self, new_value):
        self._suppress_errors = bool(new_value)


    ### EVENTS ###

    def on_done_track (self, func):
        '''
        Bind an event handler function that will be executed when a
        track is finished playing.

        This event handler will not be called if track finishes
        unhindered.  It will not be called if the track is skipped
        or if the music stream stopped.

        If the function has the following named arguments, they
        will be populated when called:
        - track: The filename of the track that finished
        - index: The index of the track in the stream
        '''
        
        self._done_track_func = func
        

    def on_done_queue (self, func):
        '''
        Bind an event handler function that will be executed when
        the entire music stream is finished playing.

        This event handler will not be called if queue finishes
        unhindered.  It will not be called if the queue stops because
        of skipping or a call to `stop()`.  It will also not be called
        if the `repeat` property is set and the queue loops back
        to the start.
        '''
        self._done_queue_func = func


music_stream = MusicStream()
music_stream.__doc__ = '''
        The queue that manages streaming larger music files.  See the
        `MusicStream` class for details.
        '''

__all__ = [
    'MUSIC_END',
    'MusicStream',
    'music_stream'
]
