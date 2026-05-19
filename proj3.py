from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None  = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)

#Bubble up the element at index to restore heap property. Return new MinHeap.
def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    new_heap = MinHeap(heap.data[:])

    if index == 0: #no parent to compare it to so heap is returned
        return new_heap

    parent: int = (index - 1) // 2

    #if child node value less than parent node value, swap places
    if new_heap.data[index] < new_heap.data[parent]:
        new_data = new_heap.data[:]
        new_data[index], new_data[parent] = new_data[parent], new_data[index]
        return heapify_up(MinHeap(new_data), parent)

    return new_heap

#Insert a Node and restore heap property via heapify_up. Return new MinHeap
def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_data = heap.data + [element]
    index = len(new_data) - 1
    return heapify_up(MinHeap(new_data), index)

def heapify_down(heap: MinHeap, index: int) -> MinHeap:

    new_heap = MinHeap(heap.data[:])
    left: int = 2 * index + 1
    right: int  = 2 * index + 2
    size: int = len(new_heap.data)

    #find child with smallest value
    if left >= size:
        return new_heap

    smallest: int = left

    if right < size and new_heap.data[right] < new_heap.data[left]:
        smallest = right

    if new_heap.data[smallest] < new_heap.data[index]:
        temp = new_heap.data[index]
        new_heap.data[index] = new_heap.data[smallest]
        new_heap.data[smallest] = temp
        return heapify_down(new_heap, smallest)

    return new_heap


#Remove and return the smallest node along with the new heap.
def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:

    if len(heap.data) == 0:
        raise IndexError("Heap is empty")

    minimum: Node = heap.data[0] #root of heap (minimum)

    new_data = heap.data[:] #shallow copy of heap data
    new_data[0] = new_data[-1] #last leaf node
    new_data = new_data[:-1]
    #swap the last leaf node to be at the position of the former root

    new_heap = MinHeap(new_data)
    if len(new_heap.data) > 0:
        new_heap = heapify_down(new_heap, 0)

    return new_heap, minimum

#Count how many times each character appears in the input string s. Return a frequency dictionary.
def count_frequency(s: str)-> dict[str,int]:
    frequencies: dict = {}
    for char in s:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    return frequencies

#Build a MinHeap from the frequency dictionary. Each character-frequency pair becomes a Node
def create_priority_queue(frequency: dict[str, int]) -> MinHeap:

    pq = MinHeap([])

    #convert (char, freq) pair into a node and insert into MinHeap
    for char, freq in frequency.items():
        node = Node(freq, char)
        pq = insert(pq, node)

    return pq

# Repeatedly combine the two lowest-frequency nodes from the heap into a new node, reinserting until a single root node remains.
def build_tree_from_queue(priority_queue: MinHeap) -> Node:
    heap = priority_queue

    while len(heap.data) > 1:
        heap, left = extract_min(heap)
        heap, right = extract_min(heap)

        if right < left:
            left, right = right, left

        combined_freq: int = left.freq + right.freq
        parent = Node(combined_freq, char=min(left.char, right.char), left=left, right=right)

        heap = insert(heap, parent)

    heap, root = extract_min(heap)
    return root


#Recursively traverse the Huffman tree to assign binary codes to each character. Left edges add "0", right edges add "1".
def generate_codes(node: Node | None, prefix="", code: dict | None =None)-> dict:
    if code is None:
        code = {}

    if node is None:
        return code

    if node.left is None and node.right is None:
        if prefix != "":
            code[node.char] = prefix
        else:
            code[node.char] = "0"
        return code

    generate_codes(node.left, prefix + "0", code)
    generate_codes(node.right, prefix + "1", code)

    return code

#Replace each character in the string s with its corresponding Huffman code. Return the encoded binary string.
def encode(s: str, codes: dict)-> str:
    binary_string = []
    for char in s:
        binary_string += [codes[char]]

    return "".join(binary_string)


#Use the Huffman tree to decode the binary string. Traverse from the root based on each bit, resetting at each leaf.
def decode(encoded_string: str, root: Node):
    result = []
    current = root

    #iterate through encoded string
    for bit in encoded_string:
        if bit == '0':
            current = current.left
        else: # bit == '1':
            current = current.right

        if current.left is None and current.right is None:
            result += [current.char]
            current = root

    return "".join(result)

def huffman_encoding(s:str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string,root)
    return encoded_string, decoded_string, codes

