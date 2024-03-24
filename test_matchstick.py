from matchstick import *


def test_answer():
    assert main_function('9+3=5') == ['8-3=5', '9-3=6', '3+3=6']

    assert main_function('9+7=8') == []

    assert main_function('7+7=9') == ['1+7=8', '7+1=8']

    assert main_function('8-1=1') == ['0+1=1']

    assert main_function('8-8=8') == ['0+8=8', '8+0=8']

    assert main_function('0-0=8') == ['0+0=0']

