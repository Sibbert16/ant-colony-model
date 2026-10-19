import matplotlib.pyplot as plt

#parameters

forager_start = 50                     #starting energy level of forager
nurse_start = 50                       #starting energy level of nurse
forager_threshold = 50                 #if forgarer or nurse goes below this energy level he will go out to forage food
nurse_threshold = 30                   #if nurse 
trip_length = 20                       #timesteps to go out and forage
food_per_trip = 100                    #energy levels gained per trip
drain = 1                              #energy level(s) lost per timestep
timestep = 1                           #timestep
feed_rate = 5                          #rate at which forager feeds nurse
n = 200                                #number of timesteps to simulate

forager_energy = forager_start         #starting energy level of forager
nurse_energy = nurse_start             #starting energy level of nurse
hive_food = 0                          #amount of food in the hive
trip_timer = 0                         #timer for foraging trips
food_per_trip = 100                      #amount of food foraged pert trip  
foraged_food = 0                       #defining variable     

#creating lists to store simulation data for plotting
time_history = []
forager_history = []
nurse_history = []
hive_history = []

for i in range(n):

    # loses energy by existing
    forager_energy -= drain
    nurse_energy -= drain

    #if energy levels reach 0 for either they die
    if forager_energy <= 0:
        print("forager starved")
        break
    if nurse_energy <= 0:
        print("nurse starved")
        break

    #simulates the time taken to forage
    if trip_timer > 0:
        trip_timer -= 1
        if trip_timer == 0:
            #for simplicity, modelling that forager returns with a fixed amount of food per trip and it doesnt matter at what point it finds it
            foraged_food = food_per_trip

    #if trip is complete forager feeds itself to full at a rate of 5 units/s
    elif  forager_energy < 100 and foraged_food > 0:
        forager_energy += 5
        foraged_food -= 5

    #if forager is hungry it forages
    elif forager_energy < forager_threshold:
        trip_timer = trip_length

    #if forager not hungry it feeds nurse after feeding itself to full and surplus food is stored in hive
    else:      
        hive_food += foraged_food
        forager_energy -= 5
        nurse_energy += 5


    #stores data per timestep
    time_history.append(i)
    forager_history.append(forager_energy)
    nurse_history.append(nurse_energy)
    hive_history.append(hive_food)
    print(nurse_energy, forager_energy, hive_food)

plt.figure(figsize=(10,5))

plt.plot(time_history, forager_history, label="Forager")
plt.plot(time_history, nurse_history, label="Nurse")

plt.xlabel("Time step")
plt.ylabel("Energy")
plt.title("Ant energy over time")

plt.legend()

plt.show()

plt.figure(figsize=(10,5))

plt.plot(time_history, hive_history, label="Hive Food")

plt.xlabel("Time step")
plt.ylabel("Hive food")
plt.title("Stored hive food over time")

plt.legend()

plt.show()

