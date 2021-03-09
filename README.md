# speeddial_research
My speed dial research


This is the UGLY code I use to generate a 500MB  pickle file with all 11 direction inputs, as well as all state transitions forwards and backwards.  I will eventually export this into a graph database but the python dict is usable if a bit cumbersome.

Here's how you might want to use it.

Generate the pickle file with walk.py  (it takes many hours on my slow computer,  the walk is not paralellized across cores)

This pickle contains a cyclical graph in the form of a dict that contains references to its own elements.  Because of that, if you try to get the string representation of the entire dict, python will walk forever lol.  Get Ctrl+C ready.

Open it in a python shell and explore:

    >>> f = open('speeddial5.pickle', 'rb')
    >>> lockspace = pickle.load(f)
    >>> #find all states with (4,-1) as the top gate and (3,0) as the right gate
    >>> a = filter( lambda x: (x[0] == (4,-1)) and (x[1] == (3,0)), lockspace.keys() )
    >>> len(a)
    75
    >>> #get a list of shortest sequence to reach each those 75 states  (overlapping brute force seems not possible here do you disagree?)
    >>> codes.sort(key=len)
    >>> print("  ".join(codes))
    0UUUR  0UURR  0URRR  0LLRRR  0LUUUR  0UUDUR  0LURRR  0UURDR  0URDRR  0LUURR  0UUDRR  0UDURR  0RLLRR  0UUULR  0UDRRR  0URLRR  0UULRR  0ULRRR  0UUUDR  0UURLR  0LUUUDR  0UUDLUR  0DLLRRR  0UUDULR  0UUUDLR  0LLRLRR  0LLDRRR  0UDUDRR  0DLLURR  0DLLUUR  0UUDLRR  0UDLURR  0UUDUDR  0LLLDDRR  0DDLLLUR  0UDDULLR  0UUDUDLR  0UDDLLUR  0LLUDDRR  0UUDDLLR  0UDLLDRR  0DLLRDRR  0LUUUDLR  0LLUDDUR  0DLLLDRR  0UUDLRDR  0DUDLLUR  0UUDLUDR  0DUDLLRR  0UUDLLDR  0UDDLLRR  0DDLLLRR  0LLUUDDR  0LUUDLUR  0DUDLLRUR  0UDDLLLDR  0DDLLLRUR  0DDLLLLDR  0LLLUDDDR  0UUDLUDLR  0UDUDDLLR  0UDDDLLLR  0LUUDDLLR  0LUDDLLUR  0LUUDLUDR  0DUDDLLLR  0LLLLDDDR  0UDDLLUDR  0DDDDDUURR  0LUDLUDLUR  0LUDDLLUDR  0UDDLUDLLR  0DDDDDUUUR  0LUDDLLRUR  0UUUUUDLURRR



Here is a description of the data structure
the dict is 7500 (reset not included initally)  nodes (which are also dicts) keyed on a tuple representing the state,  the key is also repeated in the sub-key called 'state'

state: the tuple of the 4 wheels coordinates
[right|left|up|down]: a reference to the state node reached when a that move is given
incoming_[right|left|up|down]: a reference to the state before us (if any)  that reaches us via a move
input_sequences_from_reset: a list of combinations seen to reach this state during the 11 move brute force.





The speeddial.py came from this gist,  I wish I knew the source so I can credit and respect licensing.

https://gist.github.com/rasher/f49c146de01ef0a374e48c2ed7f7c8f6

