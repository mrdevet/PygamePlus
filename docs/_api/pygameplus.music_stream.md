---
layout: default
title: music_stream
parent: pygameplus
---
# music_stream

pygame module for controlling streamed audio

## Functions

| Function | Description |
| --- | --- |
| fadeout(...) | fadeout(time) -> None<br />stop music playback after fading out |
| get_busy(...) | get_busy() -> bool<br />check if the music stream is playing |
| get_endevent(...) | get_endevent() -> type<br />get the event a channel sends when playback stops |
| get_pos(...) | get_pos() -> time<br />get the music play time |
| get_volume(...) | get_volume() -> value<br />get the music volume |
| load(...) | load(filename) -> None<br />load(object) -> None<br />Load a music file for playback |
| pause(...) | pause() -> None<br />temporarily stop music playback |
| play(...) | play(loops=0, start=0.0, fade_ms = 0) -> None<br />Start the playback of the music stream |
| queue(...) | queue(filename) -> None<br />queue a sound file to follow the current |
| rewind(...) | rewind() -> None<br />restart music |
| set_endevent(...) | set_endevent() -> None<br />set_endevent(type) -> None<br />have the music send an event when playback stops |
| set_pos(...) | set_pos(pos) -> None<br />set position to play from |
| set_volume(...) | set_volume(volume) -> None<br />set the music volume |
| stop(...) | stop() -> None<br />stop the music playback |
| unload(...) | unload() -> None<br />Unload the currently loaded music to free up resources |
| unpause(...) | unpause() -> None<br />resume paused music |

## Function Details

### `fadeout(...)`

fadeout(time) -> None<br />stop music playback after fading out

### `get_busy(...)`

get_busy() -> bool<br />check if the music stream is playing

### `get_endevent(...)`

get_endevent() -> type<br />get the event a channel sends when playback stops

### `get_pos(...)`

get_pos() -> time<br />get the music play time

### `get_volume(...)`

get_volume() -> value<br />get the music volume

### `load(...)`

load(filename) -> None<br />load(object) -> None<br />Load a music file for playback

### `pause(...)`

pause() -> None<br />temporarily stop music playback

### `play(...)`

play(loops=0, start=0.0, fade_ms = 0) -> None<br />Start the playback of the music stream

### `queue(...)`

queue(filename) -> None<br />queue a sound file to follow the current

### `rewind(...)`

rewind() -> None<br />restart music

### `set_endevent(...)`

set_endevent() -> None<br />set_endevent(type) -> None<br />have the music send an event when playback stops

### `set_pos(...)`

set_pos(pos) -> None<br />set position to play from

### `set_volume(...)`

set_volume(volume) -> None<br />set the music volume

### `stop(...)`

stop() -> None<br />stop the music playback

### `unload(...)`

unload() -> None<br />Unload the currently loaded music to free up resources

### `unpause(...)`

unpause() -> None<br />resume paused music

