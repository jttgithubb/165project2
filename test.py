import decimal as dec
from zipzip_tree import ZipZipTree, Rank

if __name__ == "__main__":
    '''bin found:  [Node: 0.05, 2, 2, Rank(geometric_rank=1, uniform_rank=7)]
    0.0 1 Rank(geometric_rank=0, uniform_rank=4) 1 None None
    0.05 2 Rank(geometric_rank=1, uniform_rank=7) 2 [Node: 0.0, 1, 1, Rank(geometric_rank=0, uniform_rank=4)] [Node: 0.21, 0, 0, Rank(geometric_rank=0, uniform_rank=6)]
    0.21 0 Rank(geometric_rank=0, uniform_rank=6) 0 None None

    bin found:  None
    0.0 2 Rank(geometric_rank=1, uniform_rank=7) 2 None None'''

    tree = ZipZipTree(12)
    tree.insert(0.21, 0, Rank(geometric_rank=0, uniform_rank=6))
    tree.insert(0.0, 1, Rank(geometric_rank=0, uniform_rank=4))
    tree.insert(0.05, 2, Rank(geometric_rank=1, uniform_rank=7))
    
    tree.inorder_traversal()
    tree.remove(0.05)
    tree.inorder_traversal()
    tree.insert(0.0, 2, Rank(geometric_rank=1, uniform_rank=7))
    tree.inorder_traversal()