# uristt

`stt://` and `tts://` URI capability packs for `urisys-node`.

Standalone sibling of `urihim`, `uriocr`, etc. — not bundled inside `urisys-automation-lab`.

```bash
pip install uristt
# monorepo dev:
cd tellmesh/uristt && uv sync --extra dev
```

## Ekosystem TellMesh

Orchestrator: **[urisys](https://github.com/tellmesh/urisys)** · Mapa: **[MESH.md](https://github.com/tellmesh/urisys/blob/main/docs/MESH.md)** · Model: **[ECOSYSTEM.md](https://github.com/tellmesh/urisys/blob/main/docs/ECOSYSTEM.md)**

| Pole | Wartość |
|------|---------|
| **Warstwa** | Capability pack |
| **Scheme** | `stt://` / `tts://` |
| **Zależność** | `uricontrol>=0.1.8` |
| **Edge** | urisys-automation-lab |

Runtime edge: **`uri_control.edge`** w pakiecie **`uricontrol`** (legacy PyPI `uricore` / `urisysedge` usunięty 2026-06).
Resolver intencji: **`uriresolver`** (`uri_resolver`) + transport w **`uritransport`**; policy gate: **`uriguard`** (`uri_guard`).

<!-- end-ecosystem -->
