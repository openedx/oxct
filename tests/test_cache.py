import unittest
from unittest.mock import Mock

from oxct.server import cache

mock_caller = Mock()


@cache.memoize
def dummy_function(arg1, arg2, arg3=3):
    mock_caller(arg1, arg2, arg3=arg3)
    return arg1 + 10 * arg2 + 100 * arg3


class CacheTests(unittest.TestCase):
    def setUp(self):
        # This is horrible and should probably be improved
        cache.Cache.MIN_TTL_SECONDS = 1
        cache.Cache.MAX_TTL_SECONDS = 2
        cache.Cache.instance().clear()

    def test_recompute_fifo(self):
        cache.Cache.instance().clear()

        mock_caller.reset_mock()
        dummy_function(1, 2, arg3=3)
        mock_caller.assert_called_once_with(1, 2, arg3=3)

        mock_caller.reset_mock()
        dummy_function(1, 2, arg3=3)
        mock_caller.assert_not_called()

        cache.recompute_expired(count=1)
        mock_caller.assert_called_once_with(1, 2, arg3=3)
