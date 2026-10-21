from parameters import *

def run_simulation(food_per_trip):

    #reset everything
    nurses = []                 #starting energy level of nurses
    foragers = []             #starting energy level of forager
    hive_food = 0                          #amount of food in the hive
    trip_timers = []                      #timers for foraging trips                  
    foraged_food = 0                       #defining variable     

    for i in range(starting_foragers):
        foragers.append(forager_start)
        trip_timers.append(0)

    for i in range(starting_nurses):
        nurses.append(nurse_start)

    #creating lists to store simulation data for plotting
    time_history = []
    forager_history = []
    nurse_history = []
    hive_history = []
    nurse_count_history = []

    for i in range(n):

        #loses energy by existing
        for t in range(len(foragers)):
            foragers[t] -= drain
        #whole list of nurses lose energy
        for t in range(len(nurses)):
            nurses[t] -= drain

        #if energy levels reach 0 for either they die
        for t in range(len(foragers)):
            if foragers[t] <= 0:
                print("forager", t, "starved")
                foragers = [energy for energy in foragers if energy > 0]
                break
        
        for t in range(len(nurses)):
            if nurses[t] <= 0:
                print("nurse", t, "starved")
                nurses = [energy for energy in nurses if energy > 0]
                break

        #simulates the time taken to forage
        for t in range(len(foragers)):
            if trip_timers[t] > 0:
                trip_timers[t] -= 1
                foragers[t] -= drain
            if trip_timers[t] == 0:
                #for simplicity, modelling that forager returns with a fixed amount of food per trip and it doesnt matter at what point it finds it
                    foragers[t] += food_per_trip

        #if any forager is hungry it forages
        for t in range(len(foragers)):
            if foragers[t] < forager_threshold and trip_timers[t] == 0:
                trip_timers[t] = trip_length

        #if foragers not hungry it feeds nurse after feeding itself to full and surplus food is stored in hive
        else:      
            for t in range(len(nurses)):
                while (nurses[t] < nurse_threshold and nurses[t] < ant_full and foraged_food > 0):
                    food_given = min(feed_rate, foraged_food)
                    foraged_food -= food_given
                    nurses[t] += food_given
                
            hive_food += foraged_food
            foraged_food = 0

        while hive_food >= hatch_cost:
            hive_food -= hatch_cost
            nurses.append(nurse_start)
            print("Nurse", len(nurses), "hatched at time", i)

        nurse_count_history.append(len(nurses))
    
    return hive_food, nurse_count_history