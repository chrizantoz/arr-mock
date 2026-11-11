# 🧪 arr-mock

A fake **Sonarr, Radarr, Whisparr and Bazarr** in one small Python file. No Docker, no database, no API keys to find: start it, point your app at it, and test the whole chain against synthetic media files.

Born inside [Auditarr](https://github.com/chrizantoz/auditarr), where it runs the end-to-end and chaos tests in CI. Published on its own so other arr companion apps can use it too.

## 🚀 Start it

```bash
python arr_mock.py 8765            # http://127.0.0.1:8765/sonarr , /radarr , /whisparr , /bazarr   (API key: test)
python arr_mock.py 8765 --chaos    # same, with random 500s, slow answers and Radarr dropping connections for a while
```

Or from Python, with your own world and real files on disk:

```python
import arr_mock, synthlib
W = arr_mock.default_world("/data/tv", "/data/movies")         # one show, three files, one missing episode, one movie
synthlib.make(W["files"][1]["path"], alang="fre")              # a real 30-second MKV with French audio (needs ffmpeg)
srv = arr_mock.start(W)                                        # port 0 = pick a free one
print(srv.server_address, srv.calls)                           # every write your app sends lands in srv.calls
srv.chaos = arr_mock.chaos()                                   # flip chaos on mid-test; set to None to turn it off
```

## 📋 What it answers

| app | endpoints |
|---|---|
| Sonarr / Whisparr | `series`, `series/{id}`, `episode?seriesId=`, `episodefile?seriesId=`, `episodefile/{id}`, `series/editor`, `tag`, `rootfolder`, `system/status`, `command`, `queue`, `history`, `blocklist`, `notification` |
| Radarr | `movie`, `movie/{id}`, `moviefile?movieId=`, `moviefile/{id}`, `movie/editor` and the shared ones above |
| Bazarr | `episodes/wanted`, `movies/wanted`, `episodes`, `episodes/history`, `movies/history`, `subtitles` (PATCH search), `providers/*`, `system/status` |

Episode files only "exist" when the file is really on disk, so deleting or moving a file behaves like the real thing. Writes are accepted and recorded, nothing is validated: the point is to see what your app *sends*, not to re-implement an arr.

## 🌪️ Chaos mode

`arr_mock.chaos(seed=11, p500=0.08, pslow=0.04, slow_s=2, vanish_app="radarr", vanish_from=2, vanish_len=12)`

A share of requests answer 500, a share answer slowly, and one app drops the connection for a window of requests. Deterministic for a given seed. Good for proving your app finishes degraded instead of crashing, keeps its data when a service vanishes, and makes no half-done writes.

## 🎬 Synthetic media

`synthlib.make(path, seconds=30, audio=True, alang="eng", vopts=None, aopts=None, title=None, aoffset=0.0, extra=None)` builds a real, tiny video with ffmpeg: pick the audio language, drop the audio track, add an audio delay, or pass extra ffmpeg options for 10-bit, interlaced or AV1 cases.

## 🙏 Support

Free under GPL-3.0. If it saved you an evening: [GitHub Sponsors](https://github.com/sponsors/chrizantoz) · [Ko-fi](https://ko-fi.com/chrizantoz)
