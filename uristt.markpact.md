# UriPack: uristt

Self-contained Markpact — definitions, full source, run config. Unpack & run: `urisys markpact run uristt/uristt.markpact.md --as service` (writes `.markpact/`).

```yaml markpact:pack
apiVersion: urisys.io/v1
kind: UriPack
metadata:
  id: uristt-pack
  version: 1.0.0
  language: python
description: Speech-to-text pack (mock MVP; browser passthrough + audio transcribe).
schemes:
- stt
capabilities:
- id: stt.session.start
  uri: stt://local/session/{session}/command/start
  kind: command
  operation: stt.session.start
  handler: python://uristt.handlers:session_start
  side_effects: true
  approval: required
- id: stt.session.transcript
  uri: stt://local/session/{session}/query/transcript
  kind: query
  operation: stt.session.transcript
  handler: python://uristt.handlers:session_transcript
  side_effects: false
  approval: not_required
- id: stt.audio.transcribe
  uri: stt://local/audio/command/transcribe
  kind: command
  operation: stt.audio.transcribe
  handler: python://uristt.handlers:audio_transcribe
  side_effects: true
  approval: required
policy:
  default: deny_mutations_without_approval
runtime:
  default_environment: mock
  supports:
  - mock
  - local
  - docker
```

```yaml markpact:run
modes:
- pack
- service
- flow
- interface
- adapter
default: service
scheme: stt
service:
  port: 8790
  wire: POST /uri/call
flow:
  ids: []
adapter:
  wire: POST /uri/call
  events: GET /events
```

```python markpact:module path=uristt/__init__.py
from __future__ import annotations

from .routes import manifest_paths, register

__all__ = ["register", "manifest_paths"]
```

```python markpact:module path=uristt/handlers.py
from __future__ import annotations

from typing import Any

_SESSIONS: dict[str, dict[str, Any]] = {}


def _session_id(context: dict[str, Any]) -> str:
    return (context.get("params") or {}).get("session", "main")


def session_start(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    sid = _session_id(context)
    entry = {
        "session": sid,
        "language": payload.get("language", "pl-PL"),
        "mode": payload.get("mode", "browser"),
        "status": "listening",
        "transcript": "",
    }
    _SESSIONS[sid] = entry
    return {"ok": True, "session": entry}


def session_transcript(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    sid = _session_id(context)
    session = _SESSIONS.setdefault(
        sid,
        {"session": sid, "language": "pl-PL", "mode": "browser", "status": "idle", "transcript": ""},
    )
    if payload.get("text"):
        session["transcript"] = str(payload["text"])
    if not session["transcript"]:
        session["transcript"] = payload.get("default_text") or "kliknij OK"
    return {
        "ok": True,
        "session": sid,
        "text": session["transcript"],
        "transcript": session["transcript"],
        "language": session.get("language", "pl-PL"),
        "engine": "mock-browser" if session.get("mode") == "browser" else "mock-local",
    }


def tts_speak(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    del context
    text = str(payload.get("text") or payload.get("transcript") or "").strip()
    if not text:
        return {"ok": False, "error": "missing text"}
    return {
        "ok": True,
        "text": text,
        "spoken": True,
        "engine": payload.get("engine", "mock"),
        "audio_url": None,
    }


def audio_transcribe(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    del context
    text = payload.get("text") or payload.get("transcript")
    if not text and payload.get("audio_b64"):
        text = "kliknij OK"
    if not text:
        text = "kliknij OK"
    return {
        "ok": True,
        "transcript": text,
        "language": payload.get("language", "pl-PL"),
        "engine": payload.get("engine", "mock"),
        "audio_received": bool(payload.get("audio_b64")),
    }
```

```python markpact:module path=uristt/routes.py
from __future__ import annotations

from importlib.resources import files

from uri_control.edge.manifest import register_manifest_files


def manifest_paths():
    root = files(__package__)
    return [root.joinpath("manifest.yaml"), root.joinpath("manifest.tts.yaml")]


def register(rt):
    register_manifest_files(rt, manifest_paths())
```

```markdown markpact:docs
# uristt

`stt://` and `tts://` URI capability packs for `urisys-node`.

Standalone sibling of `urihim`, `uriocr`, etc. — not bundled inside `urisys-automation-lab`.

~~~bash
pip install uristt
# monorepo dev:
cd tellmesh/uristt && uv sync --extra dev
~~~
```

