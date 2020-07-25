#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
import unittest

from datetime import datetime
from types import GeneratorType
from typing import List, Sequence, Tuple

from xotless.domains import IntervalSet, EquivalenceSet as EqSet, Range

from hypothesis.stateful import rule, run_state_machine_as_test

from travertine.types import AttributeLocator, Procedure, TypedAttribute, SimpleType
from travertine.tables import (
    generate_demand_datas,
    generate_tables,
    _get_table_avm_index,
    Table,
    NULL_FORMAT,
    TableFormat,
    ATTR_FORMAT,
    AttrFormatConfiguration,
    ProcedureName,
    DemandData,
    MISSING_CELL,
)
from travertine.predicates import (
    QuantityPredicate,
    ValidityPredicate,
    ExecutionPredicate,
    MatchesAttributePredicate,
    AttributeInRangePredicate,
    Otherwise,
)
from travertine.procedures import ConstantProcedure, BranchingProcedure, FormulaProcedure

from travertine.testing.strategies.programs import ProcedureMachine
from travertine.testing.strategies.tables import table_formats

from .tools import KaboomProcedure


quantity_locator = AttributeLocator.of_request("quantity", float)
date_locator = AttributeLocator.of_demand("date", datetime)
occupation_locator = AttributeLocator.of_commodity("occupation", str)
occupation_attr = occupation_locator.attr
startdate_locator = AttributeLocator.of_commodity(
    "start_date", datetime, "Execution date"
)
TABLE_FORMAT = TableFormat(
    tables_conf=AttrFormatConfiguration(
        attrs=[quantity_locator], how=ATTR_FORMAT.BY_VALUE
    ),
    columns_conf=[
        AttrFormatConfiguration(
            attrs=[occupation_locator, date_locator], how=ATTR_FORMAT.BY_VALUE
        ),
        AttrFormatConfiguration(attrs=[startdate_locator], how=ATTR_FORMAT.BY_NAME),
    ],
)
TABLE_FORMAT_START_DATE_FIRST = TableFormat(
    tables_conf=AttrFormatConfiguration(
        attrs=[quantity_locator], how=ATTR_FORMAT.BY_VALUE
    ),
    columns_conf=[
        AttrFormatConfiguration(attrs=[startdate_locator], how=ATTR_FORMAT.BY_NAME),
        AttrFormatConfiguration(
            attrs=[occupation_locator, date_locator], how=ATTR_FORMAT.BY_VALUE
        ),
    ],
)


ATTR_PAX = TypedAttribute("pax", SimpleType.from_python_type(int))
ATTR_PAX_LOCATOR = AttributeLocator.of_commodity(ATTR_PAX)


class PriceTableMachine(ProcedureMachine):
    @rule(proc=ProcedureMachine.basic_procedures)
    def check_basic_procs_return_a_single_row_with_no_attrs(self, proc):
        rows = list(
            generate_demand_datas(proc.avm, _get_table_avm_index(proc.avm, NULL_FORMAT))
        )
        assert len(rows) == 1
        assert not rows[0].attrs

    @rule(proc=ProcedureMachine.validity_branching_procedures)
    def check_validity_branchings_generate_date_attr(self, proc):
        rows = list(
            generate_demand_datas(proc.avm, _get_table_avm_index(proc.avm, NULL_FORMAT))
        )
        for row in rows:
            assert (
                AttributeLocator.of_demand("date", datetime) in row.attr_locators
            ), f"Demand's date is not in {row.attrs_locators}"

    @rule(proc=ProcedureMachine.execution_branching_procedures)
    def check_exec_branchings_generate_start_date_attr(self, proc):
        rows = list(
            generate_demand_datas(proc.avm, _get_table_avm_index(proc.avm, NULL_FORMAT))
        )
        for row in rows:
            assert (
                AttributeLocator.of_commodity("start_date", datetime) in row.attr_locators
            ), f"Commodity's start_date is not in {row.attrs_locators}"

    @rule(proc=ProcedureMachine.procedures)
    def check_consistency_of_attrs(self, proc):
        datasets: List[DemandData] = list(
            generate_demand_datas(proc.avm, _get_table_avm_index(proc.avm, NULL_FORMAT))
        )
        if datasets:
            locators = datasets[0].attr_locators
            assert all(ds.attr_locators == locators for ds in datasets)

    @rule(proc=ProcedureMachine.procedures, fmt=table_formats)
    def check_we_can_compute_price_tables_for_any_format(self, proc, fmt):
        for table in generate_tables((("proc", proc),)):
            for _row in table.rows:
                pass

    @rule(proc=ProcedureMachine.procedures, fmt=table_formats)
    def check_table_attributes_in_the_index_are_in_the_avm(self, proc, fmt):
        avm = proc.avm
        index = _get_table_avm_index(avm, fmt)
        for attr in index:
            assert attr in avm, f"{attr} not in {avm}"


