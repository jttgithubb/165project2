import decimal as dec
from zipzip_tree import ZipZipTree, Rank

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    # initialize our tree structure of bins
    n = len(items)
    free_space.append(1.0)
    bins_tree = ZipZipTree(n)
    bin_id = 0
    bins_tree.insert(bin_id, 1.0)



def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    pass