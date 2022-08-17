---
layout: default
title: MusicStream
parent: pygameplus
---
# MusicStream

A MusicStream is a queue that manages a collection of music to be streamed during the game.  Music is loaded in chunks for efficiency and the next track is pre-loaded for a seemless transition.

You will not be able to create your own MusicStream.  Instead, you should use the `music_stream` variable, included in this module, which contains the single possible MusicStream object.

Note that the music stream will only be able to work properly when the game loop is running.

---

## Attribute Summary

### Methods

| <a href="#add_track">`.add_track(music_file)`</a> | Add a single music track to the end of the stream. |
| <a href="#add_tracks">`.add_tracks(*music_files)`</a> | Add one or more music tracks to the end of the stream. |
| <a href="#clear_tracks">`.clear_tracks()`</a> | Clear all tracks from the music stream. |
| <a href="#find_track_index">`.find_track_index(music_file, start=0, end=-1)`</a> | Get the index of the first occurrense of a music track in the stream. |
| <a href="#insert_track">`.insert_track(index, music_file)`</a> | Add a single music track to the stream before the track  with the given index. |
| <a href="#on_done_queue">`.on_done_queue(func)`</a> | Bind an event handler function that will be executed when the entire music stream is finished playing. |
| <a href="#on_done_track">`.on_done_track(func)`</a> | Bind an event handler function that will be executed when a track is finished playing. |
| <a href="#pause">`.pause()`</a> | Pause the music stream so it can be continued at the current position. |
| <a href="#play">`.play(fade_in=None)`</a> | Play the music stream. |
| <a href="#pop_track">`.pop_track(index=None)`</a> | Remove and return the music track at the given index. |
| <a href="#remove_track">`.remove_track(music_file)`</a> | Remove the first occurrence of a music track from the stream. |
| <a href="#skip_to_first">`.skip_to_first(fade_in=None)`</a> | Skip to the first track in the stream. |
| <a href="#skip_to_index">`.skip_to_index(index, fade_in=None)`</a> | Skip to the given track index in the stream. |
| <a href="#skip_to_next">`.skip_to_next(fade_in=None)`</a> | Skip to the next track in the stream. |
| <a href="#skip_to_previous">`.skip_to_previous(fade_in=None)`</a> | Skip to the previous track in the stream. |
| <a href="#stop">`.stop(fade_out=None)`</a> | Stop the music stream and return to the beginning. |

### Properties

| <a href="#current_track">`.current_track`</a> | *Readonly.*  The filename of the current track. |
| <a href="#paused">`.paused`</a> | *Readonly.*  Whether or not the stream is currently paused. |
| <a href="#playing">`.playing`</a> | *Readonly.*  Whether or not the stream is currently playing. |
| <a href="#repeat">`.repeat`</a> | Whether or not the stream repeats when it reaches its end. |
| <a href="#repeat_one">`.repeat_one`</a> | Whether or not the current track will be repeated when it reaches its end. |
| <a href="#size">`.size`</a> | *Readonly.*  The number of tracks in the stream. |
| <a href="#status">`.status`</a> | *Readonly.*  The current status of the music stream. |
| <a href="#suppress_errors">`.suppress_errors`</a> | Whether or not errors are suppressed. |
| <a href="#track_index">`.track_index`</a> | The index of the current track. |
| <a href="#volume">`.volume`</a> | The volume of the stream. |

---

## Attribute Details

### `.add_track(music_file)` {#add_track}

> Add a single music track to the end of the stream.
> 
> The argument should be a music filename, including its file type (e.g. '.mp3', '.ogg', '.wav').
> 
> Adding a track to the stream will not play the stream. Use the `play()` method to start the stream after tracks have been added.
> 
> Unless errors have been suppressed, the following will cause exceptions: - A track is loaded into an empty stream and it can't be loaded

### `.add_tracks(*music_files)` {#add_tracks}

> Add one or more music tracks to the end of the stream.
> 
> The arguments should be music filenames, including its file type (e.g. '.mp3', '.ogg', '.wav').  The argument can also be a list of music filenames.
> 
> Adding tracks to the stream will not play the stream. Use the `play()` method to start the stream after tracks have been added.
> 
> Unless errors have been suppressed, the following will cause exceptions: - A track is loaded into an empty stream and it can't be loaded

### `.clear_tracks()` {#clear_tracks}

> Clear all tracks from the music stream.
> 
> This will stop the music stream.

### `.find_track_index(music_file, start=0, end=-1)` {#find_track_index}

> Get the index of the first occurrense of a music track in the stream.
> 
> Track indices start at 0 for the first track.
> 
> Use the `start` and `end` arguments to search a slice of the stream.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The music file is not in the stream (or slice of the stream)

### `.insert_track(index, music_file)` {#insert_track}

> Add a single music track to the stream before the track  with the given index.
> 
> Track indices start at 0 for the first track.  If a  negative index is given, the method skips to the track that far from the end.
> 
> The second argument should be a music filenames,  including its file type (e.g. '.mp3', '.ogg', '.wav').

### `.on_done_queue(func)` {#on_done_queue}

> Bind an event handler function that will be executed when the entire music stream is finished playing.
> 
> This event handler will not be called if queue finishes unhindered.  It will not be called if the queue stops because of skipping or a call to `stop()`.  It will also not be called if the `repeat` property is set and the queue loops back to the start.

