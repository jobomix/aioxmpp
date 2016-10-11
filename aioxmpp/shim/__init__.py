########################################################################
# File name: __init__.py
# This file is part of: aioxmpp
#
# LICENSE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
#
########################################################################
"""
:mod:`~aioxmpp.shim` --- Stanza Headers and Internet Metadata (:xep:`0131`)
###########################################################################

This module provides support for :xep:`131` stanza headers. The following
attributes are added by this module to the existing stanza classes:

.. attribute:: aioxmpp.Message.xep0131_headers

   A :class:`xso.Headers` instance or :data:`None`. Represents the SHIM headers of
   the stanza.

.. attribute:: aioxmpp.Presence.xep0131_headers

   A :class:`xso.Headers` instance or :data:`None`. Represents the SHIM headers of
   the stanza.

The attributes are available as soon as :mod:`aioxmpp.shim` is loaded.

.. autoclass:: Service

.. currentmodule:: aioxmpp.shim.xso

.. autoclass:: Headers

"""
from . import xso

from .service import (
    Service,
)