class PriceTableCaseIssue781Mixin:
    def _test_regression_issue781_table_generation_using_format(self, table_format):
        first_step = BranchingProcedure(
            (QuantityPredicate(1, 4), ConstantProcedure(1)),
            (QuantityPredicate(4, 8), ConstantProcedure(2)),
            (QuantityPredicate(8, 14), ConstantProcedure(3)),
        )
        second_step = BranchingProcedure(
            # Prices from 2019-01-01 up to 2019-04-30
            (
                ValidityPredicate(datetime(2019, 1, 1), datetime(2019, 5, 1)),
                ConstantProcedure(42),
            ),
            # Prices from 2018-12-01 up to 2019-05-31
            (
                ValidityPredicate(datetime(2018, 12, 1), datetime(2019, 6, 1)),
                ConstantProcedure(69),
            ),
            (ValidityPredicate(datetime(2019, 2, 1), datetime(2019, 7, 1)), first_step),
            # Other dates.
            (Otherwise(), ConstantProcedure(51)),
        )
        tables = list(
            generate_full_tables(
                (("second_step", second_step),), table_format=table_format
            )
        )
        table = tables[0]
        rows = table.rows
        headers = table.columns_headers
        self.assertEqual(
            headers,
            (
                (
                    Range.new_open_right(
                        datetime(2019, 1, 1, 0, 0), datetime(2019, 5, 1, 0, 0)
                    ).lift(),
                ),
                (
                    IntervalSet(
                        (
                            Range.new_open_right(
                                datetime(2018, 12, 1, 0, 0), datetime(2019, 1, 1, 0, 0)
                            ),
                            Range.new_open_right(
                                datetime(2019, 5, 1, 0, 0), datetime(2019, 6, 1, 0, 0)
                            ),
                        )
                    ),
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 6, 1, 0, 0), datetime(2019, 7, 1, 0, 0)
                    ).lift(),
                ),
            ),
        )
        self.assertEqual(rows, [(42, 69, 1)])


