# -*- coding: utf-8 -*-
"""
Inventory builder

A customized builder which only generates intersphinx "object.inv"
inventory files. The documentation files are not written.
"""

import sys
from os import path
from typing import Any

from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.util.inventory import InventoryFile
from sphinx.util.logging import getLogger

__version__ = '0.2.0'

logger = getLogger(__name__)


class _InventoryMixin:
    """
    Shared behavior: don’t write HTML, just dump objects.inv.
    """
    format = "inventory"
    epilog = "The inventory file is in %(outdir)s."

    def get_outdated_docs(self) -> set[str]:
        return self.env.found_docs

    def write_doc(self, docname, doctree):
        # suppress writing HTML files
        return

    def copy_static_files(self):
        return

    def finish(self) -> None:
        """
        Only write the inventory files.
        """
        assert self.env is not None
        InventoryFile.dump(
            path.join(self.outdir, self.app.config.inventory_filename), self.env, self
        )


class InventoryHtmlBuilder(_InventoryMixin, StandaloneHTMLBuilder):
    """Inventory builder with html-style URIs."""
    name = "inventory-html"


class InventorySingleHtmlBuilder(_InventoryMixin, SingleFileHTMLBuilder):
    """Inventory builder with singlehtml-style URIs."""
    name = "inventory-singlehtml"


def disable_intersphinx(app, config):
    inventory_builders = ["inventory-html", "inventory-singlehtml"]
    if detect_builder(app) in inventory_builders:
        config.intersphinx_mapping = {}
        config.intersphinx_disabled_reftypes = ['*']

        config.suppress_warnings = ['ref.*', 'docutils']


def detect_builder(app):
    argv = sys.argv
    try:
        i = list(argv).index("-b")
        name = argv[i + 1]
    except ValueError:
        for a in argv:
            if a.startswith("--builder="):
                name = a.split("=", 1)[1]
                break
    return name


def ignore_external_refs(app, env, node, contnode):
    """
    Called when Sphinx can’t resolve a reference.
    Returns None to ignore it (no warning), or returns contnode to continue.
    """
    # intersphinx adds a custom attribute to its nodes:
    if getattr(node, 'intersphinx', False):
        # This is an external reference — ignore it completely
        return None

    # All other refs (internal) will trigger normal warnings
    return contnode


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("inventory_filename", default="objects.inv", rebuild="")

    # Register both builders
    app.add_builder(InventoryHtmlBuilder)
    app.add_builder(InventorySingleHtmlBuilder)

    def on_builder_inited(app):
        if app.builder.name in ('inventory-singlehtml', 'singlehtml'):
            original_get_target_uri = app.builder.get_target_uri

            # Patch get_target_uri to fix internal links for single-page builds.
            # Rewrites "#document-{page}#{anchor}" → "{root_doc}.html#{anchor}"
            def patched_get_target_uri(docname, typ=None):
                uri = original_get_target_uri(docname, typ)
                if uri.startswith('#document-'):
                    next_hash = uri.find('#', len('#document-'))
                    suffix = uri[next_hash:] if next_hash != -1 else ''
                    return app.config.root_doc + app.builder.out_suffix + suffix
                return uri

            app.builder.get_target_uri = patched_get_target_uri

    app.connect("config-inited", disable_intersphinx)
    app.connect("builder-inited", on_builder_inited)
    app.connect("missing-reference", ignore_external_refs)

    return {"parallel_read_safe": True}
