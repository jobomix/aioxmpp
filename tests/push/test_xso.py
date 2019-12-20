########################################################################
# File name: test_xso.py
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
import unittest

import aioxmpp.xso
from aioxmpp import xso
from aioxmpp import forms

import aioxmpp.push.xso as push_xso
from aioxmpp.forms import TextSingle
import aioxmpp.forms.xso as forms_xso
from aioxmpp.utils import namespaces

TEST_TO = aioxmpp.structs.JID.fromstr("pubsub.example")


class TestNamespaces(unittest.TestCase):
    def test_namespace(self):
        self.assertEqual(
            namespaces.xep0357_push,
            "urn:xmpp:push:0"
        )


class TestPush(unittest.TestCase):
    def test_is_xso(self):
        self.assertTrue(issubclass(
            push_xso.Push,
            aioxmpp.xso.XSO,
        ))

    def test_tag(self):
        self.assertEqual(
            push_xso.Push.TAG,
            (namespaces.xep0357_push, "enable")
        )

    def test_is_iq_payload(self):
        self.assertIn(
            push_xso.Push.TAG,
            aioxmpp.IQ.CHILD_MAP,
        )

    def test_JID(self):
        self.assertIsInstance(
            push_xso.Push.jid,
            xso.Attr
        )
        self.assertEqual(
            push_xso.Push.jid.tag,
            (None, "jid")
        )
        self.assertIsInstance(
            push_xso.Push.jid.type_,
            xso.JID
        )
        self.assertIs(
            push_xso.Push.jid.default,
            xso.NO_DEFAULT
        )

    def test_node(self):
        self.assertIsInstance(
            push_xso.Push.node,
            xso.Attr
        )
        self.assertEqual(
            push_xso.Push.node.tag,
            (None, "node")
        )
        self.assertIsInstance(
            push_xso.Push.node.type_,
            xso.String
        )
        self.assertIs(
            push_xso.Push.node.default,
            None
        )

    def test_data(self):
        self.assertIsInstance(
            push_xso.Push.data,
            xso.Child,
        )
        self.assertSetEqual(
            push_xso.Push.data._classes,
            {
                forms.Data,
            }
        )


