# Parametric leather-tray wet mold

A parametric CAD application: one deterministic geometry model in Python and
CadQuery, a thin HTTP layer over it, and a browser front end that never contains
CAD logic.

```
packages/tray-core   the geometry. CadQuery + Pydantic. The source of truth.
packages/api         FastAPI over the core, with process-isolated CAD workers.
packages/web         React + TypeScript + Vite + React Three Fiber.
deploy/              the image, the compose stack and the smoke script.
tools/reference_probe  measurement scripts behind every number in the docs
tools/print_study      what the pair costs to print, and a 3MF-with-settings prototype
reference/           the original STEP and STL pair this was reverse-engineered from.
```

## Coffin molds for the H2C

Choose **Coffin body** or **Coffin lid** from the preset menu. Both use
3.25 mm leather and four matching 6.6 mm through-holes for M6 bolts.
The body is 12 inches long and 1¾ inches deep. The lid is ½ inch deep
with a 4 mm outward offset, allowing 0.75 mm nominal clearance per side
over the body leather at the rim.

Set shoulder position and width, head flare, and foot taper in **Shape**.
The angles are measured from the long axis. Keep the same shape settings
for both molds and adjust the lid offset after measuring the dried body.

Print each half on its own plate. The presets export diagonally oriented
parts and the 3MF includes clamp reinforcement. Check the H2C nozzle
profile and brim in the slicer, especially after changing the outline.
Use four M6 bolts with washers on the outside faces and draw the die down
gradually in an alternating pattern. Keep the leather clear of the bolt
holes, or punch matching holes in the waste margin before bolting up.

## Run it

```bash
make install
make dev        # API + worker pool + Vite
make test       # core, API and frontend suites
make doctor     # resolved configuration, and ping the API
```

## Or run the deployment, locally

The same image, compose file and Caddyfile the VPS runs, with TLS off and on
unprivileged ports.

```bash
make deploy-local      # build and start the containerised stack on :8080
make deploy-smoke      # 21 checks: TLS, CORS, SSE buffering, cache, exports, stats
make deploy-local-web  # the GitHub Pages build, pointed at that stack
make deploy-down
```

## Documentation

| | |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | the geometry core: what the reference is, how it is rebuilt, why |
| [`docs/parameter-model.md`](docs/parameter-model.md) | the parameter schema, dependencies and diagnostics |
| [`docs/api.md`](docs/api.md) | the HTTP contract, workers, caching, job lifecycle |
| [`docs/frontend.md`](docs/frontend.md) | the browser application, its state machine and viewer |
| [`docs/deployment.md`](docs/deployment.md) | GitHub Pages, the VPS, and rehearsing both locally |
| [`docs/analytics.md`](docs/analytics.md) | what the public usage counter counts, and the data behind it |
| [`docs/material-optimisation.md`](docs/material-optimisation.md) | what the pair costs to print, where the material actually goes, and a 3MF export that carries print settings |

## The rule the whole project is built around

```
female_base_profile = offset(male_base_profile, forming_gap)
```

The female cavity is a true 2D offset of the male's **base** profile — the plan
curve before any 3D edge treatment. Verified against the original Onshape STEP to
2.4 um, and enforced by tests that assert no male fillet, plate dimension or
manufacturing feature can reach it.
