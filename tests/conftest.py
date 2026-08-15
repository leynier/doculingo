"""Shared test configuration.

Set a dummy OPENAI_API_KEY before any doculingo import so that settings load
with a key even on machines without one. Tests that need to simulate a missing
key can delete it with monkeypatch.delenv.
"""

import os

os.environ.setdefault("OPENAI_API_KEY", "test")
