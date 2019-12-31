import asyncio

import aioxmpp
import aioxmpp.forms.xso as forms_xso
import aioxmpp.push.xso as push_xso
from aioxmpp.pubsub import PubSubClient
from aioxmpp.service import Service


class PushClient(Service):
    ORDER_AFTER = [
        PubSubClient,
    ]

    def __init__(self, client, **kwargs):
        super().__init__(client, **kwargs)
        self._pubsub = self.dependencies[PubSubClient]

    def get_push_config(self):
        data = forms_xso.Data(type_=forms_xso.DataType.FORM)

        data.fields.append(
            forms_xso.Field(
                var="FORM_TYPE",
                type_=forms_xso.FieldType.HIDDEN,
                values=["http://jabber.org/protocol/pubsub#publish-options"],
            )
        )

        data.fields.append(
            forms_xso.Field(
                var="service",
                type_=forms_xso.FieldType.TEXT_SINGLE,
                values=[],
                desc="The service to use for push notification: whether fcm or apns",
            )
        )

        data.fields.append(
            forms_xso.Field(
                var="device_id",
                type_=forms_xso.FieldType.TEXT_SINGLE,
                values=[],
                desc="The unique device id for push notification",
            )
        )

        data.fields.append(
            forms_xso.Field(
                var="priority",
                type_=forms_xso.FieldType.TEXT_SINGLE,
                values=[],
                desc="The message priority, whether high or normal",
            )
        )

        data.fields.append(
            forms_xso.Field(
                var="silent",
                type_=forms_xso.FieldType.TEXT_SINGLE,
                values=[],
                desc="Enable silent notification, whether true of false",
            )
        )

        return data

    @asyncio.coroutine
    def set_push_config(self, jid, config, node=None):
        """
        Update the configuration of a node.

        :param jid: Address of the PubSub service.
        :type jid: :class:`aioxmpp.JID`
        :param config: Configuration form
        :type config: :class:`aioxmpp.forms.Data`
        :param node: Name of the PubSub node to query.
        :type node: :class:`str`
        :raises aioxmpp.errors.XMPPError: as returned by the service
        :return: The configuration of the node.
        :rtype: :class:`~.forms.Data`

        .. seealso::

            :class:`aioxmpp.pubsub.NodeConfigForm`
        """

        iq = aioxmpp.stanza.IQ(type_=aioxmpp.structs.IQType.SET)
        iq.payload = push_xso.Push(
            jid=jid, node=node
        )
        iq.payload.data = config

        yield from self.client.send(iq)

    @asyncio.coroutine
    def disable_push_config(self, jid, node=None):
        iq = aioxmpp.stanza.IQ(type_=aioxmpp.structs.IQType.SET)
        iq.payload = push_xso.DisablePush(
            jid=jid, node=node
        )
        yield from self.client.send(iq)
