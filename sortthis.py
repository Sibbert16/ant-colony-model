import math
import matplotlib.pyplot as plt
import random


#parameters

n = 5000                  #timesteps to simulate

#energy levels
ant_full = 70.0                #most energy an ant can hold
start_energy = 50.0            #energy a newly hatched / starting ant has
hungry_threshold = 50.0                  #below this an ant wants feeding

# energy lost per timestep ***** one of changes we made
nurse_drain = 0.5              #nurses sit still in the nest, cheapest
forager_nest_drain = 1       #forager resting in the nest
forager_trip_drain = 2       #forager outside, walking and searching

# foraging
trip_length = 15               #timesteps a round trip takes
food_per_trip = 100.0          #food brought home per completed trip
trip_safety = 1.25             #must have 25% more energy than the trip costs - done this way as it made messing aroung with parameneter4rs easier
trip_ready = 65.0              #forager tops up to here before setting off

# feeding
feed_rate = 15.0               #max food moved by one donor per timestep
crop_max = 45.0                #max food a nurse can hold in its social stomach (crop)
donor_min = 55.0               #a nurse only gives food if it is this healthy

# hive / brood
# there is no separate hive store any more - the colony's food store is the
# food sitting in the nurses' crops
hatch_cost = 50.0              #food an egg must be fed before it hatches into a nurse
hive_reserve = 40.0            #food kept back (across all nurse crops) before eggs get fed
hatch_wellfed = 50.0           #don't lay or feed eggs while the colony is already hungry
max_eggs = 3                   #most eggs being reared at the same time

# promotion *** one changes we made, the threshold for a nurse to become a forager
promote_energy = 60.0          #only a well-fed nurse is promoted
promote_age = 20               #and only one that is old enough
ants_per_forager = 5           #colony wants 1 forager per this many ants
min_nurses = 2                 #never strip the nest below this many nurses

#forager success for coming back with food
p_success = 0.95                #comes back with food
p_death = 0.05                  #dies on journey to get food
food_spread = 0.1              #trip food varies by about ±25% (1 standard deviation)

#lifetime of ants
lifespan_mean = 1000            #average lifetime in timesteps
lifespan_spread = 0.2          #lifetimes vary by about ±20%

#disease parameters
p_catch = .1
p_spread = .05
contacts_per_step = 1
sick_drain = .5
p_recover = .07

#starting colony
start_nurses = 75
start_foragers = 25


#function stores info about new ants

def new_ant(role, energy=start_energy):
    return {
        "role": role,          #nourse/forager
        "energy": energy,      #its energy level
        "crop": 0.0,           #food for sharing
        "trip_timer": 0,       #timesteps left on foragiong trip
        "outside": False,      #true whilst awawys form the enst
        "age": 0,
        "lifespan": max(1, random.gauss(lifespan_mean, lifespan_spread * lifespan_mean)),
        "sick": False,
    }

#decides how much food ant can give
def transfer(amount,     #essentially deef rate
            giver_pool,  #how much is in crop
            ant):        #ant getting fed
    given = min(amount, giver_pool, ant_full - ant["energy"])
    ant["energy"] += given
    return given


#total food held in the nurses' social stomachs = the colony's food store
def nurse_store(ants):
    return sum(a["crop"] for a in ants if a["role"] == "nurse")


