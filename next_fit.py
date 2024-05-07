# Example file: next_fit.py
# explanations for member functions are provided in requirements.py

import decimal as dec

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	n = len(items)
	free_space.append(1.0)
	for i in range (n):
		item_f = items[i]
		item_d = dec.Decimal('{:.10f}'.format(item_f))  # item size
		bin_space_d = dec.Decimal('{:.10f}'.format(free_space[-1]))  # available space in last bin
		if item_d <= bin_space_d:  # if item fits in last bin
			assignment[i] = len(free_space) - 1
			# update the free space of the last bin precisely
			free_space[-1] = float(bin_space_d - item_d)
		else:  # if item does not fit in last bin
			free_space.append(1.0)
			assignment[i] = len(free_space) - 1
			bin_space_d = dec.Decimal('{:.10f}'.format(free_space[-1]))  # available space in last bin that was added
			free_space[-1] = float(bin_space_d - item_d)

