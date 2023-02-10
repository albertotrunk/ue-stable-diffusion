bencode.py
==========

.. image:: https://img.shields.io/pypi/v/bencode.py.svg?style=flat-square
   :target: https://pypi.python.org/pypi/bencode.py

.. image:: https://img.shields.io/travis/fuzeman/bencode.py.svg?style=flat-square
   :target: https://travis-ci.org/fuzeman/bencode.py

.. image:: https://img.shields.io/coveralls/fuzeman/bencode.py/master.svg?style=flat-square
   :target: https://coveralls.io/github/fuzeman/bencode.py

Simple bencode parser (for Python 2, Python 3 and PyPy), forked from the bencode__ package by Thomas Rampelberg.

__ https://pypi.python.org/pypi/bencode


Usage
-----

**Encode:**

.. code-block:: python

    import bencode

    bencode.encode({'title': 'Example'})
    # 'd5:title7:Examplee'

    bencode.encode(12)
    # 'i12e'

**Decode:**

.. code-block:: python

    import bencode

    bencode.decode('d5:title7:Examplee')
    # {'title': 'Example'}

    bencode.decode('i12e')
    # 12


API
---

``bencode.bencode(value)``

``bencode.encode(value)``

    Encode ``value`` into the bencode format.

``bencode.bdecode(value)``

``bencode.decode(value)``

    Decode bencode formatted string ``value``.

``bencode.bread(fd)``

    Read bencode formatted string from file or path ``fd``.

``bencode.bwrite(data, fd)``

    Write ``data`` as a bencode formatted string to file or path ``fd``.



