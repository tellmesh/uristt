from __future__ import annotations

from importlib.resources import files

from uri_control.edge.manifest import register_manifest_files


def manifest_paths():
    root = files(__package__)
    return [root.joinpath("manifest.yaml"), root.joinpath("manifest.tts.yaml")]


def register(rt):
    register_manifest_files(rt, manifest_paths())
