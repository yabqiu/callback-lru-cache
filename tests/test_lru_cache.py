import unittest
import io
from callback_lru_cache import lru_cache


def test_basic_lru_cache():
    buffer = io.StringIO()

    @lru_cache(3)
    def fetch(x):
        print('miss:', x, end='', file=buffer)
        return x + 1

    for i in [1, 2, 3, 1, 2, 4, 3, 2, 1]:
        print(f'get data for {i}: ', end='', file=buffer)
        fetch(i)
        print(file=buffer)

    assert buffer.getvalue() == """\
get data for 1: miss: 1
get data for 2: miss: 2
get data for 3: miss: 3
get data for 1: 
get data for 2: 
get data for 4: miss: 4
get data for 3: miss: 3
get data for 2: 
get data for 1: miss: 1
"""


def test_lru_cache_with_eviction_callback():
    buffer = io.StringIO()

    def eviction_callback(key, value):
        # release resources
        print(f"evicted key: {key}, {value}", end='', file=buffer)

    @lru_cache(3, evict_callback=eviction_callback)
    def fetch(x):
        print(f'miss: {x}, ', end='', file=buffer)
        return x + 1

    for i in [1, 2, 3, 1, 2, 4, 3, 2, 1]:
        print(f'get data for {i}: ', end='', file=buffer)
        fetch(i)
        print(file=buffer)

    assert buffer.getvalue() == """\
get data for 1: miss: 1, 
get data for 2: miss: 2, 
get data for 3: miss: 3, 
get data for 1: 
get data for 2: 
get data for 4: miss: 4, evicted key: 3, 4
get data for 3: miss: 3, evicted key: 1, 2
get data for 2: 
get data for 1: miss: 1, evicted key: 4, 5
"""


if __name__ == '__main__':
    unittest.main()