# Example file: insertion_sort.py

# Each sorting function should accept a list of integers as the single required
# parameter, as shown below. The input list should be sorted upon completion.
def insertion_sort(nums: list[int]):
	# loop through all unsorted list values
	for i in range(1,len(nums)):
		# store current unsorted value
		temp = nums[i]
		# store index of current unsorted value
		j = i
		# while j idx has not run off list and the element in front of j is greater than current unsorted value 
		while (j > 0 and nums[j-1] > temp):
			# shift larger element up 
			nums[j] = nums[j-1]
			# decrement j to where current unsorted value can go
			j -= 1
		# j holds idx of where current unsorted value can go, set
		nums[j] = temp 
	return nums