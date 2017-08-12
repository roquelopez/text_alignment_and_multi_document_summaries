# -*- coding: utf-8 -*-
'''
Created on 25/07/2013

@author: roque
'''
 
def viterbi(observations, states, start_probability, transition_probability, emission_probability, positions):
    ''' The Viterbi algorithm, based of the https://gist.github.com/gavinmh/4108961 implementation'''
    trellis = [{}]
    path = {}
     
    for state in states:# path for the first word
        if state in start_probability:
            trellis[0][state] = start_probability[state] * emission_probability[state][observations[0]]
            path[state] = [state]

    for observations_index in range(1,len(observations)):# path for the others words
        trellis.append({})
        new_path = {}

        states1 = positions[observations[observations_index]]

        for state in states1:
            states2 = positions[observations[observations_index-1]]
            
            (probability, possible_state) = max(
            [(trellis[observations_index-1][y0] * transition_probability[y0][state]
            * emission_probability[state][observations[observations_index]], y0) for y0 in states2])
             
            trellis[observations_index][state] = probability
            new_path[state] = path[possible_state] + [state]
     
        path = new_path
     
    states3 = positions[observations[len(observations) - 1]]
    (probability, state) = max([(trellis[len(observations) - 1][state], state) for state in states3])

    return (probability, path[state])
