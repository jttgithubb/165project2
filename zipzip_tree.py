# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass
import random as rand
import math
import decimal as dec

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

def generate_geometric_rank() -> int:
	heads = 0
	while True:
		outcome = rand.choice(['heads', 'tails'])
		if outcome == 'heads':
			heads += 1
		else:
			break
	return heads

@dataclass
class Rank:
	geometric_rank: int
	uniform_rank: int

	def __lt__(self, other: Rank) -> bool:
		if self.geometric_rank < other.geometric_rank:
			return True
		elif self.geometric_rank == other.geometric_rank:
			return self.uniform_rank < other.uniform_rank
		else:
			return False
		
class ZipZipNode:
	def __init__(self, key: KeyType, val: ValType):
		self.key = key  
		self.val = val  
		self.bVal = None
		self.rank = None
		self.left = None
		self.right = None
	
	def update_node(self):
		if self.left is not None and self.right is not None:
			left_d = dec.Decimal('{:.2f}'.format(self.left.bVal))
			right_d = dec.Decimal('{:.2f}'.format(self.right.bVal))
			cur_d = dec.Decimal('{:.2f}'.format(self.val))
			maximum = max([left_d, right_d, cur_d])
			self.bVal = float(maximum)
		elif self.left is not None and self.right is None:
			left_d = dec.Decimal('{:.2f}'.format(self.left.bVal))
			cur_d = dec.Decimal('{:.2f}'.format(self.val))
			maximum = max([left_d, cur_d])
			self.bVal = float(maximum)
		elif self.left is None and self.right is not None:
			right_d = dec.Decimal('{:.2f}'.format(self.right.bVal))
			cur_d = dec.Decimal('{:.2f}'.format(self.val))
			maximum = max([right_d, cur_d])
			self.bVal = float(maximum)
		else:
			self.bVal = self.val

	def __repr__(self):
		return f'[Node: {self.key}, {self.val}, {self.bVal}, {self.rank}]'
	
	def __eq__(self, other: ZipZipNode) -> bool:
		if other is None:
			return False
		return self.key == other.key and self.val == other.val and self.rank == other.rank
		
class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.height = 0
		self.root = None

	def get_random_rank(self) -> Rank:
		r1 = generate_geometric_rank()
		r2 = rand.randint(0, int(math.log(self.capacity)**3) - 1)
		rand_rank = Rank(r1, r2)
		return rand_rank

	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		# Initialize new node with key, value, and rank
		node_x = ZipZipNode(key, val)
		if rank is None:
			rank_x = self.get_random_rank()
			node_x.rank = rank_x
		else:
			node_x.rank = rank
		# Reference variables (rank objects are mutable)
		rank_x = node_x.rank
		key_x = node_x.key
		cur = self.root
		prev = None
		while cur is not None and (rank_x < cur.rank or (rank_x == cur.rank and key_x > cur.key)):
			prev = cur
			cur = cur.left if key_x < cur.key else cur.right
		if cur == self.root:
			self.root = node_x
		elif key_x < prev.key:
			prev.left = node_x
		else:
			prev.right = node_x
		
		if cur == None:
			node_x.left = None
			node_x.right = None
			self.size += 1
			return
		if key_x < cur.key:
			node_x.right = cur
		else:
			node_x.left = cur
		prev = node_x
		# prev holds inserted node x, curr holds the node below x that must be unzipped
		while cur is not None:
			fix = prev
			if cur.key < key_x:
				while cur is not None and cur.key <= key_x:
					prev = cur
					cur = cur.right
			else:
				while cur is not None and key_x <= cur.key:
					prev = cur
					cur = cur.left
			if fix.key > key_x or (fix == node_x and prev.key > key_x):
				fix.left = cur
			else:
				fix.right = cur
		self.size += 1

	def remove(self, key: KeyType):
		key_x = key
		cur = self.root
		prev = None
		while key != cur.key:
			prev = cur
			cur = cur.left if key < cur.key else cur.right
		left = cur.left
		right = cur.right
		if left is None:
			cur = right
		elif right is None:
			cur = left
		elif right.rank <= left.rank:
			cur = left
		else:
			cur = right
		if self.root.key == key_x:
			self.root = cur
		elif key_x < prev.key:
			prev.left = cur
		else:
			prev.right = cur
		while left is not None and right is not None:
			if right.rank <= left.rank:
				while left is not None and right.rank <= left.rank:
					prev = left
					left = left.right
				prev.right = right
			else:
				while right is not None and left.rank < right.rank:
					prev = right
					right = right.left
				prev.left = left
		self.size -= 1

	def find(self, key: KeyType) -> ValType:
		return self._find(self.root, key)
	
	def _find(self, node: ZipZipNode, key: KeyType) -> ValType:
		if node is None:
			return None
		if node.key == key:
			return node.val
		if key < node.key:
			return self._find(node.left, key)
		return self._find(node.right, key)

	def get_size(self) -> int:
		return self.size

	def get_height(self) -> int:
		return self._height(self.root)
	
	def _height(self, node: ZipZipNode) -> int:
		if node is None:
			return -1
		left_height = self._height(node.left)
		right_height = self._height(node.right)
		return max(left_height, right_height) + 1

	def get_depth(self, key: KeyType):
		return self._depth(self.root, key, 0)

	def _depth(self, node: ZipZipNode, key: KeyType, depth: int) -> int:
		if node is None:
			return -1
		if node.key == key:
			return depth
		if key < node.key:
			return self._depth(node.left, key, depth + 1)
		return self._depth(node.right, key, depth + 1)
	
	def inorder_traversal(self):
		def _inorder_traversal(node):
			if node:
				_inorder_traversal(node.left)
				print(node.key, node.val, node.rank, node.bVal, node.left, node.right, end="\n")
				_inorder_traversal(node.right)
		_inorder_traversal(self.root)
		print()

	def update_nodes(self):  # updates the best capacity of each node after removals and insertions
		self._update_nodes(self.root)

	def _update_nodes(self, node: ZipZipNode):
		if node:
			self._update_nodes(node.left)
			self._update_nodes(node.right)
			node.update_node()
			print(node)
	
	def get_bestCapacity(self, node: ZipZipNode):
		return node.bVal
	
	def find_bin(self, start: ZipZipNode, size: dec.Decimal):
		return self._find_bin(self.root, size)
	
	def _find_bin(self, node: ZipZipNode, size: dec.Decimal):
		left = node.left
		if left is not None:
			left_bVal_d = dec.Decimal('{:.2f}'.format(left.bVal)) 
			if left_bVal_d >= size:
				return self._find_bin(left, size)  # go left
		#  check myself
		node_val_d = dec.Decimal('{:.2f}'.format(node.val))
		if node_val_d >= size:
			return node
		else:
			right = node.right
			if right is not None:
				return self._find_bin(right, size)  # go right
			return None

			

		
		

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
