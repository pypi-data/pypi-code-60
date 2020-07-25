#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""Algorithms that generate price tables.

"""
import logging

from dataclasses import dataclass
from datetime import timedelta
from enum import IntFlag
from itertools import groupby, product
from typing import (
    Any,
    Callable,
    Container,
    Dict as OrderedDict,
    Iterable,
    Iterator,
    List,
    Sequence,
    Tuple,
)

from xotl.tools.fp.tools import compose, fst
from xotl.tools.fp.iterators import kleisli_compose_foldl

from xotless.types import TEq as ProcedureName
from xotless.domains import EquivalenceSet

from .i18n import _

from .types import (
    AVM,
    ATTRIBUTE_OWNER,
    AttributeLocator,
    Domain,
    Procedure,
    TypedAttribute,
    Result,
)
from .avm import MergedAVM
from .structs import Commodity, Demand, EMPTY_ENV

logger = logging.getLogger(__name__)


class ATTR_FORMAT(IntFlag):
    BY_VALUE = 0b00
    BY_NAME = 0b01


@dataclass
class AttrFormatConfiguration:
    # See TableFormat below
    attrs: Sequence[AttributeLocator] = ()
    how: ATTR_FORMAT = ATTR_FORMAT.BY_NAME
    visible: bool = True

    @classmethod
    def from_locators(cls, *locators: AttributeLocator) -> "AttrFormatConfiguration":
        return cls(tuple(locators))


@dataclass
class TableFormat:
    """A price table format.

    This format is used to configure how to generate price tables.

    For each combinations of values in the AVMs of the attributes configured
    by `tables_conf`, we must issue a new Table.

    """

    tables_conf: AttrFormatConfiguration
    columns_conf: Sequence[AttrFormatConfiguration]

    def needs_price_column(self, procedure: Procedure):
        """Return True if a procedure needs a standalone Price column.

        """
        avm = procedure.avm.keys()
        return not any(
            column_attr in avm
            for column in self.columns_conf
            if column.how == ATTR_FORMAT.BY_VALUE
            for column_attr in column.attrs
        )

    @classmethod
    def from_columns(cls, *columns: AttributeLocator) -> "TableFormat":
        """Create a configuration of a single table with ordered columns.

        """
        return cls(
            AttrFormatConfiguration(),
            tuple(AttrFormatConfiguration.from_locators(column) for column in columns),
        )


@dataclass(frozen=True)
class DemandData:
    attrs: Tuple[Tuple[AttributeLocator, Domain], ...]
    demand: Demand

    @classmethod
    def new(cls, now=None):
        return cls((), Demand.from_commodities((Commodity(None, None),), date=now))

    @property
    def attr_locators(self) -> Tuple[AttributeLocator, ...]:
        return tuple(locator for locator, _domain in self.attrs)

    @property
    def attr_names(self) -> Tuple[TypedAttribute, ...]:
        return tuple(locator.attr for locator, _domain in self.attrs)

    @property
    def attr_samples(self) -> Tuple[Any, ...]:
        return tuple(domain.sample for _loc, domain in self.attrs)

    def _extract_basic_values(self, attrs: Sequence[AttributeLocator]):
        """Extract the values of the `attrs` in the demand data.

        The order in `self.attrs` MUST BE COMPATIBLE with the order of the
        argument passed to parameter `attrs`.  This is for any two attributes
        A1, A2 appearing in both sequences, A1 is before A2 in `attrs` if and
        only if A1 is before A2 in `self.attrs`.

        Return a generator of the basic values.  The basic values are domains,
        or values of single-item domains.  An EquivalenceSet with a single
        value is flattened to its value.  Other instances yield the entire
        domain.

        """
        # NOTE: The expectation of COMPATIBLE order matches the way we
        # generate demands.  It has to do being the expected order of the
        # table_format.
        #
        # We order the attributes according to _get_table_avm_index and each
        # demand is generate following this order; so, when extracting the
        # basic values, following table index will be a compatible order.
        attrs = list(attrs)
        ours = list(self.attrs)
        while ours and attrs:
            locator, data = ours.pop(0)
            if locator == attrs[0]:
                attrs.pop(0)
                if isinstance(data, EquivalenceSet) and len(data.values) == 1:
                    yield data.sample
                else:
                    yield data

    def getattr(self, locator: AttributeLocator):
        if locator.owner == ATTRIBUTE_OWNER.DEMAND:
            return getattr(self.demand, locator.attr.name)
        elif locator.owner == ATTRIBUTE_OWNER.REQUEST:
            return getattr(self.demand.requests[0], locator.attr.name)
        else:
            assert locator.owner == ATTRIBUTE_OWNER.COMMODITY
            return getattr(self.demand.requests[0].commodity, locator.attr.name)


@dataclass(frozen=True)
class Table:
    attrs: Tuple[Tuple[AttributeLocator, Any], ...]
    columns_headers: Tuple[Any, ...]
    rows: Tuple[Any, ...]


NULL_FORMAT = TableFormat(AttrFormatConfiguration(), ())


def generate_tables(
    procedures: Sequence[Tuple[ProcedureName, Procedure]],
    table_format: TableFormat = NULL_FORMAT,
    single_table: bool = False,
    now=None,
    pricecls: Callable[[Result], Any] = None,
) -> Iterator[Table]:
    tables = _generate_tables(
        procedures, table_format, single_table, now, pricecls=pricecls
    )
    if single_table:
        alltables = list(tables)
        if alltables:
            yield Table(
                alltables[0].attrs,
                alltables[0].columns_headers,
                (row for table in alltables for row in table.rows),  # type: ignore
            )
    else:
        yield from tables


def estimate_table_size(procedures: Iterable[Procedure]) -> int:
    """Return an estimate of the number of demands needed to generate the price
    tables.

    """
    result = 0
    for procedure in procedures:
        size = 1
        for domains in procedure.avm.values():
            size *= len(domains)
        result += size
    return result


def _generate_tables(
    procedures: Sequence[Tuple[ProcedureName, Procedure]],
    table_format: TableFormat = NULL_FORMAT,
    single_table: bool = False,
    now=None,
    pricecls: Callable[[Result], Any] = None,
) -> Iterator[Table]:
    """Return an iterator of price tables.

    You may generate price tables for many `procedures`.  Each procedure is
    *identified* by a name of any type you like as long as different
    procedures have different names.

    Use `single_table` to control whether to create a table per
    procedure (automatically prepending the procedure name to the
    `table_format`'s `table_conf`.); or as the first column of the each
    table's rows.

    """

    avm = MergedAVM(*(p.avm for _name, p in procedures))
    table_generators = [
        _get_demand_data_generator(attr, domains)
        for attr, domains in avm.items()
        if table_format.tables_conf and attr in table_format.tables_conf.attrs
    ]
    initial_demand_data = DemandData.new(now=now)
    for name, procedure in procedures:
        for demand_seed in kleisli_compose_foldl(*table_generators)(initial_demand_data):
            rows = _demand_datas(
                demand_seed,
                avm,
                procedure,
                name,
                include_name=single_table,
                table_format=table_format,
                pricecls=pricecls,
            )
            headers = _get_headers(demand_seed, avm, procedure, table_format=table_format)
            yield Table(demand_seed.attrs, headers, rows)


def _get_columns(
    table: DemandData, avm: AVM, table_format: TableFormat = NULL_FORMAT
) -> OrderedDict[Tuple[AttributeLocator, ...], ATTR_FORMAT]:
    table_attrs = {attr for attr, _ in table.attrs if attr in avm}
    elegible_attrs = [attr for attr in avm if attr not in table_attrs]
    columns = {}
    for conf in table_format.columns_conf:
        attrs = tuple(attr for attr in conf.attrs if attr in elegible_attrs)
        if attrs:
            columns[attrs] = conf.how
    for attr in elegible_attrs:
        if not any(attr in key for key in columns):
            columns[(attr,)] = ATTR_FORMAT.BY_NAME
    return columns


def _get_headers(
    table: DemandData,
    avm: AVM,
    procedure: Procedure,
    table_format: TableFormat = NULL_FORMAT,
    include_name: bool = False,
):
    if include_name:
        yield _("Name")
    columns = _get_columns(table, avm, table_format)
    for locators, how in columns.items():
        if how == ATTR_FORMAT.BY_NAME:
            attrs = tuple(locator.attr for locator in locators)
            if len(attrs) == 1:
                yield attrs[0]
            else:
                yield attrs
        else:
            values = [avm[locator] for locator in locators]
            yield from product(*values)
    if table_format.needs_price_column(procedure):
        yield _("Price")


def _demand_datas(
    table: DemandData,
    avm: AVM,
    procedure: Procedure,
    name: ProcedureName,
    include_name: bool = False,
    table_format: TableFormat = NULL_FORMAT,
    pricecls: Callable[[Result], Any] = None,
):
    if pricecls is None:
        Price = lambda r: r
    else:
        Price = pricecls
    key = _get_table_group_key(
        procedure.avm,
        table_format,
        without_attrs={attr for attr, _ in table.attrs},
        with_value_columns=False,
    )
    table_attrs = {attr for attr, _ in table.attrs}
    columns = _get_columns(table, avm, table_format)
    demand_datas = generate_demand_datas(
        procedure.avm,
        without_attrs=table_attrs,
        initial_demand_data=table,
        order_by=_get_table_avm_index(procedure.avm, table_format),
    )
    for _key, datas in groupby(demand_datas, key=key):
        row: List[Any] = [name] if include_name else []
        price_computed = False
        # In a single row we can have several demand data when the
        # table has a BY_VALUE column configuration.  For instance:
        #
        #          |      Regime    |
        #          +--------+-------|
        #     Attr |  MAP   |   CP  |  Attr 2
        #     -----+--------+-------+---------
        #     xxx  |  $ 1   |  $ 2  |  yyyy
        #
        # Also we know that there must not be more than one BY_VALUE group of
        # attributes.  So we start with the first demand data, and at least
        # one configuration is BY_VALUE we put as many columns as items in
        # data.
        #
        # The alternative is that no column is BY_VALUE and we must
        # append a last column Price.
        data = next(datas)  # type: DemandData
        for attrs, how in columns.items():
            if how == ATTR_FORMAT.BY_NAME:
                cell = tuple(
                    data._extract_basic_values([attr])
                    if attr in procedure.avm
                    else MISSING_CELL
                    for attr in attrs
                )
                if len(cell) == 1:
                    row.append(cell[0])
                else:
                    row.append(cell)
            else:
                assert not price_computed
                price_computed = True
                row.append(Price(procedure(data.demand, EMPTY_ENV).result))
                for data in datas:
                    row.append(Price(procedure(data.demand, EMPTY_ENV).result))
        if not price_computed:
            row.append(Price(procedure(data.demand, EMPTY_ENV).result))
        yield row


def _get_table_avm_index(
    avm: AVM,
    table_format: TableFormat,
    without_attrs: Container[AttributeLocator] = None,
    with_value_columns=True,
) -> Sequence[AttributeLocator]:
    """Return an ordered sequence of the attributes according to the table format.

    Ignore attributes in `without_attrs`.

    If `with_value_columns` is True, include the ATTR_FORMAT.BY_VALUE as the
    last attributes in the index.

    The order is staged like this:

    - First came the attributes that make up whole tables.

    - Then all the attributes in the format's column configuration which are
      to be displayed by NAME (ignoring those not present in the AVM).

    - Next all attributes in the AVM which are not already ordered and are not
      in the columns configuration by VALUE.

    - Finally (if `with_value_columns` is True) the attributes to included by
      VALUE.

    """
    if not without_attrs:
        without_attrs = set([])
    index = tuple(
        attr
        for attr in table_format.tables_conf.attrs
        if attr in avm and attr not in without_attrs
    )
    index += tuple(
        attr
        for conf in table_format.columns_conf
        if conf.how == ATTR_FORMAT.BY_NAME
        for attr in conf.attrs
        if attr in avm and attr not in without_attrs
    )
    last_columns = tuple(
        attr
        for conf in table_format.columns_conf
        if conf.how == ATTR_FORMAT.BY_VALUE
        for attr in conf.attrs
        if attr in avm and attr not in without_attrs
    )
    seen_already = index + last_columns
    index += tuple(
        attr for attr in avm if attr not in without_attrs and attr not in seen_already
    )
    if with_value_columns:
        index += last_columns
    return index


def _get_table_group_key(
    avm: AVM,
    table_format: TableFormat,
    without_attrs: Container[AttributeLocator] = None,
    with_value_columns: bool = False,
):
    index = _get_table_avm_index(avm, table_format, without_attrs, with_value_columns)
    return lambda x: tuple(x.getattr(attr) for attr in index)


def generate_demand_datas(
    avm: AVM,
    order_by: Sequence[AttributeLocator],
    now=None,
    without_attrs: Container[AttributeLocator] = None,
    initial_demand_data: DemandData = None,
    table_format: TableFormat = NULL_FORMAT,
) -> Iterator[DemandData]:
    sort_key = compose(lambda attr: order_by.index(attr), fst)
    generators = [
        _get_demand_data_generator(attr, domains)
        for attr, domains in sorted(avm.items(), key=sort_key)
        if not without_attrs or attr not in without_attrs
    ]
    if initial_demand_data is None:
        demand_data = DemandData(
            (),
            Demand.from_commodities((Commodity(None, None),), date=now),  # type: ignore
        )
    else:
        demand_data = initial_demand_data
    return kleisli_compose_foldl(*generators)(demand_data)


def _get_demand_data_generator(
    attr: AttributeLocator, domains: Sequence[Any]
) -> Callable[[DemandData], Iterable[DemandData]]:
    def result(demand_data: DemandData) -> Iterable[DemandData]:
        demand = demand_data.demand

        def _new_attrs(domain: Domain) -> Tuple[Tuple[AttributeLocator, Any], ...]:
            return demand_data.attrs + ((attr, domain),)

        for domain in domains:
            # It's possible that we get empty domains here because the AVM of
            # a trivially empty predicate (eg. QuantityPredicate(0, 0))
            # contains the empty domain.
            #
            # In such a case, we cannot actually get any sample from the
            # domain (it's empty); and then we cannot produce a valid demand.
            if domain:
                yield DemandData(_new_attrs(domain), attr.update(demand, domain.sample))

    return result


HOUR = timedelta(hours=1)


class _MissingCell:
    def __repr__(self):
        return "NA"

    def __str__(self):
        return "-"


MISSING_CELL = _MissingCell()
