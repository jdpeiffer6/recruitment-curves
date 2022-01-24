from gettext import npgettext
import numpy as np


text = input("Choose a file 0-4")
data = np.load(("dummy_multithread_{}_data.npy").format(text))
print(data)
print('Data Executed')
