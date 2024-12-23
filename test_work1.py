from Work1 import bin_search
import pytest


@pytest.mark.parametrize("inputs, outputs", [(30,8), (1,0), (35,-1), ('a',-1)])
def test_bin_search (inputs, outputs):
    result1 = bin_search(inputs)
    print("Search Index: ", result1)
    assert result1 == outputs

#def test_bin_search1 (input_d = 70):
#    result = bin_search(input_d)
#    print("Search Index: ", result)
#    assert result == 3


#res = test_bin_search (90)
#if (res == -1):
#    print("Position Not Found")
#else:
#    print("Position Found: ", res)

res = bin_search (30)

@pytest.fixture
def test_value30 ():
    return 30

@pytest.fixture
def test_value90 ():
    return 90

@pytest.mark.parametrize ("inputs, outputs", [("test_value30", 8), ("test_value90", 10)])
def test_bin_search2(inputs, outputs, request):
    inputs = request.getfixturevalue(inputs)
    result2 = bin_search(inputs)
    assert result2 == outputs

