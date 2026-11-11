"""Starts the mock, asks each app a question, confirms a write is recorded and chaos mode bites. Run: python selfcheck.py"""
import json, sys, urllib.request, urllib.error
import arr_mock
srv = arr_mock.start(arr_mock.default_world("/tmp/arr-mock-tv", "/tmp/arr-mock-movies")); base = f"http://127.0.0.1:{srv.server_address[1]}"
def get(p, method="GET", body=None):
    r = urllib.request.Request(base + p, data=json.dumps(body).encode() if body else None, method=method, headers={"X-Api-Key": "test", "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=10) as x: return x.status, json.loads(x.read() or b"null")
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name)
check("sonarr lists a series", get("/sonarr/api/v3/series")[1][0]["title"] == "Alpha Show")
check("radarr lists a movie", get("/radarr/api/v3/movie")[1][0]["title"] == "Beta Movie")
check("bazarr has a wanted episode", get("/bazarr/api/episodes/wanted")[1]["data"][0]["sonarrEpisodeId"] == 103)
check("a command is accepted and recorded", get("/sonarr/api/v3/command", "POST", {"name": "RescanSeries", "seriesId": 1})[0] == 201 and srv.calls[-1]["body"]["name"] == "RescanSeries")
srv.chaos = arr_mock.chaos(seed=1, p500=1.0, pslow=0, vanish_len=0)
try: get("/sonarr/api/v3/series"); check("chaos: every request fails with 500 when p500=1", False)
except urllib.error.HTTPError as e: check("chaos: every request fails with 500 when p500=1", e.code == 500)
srv.shutdown(); print("all good" if ok else "FAILED"); sys.exit(0 if ok else 1)
