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
		
	def __le__(self, other: Rank) -> bool:
		if self.geometric_rank < other.geometric_rank:
			return True
		elif self.geometric_rank == other.geometric_rank:
			return self.uniform_rank <= other.uniform_rank
		else:
			return False
		
class ZipZipNode:
	def __init__(self, key: KeyType, val: ValType):
		self.key = key  
		self.val = val  
		self.bVal = None
		self.cap = None
		self.rank = None
		self.left = None
		self.right = None
	
	def update_node_bc(self):
		if self.left is not None and self.right is not None:
			left_d = dec.Decimal('{:.10f}'.format(self.left.bVal))
			right_d = dec.Decimal('{:.10f}'.format(self.right.bVal))
			cur_d = dec.Decimal('{:.10f}'.format(self.val))
			maximum = max([left_d, right_d, cur_d])
			if maximum == left_d:
				self.bVal = self.left.bVal
			elif maximum == right_d:
				self.bVal = self.right.bVal
			else:
				self.bVal = self.val
		elif self.left is not None and self.right is None:
			left_d = dec.Decimal('{:.10f}'.format(self.left.bVal))
			cur_d = dec.Decimal('{:.10f}'.format(self.val))
			maximum = max([left_d, cur_d])
			if maximum == left_d:
				self.bVal = self.left.bVal
			else:
				self.bVal = self.val
		elif self.left is None and self.right is not None:
			right_d = dec.Decimal('{:.10f}'.format(self.right.bVal))
			cur_d = dec.Decimal('{:.10f}'.format(self.val))
			maximum = max([right_d, cur_d])
			if maximum == right_d:
				self.bVal = self.right.bVal
			else:
				self.bVal = self.val
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
		update_list = []  # used to later update swapped nodes when unzipping
	
		node_x = ZipZipNode(key, val)
		node_x.bVal = val
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
			return node_x
		if key_x < cur.key:
			node_x.right = cur
		else:
			node_x.left = cur
		prev = node_x
		# prev holds inserted node x, curr holds the node below x that must be unzipped
		while cur is not None:
			fix = prev
			if cur.key <= key_x:
				while cur is not None and cur.key <= key_x:
					prev = cur
					cur = cur.right
			else:
				while cur is not None and key_x < cur.key:
					prev = cur
					cur = cur.left
			if fix.key > key_x or (fix == node_x and prev.key > key_x):
				fix.left = cur
				update_list.append(fix)
			else:
				fix.right = cur
				update_list.append(fix)
		if (isinstance(node_x.bVal, float)):
			for i in update_list[::-1]:
				i.update_node_bc()
		self.size += 1
		return node_x

	def remove(self, key: KeyType):
		update_list = []  # used to later update swapped nodes when zipping

		key_x = key
		cur = self.root
		prev = None
		removed_node = None
		while key != cur.key:
			prev = cur
			cur = cur.left if key < cur.key else cur.right
		left = cur.left
		right = cur.right

		removed_node = ZipZipNode(cur.key, cur.val)  # record the removed node
		removed_node.bVal = cur.bVal
		removed_node.cap = cur.cap
		removed_node.rank = cur.rank

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
				update_list.append(prev)

			else:
				while right is not None and left.rank < right.rank:
					prev = right
					right = right.left
				prev.left = left
				update_list.append(prev)
		if (isinstance(removed_node.bVal, float)):  # update the nodes that were zipped
			for i in update_list[::-1]:
				i.update_node_bc()
		self.size -= 1
		return removed_node

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

	def update_nodes(self):  # updates ALL NODES
		self._update_nodes(self.root)

	def _update_nodes(self, node: ZipZipNode):  # updates nodes BELOW a certain node
		if node:
			self._update_nodes(node.left)
			self._update_nodes(node.right)
			node.update_node_bc()
	
	def _update_nodes2(self, start: ZipZipNode, key: KeyType):  # updates nodes ABOVE a certain node
		if start.key == key:
			return start.bVal
		elif start.key > key:
			left_bVal = self._update_nodes2(start.left, key)  # go left
			left_bVal_d = dec.Decimal('{:.10f}'.format(left_bVal))
			right_bVal_d = dec.Decimal('{:.10f}'.format(start.right.bVal)) if start.right is not None else dec.Decimal('{:.10f}'.format(0.0))
			cur_bVal_d = dec.Decimal('{:.10f}'.format(start.val))
			max_bVal = max([left_bVal_d, right_bVal_d, cur_bVal_d])
			if max_bVal == left_bVal_d:
				start.bVal = left_bVal
			elif max_bVal == right_bVal_d:
				start.bVal = start.right.bVal if start.right is not None else 0.0
			else:
				start.bVal = start.val
			return start.bVal
		else:
			right_bVal = self._update_nodes2(start.right, key)  # go right
			left_bVal_d = dec.Decimal('{:.10f}'.format(start.left.bVal)) if start.left is not None else dec.Decimal('{:.10f}'.format(0.0))
			right_bVal_d = dec.Decimal('{:.10f}'.format(right_bVal))
			cur_bVal_d = dec.Decimal('{:.10f}'.format(start.val))
			max_bVal = max([left_bVal_d, right_bVal_d, cur_bVal_d])
			if max_bVal == left_bVal_d:
				start.bVal = start.left.bVal if start.left is not None else 0.0
			elif max_bVal == right_bVal_d:
				start.bVal = right_bVal
			else:
				start.bVal = start.val
			return start.bVal
		
	
	def get_bestCapacity(self, node: ZipZipNode):
		return node.bVal
	
	def find_bin(self, size: dec.Decimal):  # finds bin of first fit
		return self._find_bin(self.root, size)
	
	def _find_bin(self, node: ZipZipNode, size: dec.Decimal):
		cur_bC_d = dec.Decimal('{:.10f}'.format(node.bVal))
		if size > cur_bC_d:  # no bin is large enough, immediately return None
			return None
		left = node.left
		if left is not None:
			left_bVal_d = dec.Decimal('{:.10f}'.format(left.bVal)) 
			if left_bVal_d >= size:
				return self._find_bin(left, size)  # go left
		#  check myself
		node_val_d = dec.Decimal('{:.10f}'.format(node.val))
		if node_val_d >= size:
			return node
		else:
			right = node.right
			if right is not None:
				return self._find_bin(right, size)  # go right
			return None

	def find_bin2(self, size: dec.Decimal):  # finds bin of best fit
		return self._find_bin2(self.root, size)
	
	def _find_bin2(self, node: ZipZipNode, size: dec.Decimal):
		# two cases for root: large enough to hold or not
  		#  1. root is large enough
		#     - if left exists and is large enough , go left
		#     - if left exists and is not large enough, use current
		#     - if left does not exists, use current
  		#  2. cur is not large enough
		#     - if right exists and is large enough, go right
		#     - if right exists and is not large enough, go right
		#     - if right does not exists, return None
		if node is None:
			return None
		curr_cap_f = node.key
		curr_cap_d = dec.Decimal('{:.10f}'.format(curr_cap_f))
		if curr_cap_d >= size:
			if node.left is not None:
				left_cap_f = node.left.key
				left_cap_f = dec.Decimal('{:.10f}'.format(left_cap_f))
				if left_cap_f >= size:
					return self._find_bin2(node.left, size)  # go left
				potential_node = self._find_bin2(node.left.right, size)  #  potential node in between a key that cant hold and key that can hold
				if potential_node is None:
					return node
				return potential_node
			else:
				return node
			#return node # use current
		else:
			if node.right is not None:
				return self._find_bin2(node.right, size)  # go right
			return None  # no bin can contain this size
	
	def find_bin3(self, size: dec.Decimal):  # finds bin of best-fit using a tuple key of (Decimal capacity, int bin_id)
		return self._find_bin3(self.root, size)
	
	def _find_bin3(self, node: ZipZipNode, size: dec.Decimal): 
		if node is None:
			return None
		curr_cap_d = node.key[0]
		if curr_cap_d >= size:
			if node.left is not None:
				left_cap_d = node.left.key[0]
				if left_cap_d >= size:
					return self._find_bin3(node.left, size)  # go left
				potential_node = self._find_bin3(node.left.right, size)  #  potential node in between a key that cant hold and key that can hold
				if potential_node is None:
					return node
				return potential_node
			else:
				return node
			#return node # use current
		else:
			if node.right is not None:
				return self._find_bin3(node.right, size)  # go right
			return None  # no bin can contain this size

	def capacity_exist(self, key: dec.Decimal):  # checks if capacity key exists in the tree
		return self._capacity_exist(self.root, key)
	
	def _capacity_exist(self, node: ZipZipNode, key: KeyType):
		if node is None:
			return False
		node_key_d = dec.Decimal('{:.10f}'.format(node.key))  # node.key decimal
		if node_key_d == key:
			return True
		elif node_key_d > key:
			return self._capacity_exist(node.left, key)  # go left
		else:
			return self._capacity_exist(node.right, key)  # go right
	

		
		

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
