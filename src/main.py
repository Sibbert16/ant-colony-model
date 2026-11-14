from parameters2 import *
from plotting import *
from simulation2 import *

hive_food, nurse_count_history, forager_count_history, nurse_energy_history, forager_energy_history = run_simulation()
growth_plot(nurse_count_history, forager_count_history, n)
energy_plot(nurse_energy_history, forager_energy_history, n)

