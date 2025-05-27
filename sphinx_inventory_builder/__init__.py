# -*- coding: utf-8 -*-
"""
Inventory builder

A customized builder which only generates intersphinx "object.inv"
inventory files. The documentation files are not written.
"""
from __future__ import annotations

from os import path
from typing import Any

from sphinx.application import Sphinx
from sphinx.builders.dummy import DummyBuilder
from sphinx.util.inventory import InventoryFile

__version__ = "0.1.0"


class InventoryBuilder(DummyBuilder):
    """
    A customized builder which only generates intersphinx "object.inv"
    inventory files. The documentation files are not written.
    """

    name = "inventory"
    format = "inventory"
    epilog = "The inventory files are in %(outdir)s."

    def finish(self) -> None:
        """
        Only write the inventory files.
        """
        assert self.env is not None

        InventoryFile.dump(
            path.join(self.outdir, self.app.config.inventory_filename), self.env, self
        )


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("inventory_filename", default="objects.inv", rebuild="")

    app.add_builder(InventoryBuilder)
    return {"parallel_read_safe": True}
