# Sphinx Inventory Builder

This extension adds an inventory builder, a customized builder which only generates intersphinx "object.inv" inventory files.
The documentation files are not written.

## Installing

Directly install via pip by using::

    pip install sphinx-inventory-builder

Add ``sphinx_inventory_builder`` to the `extensions`_ array in your Sphinx **conf.py**.
For example:

.. code-block:: python

   extensions = ['sphinx_inventory_builder']

## How to use

Once installed, run the new `inventory` builder::

    sphinx-build -b inventory ./source ./build

## Origin Story

This extension was adopted from Sage's [inventory_builder](https://github.com/sagemath/sage/blob/2a9a4267f93588cf33119cbacc032ed9acc433e5/src/sage_docbuild/ext/inventory_builder.py) and turned into an extension so it could be used by others.
