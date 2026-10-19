#parameters

forager_start = 50                    #starting energy level of forager
nurse_start = 50                       #starting energy level of nurse
forager_threshold = 50                 #if forgarer or nurse goes below this energy level he will go out to forage food
nurse_threshold = 30                   #if nurse 
trip_length = 20                       #timesteps to go out and forage ----- randomize later
food_per_trip = 100                    #energy levels gained per trip
drain = 1                              #energy level(s) lost per timestep
timestep = 1                           #timestep
feed_rate = 5
n = 200

forager_energy = forager_start
nurse_energy = nurse_start
hive_food = 0
trip_timer = 0
foraged_food = 0

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

    if trip_timer > 0:
        trip_timer -= 1
        if trip_timer == 0:
            foraged_food = 100

    elif  forager_energy < 100 and foraged_food > 0:
        forager_energy += 5
        foraged_food -= 5
    
    elif forager_energy < forager_threshold:
        trip_timer = trip_length

    else:      
        hive_food += foraged_food
        forager_energy -= 5
        nurse_energy += 5
    print(nurse_energy, forager_energy, hive_food)