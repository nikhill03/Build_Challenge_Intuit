import unittest

from assignments.assignment1_producer_consumer import (
    BoundedQueue,
    ProducerThread,
    ConsumerThread,
)


class TestBoundedQueue(unittest.TestCase):
    def test_put_and_get_single_item(self) -> None:
        """Queue should return the same item that was put."""
        queue = BoundedQueue(capacity=2)
        queue.put(42)
        self.assertEqual(queue.get(), 42)
        self.assertEqual(len(queue), 0)

    def test_capacity_never_exceeded(self) -> None:
        """
        When we add up to 'capacity' items, the internal length
        should never exceed the configured capacity.
        """
        capacity = 2
        queue = BoundedQueue(capacity=capacity)

        queue.put("a")
        queue.put("b")

        self.assertEqual(len(queue), capacity)

    def test_invalid_capacity_raises(self) -> None:
        """Creating a queue with non-positive capacity should fail."""
        with self.assertRaises(ValueError):
            BoundedQueue(0)


class TestProducerConsumerIntegration(unittest.TestCase):
    def test_all_items_transferred(self) -> None:
        """
        Complete testing:
        - Producer reads from source list.
        - Consumer writes into destination list.
        - Verify no item is lost and order is preserved.
        """
        source_data = list(range(1, 21))
        destination_data = []

        # Use a unique sentinel object shared by producer and consumer
        sentinel = object()

        queue = BoundedQueue(capacity=3)

        producer = ProducerThread(
            source=source_data,
            queue=queue,
            sentinel=sentinel,
            name="TestProducer",
        )
        consumer = ConsumerThread(
            destination=destination_data,
            queue=queue,
            sentinel=sentinel,
            name="TestConsumer",
        )

        producer.start()
        consumer.start()

        # Give threads up to 5 seconds to finish (should be much faster)
        producer.join(timeout=5)
        consumer.join(timeout=5)

        self.assertFalse(producer.is_alive(), "Producer thread did not finish")
        self.assertFalse(consumer.is_alive(), "Consumer thread did not finish")

        # All items should be transferred in the same order
        self.assertEqual(source_data, destination_data)


if __name__ == "__main__":
    unittest.main()
