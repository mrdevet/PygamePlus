---
layout: default
title: music_stream
parent: pygameplus
---
# music_stream

Pygame module for controlling streamed audio.

Alias for [`pygame.mixer.music`](https://www.pygame.org/docs/ref/music.html#module-pygame.mixer.music).  See the pygame reference for more details.

---

## Member Summary

### Functions

| <a href="#fadeout">`fadeout(...)`</a> | fadeout(time) -> None stop music playback after fading out |
| <a href="#get_busy">`get_busy(...)`</a> | get_busy() -> bool check if the music stream is playing |
| <a href="#get_endevent">`get_endevent(...)`</a> | get_endevent() -> type get the event a channel sends when playback stops |
| <a href="#get_pos">`get_pos(...)`</a> | get_pos() -> time get the music play time |
| <a href="#get_volume">`get_volume(...)`</a> | get_volume() -> value get the music volume |
| <a href="#load">`load(...)`</a> | load(filename) -> None load(fileobj, namehint=) -> None Load a music file for playback |
| <a href="#pause">`pause(...)`</a> | pause() -> None temporarily stop music playback |
| <a href="#play">`play(...)`</a> | play(loops=0, start=0.0, fade_ms=0) -> None Start the playback of the music stream |
| <a href="#queue">`queue(...)`</a> | queue(filename) -> None queue(fileobj, namehint=, loops=0) -> None queue a sound file to follow the current |
| <a href="#rewind">`rewind(...)`</a> | rewind() -> None restart music |
| <a href="#set_endevent">`set_endevent(...)`</a> | set_endevent() -> None set_endevent(type) -> None have the music send an event when playback stops |
| <a href="#set_pos">`set_pos(...)`</a> | set_pos(pos) -> None set position to play from |
| <a href="#set_volume">`set_volume(...)`</a> | set_volume(volume) -> None set the music volume |
| <a href="#stop">`stop(...)`</a> | stop() -> None stop the music playback |
| <a href="#unload">`unload(...)`</a> | unload() -> None Unload the currently loaded music to free up resources |
| <a href="#unpause">`unpause(...)`</a> | unpause() -> None resume paused music |

---

## Member Details

### `fadeout(...)` {#fadeout}

> fadeout(time) -> None stop music playback after fading out

### `get_busy(...)` {#get_busy}

> get_busy() -> bool check if the music stream is playing

### `get_endevent(...)` {#get_endevent}

> get_endevent() -> type get the event a channel sends when playback stops

### `get_pos(...)` {#get_pos}

> get_pos() -> time get the music play time

### `get_volume(...)` {#get_volume}

> get_volume() -> value get the music volume

### `load(...)` {#load}

> load(filename) -> None load(fileobj, namehint=) -> None Load a music file for playback

### `pause(...)` {#pause}

> pause() -> None temporarily stop music playback

### `play(...)` {#play}

> play(loops=0, start=0.0, fade_ms=0) -> None Start the playback of the music stream

### `queue(...)` {#queue}

> queue(filename) -> None queue(fileobj, namehint=, loops=0) -> None queue a sound file to follow the current

### `rewind(...)` {#rewind}

> rewind() -> None restart music

### `set_endevent(...)` {#set_endevent}

> set_endevent() -> None set_endevent(type) -> None have the music send an event when playback stops

### `set_pos(...)` {#set_pos}

> set_pos(pos) -> None set position to play from

### `set_volume(...)` {#set_volume}

> set_volume(volume) -> None set the music volume

### `stop(...)` {#stop}

> stop() -> None stop the music playback

### `unload(...)` {#unload}

> unload() -> None Unload the currently loaded music to free up resources

### `unpause(...)` {#unpause}

> unpause() -> None resume paused music