#sim
def run_simulation(food_per_trip=food_per_trip, n_steps=n):

    #reset everything
    ants = [new_ant("forager") for _ in range(start_foragers)] + [new_ant("nurse") for _ in range(start_nurses)]
    eggs = []      #each egg is a dict holding how much food it has been fed so far

    #creating lists to store simulation data for plotting
    history = {
        "time": [], "nurses": [], "foragers": [], "total": [],
        "hive": [], "mean_energy": [], "sick": [], "eggs": [],
        "nurse_energy": [], "forager_energy": [],     #average energy of each role
        "nurse_crop": [], "forager_crop": [],         #food held in each role's social stomachs
    }

    #trip cost
    trip_cost = trip_length * forager_trip_drain

    for t in range(n_steps):

        #loses energy by existing
        #checks role of ant, if a forager checks whether it is in the nest, then sets drain accordingly
        for a in ants:
            a["age"] += 1
            if a["role"] == "nurse":
                a["energy"] -= nurse_drain
            elif a["outside"]:
                a["energy"] -= forager_trip_drain
            else:
                a["energy"] -= forager_nest_drain
            if a["sick"]:
                a["energy"] -= sick_drain

        #check if energy reaches 0 or if ant dies from old age
        #(a dead nurse takes the food in its crop with it)
        starved = [a for a in ants if a["energy"] <= 0]
        old = [a for a in ants if a["energy"] > 0 and a["age"] >= a["lifespan"]]
        if starved:
            print(f"t={t}: {len(starved)} ants starved")
        if old:
            print(f"t={t}: {len(old)} ants died of old age")
        ants = [a for a in ants if a["energy"] > 0 and a["age"] < a["lifespan"]]

        nurses = [a for a in ants if a["role"] == "nurse"]

        #forgaers going out and getting food
        for a in [x for x in ants if x["role"] == "forager"]:

            #forgaer is out to forage food, comes back with foodpertrip and less energy
            if a["outside"]:
                a["trip_timer"] -= 1
                if a["trip_timer"] <= 0:
                    roll = random.random()
                    if roll < p_death:
                        ants.remove(a)
                        continue
                    a["outside"] = False
                    if random.random() < p_catch:
                        a["sick"] = True
                    if roll < p_death + p_success:
                        haul = random.gauss(food_per_trip, food_spread * food_per_trip)
                        a["crop"] += max(0.0, haul)   #can't bring back negative food

            # forager tops itself up from its own load first, never from the nurses
            elif a["energy"] < trip_ready and a["crop"] > 0:
                a["crop"] -= transfer(feed_rate, a["crop"], a)

            # forager feeds one nurse directly, mouth to mouth, into the nurse's crop
            # hungriest nurses first, then whichever nurse has the emptiest crop
            elif a["crop"] > 0:
                receivers = [b for b in nurses if b["crop"] < crop_max]
                if receivers:
                    b = min(receivers, key=lambda b: (b["energy"] >= hungry_threshold, b["crop"]))
                    given = min(feed_rate, a["crop"], crop_max - b["crop"])
                    b["crop"] += given
                    a["crop"] -= given
                # if every nurse's crop is full the forager waits in the nest with its load

            #forgarer forages again, only once it has handed over all its food
            elif a["energy"] >= trip_cost * trip_safety: #needs enough energy to go on trip
                a["outside"] = True  #now foraging
                a["trip_timer"] = trip_length  #starts clock

        #disease spreads between ants inside the nest
        in_nest = [a for a in ants if not a["outside"]]
        newly_sick = []
        for a in in_nest:
            if a["sick"]:
                for other in random.sample(in_nest, min(contacts_per_step, len(in_nest))):
                    if other is not a and not other["sick"] and random.random() < p_spread:
                        newly_sick.append(other)
        for a in newly_sick:
            a["sick"] = True

        #sick ants may recover
        for a in ants:
            if a["sick"] and random.random() < p_recover:
                a["sick"] = False

        #nurse eats from its own crop, but only if it is hungry -
        #(otherwise it would hoard the load instead of passing it on)
        for a in nurses:
            if a["crop"] > 0 and a["energy"] < hungry_threshold:
                a["crop"] -= transfer(feed_rate, a["crop"], a)

        #nurses feeding other nurses

        #update list to find hungriest nurses and sort them
        hungry_nurses = sorted([a for a in nurses if a["energy"] < hungry_threshold],
                        key=lambda a: a["energy"])

        #check if a nurse can feed
        for donor in nurses:
            if not hungry_nurses:
                break
            if donor["crop"] <= 0 or donor["energy"] < donor_min:
                continue

            #pick who to feed
            target = next((h for h in hungry_nurses if h is not donor), None)
            if target is None:
                break

            #feeding occurs - target gets feedrate energy
            donor["crop"] -= transfer(feed_rate, donor["crop"], target)
            if target["energy"] >= hungry_threshold:
                hungry_nurses.remove(target)

        #nurses feeding eggs
        #adults come first: eggs only get fed once no nurse is still hungry,
        #the colony is coping, and only from food above the reserve
        mean_energy = sum(a["energy"] for a in ants) / len(ants) if ants else 0.0
        spare = nurse_store(ants) - hive_reserve
        if eggs and not hungry_nurses and mean_energy >= hatch_wellfed:
            for donor in sorted(nurses, key=lambda b: b["crop"], reverse=True):  #fullest crop gives first
                if spare <= 0 or not eggs:
                    break
                if donor["crop"] <= 0 or donor["energy"] < donor_min:
                    continue
                egg = max(eggs, key=lambda e: e["fed"])   #finish the most-fed egg first
                given = min(feed_rate, donor["crop"], spare, hatch_cost - egg["fed"])
                donor["crop"] -= given
                egg["fed"] += given
                spare -= given

                #egg has been fed enough, it hatches into a nurse
                if egg["fed"] >= hatch_cost:
                    eggs.remove(egg)
                    ants.append(new_ant("nurse"))
                    print(f"t={t}: nurse hatched, colony = {len(ants)}")

        #new egg laid if the colony is coping and the nurses are holding a buffer of food
        if len(eggs) < max_eggs and mean_energy >= hatch_wellfed and nurse_store(ants) >= hive_reserve:
            eggs.append({"fed": 0.0})

        # nurse promoting to forager
        n_foragers = sum(1 for a in ants if a["role"] == "forager") # counts foraggers
        n_nurses = len(ants) - n_foragers #counts nurses
        wanted = max(1, math.ceil(len(ants) / ants_per_forager)) # we want specifgic number of ants per forager

        #shortage = fewer than half the foragers we want
        shortage = n_foragers < wanted / 2

        if shortage:
            need_energy = trip_cost * trip_safety   #just enough to survive one trip (30)
            need_age = 0                            #any age will do
            keep_nurses = 1                         #must keep 1 nurse - nurses are now the food store
        else:
            need_energy = promote_energy
            need_age = promote_age
            keep_nurses = min_nurses

        if n_foragers < wanted and n_nurses > keep_nurses:
            eligible = [a for a in ants
                        if a["role"] == "nurse"
                        and a["energy"] >= need_energy
                        and a["age"] >= need_age]
            if eligible:
                promoted = max(eligible, key=lambda a: a["age"])
                promoted["role"] = "forager"
                #promoted ant keeps its crop and, as a forager, hands it back to the nurses
                print(f"t={t}: nurse promoted to forager")

        #recording
        history["time"].append(t)
        history["nurses"].append(sum(1 for a in ants if a["role"] == "nurse"))
        history["foragers"].append(sum(1 for a in ants if a["role"] == "forager"))
        history["total"].append(len(ants))
        history["hive"].append(nurse_store(ants))      #food in nurse crops
        history["mean_energy"].append(sum(a["energy"] for a in ants) / len(ants) if ants else 0.0)
        history["sick"].append(sum(1 for a in ants if a["sick"]))
        history["eggs"].append(len(eggs))
        nurses_now = [a for a in ants if a["role"] == "nurse"]
        foragers_now = [a for a in ants if a["role"] == "forager"]
        #nan when a role has no ants, so the plot shows a gap instead of a fake 0
        history["nurse_energy"].append(sum(a["energy"] for a in nurses_now) / len(nurses_now) if nurses_now else float("nan"))
        history["forager_energy"].append(sum(a["energy"] for a in foragers_now) / len(foragers_now) if foragers_now else float("nan"))
        history["nurse_crop"].append(sum(a["crop"] for a in nurses_now))
        history["forager_crop"].append(sum(a["crop"] for a in foragers_now))
    return nurse_store(ants), history

