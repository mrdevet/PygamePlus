'''
Pygame module for controlling streamed audio.

Alias for [`pygame.mixer.music`](https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music).  See the pygame reference for more details.
'''

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

import pygame

from . import pgputils

MUSIC_END = pygame.event.custom_type()
pygame.mixer.music.set_endevent(MUSIC_END)


class MusicStream (object):
    '''
    '''

    # Used to enforce this as a singleton class
    __the_music_stream = None

    def __init__ (self):
        '''
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
        self._repeat = False
        self._repeat_one = False

        self._done_track_func = None
        self._done_queue_func = None


    def __str__ (self):
        if self._track_index is None:
            return f'<MusicStream({self.status}, no tracks)'
        return f'<MusicStream({self.status}, track index {self._track_index} of {len(self._files)}: {self.current_track})'

    def __repr__ (self):
        return self.__str__()


    def _queue_next (self):
        if self._in_use:
            if self._repeat_one:
                pygame.mixer.music.queue(self._files[self._track_index])
            elif self._track_index < len(self._files) - 1:
                pygame.mixer.music.queue(self._files[self._track_index + 1])
            elif self._repeat:
                pygame.mixer.music.queue(self._files[0])


    def _handle_end_event (self):
        if not self._in_use:
            return
        if self._done_track_func is not None:
            pgputils.call_with_args(self._done_track_func,
                                    index=self._track_index,
                                    track=self._files[self._track_index])
        if not music_stream.repeat_one:
            music_stream._track_index += 1
            if music_stream._track_index == music_stream.size:
                music_stream._track_index = 0
                if not music_stream.repeat:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self._files[0])
                    self._in_use = False
                    if self._done_queue_func is not None:
                        pgputils.call_with_args(self._done_queue_func)
        self._queue_next()


    ### STREAM CONTROLS ###
    
    def play (self, fade_in=None):
        if not self._files:
            raise IndexError('There are no music files in the queue!')
        if self._in_use:
            if self._paused:
                pygame.mixer.music.unpause()
                self._paused = False
            else:
                raise RuntimeError('The music stream is already playing!')
        else:
            try:
                fade_ms = int(fade_in * 1000) if fade_in else 0
            except:
                raise ValueError(f'Invalid fade in time: {fade_in}')
            pygame.mixer.music.play(fade_ms=fade_ms)
            self._in_use = True
            self._queue_next()


    def pause (self):
        if not self._in_use:
            raise RuntimeError('The music is not playing!')
        if self._paused:
            raise RuntimeError('The music is already paused!')
        self._paused = True
        pygame.mixer.music.pause()


    def stop (self, fade_out=None):
        if not self._in_use:
            raise RuntimeError('The music is already stopped!')
        self._in_use = False
        if fade_out and not self._paused:
            try:
                fade_ms = int(fade_out * 1000)
            except:
                raise ValueError(f'Invalid fade out time: {fade_out}')
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        self._track_index = 0
        pygame.mixer.music.load(self._files[0])


    def skip_to_next (self, fade_in=None):
        self._paused = False
        if self._track_index < len(self._files) - 1:
            self._track_index += 1
        else:
            self._track_index = 0
            if not self._repeat:
                self._in_use = False
        pygame.mixer.music.load(self._files[self._track_index])
        if self._in_use:
            self._in_use = False
            self.play(fade_in)

    def skip_to_previous (self, fade_in=None):
        self._paused = False
        if self._track_index > 0:
            self._track_index -= 1
        else:
            self._track_index = len(self._files) - 1
            if not self._repeat:
                self._in_use = False
        pygame.mixer.music.load(self._files[self._track_index])
        if self._in_use:
            self._in_use = False
            self.play(fade_in)


    def skip_to_first (self, fade_in=None):
        self._paused = False
        self._track_index = 0
        pygame.mixer.music.load(self._files[self._track_index])
        if self._in_use:
            self._in_use = False
            self.play(fade_in)


    def skip_to_index (self, index, fade_in=None):
        self._paused = False
        if not isinstance(index, int):
            raise TypeError(f'The track index must be an integer! (given {index}')
        size = len(self._files)
        if index < -size or index >= size:
            raise ValueError(f'Invalid track number for a queue of size {size}: {index}')
        if index < 0:
            index += size
        self._track_index = index
        pygame.mixer.music.load(self._files[self._track_index])
        if self._in_use:
            self._in_use = False
            self.play(fade_in)


    ### STREAM TRACK MANAGEMENT ###

    def add_tracks (self, *music_files):
        old_size = len(self._files)
        for music_file in music_files:
            if isinstance(music_file, list):
                self.add_tracks(*music_file)
            else:
                self._files.append(music_file)
        if self._track_index is None:
            pygame.mixer.music.load(self._files[0])
            self._track_index = 0
        if self._in_use and self._track_index == old_size - 1 and not self._repeat_one:
            self._queue_next()


    def insert_track (self, index, music_file):
        self._files.insert(index, music_file)
        if index <= self._track_index:
            self._track_index += 1
        if self._in_use and self._track_index == index - 1 and not self._repeat_one:
            self._queue_next()


    def find_track_index (self, music_file, start=0, end=-1):
        try:
            return self._files.index(music_file, start, end)
        except ValueError:
            raise ValueError(f'Track not in the queue: {music_file}') from None


    def remove_track (self, music_file):
        try:
            index = self.find_track_index(music_file)
            self.pop_track(index)
        except ValueError:
            raise ValueError(f'Track not in the queue: {music_file}') from None


    def pop_track (self, index=None):
        if index is None:
            index = len(self._files) - 1
        if index == self._track_index:
            self.skip_to_next()
        track = self._files.pop(index)
        if index <= self._track_index:
            self._track_index -= 1
        if self._in_use and index == self._track_index + 1 and self._in_use and not self._repeat_one:
            self._queue_next()
        return track


    def clear_tracks (self):
        self._files.clear()
        pygame.mixer.music.unload()
        self._track_index = None
        self._in_use = False
        self._paused = False


    ### PROPERTIES ###
    
    @property
    def status (self):
        if not self._in_use:
            return 'stopped'
        elif self._paused:
            return 'paused'
        else:
            return 'playing'


    @property
    def playing (self):
        return self._in_use and not self._paused


    @property
    def paused (self):
        return self._paused


    @property
    def volume (self):
        return pygame.mixer.music.get_volume()

    @volume.setter
    def volume (self, new_value):
        try:
            pygame.mixer.music.set_volume(float(new_value))
        except ValueError:
            raise ValueError(f'Invalid volume: {new_value!r}') from None


    @property
    def size (self):
        return len(self._files)


    @property
    def track_index (self):
        return self._track_index

    @track_index.setter
    def track_index (self, new_value):
        self.skip_to_index(new_value)


    @property
    def current_track (self):
        if self._track_index is None:
            return None
        return self._files[self._track_index]


    @property
    def repeat (self):
        return self._repeat

    @repeat.setter
    def repeat (self, new_value):
        self._repeat = bool(new_value)
        if self._in_use and self._track_index == len(self._files) - 1 and not self._repeat_one:
            self._queue_next()


    @property
    def repeat_one (self):
        return self._repeat_one

    @repeat_one.setter
    def repeat_one (self, new_value):
        self._repeat_one = bool(new_value)
        if self._in_use:
            self._queue_next()


    @property
    def position_in_track (self):
        raise NotImplementedError()

    @position_in_track.setter
    def position_in_track (self, new_value):
        raise NotImplementedError()


    ### EVENTS ###

    def on_done_track (self, func):
        self._done_track_func = func
        

    def on_done_queue (self, func):
        self._done_queue_func = func


music_stream = MusicStream()

__all__ = [
    'MUSIC_END',
    'MusicStream',
    'music_stream'
]
