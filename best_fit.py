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
    #bins_tree.insert(new_bin_cap, new_bin_id)  # Initial bin node [Node 0, key:1.0, val:0, bVal:0...]
    initial_key = (dec.Decimal('{:.10f}'.format(new_bin_cap)), new_bin_id)  # Handles duplicate capacities
    initial_bin = bins_tree.insert(initial_key, new_bin_id)  # Initial bin node [Node 0, key:(Decimal capacity, Integer bin_id), val:0, bVal:0 ... AND cap:1.0] 
    initial_bin.cap = new_bin_cap

    for i in range(n):
        item_f = items[i]
        item_d = dec.Decimal('{:.10f}'.format(item_f))  # get item size
        # function to find the node that will BEST hold the item or None then insert a new node to hold the item
        #bin_found = bins_tree.find_bin2(item_d)
        bin_found = bins_tree.find_bin3(item_d)
        if bin_found is not None:  # place item in bin and update the tree
            bin_key = bin_found.key
            bin_found = bins_tree.remove(bin_key) # remove bin from the tree
            assignment[i] = bin_key[1]
            new_cap_f = free_space[bin_key[1]] - item_f
            free_space[bin_key[1]] = new_cap_f
            new_key = (dec.Decimal('{:.10f}'.format(new_cap_f)), bin_key[1])
            reinserted_node = bins_tree.insert(new_key, bin_key[1], bin_found.rank)  # reinsert node with new capacity
            reinserted_node.cap = new_cap_f
        else:
            new_bin_id += 1
            assignment[i] = new_bin_id
            new_bin_cap_f = new_bin_cap - item_f
            free_space.append(new_bin_cap_f)
            new_key = (dec.Decimal('{:.10f}'.format(new_bin_cap_f)), new_bin_id)
            inserted_node = bins_tree.insert(new_key, new_bin_id)  # insert new bin
            inserted_node.cap = new_bin_cap_f
            
def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    items_list = list(items)
    hybrid_sort1(items_list)
    items_list = items_list[::-1]
    best_fit(items_list, assignment, free_space)