### `.on_done_track(func)` {#on_done_track}

> Bind an event handler function that will be executed when a track is finished playing.
> 
> This event handler will not be called if track finishes unhindered.  It will not be called if the track is skipped or if the music stream stopped.
> 
> If the function has the following named arguments, they will be populated when called: - track: The filename of the track that finished - index: The index of the track in the stream

### `.pause()` {#pause}

> Pause the music stream so it can be continued at the current position.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The music is stopped - The music is already paused

### `.play(fade_in=None)` {#play}

> Play the music stream.
> 
> If stopped, playback starts at the beginning of the current track.  If paused, playback resumes at the point it was passed.
> 
> Optionally, you can provide a `fade_in` time, in seconds.  This will be ignored when unpausing the stream.
> 
> Unless errors have been suppressed, the following will cause exceptions: - No tracks in the stream - The music is already playing - An invalid `fade_in` time - The music track can't be played

### `.pop_track(index=None)` {#pop_track}

> Remove and return the music track at the given index.
> 
> Track indices start at 0 for the first track.  If a  negative index is given, the method pops the track that far from the end.
> 
> If no index is given, the last track will be popped.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The index is out of bounds

### `.remove_track(music_file)` {#remove_track}

> Remove the first occurrence of a music track from the stream.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The music file is not in the stream (or slice of the stream)

### `.skip_to_first(fade_in=None)` {#skip_to_first}

> Skip to the first track in the stream.
> 
> If the stream is playing/paused, the first track will  start playing immediately.  If the stream is stopped, a call to `play()` will start the stream at the beginning.
> 
> Optionally, you can provide a `fade_in` time, in seconds, that will be used if the previous track plays immediately. It will be ignored if the stream is stopped.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The first music track can't be played

### `.skip_to_index(index, fade_in=None)` {#skip_to_index}

> Skip to the given track index in the stream.
> 
> Track indices start at 0 for the first track.  If a  negative index is given, the method skips to the track that far from the end.
> 
> If the stream is playing/paused, the new track will  start playing immediately.  If the stream is stopped, a call to `play()` will start the stream at the new track.
> 
> Optionally, you can provide a `fade_in` time, in seconds, that will be used if the new track plays immediately. It will be ignored if the stream is stopped.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The index is not an integer - The index is out of bounds - The given music track can't be played

### `.skip_to_next(fade_in=None)` {#skip_to_next}

> Skip to the next track in the stream.
> 
> If the stream is playing/paused, the next track will  start playing immediately.  If the stream is stopped, a call to `play()` will start the stream at the new track position.
> 
> If previously playing the last track, the stream will be  stopped, unless the `repeat` property is set, in which case stream will loop back to the first track.
> 
> Optionally, you can provide a `fade_in` time, in seconds, that will be used if the next track plays immediately. It will be ignored if the stream is stopped.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The next music track can't be played

### `.skip_to_previous(fade_in=None)` {#skip_to_previous}

> Skip to the previous track in the stream.
> 
> If the stream is playing/paused, the previous track will  start playing immediately.  If the stream is stopped, a call to `play()` will start the stream at the new track position.
> 
> If previously playing the first track, the stream will be  stopped, unless the `repeat` property is set, in which case stream will loop to the last track.  If stopped, the last track will become the current track as well.
> 
> Optionally, you can provide a `fade_in` time, in seconds, that will be used if the previous track plays immediately. It will be ignored if the stream is stopped.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The previous music track can't be played

### `.stop(fade_out=None)` {#stop}

> Stop the music stream and return to the beginning.
> 
> Optionally, you can provide a `fade_out` time, in seconds. This method will block until the fade is complete.
> 
> Unless errors have been suppressed, the following will cause exceptions: - The music is already stopped - An invalid `fade_out` time

### `.current_track` {#current_track}

> *Readonly.*  The filename of the current track.
> 
> If the stream is empty, this will be None.

### `.paused` {#paused}

> *Readonly.*  Whether or not the stream is currently paused.
> 
> This will be false when the stream is stopped or playing.

### `.playing` {#playing}

> *Readonly.*  Whether or not the stream is currently playing.
> 
> This will be false when the stream is stopped or paused.

### `.repeat` {#repeat}

> Whether or not the stream repeats when it reaches its end.

### `.repeat_one` {#repeat_one}

> Whether or not the current track will be repeated when it reaches its end.

### `.size` {#size}

> *Readonly.*  The number of tracks in the stream.

### `.status` {#status}

> *Readonly.*  The current status of the music stream.
> 
> Will be only of `'stopped'`, `'paused'` or `'playing'`.

### `.suppress_errors` {#suppress_errors}

> Whether or not errors are suppressed.
> 
> If this is `True`, all non-breaking errors are warned and the stream will skip the track that's not working.
> 
> If this is `False`, all errors are treated as exceptions.

### `.track_index` {#track_index}

> The index of the current track.
> 
> This will be an integer between 0 (first track) and one less than the size of the stream.
> 
> Unless errors have been suppressed, the following will cause exceptions: - Setting to an invalid value (see above) - Setting to a music track can't be played

### `.volume` {#volume}

> The volume of the stream.
> 
> This will be a number between 0 (mute) and 1 (full volume).
> 
> Unless errors have been suppressed, the following will cause exceptions: - Setting to and invalid value (see above)

