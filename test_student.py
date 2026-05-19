import unittest
from math import expm1

from proj3 import *

class TestProj3(unittest.TestCase):
    def test_heapify_up_single_swap(self):
        heap = MinHeap([Node(1, "a"), Node(5, "b"), Node(3, "c"), Node(8, "d")])
        heap.data.append(Node(2, "e"))

        result = heapify_up(heap, 4)
        expected = MinHeap([Node(1, "a"), Node(2, "e"), Node(3, "c"), Node(8, "d"), Node(5, "b")])

        self.assertEqual(result, expected)

    def test_heapify_up_to_root(self):
        heap = MinHeap([Node(5, "d"), Node(10, "g"), Node(15, "h")])
        heap.data.append(Node(1, "a"))

        result = heapify_up(heap, 3)
        expected = MinHeap([Node(1, "a"), Node(5, "d"), Node(15, "h"), Node(10, "g")])

        self.assertEqual(result, expected)

    def test_heapify_up_no_swaps(self):
        heap = MinHeap([Node(5, "d"), Node(10, "g"), Node(15, "h")])
        heap.data.append(Node(25, "a"))

        result = heapify_up(heap, 3)
        expected = MinHeap([Node(5, "d"), Node(10, "g"), Node(15, "h"), Node(25, "a")])

        self.assertEqual(result, expected)

    def test_insert(self):
        heap = MinHeap([Node(1, "a"), Node(5, "b"), Node(3, "c"), Node(8, "d")])
        entry = Node(2, "e")

        result = insert(heap, entry)
        expected = MinHeap([Node(1, "a"), Node(2, "e"), Node(3, "c"), Node(8, "d"), Node(5, "b")])

        self.assertEqual(result, expected)

    def test_heapify_down_single_swap(self):
        heap = MinHeap([Node(5, "r"), Node(1, "a"), Node(2, "b")])
        result = heapify_down(heap, 0)
        expected = MinHeap([Node(1, "a"), Node(5, "r"), Node(2, "b")])
        self.assertEqual(result, expected)

    def test_heapify_down_to_leaf_node(self):
        heap = MinHeap([Node(30, "z"), Node(1, "a"), Node(2, "e"), Node(3, "c"), Node(8, "d"), Node(5, "b")])
        result = heapify_down(heap, 0)
        expected = MinHeap([Node(1, "a"), Node(3, "c"), Node(2, "e"), Node(30, "z"), Node(8,"d"), Node(5, "b")])
        self.assertEqual(result, expected)

    def test_heapify_no_swaps(self):
        heap = MinHeap([Node(1, "a"), Node(3, "c"), Node(2, "e"), Node(30, "z"), Node(8,"d"), Node(5, "b")])
        result = heapify_down(heap, 2)
        expected = MinHeap([Node(1, "a"), Node(3, "c"), Node(2, "e"), Node(30, "z"), Node(8,"d"), Node(5, "b")])

        self.assertEqual(result, expected)

    def test_extract_min(self):
        heap = MinHeap([Node(2, "a"), Node(5, "b"), Node(8, "c")])
        new_heap, min_node = extract_min(heap)
        expected_min = Node(2, "a")
        expected_heap = MinHeap([Node(5,"b"), Node(8, "c")])

        self.assertEqual(new_heap, expected_heap)
        self.assertEqual(min_node, expected_min)

    def test_empty_heap(self):
        heap = MinHeap([])
        with self.assertRaises(IndexError):
            extract_min(heap)

    def test_check_frequencies(self):
        string = "coconut"
        frequencies = count_frequency(string)
        expected = {"c":2, "o":2, "n":1, "u":1, "t":1}

        self.assertEqual(frequencies, expected)

    def test_create_queue(self):
        test_freq = {"a":5, "b":2, "c":8}
        result = create_priority_queue(test_freq)
        values = [(node.char, node.freq) for node in result.data]

        self.assertIn(("a", 5), values)
        self.assertIn(("b", 2), values)
        self.assertIn(("c", 8), values)
        self.assertEqual(len(result.data), 3)

    def test_generate_code_simple(self):
        string = "aabbcc"
        freq_dict = count_frequency(string)
        q = create_priority_queue(freq_dict)
        tree = build_tree_from_queue(q)
        result = generate_codes(tree)
        expected = {"c": "0", "a":"10", "b":"11"}
        self.assertEqual(result, expected)

    def test_encode(self):
        string = "coconut"
        dictionary = {"c":"00", "o":"01", "n":"100", "u":"101", "t":"110"}
        result = encode(string, dictionary)
        expected = "00010001100101110"

        self.assertEqual(result, expected)

    def test_decode(self):
        root = Node(8, "",
                    left= Node(4,"",
                               left = Node(2, "c"),
                               right=Node(2, "o")),
                    right=Node(4,"",
                               left = Node(2, "",
                                           left = Node(1, "n"),
                                           right = Node(1, "u")),
                               right= Node(2, "",
                                           left=Node(1, "t"),
                                           right = Node(1, ""))))
        encoded_string = "00010001100101110"
        result = decode(encoded_string, root)
        expected = "coconut"

        self.assertEqual(result, expected)