from __future__ import annotations

import threading
from typing import Any, List, Optional


class BoundedQueue:
    """
    This class is a simple thread-safe bounded queue using a Condition variable.

    - put(item) which blocks when the queue is full until space is available.
    - get() which blocks when the queue is empty until an item is available.

    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._items: List[Any] = []
        self._condition = threading.Condition()

    def put(self, item: Any) -> None:
        """
        Add an item to the queue.
        Blocks if the queue is full.
        """
        with self._condition:
            # Wait while the queue is already full.
            while len(self._items) >= self._capacity:
                self._condition.wait()

            self._items.append(item)

            # Notify waiting consumers that a new item is available.
            self._condition.notify_all()

    def get(self) -> Any:
        """
        Remove and return an item from the queue.
        Blocks if the queue is empty.
        """
        with self._condition:
            # Wait while the queue is empty.
            while not self._items:
                self._condition.wait()

            item = self._items.pop(0)

            # Notify waiting producers that space is now available.
            self._condition.notify_all()
            return item

    def __len__(self) -> int:
        """Helpful in tests / debugging."""
        with self._condition:
            return len(self._items)


class ProducerThread(threading.Thread):
    """
    Producer that reads items from a source container
    and pushes them into the shared bounded queue.
    """

    def __init__(
        self,
        source: List[Any],
        queue: BoundedQueue,
        sentinel: Optional[Any] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.source = source
        self.queue = queue
        # Sentinel is a special value placed at the end to signal "no more items".
        self.sentinel = sentinel

    def run(self) -> None:
        # Push each element from the source into the queue.
        for item in self.source:
            self.queue.put(item)

        # Finally, push the sentinel to indicate completion.
        if self.sentinel is not None:
            self.queue.put(self.sentinel)


class ConsumerThread(threading.Thread):
    """
    Consumer that pulls items from the shared bounded queue
    and stores them into a destination container.
    """

    def __init__(
        self,
        destination: List[Any],
        queue: BoundedQueue,
        sentinel: Optional[Any] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.destination = destination
        self.queue = queue
        self.sentinel = sentinel

    def run(self) -> None:
        while True:
            item = self.queue.get()

            # If we see the sentinel, stop consuming.
            # Use identity check so sentinel can be a unique object().
            if self.sentinel is not None and item is self.sentinel:
                break

            self.destination.append(item)


def run_demo() -> None:
    """
    - Creates a producer that reads from a list of integers.
    - Consumer transfers them to another list.
    - Verifies all items were transferred correctly.
    """
    source_data = list(range(1, 11))  # sample "source container"
    destination_data: List[int] = []  # "destination container"

    # Use a UNIQUE sentinel object shared by producer and consumer
    sentinel_value = object()

    shared_queue = BoundedQueue(capacity=3)

    producer = ProducerThread(
        source=source_data,
        queue=shared_queue,
        sentinel=sentinel_value,
        name="ProducerThread",
    )
    consumer = ConsumerThread(
        destination=destination_data,
        queue=shared_queue,
        sentinel=sentinel_value,
        name="ConsumerThread",
    )

    # Start both threads
    producer.start()
    consumer.start()

    # Wait for both to finish
    producer.join()
    consumer.join()

    print("Source data:     ", source_data)
    print("Destination data:", destination_data)
    print("Transfer successful:", source_data == destination_data)


if __name__ == "__main__":
    # Running this file directly will execute the demo.
    run_demo()