#plotting

#run the simulation
random.seed(1)                       #change this number to see a different run
_, h = run_simulation(n_steps=5000)

#find when the colony dies out (if it does), and stop the plot just after that
end = len(h["time"])
for t, total in zip(h["time"], h["total"]):
    if total == 0:
        end = t
        break
stop = min(len(h["time"]), end + 100)
time = h["time"][:stop]

#same colour for the same kind of ant on every graph
NURSE = "#2a78d6"     #blue
FORAGER = "#eb6834"   #orange
EGG = "#1baf7a"       #green

#3 graphs stacked on top of each other, sharing the timestep axis
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

#graph 1: how many of each type
ax1.step(time, h["nurses"][:stop], where="post", color=NURSE, label="Nurses")
ax1.step(time, h["foragers"][:stop], where="post", color=FORAGER, label="Foragers")
ax1.step(time, h["eggs"][:stop], where="post", color=EGG, label="Eggs")
ax1.set_title("Population", loc="left", fontweight="bold")
ax1.set_ylabel("count")

#graph 2: average energy of nurses and foragers
ax2.plot(time, h["nurse_energy"][:stop], color=NURSE, linewidth=0.9, label="Nurses")
ax2.plot(time, h["forager_energy"][:stop], color=FORAGER, linewidth=0.9, label="Foragers")
ax2.axhline(hungry_threshold, color="grey", linestyle="--", linewidth=0.8, label="Hungry threshold")
ax2.set_ylim(0, ant_full + 5)
ax2.set_title("Average energy", loc="left", fontweight="bold")
ax2.set_ylabel("energy")

#graph 3: food held in social stomachs (crops)
ax3.plot(time, h["nurse_crop"][:stop], color=NURSE, linewidth=0.9, label="In nurse crops (colony store)")
ax3.plot(time, h["forager_crop"][:stop], color=FORAGER, linewidth=0.9, label="In forager crops (unloading)")
ax3.set_title("Food stored in social stomachs", loc="left", fontweight="bold")
ax3.set_ylabel("food")
ax3.set_xlabel("timestep")
ax3.set_xlim(0, time[-1])

#tidy up all 3 graphs the same way
for ax in (ax1, ax2, ax3):
    ax.grid(axis="y", color="#e4e3df")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="lower right", bbox_to_anchor=(1, 1), ncol=3, frameon=False)
    if end < len(h["time"]):                 #dotted line where the colony died
        ax.axvline(end, color="grey", linestyle=":", linewidth=0.8)

fig.tight_layout()
plt.savefig("colony_plots.png", dpi=150)
plt.show()
