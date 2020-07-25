# coding: utf-8
import pprint
import six
from enum import Enum
from . import TransactionAwareEntity


class ChargeFlowLevelPaymentLink(TransactionAwareEntity):

    swagger_types = {
    
        'charge_flow_level': 'ChargeFlowLevel',
        'payment_link': 'str',
    }

    attribute_map = {
        'charge_flow_level': 'chargeFlowLevel','payment_link': 'paymentLink',
    }

    
    _charge_flow_level = None
    _payment_link = None

    def __init__(self, **kwargs):
        self.discriminator = None
        
        self.charge_flow_level = kwargs.get('charge_flow_level', None)
        self.payment_link = kwargs.get('payment_link', None)
        super().__init__(**kwargs)
        self.swagger_types.update(super().swagger_types)
        self.attribute_map.update(super().attribute_map)

    
    @property
    def charge_flow_level(self):
        """Gets the charge_flow_level of this ChargeFlowLevelPaymentLink.

            

        :return: The charge_flow_level of this ChargeFlowLevelPaymentLink.
        :rtype: ChargeFlowLevel
        """
        return self._charge_flow_level

    @charge_flow_level.setter
    def charge_flow_level(self, charge_flow_level):
        """Sets the charge_flow_level of this ChargeFlowLevelPaymentLink.

            

        :param charge_flow_level: The charge_flow_level of this ChargeFlowLevelPaymentLink.
        :type: ChargeFlowLevel
        """

        self._charge_flow_level = charge_flow_level
    
    @property
    def payment_link(self):
        """Gets the payment_link of this ChargeFlowLevelPaymentLink.

            

        :return: The payment_link of this ChargeFlowLevelPaymentLink.
        :rtype: str
        """
        return self._payment_link

    @payment_link.setter
    def payment_link(self, payment_link):
        """Sets the payment_link of this ChargeFlowLevelPaymentLink.

            

        :param payment_link: The payment_link of this ChargeFlowLevelPaymentLink.
        :type: str
        """

        self._payment_link = payment_link
    

    def to_dict(self):
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            elif isinstance(value, Enum):
                result[attr] = value.value
            else:
                result[attr] = value
        if issubclass(ChargeFlowLevelPaymentLink, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, ChargeFlowLevelPaymentLink):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
