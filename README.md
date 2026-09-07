# Trek site template

A static, offline-capable trip dossier for a multi-day trek: day plan in one or two languages,
interactive map drawn from the real GPX, elevation profile, per-day live weather with warnings and
an hourly chart, a position snapshot that marks finished days done, annotated section maps, and the
GPX as a download for OsmAnd. Deploys to a VPS with KitSHn.

Built from the GR52 dossier at https://gr52.yarden-zamir.com. Use it through the `trek-dossier`
agent skill, which lists the inputs and the steps.

## How it fits together

- `trek.json`: the one config. See `trek.example.json` for every key: `slug`, `name`, `shortName`,
  `description`, `hostname`, `gpx`, `gpxDescription`, `timezone`, `plannedStart` (hour), `tentWindow`
  (optional "HH:MM"), `languages`, `elevationDataset`, `places` (text → map focus query),
  `waypoints`, `route` (`osm_relations` in walking order + `start`, or `gpx_in`), `sectionMaps`,
  `enrich` (`water_radius_m`, optional `boundary`), `side_trips`, `strings` (per-language overrides
  of the app's wording, for example the heat warning), `weatherModel` and `weatherModelLabel`
  (Open-Meteo model id such as `meteofrance_seamless` for the Alps; values beyond that model's
  horizon are filled from the default blend; unset means the default blend, which matched the
  Israel Meteorological Service within about 1 °C).
- `src/body.html`: the content, written per trek, both languages. `src/head.html` (theme),
  `src/scripts.html` (language toggle, profile), `src/sw.js` (service worker template).
- `site/map.js`: the generic app. Reads `window.TREK` (injected by the build) and the GPX.
- `src/build.py`: assembles `site/index.html`, `site/sw.js`, `site/manifest.webmanifest`,
  `Caddyfile.j2`. Adds table captions and card labels, links place names, inserts section maps.
- `tools/`: `build_gpx.py` (route + waypoints + OpenStreetMap enrichment), `elevation.py`
  (OpenTopoData heights), `maps.py` (section maps from OpenTopoMap tiles), `side_trips.py`
  (optional routed side tracks), `check.py` (headless Chrome verification of the built site).

## Conventions the app relies on

Waypoint names carry meaning. The app reads them to find days, nights and the finish:

- `NIGHT n · <date> · <place>: <note>` for each sleeping spot, `NIGHT 0` for the night before day 1.
- `FINISH · <date> · <place>` for the end.
- `PASS · <name> <ele> m - <note>` for cols and summits on the line (type `Summit`).
- `FALLBACK night n · …` and `NIGHT n option B · …` are ignored by the day logic.
- Types: Night, Flag, Lodging, Campsite, Water, Summit, SideTrip, ViaFerrata, Escape, Transport,
  Shelter, Info. Type sets the colour and icon in OsmAnd and the map layer group.
- Tracks: `ROUTE i of N · …` (the walking line, in order), `BOUNDARY · …`, `SIDE TRIP · …`,
  `VIA FERRATA · …`.

Day cards in `src/body.html` carry `data-day="n"` and `data-date="YYYY-MM-DD"`. The planned
hours chip (`8–9 h`) in a card feeds the arrival estimate and the hourly walking window.

## Per-trek README

Keep this file's structure; replace the heading and the first paragraph with the trek, its dates
and the live URL, and drop this section.

## Build and check

```sh
uv run tools/build_gpx.py      # route + waypoints from trek.json
uv run tools/elevation.py      # heights
uv run tools/maps.py           # section maps
uv run src/build.py            # the page
uv run tools/check.py          # headless Chrome: map, weather, links, snapshot, hourly chart
uv run tools/check.py --url https://your.host/   # same checks against the deployed site
```

## Credits

Route data © OpenStreetMap contributors (ODbL). Map tiles © OpenTopoMap (CC BY-SA). Heights from
OpenTopoData. Weather from Open-Meteo. Leaflet 1.9.4 vendored under `site/vendor/`.

## License

MIT
