srslib - Sender Rewriting Scheme (SRS) library for Python
=========================================================

**srslib** is a modern Python implementation of the `Sender Rewriting
Scheme (SRS) <https://en.wikipedia.org/wiki/Sender_Rewriting_Scheme>`__.

Highlights:

-  Compatible with Python 2.7 and 3.x;
-  Implements the standard "Guarded" SRS scheme as described in the
   `original SRS paper <http://www.libsrs2.org/srs/srs.pdf>`__;
-  Simple to use and understand.

Installation
------------

.. code:: sh

    pip install srslib

Example Usage
-------------

.. code:: py

    import srslib

    srs = srslib.SRS('my_secret_key')

    # Rewrites an email from alice@A.com to B.com
    rewritten_addr = srs.forward('alice@A.com', 'B.com')
    # => 'SRS0=ZPM1=67=A.com=alice@B.com'

    # Reverse it to get the address to bounce to.
    try:
      bounce_addr = srs.reverse(rewritten_addr)
      # => 'alice@A.com'
    except srslib.Error as e:
      ...  # Handle errors

Documentation
-------------

The full documentation for **srslib** lives at
https://srslib.readthedocs.io/.

Implementation
--------------

This library is a clean re-implementation of SRS in modern Python based
on the `original SRS paper <http://www.libsrs2.org/srs/srs.pdf>`__, and
taking inspiration from the canonical
`libsrs2 <https://github.com/shevek/libsrs2>`__ C implementation and the
older `pysrs <http://www.bmsi.com/python/pysrs.html>`__ library (which
itself is based on the
`Mail::SRS <http://search.cpan.org/~shevek/Mail-SRS-0.31/lib/Mail/SRS.pm>`__
Perl package).

Compared to these two libraries, **srslib**

-  ... is a clean, modern, pure-Python implementation and supports
   Python 3.x;
-  ... discards baggage from Mail::SRS around legacy schemes and
   settings.

License
-------

Licensed under the Apache License, Version 2.0.
