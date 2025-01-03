from Grouping_Sets import grouping_sets_using_duckdb
import pytest
from loguru import logger

logger.info("Starting the testing with Parametrize")

@pytest.mark.parametrize("input1, input2, output", [('supplier','Abc',0),('brand','Apple',0)])
def test_grouping_sets(input1, input2, output):
    result = grouping_sets_using_duckdb (input1, input2)
    assert output == result
