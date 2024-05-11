import decimal as dec
from zipzip_tree import ZipZipTree, Rank
from hybrid_sort1 import hybrid_sort1

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    # initialize our tree structure of bins
    n = len(items)
    bins_tree = ZipZipTree(n)
    # start the tree with a bin of capacity 1
    free_space.append(1.0)
    new_bin_id = 0
    bins_tree.insert(new_bin_id, 1.0)

    for i in range(n):
        item_f = items[i]
        item_d = dec.Decimal('{:.10f}'.format(item_f))  # get item size
        # function to find the node that will hold the item or None then insert a new node to hold the item
        bin_found = bins_tree.find_bin(item_d)
        if bin_found is not None:  # place item in bin and update the tree
            bin_found.val -= item_f  # Remove decimal subtraction
            bin_found.update_node_bc()  # update the immediate subtree
            bins_tree._update_nodes2(bins_tree.root, bin_found.key)  # update the nodes above node
            assignment[i] = bin_found.key
            free_space[bin_found.key] -= item_f  # Remove decimal subtraction
        else:
            new_bin_id += 1
            new_bin_cap_f = 1.0 - item_f
            assignment[i] = new_bin_id
            free_space.append(new_bin_cap_f)
            bins_tree.insert(new_bin_id, new_bin_cap_f)
            bins_tree._update_nodes2(bins_tree.root, new_bin_id) # update the nodes above node



def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items_list = list(items)
    hybrid_sort1(items_list)
    items_list = items_list[::-1]
    first_fit(items_list, assignment, free_space)