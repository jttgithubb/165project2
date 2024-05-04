# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass
import random as rand
import math

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
		self.rank = None
		self.left = None
		self.right = None
	
	def __eq__(self, other: ZipZipNode) -> bool:
		return self.key == other.key and self.val == other.val and self.rank == other.rank
		
class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.height = 0
		self.root = None

	def get_random_rank(self) -> Rank:
		rand_rank = Rank()
		r1 = generate_geometric_rank()
		r2 = rand.randint(0, math.log(self.capacity)**3 - 1)
		rand_rank.geometric_rank = r1
		rand_rank.uniform_rank = r2
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
		while cur is not None and (rank_x < cur.rank or (rank_x == cur.rank and key_x < cur.key)):
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
			if fix.key > key_x or (fix == node_x and key_x < prev.key):
				fix.left = cur
			else:
				fix.right = cur

	def remove(self, key: KeyType):
		pass

	def find(self, key: KeyType) -> ValType:
		pass

	def get_size(self) -> int:
		return self.size

	def get_height(self) -> int:
		return self.height

	def get_depth(self, key: KeyType):
		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
