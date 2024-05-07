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
        item_d = dec.Decimal('{:.2f}'.format(item_f))  # get item size
        # function to find the node that will hold the item or None then insert a new node to hold the item
        bin_found = bins_tree.find_bin(bins_tree.root, item_d)
        if bin_found is not None:  # place item in bin and update the tree
            bin_cap_f = bin_found.val
            bin_cap_d = dec.Decimal('{:.2f}'.format(bin_cap_f))
            bin_found.val = float(bin_cap_d - item_d)
            #bins_tree.update_nodes()
            bins_tree._update_nodes(bin_found)
            bins_tree._update_nodes2(bins_tree.root, bin_found.key)
            assignment[i] = bin_found.key
            free_space[bin_found.key] = float(dec.Decimal('{:.2f}'.format(free_space[bin_found.key])) - item_d)
        else:
            new_bin_id += 1
            bin_cap_f = 1.0
            bin_cap_d = dec.Decimal('{:.2f}'.format(bin_cap_f)) - item_d
            bin_cap_f = float(bin_cap_d)
            assignment[i] = new_bin_id
            free_space.append(bin_cap_f)
            new_node = bins_tree.insert(new_bin_id, bin_cap_f)
            #bins_tree.update_nodes()
            bins_tree._update_nodes(new_node)
            bins_tree._update_nodes2(bins_tree.root, new_bin_id)



def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items_list = list(items)
    hybrid_sort1(items_list)
    items_list = items_list[::-1]
    first_fit(items_list, assignment, free_space)