########################################################################
# File name: test_service.py
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
import io
import aioxmpp.xml as xml
import aioxmpp.disco
import aioxmpp.forms
import aioxmpp.push.service as push_service
import aioxmpp.push.xso as push_xso
import aioxmpp.service
import aioxmpp.stanza
import aioxmpp.structs
from aioxmpp.push.xso import PushConfigForm
from aioxmpp.testutils import (
    make_connected_client,
    CoroutineMock,
    run_coroutine,
)

TEST_FROM = aioxmpp.structs.JID.fromstr("foo@bar.example/baz")
TEST_JID1 = aioxmpp.structs.JID.fromstr("bar@bar.example/baz")
TEST_JID2 = aioxmpp.structs.JID.fromstr("baz@bar.example/baz")
TEST_JID3 = aioxmpp.structs.JID.fromstr("fnord@bar.example/baz")
TEST_TO = aioxmpp.structs.JID.fromstr("pubsub.example")


class TestService(unittest.TestCase):
    def test_is_service(self):
        self.assertTrue(issubclass(
            push_service.PushClient,
            aioxmpp.service.Service
        ))

    def setUp(self):
        self.disco = unittest.mock.Mock()
        self.pubsub = unittest.mock.Mock()
        self.cc = make_connected_client()
        self.cc.local_jid = TEST_FROM
        self.cc.query_info = CoroutineMock()
        self.cc.query_info.side_effect = AssertionError
        self.cc.query_items = CoroutineMock()
        self.cc.query_items.side_effect = AssertionError
        self.s = push_service.PushClient(self.cc, dependencies={
            aioxmpp.PubSubClient: self.pubsub,
            aioxmpp.DiscoClient: self.disco,
        })

        self.disco.mock_calls.clear()
        self.pubsub.mock_calls.clear()
        self.cc.mock_calls.clear()

    def tearDown(self):
        del self.s
        del self.cc
        del self.disco
        del self.pubsub

    def test_enable_push(self):
        config = unittest.mock.Mock(spec=aioxmpp.forms.Data)

        run_coroutine(self.s.set_push_config(
            TEST_TO,
            config,
            node="some_node",
        ))

        self.cc.send.assert_called_once_with(unittest.mock.ANY)

        _, (iq,), _ = self.cc.send.mock_calls[0]

        self.assertIsInstance(iq, aioxmpp.IQ)
        self.assertEqual(iq.type_, aioxmpp.IQType.SET)

        self.assertIsInstance(iq.payload, push_xso.Push)
        self.assertIs(iq.payload.data, config)
        self.assertIs(iq.payload.jid, TEST_TO)
        self.assertEqual(iq.payload.node, "some_node")

    def test_get_push_config(self):
        config = self.s.get_push_config()
        form = PushConfigForm.from_xso(config)

        form.service.value = 'fcm'
        form.device_id.value = 'dummy_device_id'
        form.priority.value = 'high'
        form.silent.value = 'false'

        result = form.render_reply()
        self.assertEqual(
            len(result.fields),
            4
        )

        service_field = result.fields[0]
        self.assertSequenceEqual(
            service_field.values,
            ["fcm"]
        )
        self.assertEqual(
            service_field.desc,
            "The service to use for push notification: whether fcm or apns",
        )

        device_id = result.fields[1]
        self.assertSequenceEqual(
            device_id.values,
            ["dummy_device_id"]
        )
        self.assertEqual(
            device_id.desc,
            "The unique device id for push notification",
        )

        priority = result.fields[2]
        self.assertSequenceEqual(
            priority.values,
            ["high"]
        )
        self.assertEqual(
            priority.desc,
            "The message priority, whether high or normal",
        )

        silent = result.fields[3]
        self.assertSequenceEqual(
            silent.values,
            ["false"]
        )
        self.assertEqual(
            silent.desc,
            "Enable silent notification, whether true of false",
        )

    def test_push_xml_output(self):
        b = io.BytesIO()
        push = push_xso.Push(jid=TEST_TO, node="some_node")
        config = self.s.get_push_config()
        form = PushConfigForm.from_xso(config)

        form.service.value = 'fcm'
        form.device_id.value = 'dummy_device_id'
        form.priority.value = 'high'
        form.silent.value = 'false'

        push.data = form.render_reply()

        xml.write_single_xso(push, b)
        assert b.getvalue() == b'<enable xmlns="urn:xmpp:push:0" ' \
                               b'jid="pubsub.example" node="some_node">' \
                               b'<x xmlns="jabber:x:data" type="submit">' \
                               b'<field type="hidden" var="FORM_TYPE">' \
                               b'<value>http://jabber.org/protocol/pubsub#publish-options</value>' \
                               b'</field><field type="text-single" var="service">' \
                               b'<desc>The service to use for push notification: whether fcm or apns</desc>' \
                               b'<value>fcm</value></field><field type="text-single" var="device_id">' \
                               b'<desc>The unique device id for push notification</desc>' \
                               b'<value>dummy_device_id</value></field>' \
                               b'<field type="text-single" var="priority">' \
                               b'<desc>The message priority, whether high or normal</desc>' \
                               b'<value>high</value></field><field type="text-single" var="silent">' \
                               b'<desc>Enable silent notification, whether true of false</desc>' \
                               b'<value>false</value></field></x></enable>'

    def test_disable_push_xml_output(self):
        b = io.BytesIO()
        push = push_xso.DisablePush(jid=TEST_TO, node="some_node")
        xml.write_single_xso(push, b)
        assert b.getvalue() == b'<disable xmlns="urn:xmpp:push:0" jid="pubsub.example" node="some_node"/>'
