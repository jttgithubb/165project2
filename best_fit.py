import decimal as dec
from zipzip_tree import ZipZipTree, Rank
from hybrid_sort1 import hybrid_sort1

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    # intialize the tree structure of bins
    n = len(items)
    new_bin_cap = 1.0
    new_bin_id = 0
    free_space.append(new_bin_cap)
    bins_tree = ZipZipTree(n)
    bins_tree.insert(new_bin_cap, new_bin_id)  # Initial bin node [Node 0, key:1.0, val:0, bVal:0 ...]

    for i in range(n):
        item_f = items[i]
        item_d = dec.Decimal('{:.2f}'.format(item_f))  # get item size
        # function to find the node that will BEST hold the item or None then insert a new node to hold the item
        bin_found = bins_tree.find_bin2(bins_tree.root, item_d)
        if bin_found is not None:  # place item in bin and update the tree
            bin_key = bin_found.key
            bin_found = bins_tree.remove(bin_key) # remove bin from the tree
            new_key_d = dec.Decimal('{:.2f}'.format(free_space[bin_found.val])) - item_d
            assignment[i] = bin_found.val
            new_key_f = float(new_key_d)
            free_space[bin_found.val] = new_key_f
            # ensure no ties by subtracting 0.01 until unique key is found and can be inserted
            '''while (bins_tree.capacity_exist(new_key_d)):
                new_key_d = new_key_d - dec.Decimal('0.01')'''
                #if new_key_d == dec.Decimal('0.00'):
            bins_tree.insert(new_key_f, bin_found.val, bin_found.rank)  # reinsert node with new capacity
        else:
            new_bin_id += 1
            assignment[i] = new_bin_id
            new_bin_cap_d = dec.Decimal('{:.2f}'.format(new_bin_cap)) - item_d
            # ensure no ties by subtracting 0.01 until unique key is found and can be inserted
            '''while (bins_tree.capacity_exist(new_bin_cap_d)):
                new_bin_cap_d = new_bin_cap_d - dec.Decimal('0.01')'''
                #if new_key_d == dec.Decimal('0.00'):
            new_bin_cap_f = float(new_bin_cap_d)
            free_space.append(new_bin_cap_f)
            bins_tree.insert(new_bin_cap_f, new_bin_id)  # insert new bin

            
def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items_list = list(items)
    hybrid_sort1(items_list)
    items_list = items_list[::-1]
    best_fit(items_list, assignment, free_space)