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
:mod:`~aioxmpp.push` --- XMPP Ping (:xep:`199`)
###############################################

To start using Push services in your application, you have to load the
:class:`.PushClient` into the client, using :meth:`~.node.Client.summon`.

Service
=======

.. currentmodule:: aioxmpp

.. autoclass:: PushClient

.. currentmodule:: aioxmpp.push

.. currentmodule:: aioxmpp.push.xso

XSOs
====

Sometimes it is useful to send a ping manually instead of relying on the
:class:`Service`. For this, the :class:`Ping` IQ payload can be used.



Forms
-----

.. currentmodule:: aioxmpp.push

.. autoclass:: PushConfigForm

"""

from .service import PushClient
from .xso import Push, DisablePush, PushConfigForm

Service = PushClient
