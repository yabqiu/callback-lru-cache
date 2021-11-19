=====================================
LRU Cache with callback for eviction
=====================================

We can use Python built-in functions.lru_cache, but when a cached item is evicted, there is no chance \
to release corresponding resources.

This LRU Cache with callback feature provides the similar usage as functions.lru_cache with decorator \
`@lru_cache`. Plus, it can task a `eviction_callback` function to do clean works. The function signature \
is `callback(key, value)`.

*Basic LRU Cache*

.. code-block:: python

    @lru_cache(3)
    def fetch(x):
        print('miss:', x, end='')
        return x + 1


    for i in [1, 2, 3, 1, 2, 4, 3, 2, 1]:
        print(f'get data for {i}: ', end='')
        fetch(i)
        print()

*Output:*

.. code-block::

    get data for 1: miss: 1
    get data for 2: miss: 2
    get data for 3: miss: 3
    get data for 1:
    get data for 2:
    get data for 4: miss: 4
    get data for 3: miss: 3
    get data for 2:
    get data for 1: miss: 1

*LRU Cache with callback for eviction*

.. code-block:: python

    def eviction_callback(key, value):
        # release resources
        print(f"evicted key: {key}, {value}", end='')


    @lru_cache(3, evict_callback=eviction_callback)
    def fetch(x):
        print(f'miss: {x}, ', end='')
        return x + 1


    for i in [1, 2, 3, 1, 2, 4, 3, 2, 1]:
        print(f'get data for {i}: ', end='')
        fetch(i)
        print()

*Output:*

.. code-block::

    get data for 1: miss: 1,
    get data for 2: miss: 2,
    get data for 3: miss: 3,
    get data for 1:
    get data for 2:
    get data for 4: miss: 4, evicted key: 3, 4
    get data for 3: miss: 3, evicted key: 1, 2
    get data for 2:
    get data for 1: miss: 1, evicted key: 4, 5