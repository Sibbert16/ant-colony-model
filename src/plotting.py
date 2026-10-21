import matplotlib.pyplot as plt

def growth_plot(nurse_count_history, forager_count_history, n):
    plt.figure(figsize=(10,5))
    plt.plot(range(n), nurse_count_history, label="Nurses")
    plt.plot(range(n), forager_count_history, label="Foragers")

    plt.xlabel("Time step")
    plt.ylabel("Number of ants")
    plt.title("Colony growth over time")

    plt.show()


feed_rates = []
final_hive_food = []
nurse_count = []

#for rate in range(150, 150, 10):
#
#    final_food, nurses_alive = run_simulation(rate)
#
#    feed_rates.append(rate)
#    final_hive_food.append(final_food)
#    nurse_count.append(nurses_alive)

#plt.figure(figsize=(10,5))

#plt.plot(feed_rates, final_hive_food, label="Hive Food")

#plt.xlabel("Foraged Food per Trip")
#plt.ylabel("Hive Food")
#plt.title("Hive Food vs Foraged Food per Trip")

#plt.legend()

#plt.show()