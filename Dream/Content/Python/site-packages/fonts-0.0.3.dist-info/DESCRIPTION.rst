Python Fonts
============

A Python framework for distributing and managing fonts.

Why
===

While Python can access system fonts, it has no direct way of guaranteeing a particular font is available, or any way of including it as a dependency.

Fonts aims to tackle this problem with tools for packaging and distributing fonts via PyPi, which can be easily located and used in Python using PIL or otherwise.

How
===

Fonts uses ``entry_points`` to expose the font files located in each package.

To use these fonts in your project you should include them as a dependency and either grab the font paths using ``pkg_resources.iter_entry_points('fonts_ttf')`` or use this fonts module to collate them for you.

For example::

    from PIL import ImageFont
    from fonts.ttf import AmaticSC
    font = ImageFont.truetype(AmaticSC)

Fonts
=====

- Fredoka One (Sans-Serif, OFL) - https://pypi.org/project/font-fredoka-one
- Amatic SC (Hand-Drawn, OFL) - https://pypi.org/project/font-amatic-sc


0.0.3
=====

- Added otf support


