import matplotlib.pyplot as plt



#parameters

forager_start = 50                     #starting energy level of forager
nurse_start = 50                       #starting energy level of nurse
forager_threshold = 50                 #if forager or nurse goes below this energy level he will go out to forage food
nurse_threshold = 50                   #if nurse has less than this energy level it will be fed by forager
trip_length = 15                       #timesteps to go out and forage
food_per_trip = 100                    #food foraged gained per trip
drain = 1                              #energy level(s) lost per timestep
timestep = 1                           #timestep
feed_rate = 15                          #rate at which forager feeds nurse
n = 400                                #number of timesteps simulate
ant_full = 70                          #max amount of energy an ant can have
hatch_cost = 50                        #hive energy cost of hatching a new ant

def run_simulation(food_per_trip):

    #reset everything
    forager_energy = forager_start         #starting energy level of forager
    nurses = [nurse_start]             #starting energy level of nurse
    hive_food = 0                          #amount of food in the hive
    trip_timer = 0                         #timer for foraging trips                  
    foraged_food = 0                       #defining variable     

    #creating lists to store simulation data for plotting
    time_history = []
    forager_history = []
    nurse_history = []
    hive_history = []
    nurse_count_history = []

    for i in range(n):

        #loses energy by existing
        forager_energy -= drain
        #whole list of nurses lose energy
        for t in range(len(nurses)):
            nurses[t] -= drain

        #if energy levels reach 0 for either they die
        if forager_energy <= 0:
           print("forager starved")
           break
        
        for t in range(len(nurses)):
            if nurses[t] <= 0:
                print("nurse", t, "starved")
                nurses = [energy for energy in nurses if energy > 0]
                break

        #simulates the time taken to forage
        if trip_timer > 0:
            trip_timer -= 1
            if trip_timer == 0:
                #for simplicity, modelling that forager returns with a fixed amount of food per trip and it doesnt matter at what point it finds it
               foraged_food = food_per_trip

        #if trip is complete forager feeds itself to full at a rate of 5 units/s
        elif  forager_energy < ant_full and foraged_food > 0:
           food_given = min(feed_rate, foraged_food)
           forager_energy += food_given
           foraged_food -= food_given

        #if forager is hungry it forages
        elif forager_energy < forager_threshold:
            trip_timer = trip_length

        #if forager not hungry it feeds nurse after feeding itself to full and surplus food is stored in hive
        else:      
            for t in range(len(nurses)):
                while (nurses[t] < nurse_threshold and nurses[t] < ant_full and foraged_food > 0):
                    food_given = min(feed_rate, foraged_food)
                    foraged_food -= food_given
                    nurses[t] += food_given
                    print(f"Fed nurse {t}: energy = {nurses[t]}, food left = {foraged_food}")
                
            hive_food += foraged_food
            foraged_food = 0

        print(f"t={i}, hive={hive_food}, carried={foraged_food}, nurses={len(nurses)}")

        while hive_food >= hatch_cost:
            hive_food -= hatch_cost
            nurses.append(nurse_start)
            print("Nurse", len(nurses), "hatched at time", i)

        nurse_count_history.append(len(nurses))
    
    return hive_food, nurse_count_history  #len(nurses)

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

final_food, nurse_count_history = run_simulation(food_per_trip)
plt.figure(figsize=(10,5))

plt.plot(range(n), nurse_count_history)

plt.xlabel("Time step")
plt.ylabel("Number of nurses")
plt.title("Colony growth over time")

plt.show()