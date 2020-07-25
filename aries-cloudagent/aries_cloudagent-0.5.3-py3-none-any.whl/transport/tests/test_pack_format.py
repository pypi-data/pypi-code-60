import json

from asynctest import TestCase as AsyncTestCase, mock as async_mock

from ...config.injection_context import InjectionContext

from ...protocols.routing.v1_0.message_types import FORWARD
from ...wallet.base import BaseWallet
from ...wallet.basic import BasicWallet
from ...wallet.error import WalletError

from ..error import MessageEncodeError, MessageParseError
from ..pack_format import PackWireFormat
from .. import pack_format as test_module


class TestPackWireFormat(AsyncTestCase):
    test_message_type = "PROTOCOL/MESSAGE"
    test_message_id = "MESSAGE_ID"
    test_content = "CONTENT"
    test_thread_id = "THREAD_ID"
    test_message = {
        "@type": test_message_type,
        "@id": test_message_id,
        "~thread": {"thid": test_thread_id},
        "~transport": {"return_route": "all"},
        "content": test_content,
    }
    test_seed = "testseed000000000000000000000001"
    test_routing_seed = "testseed000000000000000000000002"

    def setUp(self):
        self.wallet = BasicWallet()
        self.context = InjectionContext()
        self.context.injector.bind_instance(BaseWallet, self.wallet)

    async def test_errors(self):
        serializer = PackWireFormat()
        bad_values = [None, "", "1", "[]", "{..."]

        for message_json in bad_values:
            with self.assertRaises(MessageParseError):
                message_dict, delivery = await serializer.parse_message(
                    self.context, message_json
                )

        x_message = {
            "@id": TestPackWireFormat.test_message_id,
            "~thread": {"thid": TestPackWireFormat.test_thread_id},
            "~transport": {"return_route": "all"},
            "content": "{}",
        }

        serializer.task_queue = None
        with async_mock.patch.object(
            serializer, "unpack", async_mock.CoroutineMock()
        ) as mock_unpack:
            mock_unpack.return_value = "{missing-brace"
            with self.assertRaises(MessageParseError) as context:
                await serializer.parse_message(self.context, json.dumps(x_message))
        assert "Message JSON parsing failed" in str(context.exception)

        serializer = PackWireFormat()
        serializer.task_queue = None
        with async_mock.patch.object(
            serializer, "unpack", async_mock.CoroutineMock()
        ) as mock_unpack:
            mock_unpack.return_value = json.dumps([1, 2, 3])
            with self.assertRaises(MessageParseError) as context:
                await serializer.parse_message(self.context, json.dumps(x_message))
        assert "Message JSON result is not an object" in str(context.exception)

        with self.assertRaises(MessageParseError):
            await serializer.unpack(InjectionContext(), "...", None)

    async def test_pack_x(self):
        serializer = PackWireFormat()

        with self.assertRaises(MessageEncodeError):
            await serializer.pack(self.context, None, None, None, None)

        with self.assertRaises(MessageEncodeError):
            await serializer.pack(InjectionContext(), None, ["key"], None, ["key"])

        mock_wallet = async_mock.MagicMock(
            pack_message=async_mock.CoroutineMock(side_effect=WalletError())
        )
        context = InjectionContext(enforce_typing=False)
        context.injector.bind_instance(BaseWallet, mock_wallet)
        with self.assertRaises(MessageEncodeError):
            await serializer.pack(context, None, ["key"], None, ["key"])

        context.injector.clear_binding(BaseWallet)
        mock_wallet = async_mock.MagicMock(
            pack_message=async_mock.CoroutineMock(
                side_effect=[json.dumps("message").encode("utf-8"), WalletError()]
            )
        )
        context.injector.bind_instance(BaseWallet, mock_wallet)
        with async_mock.patch.object(
            test_module, "Forward", async_mock.MagicMock()
        ) as mock_forward:
            mock_forward.return_value = async_mock.MagicMock(
                to_json=async_mock.MagicMock()
            )
            with self.assertRaises(MessageEncodeError):
                await serializer.pack(context, None, ["key"], ["key"], ["key"])

    async def test_unpacked(self):
        serializer = PackWireFormat()
        message_json = json.dumps(self.test_message)
        message_dict, delivery = await serializer.parse_message(
            self.context, message_json
        )
        assert message_dict == self.test_message
        assert message_dict["@type"] == self.test_message_type
        assert delivery.thread_id == self.test_thread_id
        assert delivery.direct_response_mode == "all"

    async def test_fallback(self):
        serializer = PackWireFormat()

        message = self.test_message.copy()
        message.pop("@type")
        message_json = json.dumps(message)

        message_dict, delivery = await serializer.parse_message(
            self.context, message_json
        )
        assert delivery.raw_message == message_json
        assert message_dict == message

    async def test_encode_decode(self):
        local_did = await self.wallet.create_local_did(self.test_seed)
        serializer = PackWireFormat()
        recipient_keys = (local_did.verkey,)
        routing_keys = ()
        sender_key = local_did.verkey
        message_json = json.dumps(self.test_message)

        packed_json = await serializer.encode_message(
            self.context, message_json, recipient_keys, routing_keys, sender_key
        )
        packed = json.loads(packed_json)

        assert isinstance(packed, dict) and "protected" in packed

        message_dict, delivery = await serializer.parse_message(
            self.context, packed_json
        )
        assert message_dict == self.test_message
        assert message_dict["@type"] == self.test_message_type
        assert delivery.thread_id == self.test_thread_id
        assert delivery.direct_response_mode == "all"

        plain_json = json.dumps("plain")
        assert (
            await serializer.encode_message(self.context, plain_json, None, None, None)
            == plain_json
        )

    async def test_forward(self):
        local_did = await self.wallet.create_local_did(self.test_seed)
        router_did = await self.wallet.create_local_did(self.test_routing_seed)
        serializer = PackWireFormat()
        recipient_keys = (local_did.verkey,)
        routing_keys = (router_did.verkey,)
        sender_key = local_did.verkey
        message_json = json.dumps(self.test_message)

        packed_json = await serializer.encode_message(
            self.context, message_json, recipient_keys, routing_keys, sender_key
        )
        packed = json.loads(packed_json)

        assert isinstance(packed, dict) and "protected" in packed

        message_dict, delivery = await serializer.parse_message(
            self.context, packed_json
        )
        assert message_dict["@type"] == FORWARD
        assert delivery.recipient_verkey == router_did.verkey
        assert delivery.sender_verkey is None
