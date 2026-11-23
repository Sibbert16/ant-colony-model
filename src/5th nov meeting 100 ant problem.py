import matplotlib as plt

# ---------------- PARAMETERS ----------------

TOTAL_ANTS = 100

forager_start = 50
nurse_start = 50

forager_threshold = 50
nurse_threshold = 50

ant_full = 70

food_per_trip = 100
feed_rate = 5
trip_length = 20
drain = 1

timesteps = 1000


# ---------------- SIMULATION ----------------

def run_simulation(starting_foragers):

    starting_nurses = TOTAL_ANTS - starting_foragers

    nurses = [nurse_start] * starting_nurses
    foragers = [forager_start] * starting_foragers
    trip_timers = [0] * starting_foragers

    for t in range(timesteps):

        # everyone loses energy
        for i in range(len(foragers)):
            foragers[i] -= drain

        for i in range(len(nurses)):
            nurses[i] -= drain

        # colony dies if anyone starves
        if any(f <= 0 for f in foragers):
            return t

        if any(n <= 0 for n in nurses):
            return t

        # travelling
        for i in range(len(foragers)):

            if trip_timers[i] > 0:

                trip_timers[i] -= 1

                if trip_timers[i] == 0:
                    foragers[i] += food_per_trip

        # hungry foragers leave
        for i in range(len(foragers)):

            if trip_timers[i] == 0 and foragers[i] < forager_threshold:
                trip_timers[i] = trip_length

        # feed nurses
        for nurse in range(len(nurses)):

            while nurses[nurse] < nurse_threshold:

                fed = False

                for f in range(len(foragers)):

                    if trip_timers[f] == 0 and foragers[f] > forager_threshold:

                        food = min(
                            feed_rate,
                            foragers[f] - forager_threshold,
                            ant_full - nurses[nurse]
                        )

                        if food > 0:
                            nurses[nurse] += food
                            foragers[f] -= food
                            fed = True
                            break

                if not fed:
                    break

    return timesteps


# ---------------- RUN EVERY RATIO ----------------

survival = []

ratios = []

for starting_foragers in range(TOTAL_ANTS + 1):

    time_alive = run_simulation(starting_foragers)

    survival.append(time_alive)

    ratios.append(starting_foragers)

    print(
        f"Foragers = {starting_foragers:3d} | "
        f"Nurses = {TOTAL_ANTS-starting_foragers:3d} | "
        f"Survived {time_alive} steps"
    )


# ---------------- PLOT ----------------

plt.figure(figsize=(10,6))

plt.plot(ratios, survival, linewidth=2)

plt.xlabel("Initial number of foragers")
plt.ylabel("Timesteps until first starvation")
plt.title("100-ant colony: survival vs nurse/forager ratio")

plt.grid(True)

plt.show()
