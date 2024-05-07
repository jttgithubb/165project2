# defines the hybrid sort function with H = n**0.2
from insertion_sort import insertion_sort

def hybrid_sort1(nums: list[int], h = None):
    # initialize h at the start
    if h is None:
        h = len(nums) ** 0.2
    if (len(nums) > h):
        # find the middle index using the floor div operator
        mid_idx = len(nums) // 2
        # divide your input list into left and right halves
        left_half = nums[:mid_idx]
        right_half = nums[mid_idx:]
        # recursively call hybridsort twice for the left and right halves of list
        hybrid_sort1(left_half, h)
        hybrid_sort1(right_half, h)
        # merge the sorted left and right halves
        # init counters i,j for the left and right halves
        # init a counter k for directly accessing the nums list
        i = 0
        j = 0
        k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                nums[k] = left_half[i]
                i += 1
            else:
                nums[k] = right_half[j]
                j += 1
            k += 1
        # add any remaining values from the left list
        while i < len(left_half):
            nums[k] = left_half[i]
            i += 1
            k += 1
        # add any remaining values from the right list
        while j < len(right_half):
            nums[k] = right_half[j]
            j += 1
            k += 1
    else:
        insertion_sort(nums)
    