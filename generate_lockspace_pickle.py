import speeddial
import copy
import pickle
import sys


sys.setrecursionlimit(5000000)
states_reached = {}


SYMBOLS="UDLR"
METHODS=['up','down','left','right']

lock=speeddial.Lock()
step_string = "0" 

#while this script is rather naive, ugly, and unoptimized it only needs to run one time
#it gets all the states and transitions in a walkable static datastrucure which we pickle for later use.

#recursive walk of the length 11 input space
def walk( lock, step_string ):
  #should only hit on the initial state
  if (lock.state() ) not in states_reached:
    print("creating first node in the graph")
    states_reached[(lock.state())] = { 'incoming_right': [], 'incoming_left': [], 'incoming_down': [], 'incoming_up':[] }
    states_reached[(lock.state())]['state'] = lock.state()

  #exit conditions
  #if len(states_reached) == 7501:
  #  return
  if len(step_string) > 12:
    return
  
  for direction in METHODS:
     ##don't do five in a row unless we are fresh off the reset
     #if len(step_string) > 6 and step_string[-5:] == SYMBOLS[METHODS.index(direction)] * 5:
     #  return
     new_lock = speeddial.Lock(lock.state())
     getattr(new_lock, direction )()

     if (new_lock.state() ) not in states_reached:
       print ("we have reached %s/7501 states" % len(states_reached) )
       states_reached[(new_lock.state())] = { 'input_sequences_from_reset': [], 'incoming_right': None, 'incoming_left': None, 'incoming_down': None, 'incoming_up':None }
       states_reached[(new_lock.state())]['state'] = new_lock.state()
       
     states_reached[lock.state()][direction] = states_reached[new_lock.state()]
     states_reached[new_lock.state()]['incoming_' + direction ] = ( states_reached[lock.state()] )
     #remember that
     new_step_string = "%s%s" % ( step_string, SYMBOLS[METHODS.index(direction)])
     states_reached[new_lock.state()]['input_sequences_from_reset'].append( new_step_string )
     states_reached[new_lock.state()]['input_sequences_from_reset'].sort(key=len)
     #call ourself
     walk( speeddial.Lock(new_lock.state()) , new_step_string)

walk(lock,step_string)

##we got all 7501 states but need to clean up what transitions we missed
## bc so far we have just exhausted the wheel state space, not the transition space
## actually: this was just to work around bugs but I leave it in here to be safe
print("filling in missing transitions")
for state in states_reached:
  for direction in METHODS:
    if direction not in states_reached[state]:
     print("cleaning up for %s %s" % (state, direction))
     new_lock = speeddial.Lock(state)
     getattr(new_lock, direction)
     states_reached[state][direction] = states_reached[new_lock.state()]
     states_reached[new_lock.state()]['incoming_' + direction ].append( states_reached[state] )
    
print("pickling")

with open('speeddial5.pickle', 'wb') as handle:
    pickle.dump(states_reached, handle, protocol=pickle.HIGHEST_PROTOCOL)


