# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 2020

@author: dinerd
"""

import testUtility

#Get player names
player_names = testUtility.get_player_names()

#number of curses and victory cards
nV = testUtility.get_num_victory_cards(player_names)
nC = testUtility.get_num_curse_cards(player_names)

"""
Test Case: Increase the number of victory cards
"""
nV = 50

#Define box
box = testUtility.get_box(nV)

supply_order = testUtility.get_supply_order()

#Pick 10 cards from box to be in the supply and teh cards which are always in supply
supply = testUtility.get_supply(box, player_names, nV, nC)

#initialize the trash
trash = testUtility.get_trash()

#Costruct the Player objects
players = testUtility.get_players(player_names)

#Play the game
testUtility.play_game(supply, supply_order, players, trash)
            

#Final score
testUtility.print_final_score(players)