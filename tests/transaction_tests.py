import os, sys

from nose.tools import assert_is_instance

from abcbank.transaction import Transaction

def test_type():
    t = Transaction(5)
    assert_is_instance(t, Transaction, "correct type")

test_type()
