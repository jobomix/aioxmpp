import aioxmpp.xso
from aioxmpp.xso import Attr
from aioxmpp.xso import JID
from aioxmpp.xso import Child
from aioxmpp.utils import namespaces
import aioxmpp.forms

namespaces.xep0357_push = "urn:xmpp:push:0"


@aioxmpp.IQ.as_payload_class
class Push(aioxmpp.xso.XSO):
    """
    Simple XSO to represent an XMPP push notification.

    It takes no arguments and has no attributes or children.
    """

    TAG = (namespaces.xep0357_push, "enable")

    jid = Attr(
        "jid",
        type_=JID()
    )

    node = Attr(
        "node",
        default=None
    )

    data = Child([
        aioxmpp.forms.Data,
    ])

    def __init__(self, jid, node=None):
        super().__init__()
        self.jid = jid
        self.node = node


class PushConfigForm(aioxmpp.forms.Form):

    FORM_TYPE = 'http://jabber.org/protocol/pubsub#publish-options'

    service = aioxmpp.forms.TextSingle(
        var='service',
        label='The service to use for push notification: whether fcm or apns'
    )

    device_id = aioxmpp.forms.TextSingle(
        var='device_id',
        label='The unique device id for push notification'
    )

    silent = aioxmpp.forms.TextSingle(
        var='silent',
        label='Enable silent notification, whether true of false'
    )

    priority = aioxmpp.forms.TextSingle(
        var='priority',
        label='The message priority, whether high or normal'
    )
