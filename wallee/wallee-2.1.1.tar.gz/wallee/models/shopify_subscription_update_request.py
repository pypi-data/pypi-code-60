# coding: utf-8
import pprint
import six
from enum import Enum



class ShopifySubscriptionUpdateRequest:

    swagger_types = {
    
        'billing_day_of_month': 'int',
        'billing_interval_amount': 'int',
        'billing_interval_unit': 'ShopifySubscriptionBillingIntervalUnit',
        'billing_weekday': 'ShopifySubscriptionWeekday',
        'id': 'int',
        'items': 'list[ShopifySubscriptionEditModelItem]',
        'maximal_billing_cycles': 'int',
        'maximal_suspendable_cycles': 'int',
        'minimal_billing_cycles': 'int',
        'store_order_confirmation_email_enabled': 'bool',
        'subscriber_suspension_allowed': 'bool',
        'termination_billing_cycles': 'int',
    }

    attribute_map = {
        'billing_day_of_month': 'billingDayOfMonth','billing_interval_amount': 'billingIntervalAmount','billing_interval_unit': 'billingIntervalUnit','billing_weekday': 'billingWeekday','id': 'id','items': 'items','maximal_billing_cycles': 'maximalBillingCycles','maximal_suspendable_cycles': 'maximalSuspendableCycles','minimal_billing_cycles': 'minimalBillingCycles','store_order_confirmation_email_enabled': 'storeOrderConfirmationEmailEnabled','subscriber_suspension_allowed': 'subscriberSuspensionAllowed','termination_billing_cycles': 'terminationBillingCycles',
    }

    
    _billing_day_of_month = None
    _billing_interval_amount = None
    _billing_interval_unit = None
    _billing_weekday = None
    _id = None
    _items = None
    _maximal_billing_cycles = None
    _maximal_suspendable_cycles = None
    _minimal_billing_cycles = None
    _store_order_confirmation_email_enabled = None
    _subscriber_suspension_allowed = None
    _termination_billing_cycles = None

    def __init__(self, **kwargs):
        self.discriminator = None
        
        self.billing_day_of_month = kwargs.get('billing_day_of_month', None)
        self.billing_interval_amount = kwargs.get('billing_interval_amount', None)
        self.billing_interval_unit = kwargs.get('billing_interval_unit', None)
        self.billing_weekday = kwargs.get('billing_weekday', None)
        self.id = kwargs.get('id', None)
        self.items = kwargs.get('items', None)
        self.maximal_billing_cycles = kwargs.get('maximal_billing_cycles', None)
        self.maximal_suspendable_cycles = kwargs.get('maximal_suspendable_cycles', None)
        self.minimal_billing_cycles = kwargs.get('minimal_billing_cycles', None)
        self.store_order_confirmation_email_enabled = kwargs.get('store_order_confirmation_email_enabled', None)
        self.subscriber_suspension_allowed = kwargs.get('subscriber_suspension_allowed', None)
        self.termination_billing_cycles = kwargs.get('termination_billing_cycles', None)
        

    
    @property
    def billing_day_of_month(self):
        """Gets the billing_day_of_month of this ShopifySubscriptionUpdateRequest.

            Define the day of the month on which the recurring orders should be created.

        :return: The billing_day_of_month of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._billing_day_of_month

    @billing_day_of_month.setter
    def billing_day_of_month(self, billing_day_of_month):
        """Sets the billing_day_of_month of this ShopifySubscriptionUpdateRequest.

            Define the day of the month on which the recurring orders should be created.

        :param billing_day_of_month: The billing_day_of_month of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._billing_day_of_month = billing_day_of_month
    
    @property
    def billing_interval_amount(self):
        """Gets the billing_interval_amount of this ShopifySubscriptionUpdateRequest.

            

        :return: The billing_interval_amount of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._billing_interval_amount

    @billing_interval_amount.setter
    def billing_interval_amount(self, billing_interval_amount):
        """Sets the billing_interval_amount of this ShopifySubscriptionUpdateRequest.

            

        :param billing_interval_amount: The billing_interval_amount of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._billing_interval_amount = billing_interval_amount
    
    @property
    def billing_interval_unit(self):
        """Gets the billing_interval_unit of this ShopifySubscriptionUpdateRequest.

            Define how frequently recurring orders should be created.

        :return: The billing_interval_unit of this ShopifySubscriptionUpdateRequest.
        :rtype: ShopifySubscriptionBillingIntervalUnit
        """
        return self._billing_interval_unit

    @billing_interval_unit.setter
    def billing_interval_unit(self, billing_interval_unit):
        """Sets the billing_interval_unit of this ShopifySubscriptionUpdateRequest.

            Define how frequently recurring orders should be created.

        :param billing_interval_unit: The billing_interval_unit of this ShopifySubscriptionUpdateRequest.
        :type: ShopifySubscriptionBillingIntervalUnit
        """

        self._billing_interval_unit = billing_interval_unit
    
    @property
    def billing_weekday(self):
        """Gets the billing_weekday of this ShopifySubscriptionUpdateRequest.

            Define the weekday on which the recurring orders should be created.

        :return: The billing_weekday of this ShopifySubscriptionUpdateRequest.
        :rtype: ShopifySubscriptionWeekday
        """
        return self._billing_weekday

    @billing_weekday.setter
    def billing_weekday(self, billing_weekday):
        """Sets the billing_weekday of this ShopifySubscriptionUpdateRequest.

            Define the weekday on which the recurring orders should be created.

        :param billing_weekday: The billing_weekday of this ShopifySubscriptionUpdateRequest.
        :type: ShopifySubscriptionWeekday
        """

        self._billing_weekday = billing_weekday
    
    @property
    def id(self):
        """Gets the id of this ShopifySubscriptionUpdateRequest.

            

        :return: The id of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ShopifySubscriptionUpdateRequest.

            

        :param id: The id of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._id = id
    
    @property
    def items(self):
        """Gets the items of this ShopifySubscriptionUpdateRequest.

            

        :return: The items of this ShopifySubscriptionUpdateRequest.
        :rtype: list[ShopifySubscriptionEditModelItem]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this ShopifySubscriptionUpdateRequest.

            

        :param items: The items of this ShopifySubscriptionUpdateRequest.
        :type: list[ShopifySubscriptionEditModelItem]
        """

        self._items = items
    
    @property
    def maximal_billing_cycles(self):
        """Gets the maximal_billing_cycles of this ShopifySubscriptionUpdateRequest.

            Define the maximum number of orders the subscription will run for.

        :return: The maximal_billing_cycles of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._maximal_billing_cycles

    @maximal_billing_cycles.setter
    def maximal_billing_cycles(self, maximal_billing_cycles):
        """Sets the maximal_billing_cycles of this ShopifySubscriptionUpdateRequest.

            Define the maximum number of orders the subscription will run for.

        :param maximal_billing_cycles: The maximal_billing_cycles of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._maximal_billing_cycles = maximal_billing_cycles
    
    @property
    def maximal_suspendable_cycles(self):
        """Gets the maximal_suspendable_cycles of this ShopifySubscriptionUpdateRequest.

            Define the maximum number of orders the subscription can be suspended for at a time.

        :return: The maximal_suspendable_cycles of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._maximal_suspendable_cycles

    @maximal_suspendable_cycles.setter
    def maximal_suspendable_cycles(self, maximal_suspendable_cycles):
        """Sets the maximal_suspendable_cycles of this ShopifySubscriptionUpdateRequest.

            Define the maximum number of orders the subscription can be suspended for at a time.

        :param maximal_suspendable_cycles: The maximal_suspendable_cycles of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._maximal_suspendable_cycles = maximal_suspendable_cycles
    
    @property
    def minimal_billing_cycles(self):
        """Gets the minimal_billing_cycles of this ShopifySubscriptionUpdateRequest.

            Define the minimal number of orders the subscription will run for.

        :return: The minimal_billing_cycles of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._minimal_billing_cycles

    @minimal_billing_cycles.setter
    def minimal_billing_cycles(self, minimal_billing_cycles):
        """Sets the minimal_billing_cycles of this ShopifySubscriptionUpdateRequest.

            Define the minimal number of orders the subscription will run for.

        :param minimal_billing_cycles: The minimal_billing_cycles of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._minimal_billing_cycles = minimal_billing_cycles
    
    @property
    def store_order_confirmation_email_enabled(self):
        """Gets the store_order_confirmation_email_enabled of this ShopifySubscriptionUpdateRequest.

            

        :return: The store_order_confirmation_email_enabled of this ShopifySubscriptionUpdateRequest.
        :rtype: bool
        """
        return self._store_order_confirmation_email_enabled

    @store_order_confirmation_email_enabled.setter
    def store_order_confirmation_email_enabled(self, store_order_confirmation_email_enabled):
        """Sets the store_order_confirmation_email_enabled of this ShopifySubscriptionUpdateRequest.

            

        :param store_order_confirmation_email_enabled: The store_order_confirmation_email_enabled of this ShopifySubscriptionUpdateRequest.
        :type: bool
        """

        self._store_order_confirmation_email_enabled = store_order_confirmation_email_enabled
    
    @property
    def subscriber_suspension_allowed(self):
        """Gets the subscriber_suspension_allowed of this ShopifySubscriptionUpdateRequest.

            

        :return: The subscriber_suspension_allowed of this ShopifySubscriptionUpdateRequest.
        :rtype: bool
        """
        return self._subscriber_suspension_allowed

    @subscriber_suspension_allowed.setter
    def subscriber_suspension_allowed(self, subscriber_suspension_allowed):
        """Sets the subscriber_suspension_allowed of this ShopifySubscriptionUpdateRequest.

            

        :param subscriber_suspension_allowed: The subscriber_suspension_allowed of this ShopifySubscriptionUpdateRequest.
        :type: bool
        """

        self._subscriber_suspension_allowed = subscriber_suspension_allowed
    
    @property
    def termination_billing_cycles(self):
        """Gets the termination_billing_cycles of this ShopifySubscriptionUpdateRequest.

            Define the number of orders the subscription will keep running for after its termination has been requested.

        :return: The termination_billing_cycles of this ShopifySubscriptionUpdateRequest.
        :rtype: int
        """
        return self._termination_billing_cycles

    @termination_billing_cycles.setter
    def termination_billing_cycles(self, termination_billing_cycles):
        """Sets the termination_billing_cycles of this ShopifySubscriptionUpdateRequest.

            Define the number of orders the subscription will keep running for after its termination has been requested.

        :param termination_billing_cycles: The termination_billing_cycles of this ShopifySubscriptionUpdateRequest.
        :type: int
        """

        self._termination_billing_cycles = termination_billing_cycles
    

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
        if issubclass(ShopifySubscriptionUpdateRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, ShopifySubscriptionUpdateRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
