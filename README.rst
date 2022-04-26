*********
Mopidy-Cd-Autoplay
*********

`Mopidy <http://www.mopidy.com/>`_ extension to automatically queue songs from audio CDs using Mopidy-Cd extension.


Installation
============

Install by running::

      sudo pip install Mopidy-Cd-Autoplay

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com <http://apt.mopidy.com/>`_.

Note: You need to add the ``mopidy`` user to the ``cdrom`` group::

      adduser mopidy cdrom


Configuration
=============

No configuration required.


Project resources
=================

- `Source code <https://github.com/mczerski/mopidy-cd-autoplay.git>`_
- `Issue tracker <https://github.com/mczerski/mopidy-cd-autoplay.git>`_


Known issues
=========


Changelog
=========

v0.1.0 (2022-04-26)
-------------------

- Initial version.
- Inseritng CD automatically add all CD tracks to tracklist.
- Removing CD automatically removes all CD tracks from tracklist.  
