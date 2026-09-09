# Trek site template

A static, offline-capable trip dossier for a multi-day trek: a day plan in one or more languages,
an interactive map drawn from the real GPX, elevation profile, per-day live weather with derived
warnings, an hour-by-hour day simulator with a start-time slider, a position snapshot that marks
finished days done, annotated section maps, and the GPX as a download for OsmAnd. Deploys to a VPS
with KitSHn. Content is data (`content.yaml`); the tools do the rest.

Sites built from it:

- [gr52.yarden-zamir.com](https://gr52.yarden-zamir.com), the GR52 across the Mercantour, 7 days, tent, alpine
- [yam2yam.yarden-zamir.com](https://yam2yam.yarden-zamir.com), the Israel Sea to Sea, 4 days, tent, heat

The `trek-dossier` agent skill in `skills/trek-dossier/SKILL.md` is the workflow. Install it with
`ln -s $(pwd)/skills/trek-dossier ~/.claude/skills/trek-dossier` so edits here are live.

## The two files you write

- `trek.json`: the config. `trek.example.json` shows every key. Route (OpenStreetMap relation ids in
  walking order, or a GPX), waypoints (nights, passes, escapes, notes), hostname, dates, accent
  colour, and the knobs the app uses (`plannedStart`, `treeline`, `exposed`, `heatLimit`,
  `weatherModel`). `tools/derive.py` fills `places`, `sectionMaps` and location-based defaults.
- `content.yaml`: the page text per language. One entry per day with `title`, `label`, `stats`,
  `hours`, `text`; then rules, the refuges table, technical options, practical lists, extra
  sections and links. Inline `<b>`, `<i>`, `<a>` are allowed; no other markup. The renderer emits
  every attribute the app depends on, so the structure cannot be wrong.

## Commands

```sh
uv run tools/new.py --slug … --name … --hostname … --start YYYY-MM-DD --days N   # scaffold a trek repo
uv run tools/find_route.py --bbox … [--name …] [--pick id,id]   # find the OpenStreetMap relations
uv run tools/research.py      # OSM deep dive along the line → research/osm.md + proposed waypoints
uv run tools/dates.py      # holidays, Shabbat, sun, moon, clock changes on the dates
uv run tools/climate.py       # ten years of reanalysis on the dates per night and pass
uv run tools/build_gpx.py     # route + waypoints + OSM water/huts/shelters → the GPX
uv run tools/elevation.py     # heights for every point (resumable)
uv run tools/derive.py        # places, section maps, defaults into trek.json
uv run tools/maps.py          # annotated section maps as WebP
uv run tools/doctor.py        # config, waypoints, content and GPX checks with fixes spelled out
uv run src/build.py           # content.yaml → page, service worker, manifest, Caddyfile.j2, favicon
uv run tools/check.py [--url https://host/]   # headless Chrome: map, weather, links, snapshot, simulator, screenshot
uv run tools/all.py [--from build] [--skip maps]   # doctor → gpx → elevation → maps → build → doctor → check
uv run tools/import_body.py   # convert a hand-written src/body.html into content.yaml (migration)
uv run tools/side_trips.py    # optional: route side trips over OSM paths
```

## What the page does

- **Map** from the GPX with layer toggles per track and waypoint kind, place names and day titles
  linking to it, deep links `#map=<name>` and `#map=day:N`.
- **Weather** per day at the night spot and the day's high point from Open-Meteo, with a per-trek
  model choice (`weatherModel`, values beyond its horizon filled from the default blend). Warnings
  are computed, not typed: storm (thunderstorm code, or CAPE ≥ 400 with lifted index ≤ −2 and rain
  chance ≥ 20 %), rain, snow, wind, frost, heat, fog, UV, late arrival. Every warning links to its
  numbers on Open-Meteo.
- **Day simulator**: a start-time slider over your altitude and exposure through the day, the
  weather at the place you would be, an ECMWF ensemble storm strip, the events you meet, and a
  recommended start. Weather for every hour at every sample point along the route is fetched once
  and cached, so the slider and offline use need no requests.
- **Snapshot**: one position fix, or a long-press to pick on the map, marks earlier days done and
  fills today's card with distance, ascent left and an arrival estimate.
- **Offline**: a versioned service worker precaches the page, GPX, app, section maps; tiles and
  fonts are cached as used; "Save whole route offline" stores a tile corridor.

## Conventions the app relies on

Waypoint names carry meaning: `NIGHT n · <date> · <place>: <note>` (with `NIGHT 0` the night
before day 1), `FINISH · …`, `PASS · <name> <ele> m - <note>` (type `Summit`), `NIGHT n option B`
and `FALLBACK` are ignored by the day logic. Types (Night, Flag, Lodging, Campsite, Water, Summit,
SideTrip, ViaFerrata, Escape, Transport, Shelter, Info) set colours, icons and map layers. Tracks:
`ROUTE i of N · …`, `BOUNDARY · …`, `SIDE TRIP · …`, `VIA FERRATA · …`.

## Layout

- `src/`: `render.py` (content.yaml → body), `build.py`, `head.html` (theme), `scripts.html`, `sw.js`
- `site/`: `map.js` (the app), `vendor/` (Leaflet 1.9.4), built files
- `tools/`: the commands above; `research/`: what the research tools write, plus `findings.md`
- `container/Caddyfile`, `compose.yml`, `Dockerfile`, `.kitshn.yaml`, `kitshn.md`: the deploy recipe

## Credits

Route data © OpenStreetMap contributors (ODbL). Tiles © OpenTopoMap (CC BY-SA). Heights from
OpenTopoData. Weather, ensembles and reanalysis from Open-Meteo. Leaflet under `site/vendor/`.

## License

MIT