class PriceTableCase(unittest.TestCase, PriceTableCaseIssue781Mixin):
    maxDiff = None

    def test_price_tables_with_hypothesis_generated_programs(self):
        run_state_machine_as_test(PriceTableMachine)

    def test_mixing_eqset_with_interval_sets(self):
        # Setup a program with two branching procedures.  The first one
        # (`procedure`) has a single branch with a predicate '1 <= pax < 3'.
        # This branch goes to a second branching procedure (`second_proc`)
        # with 4 branches each with with a condition of type 'pax == $val'.
        second_proc = BranchingProcedure(
            (MatchesAttributePredicate(ATTR_PAX, 1), ConstantProcedure(69 + 1)),
            (MatchesAttributePredicate(ATTR_PAX, 2), ConstantProcedure(69 + 2)),
            (MatchesAttributePredicate(ATTR_PAX, 3), ConstantProcedure(69 + 3)),
            (MatchesAttributePredicate(ATTR_PAX, 4), ConstantProcedure(69 + 4)),
        )
        procedure = BranchingProcedure(
            (AttributeInRangePredicate(ATTR_PAX, 1, 3), second_proc)
        )

        # Since branching procedures produce a *filtering* AVM, only the
        # values 1 and 2 are to be shown in the table.
        self.assertTrue(any(1 in domain for domain in procedure.avm[ATTR_PAX_LOCATOR]))
        self.assertTrue(any(2 in domain for domain in procedure.avm[ATTR_PAX_LOCATOR]))
        self.assertFalse(any(3 in domain for domain in procedure.avm[ATTR_PAX_LOCATOR]))
        self.assertFalse(any(4 in domain for domain in procedure.avm[ATTR_PAX_LOCATOR]))

    def test_regression_generation_of_None_for_quantity(self):
        v1 = ConstantProcedure(42)
        v2 = BranchingProcedure(
            (QuantityPredicate(0, 0), v1), (QuantityPredicate(0, 1), v1)
        )
        for demand_data in generate_demand_datas(
            v2.avm, _get_table_avm_index(v2.avm, NULL_FORMAT)
        ):
            demand = demand_data.demand
            self.assertEqual(len(demand.requests), 1)
            self.assertIsNot(demand.requests[0].quantity, None)

    def test_table_generation_with_multiple_procedures(self):
        first_step = BranchingProcedure(
            (QuantityPredicate(1, 4), ConstantProcedure(1)),
            (QuantityPredicate(4, 8), ConstantProcedure(2)),
            (QuantityPredicate(8, 14), ConstantProcedure(3)),
        )
        second_step = BranchingProcedure(
            (
                ValidityPredicate(datetime(2018, 12, 1), datetime(2019, 6, 1)),
                ConstantProcedure(69),
            ),
            (
                ValidityPredicate(datetime(2019, 6, 1), datetime(2020, 7, 1)),
                ConstantProcedure(85),
            ),
        )
        third_step = BranchingProcedure(
            (QuantityPredicate(1, 6), ConstantProcedure(22)),
            (QuantityPredicate(6, 14), ConstantProcedure(96)),
        )
        table = list(
            generate_full_tables(
                (
                    ("first_step", first_step),
                    ("second_step", second_step),
                    ("third_step", third_step),
                ),
                single_table=True,
            )
        )[0]
        self.assertEqual(
            table.rows,
            [
                ("first_step", Range.new_open_right(1, 4).lift(), MISSING_CELL, 1),
                ("first_step", Range.new_open_right(4, 8).lift(), MISSING_CELL, 2),
                ("first_step", Range.new_open_right(8, 14).lift(), MISSING_CELL, 3),
                (
                    "second_step",
                    MISSING_CELL,
                    Range.new_open_right(
                        datetime(2018, 12, 1, 0, 0), datetime(2019, 6, 1, 0, 0)
                    ).lift(),
                    69,
                ),
                (
                    "second_step",
                    MISSING_CELL,
                    Range.new_open_right(
                        datetime(2019, 6, 1, 0, 0), datetime(2020, 7, 1, 0, 0)
                    ).lift(),
                    85,
                ),
                ("third_step", Range.new_open_right(1, 6).lift(), MISSING_CELL, 22),
                ("third_step", Range.new_open_right(6, 14).lift(), MISSING_CELL, 96),
            ],
        )

    def test_regression_table_generation_with_ranged_procedures(self):
        first_step = BranchingProcedure(
            (QuantityPredicate(1, 4), ConstantProcedure(1)),
            (QuantityPredicate(4, 8), ConstantProcedure(2)),
            (QuantityPredicate(8, 14), ConstantProcedure(3)),
        )
        second_step = BranchingProcedure(
            # Prices from 2019-01-01 up to 2019-04-30
            (
                ValidityPredicate(datetime(2019, 1, 1), datetime(2019, 5, 1)),
                ConstantProcedure(42),
            ),
            # Prices from 2018-12-01 up to 2019-05-31
            (
                ValidityPredicate(datetime(2018, 12, 1), datetime(2019, 6, 1)),
                ConstantProcedure(69),
            ),
            (ValidityPredicate(datetime(2019, 2, 1), datetime(2019, 7, 1)), first_step),
            # Other dates.
            (Otherwise(), ConstantProcedure(51)),
        )
        table = list(
            generate_full_tables(
                (("second_step", second_step),),
                TableFormat.from_columns(date_locator, quantity_locator),
            )
        )
        rows = list(table)[0].rows
        # Compare the set of rows because I'm not interested in the order in
        # which they are produced.  But I do need know the order in which
        # columns are in each row.
        self.assertEqual(
            set(rows),
            {
                (
                    Range.new_open_right(
                        datetime(2019, 1, 1, 0, 0), datetime(2019, 5, 1, 0, 0)
                    ).lift(),
                    Range.new_open_right(1, 4).lift(),
                    42,
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 1, 1, 0, 0), datetime(2019, 5, 1, 0, 0)
                    ).lift(),
                    Range.new_open_right(4, 8).lift(),
                    42,
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 1, 1, 0, 0), datetime(2019, 5, 1, 0, 0)
                    ).lift(),
                    Range.new_open_right(8, 14).lift(),
                    42,
                ),
                (
                    IntervalSet(
                        (
                            Range.new_open_right(
                                datetime(2018, 12, 1, 0, 0), datetime(2019, 1, 1, 0, 0)
                            ),
                            Range.new_open_right(
                                datetime(2019, 5, 1, 0, 0), datetime(2019, 6, 1, 0, 0)
                            ),
                        )
                    ),
                    Range.new_open_right(1, 4).lift(),
                    69,
                ),
                (
                    IntervalSet(
                        (
                            Range.new_open_right(
                                datetime(2018, 12, 1, 0, 0), datetime(2019, 1, 1, 0, 0)
                            ),
                            Range.new_open_right(
                                datetime(2019, 5, 1, 0, 0), datetime(2019, 6, 1, 0, 0)
                            ),
                        )
                    ),
                    Range.new_open_right(4, 8).lift(),
                    69,
                ),
                (
                    IntervalSet(
                        (
                            Range.new_open_right(
                                datetime(2018, 12, 1, 0, 0), datetime(2019, 1, 1, 0, 0)
                            ),
                            Range.new_open_right(
                                datetime(2019, 5, 1, 0, 0), datetime(2019, 6, 1, 0, 0)
                            ),
                        )
                    ),
                    Range.new_open_right(8, 14).lift(),
                    69,
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 6, 1, 0, 0), datetime(2019, 7, 1, 0, 0)
                    ).lift(),
                    Range.new_open_right(1, 4).lift(),
                    1,
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 6, 1, 0, 0), datetime(2019, 7, 1, 0, 0)
                    ).lift(),
                    Range.new_open_right(4, 8).lift(),
                    2,
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 6, 1, 0, 0), datetime(2019, 7, 1, 0, 0)
                    ).lift(),
                    Range.new_open_right(8, 14).lift(),
                    3,
                ),
            },
        )

    def test_regression_issue781_table_generation_using_format(self):
        self._test_regression_issue781_table_generation_using_format(TABLE_FORMAT)

    def test_format_with_a_single_column_BY_VALUE(self):
        step = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), ConstantProcedure(1)),
            (MatchesAttributePredicate(occupation_attr, "DBL"), ConstantProcedure(2)),
            (MatchesAttributePredicate(occupation_attr, "TPL"), ConstantProcedure(3)),
        )
        tables = list(generate_full_tables((("step", step),), table_format=TABLE_FORMAT))
        headers = tables[0].columns_headers
        rows = tables[0].rows
        self.assertEqual(
            headers, ((EqSet({"SGL"}),), (EqSet({"DBL"}),), (EqSet({"TPL"}),))
        )
        self.assertEqual(rows, [(1, 2, 3)])

    def test_format_with_a_single_column_BY_VALUE_and_other_BY_NAME(self):
        step123 = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), ConstantProcedure(1)),
            (MatchesAttributePredicate(occupation_attr, "DBL"), ConstantProcedure(2)),
            (MatchesAttributePredicate(occupation_attr, "TPL"), ConstantProcedure(3)),
        )
        step456 = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), ConstantProcedure(4)),
            (MatchesAttributePredicate(occupation_attr, "DBL"), ConstantProcedure(5)),
            (MatchesAttributePredicate(occupation_attr, "TPL"), ConstantProcedure(6)),
        )
        exec_step = BranchingProcedure(
            # Prices from 2019-01-01 up to 2019-04-30
            (ExecutionPredicate(datetime(2019, 1, 1), datetime(2019, 5, 1)), step123),
            # Prices from 2018-12-01 up to 2019-05-31
            (ExecutionPredicate(datetime(2018, 12, 1), datetime(2019, 6, 1)), step456),
            (
                ExecutionPredicate(datetime(2019, 2, 1), datetime(2019, 7, 1)),
                ConstantProcedure(69),
            ),
            # Other dates.
            (Otherwise(), ConstantProcedure(42)),
        )
        tables = list(
            generate_full_tables((("step", exec_step),), table_format=TABLE_FORMAT)
        )
        headers = tables[0].columns_headers
        rows = tables[0].rows
        self.assertEqual(
            headers,
            (
                (EqSet({"SGL"}),),
                (EqSet({"DBL"}),),
                (EqSet({"TPL"}),),
                TypedAttribute.from_typed_name("start_date", datetime),
            ),
        )
        self.assertEqual(
            rows,
            [
                (
                    1,
                    2,
                    3,
                    Range.new_open_right(
                        datetime(2019, 1, 1), datetime(2019, 5, 1)
                    ).lift(),
                ),
                (
                    4,
                    5,
                    6,
                    IntervalSet(
                        (
                            Range.new_open_right(
                                datetime(2018, 12, 1), datetime(2019, 1, 1)
                            ),
                            Range.new_open_right(
                                datetime(2019, 5, 1), datetime(2019, 6, 1)
                            ),
                        )
                    ),
                ),
                (
                    69,
                    69,
                    69,
                    Range.new_open_right(
                        datetime(2019, 6, 1), datetime(2019, 7, 1)
                    ).lift(),
                ),
            ],
        )

    def test_format_with_a_single_column_BY_VALUE_and_other_BY_NAME_flipped(self):
        step123 = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), ConstantProcedure(1)),
            (MatchesAttributePredicate(occupation_attr, "DBL"), ConstantProcedure(2)),
            (MatchesAttributePredicate(occupation_attr, "TPL"), ConstantProcedure(3)),
        )
        step456 = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), ConstantProcedure(4)),
            (MatchesAttributePredicate(occupation_attr, "DBL"), ConstantProcedure(5)),
            (MatchesAttributePredicate(occupation_attr, "TPL"), ConstantProcedure(6)),
        )
        exec_step = BranchingProcedure(
            # Prices from 2019-01-01 up to 2019-04-30
            (ExecutionPredicate(datetime(2019, 1, 1), datetime(2019, 5, 1)), step123),
            # Prices from 2018-12-01 up to 2019-05-31
            (ExecutionPredicate(datetime(2018, 12, 1), datetime(2019, 6, 1)), step456),
            (
                ExecutionPredicate(datetime(2019, 2, 1), datetime(2019, 7, 1)),
                ConstantProcedure(69),
            ),
            # Other dates.
            (Otherwise(), ConstantProcedure(42)),
        )
        tables = list(
            generate_full_tables(
                (("step", exec_step),), table_format=TABLE_FORMAT_START_DATE_FIRST
            )
        )
        headers = tables[0].columns_headers
        rows = tables[0].rows
        self.assertEqual(
            headers,
            (
                TypedAttribute.from_typed_name("start_date", datetime),
                (EqSet({"SGL"}),),
                (EqSet({"DBL"}),),
                (EqSet({"TPL"}),),
            ),
        )
        self.assertEqual(
            rows,
            [
                (
                    Range.new_open_right(
                        datetime(2019, 1, 1), datetime(2019, 5, 1)
                    ).lift(),
                    1,
                    2,
                    3,
                ),
                (
                    IntervalSet(
                        (
                            Range.new_open_right(
                                datetime(2018, 12, 1), datetime(2019, 1, 1)
                            ),
                            Range.new_open_right(
                                datetime(2019, 5, 1), datetime(2019, 6, 1)
                            ),
                        )
                    ),
                    4,
                    5,
                    6,
                ),
                (
                    Range.new_open_right(
                        datetime(2019, 6, 1), datetime(2019, 7, 1)
                    ).lift(),
                    69,
                    69,
                    69,
                ),
            ],
        )

    def test_table_rows_are_lazy(self):
        # The TABLE_FORMAT will create three tables: one for each branch.  If
        # we ever try to read the rows of the second table, Kaboom!! but
        # reading the rows of the third table should not entail reading the
        # rows of the second.
        procedure = BranchingProcedure(
            (QuantityPredicate(1, 10), ConstantProcedure(69)),
            (QuantityPredicate(10, 20), KaboomProcedure()),
            (QuantityPredicate(20, 30), ConstantProcedure(42)),
        )
        top_procedure = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), procedure),
            (
                MatchesAttributePredicate(occupation_attr, "DBL"),
                FormulaProcedure(procedure, code="100 + #1"),
            ),
            (
                MatchesAttributePredicate(occupation_attr, "TPL"),
                FormulaProcedure(procedure, code="200 + #1"),
            ),
        )
        tables = generate_tables(
            (("procedure", top_procedure),), table_format=TABLE_FORMAT
        )
        table = next(tables)
        rows = _read_table_rows(table)
        self.assertEqual(rows, [(69, 169, 269)])
        next(tables)  # Skip dangerous second table.
        table = next(tables)
        rows = _read_table_rows(table)
        self.assertEqual(rows, [(42, 142, 242)])

    def test_table_rows_are_lazy_but_do_work(self):
        procedure = BranchingProcedure(
            (QuantityPredicate(1, 10), ConstantProcedure(69)),
            (QuantityPredicate(10, 20), KaboomProcedure()),
            (QuantityPredicate(20, 30), ConstantProcedure(42)),
        )
        top_procedure = BranchingProcedure(
            (MatchesAttributePredicate(occupation_attr, "SGL"), procedure),
            (
                MatchesAttributePredicate(occupation_attr, "DBL"),
                FormulaProcedure(procedure, code="100 + #1"),
            ),
            (
                MatchesAttributePredicate(occupation_attr, "TPL"),
                FormulaProcedure(procedure, code="200 + #1"),
            ),
        )
        tables = generate_tables(
            (("procedure", top_procedure),), table_format=TABLE_FORMAT
        )
        table = next(tables)
        rows = _read_table_rows(table)
        self.assertEqual(rows, [(69, 169, 269)])

        table = next(tables)
        with self.assertRaises(AssertionError):
            rows = _read_table_rows(table)

        table = next(tables)
        rows = _read_table_rows(table)
        self.assertEqual(rows, [(42, 142, 242)])


def generate_full_tables(
    procedures: Sequence[Tuple[ProcedureName, Procedure]],
    table_format: TableFormat = NULL_FORMAT,
    single_table: bool = False,
    now=None,
):
    """Procedures the table prices but ensures to convert generators to list.

    This allows to test the result of tables.

    """
    for table in generate_tables(
        procedures, table_format, single_table=single_table, now=now
    ):
        yield Table(table.attrs, tuple(table.columns_headers), _read_table_rows(table))


def _read_table_rows(table):
    from typing import List, Any

    rows: List[Tuple[Any, ...]] = []
    for original_row in table.rows:
        row: List[Any] = []
        for cell in original_row:
            if isinstance(cell, (GeneratorType, tuple)):
                for c in cell:
                    row.append(c)
            else:
                row.append(cell)
        rows.append(tuple(row))
    return rows
