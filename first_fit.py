import decimal as dec
from zipzip_tree import ZipZipTree, Rank

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    # initialize our tree structure of bins
    n = 3
    bins_tree = ZipZipTree(n)
    # start the tree with a bin of capacity 1
    free_space.append(1.0)
    bin_id = 0
    bins_tree.insert(bin_id, 1.0)
    bins_tree.update_nodes()
    bins_tree.insert(1, 2.0)
    bins_tree.update_nodes()
    bins_tree.insert(2, 3.0)
    bins_tree.update_nodes()
    print("root: ", bins_tree.root)
    bins_tree.inorder_traversal()


    item_f = 1.0
    item_d = dec.Decimal('{:.2f}'.format(item_f))  # get item size
    # function to find the node that will hold the item or None then insert a new node to hold the item
    bin_found = bins_tree.find_bin(bins_tree.root, item_d)
    if bin_found is not None:
        print(bin_found)
    else:
        print("No bin found")


    '''for i in range(n):
        item_f = items[i]
        item_d = dec.Decimal('{:.2f}'.format(item_f))  # get item size
        # function to find the node that will hold the item or None then insert a new node to hold the item
        bin_found = bins_tree.find_bin(bins_tree.root, item_d)'''




def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    pass