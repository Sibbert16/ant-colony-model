#parameters

n = 5000                  #timesteps to simulate

#energy levels
ant_full = 70.0                #most energy an ant can hold
start_energy = 50.0            #energy a newly hatched / starting ant has
hungry_threshold = 50.0                  #below this an ant wants feeding

# energy lost per timestep ***** one of changes we made
nurse_drain = 0.5              #nurses sit still in the nest, cheapest
forager_nest_drain = 0.8       #forager resting in the nest
forager_trip_drain = 1.6       #forager outside, walking and searching

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
lifespan_mean = 200            #average lifetime in timesteps
lifespan_spread = 0.2          #lifetimes vary by about ±20%

#disease parameters
p_catch = .1
p_spread = .05
contacts_per_step = 1
sick_drain = .5
p_recover = .07