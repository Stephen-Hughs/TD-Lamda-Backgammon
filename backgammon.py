#!C:\Users\Lee\AppData\Local\Programs\Python\Python38-32\python.exe

import random
import copy
import sys
from TD_Gammon import *

sys.setrecursionlimit(10000)

class Game:
    def __init__(self):
        self.board = [
                ["b", "b"],
                [],
                [],
                [],
                [],
                ["a","a","a","a","a"],
                [],
                ["a","a","a"],
                [],
                [],
                [],
                ["b","b","b","b","b"],
                ["a","a","a","a","a"],
                [],
                [],
                [],
                ["b","b","b"],
                [],
                ["b","b","b","b","b"],
                [],
                [],
                [],
                [],
                ["a","a"],
                ]
        self.player = "a"
        self.bar = [0,0]
        self.borne = [0,0]
        self.dice = [None, None]
        self.moves = []
        self.winner = None
    def rollDice(self):
        self.dice[0] = random.randint(1,6)
        self.dice[1] = random.randint(1,6)
        if(self.dice[0] == self.dice[1]):
            self.moves = [self.dice[0],self.dice[0],self.dice[0],self.dice[0]]
        else:
            self.moves = [self.dice[0],self.dice[1]]
    def checkWinner(self):
        if(self.borne[0] == 15):
            self.winner = "a"
            return True
        if(self.borne[1] == 15):
            self.winner = "b"
            return True
        return False

    def can_bourne_off(self):
        if(self.bar[(0 if (self.player == "a") else 1)] > 0 ):
            return False
        if(self.player == "b"):
            for x in range(18):
                if("b" in self.board[x]):
                    return False
        else:
            for x in range(18,24):
                if("a" in self.board[x]):
                    return False
        return True;
        
    
    def executeMoves(self, moves):
        #we assume all moves are valid
        for move in moves:
            #if moving off the bar
            if(move[0] == -1):
                temp = self.player
                #if moving to enemy occupied point
                if(len(self.board[move[1]]) == 1 and self.board[move[1]][0] == ("a" if (self.player == "b") else "b")):
                    self.bar[(0 if (self.player == "b") else 1)] += 1
                    self.board[move[1]][0] = temp
                #if not moving to enemy occupied point
                else:
                    self.board[move[1]].append(temp)
                self.bar[(0 if (self.player == "a") else 1)] -= 1
            #if not moving from off the bar
            else:
                temp = self.board[move[0]].pop()
                #if not boarding off
                if(move[1] < 24):
                    #if moving to enemy occupied point
                    if(len(self.board[move[1]]) == 1 and self.board[move[1]][0] == ("a" if (self.player == "b") else "b")):
                        self.bar[(0 if (self.player == "b") else 1)] += 1
                        self.board[move[1]][0] = temp
                    #if not moving to enemy occupied point
                    else:
                        self.board[move[1]].append(temp)
                #if boarding off
                else:
                    self.borne[(0 if (self.player == "a") else 1)] += 1

def get_possible_states(game, movesRef):
    moves = movesRef[:]
    states = []
    cbo = game.can_bourne_off();
    dirx = (1 if (game.player == "b") else -1)
    if(len(moves) == 1):
        if(game.bar[(0 if (game.player =="a") else 1)] > 0):
            #you need to get off the bar
            if(game.player == "a"):
                if(len(game.board[24-moves[0]]) < 2 or game.board[24-moves[0]][1] == game.player):
                    temp = copy.deepcopy(game)
                    temp.executeMoves([[-1,24-moves[0]]])
                    temp.player = ("a" if (temp.player == "b") else "b")
                    temp.dice = [None, None]
                    temp.moves = []
                    states.append(temp)
            else:
                if(len(game.board[moves[0]]) < 2 or game.board[moves[0]][1] == game.player):
                    temp = copy.deepcopy(game)
                    temp.executeMoves([[-1,moves[0]]])
                    temp.player = ("a" if (temp.player == "b") else "b")
                    temp.dice = [None, None]
                    temp.moves = []
                    states.append(temp)
        else:
            for x in range(24):
                if(game.player in game.board[x]):
                    #piece exists here. see if you can move
                    if(cbo and (x + (dirx*moves[0]) > 23 or x + (dirx*moves[0]) < 0)):
                        #bourne off
                        temp = copy.deepcopy(game)
                        temp.executeMoves([[x,24]])
                        temp.player = ("a" if (temp.player == "b") else "b")
                        temp.dice = [None, None]
                        temp.moves = []
                        states.append(temp)
                    elif((x + (dirx*moves[0]) < 24 and x + (dirx*moves[0]) > -1) and (len(game.board[x+(dirx*moves[0])]) < 2 or game.board[x+(dirx*moves[0])][1] == game.player)):
                        #not bourne off
                        temp = copy.deepcopy(game)
                        temp.executeMoves([[x,x+(dirx*moves[0])]])
                        temp.player = ("a" if (temp.player == "b") else "b")
                        temp.dice = [None, None]
                        temp.moves = []
                        states.append(temp)
        if(len(states) == 0):
            states.append(game)
        return states;
    #do stuff
    if(len(moves) > 1 and moves[0] == moves[1]):
        #rolled doubles: check each point on board
        if(game.bar[(0 if (game.player == "a") else 1)] == 0):
            #no pieces on the bar
            for x in range(24):
                if(game.player in game.board[x]):
                    #piece exists here. see if you can move
                    if(cbo and (x + (dirx*moves[0]) > 23 or x + (dirx*moves[0]) < 0)):
                        #bourne off
                        temp = copy.deepcopy(game)
                        temp.executeMoves([[x,24]])
                        states.extend(get_possible_states(temp, moves[:-1]))
                    elif((x + (dirx*moves[0]) < 24 and x + (dirx*moves[0]) > -1) and (len(game.board[x+(dirx*moves[0])]) < 2 or game.board[x+(dirx*moves[0])][1] == game.player)):
                        #not bourne off
                        temp = copy.deepcopy(game)
                        temp.executeMoves([[x,x+(dirx*moves[0])]])
                        states.extend(get_possible_states(temp, moves[:-1]))
        else:
            #need to get off the bar
            if(game.player == "a"):
                if(len(game.board[24-moves[0]]) < 2 or game.board[24-moves[0]][1] == game.player):
                    temp = copy.deepcopy(game)
                    temp.executeMoves([[-1,24-moves[0]]])
                    states.extend(get_possible_states(temp, moves[:-1]))
            else:
                if(len(game.board[moves[0]]) < 2 or game.board[moves[0]][1] == game.player):
                    temp = copy.deepcopy(game)
                    temp.executeMoves([[-1,moves[0]]])
                    states.extend(get_possible_states(temp, moves[:-1]))
    else:
        #assume len(moves) = 2
        for move in moves:
            if(game.bar[(0 if (game.player =="a") else 1)] > 0):
                #you need to get off the bar
                if(game.player == "a"):
                    if(len(game.board[24-move]) < 2 or game.board[24-move][1] == game.player):
                        temp = copy.deepcopy(game)
                        tempMoves = moves[:]
                        temp.executeMoves([[-1,24-move]])
                        tempMoves.remove(move)
                        states.extend(get_possible_states(temp, tempMoves))
                else:
                    if(len(game.board[move]) < 2 or game.board[move][1] == game.player):
                        temp = copy.deepcopy(game)
                        tempMoves = moves[:]
                        temp.executeMoves([[-1,move]])
                        tempMoves.remove(move)
                        states.extend(get_possible_states(temp, tempMoves))
            else:
                for x in range(24):
                    if(game.player in game.board[x]):
                        #piece exists here. see if you can move
                        if(cbo and (x + (dirx*move) > 23 or x + (dirx*move) < 0)):
                            #bourne off
                            temp = copy.deepcopy(game)
                            tempMoves = moves[:]
                            temp.executeMoves([[x,24]])
                            tempMoves.remove(move)
                            states.extend(get_possible_states(temp, tempMoves))
                        elif((x + (dirx*move) < 24 and x + (dirx*move) > -1) and (len(game.board[x+(dirx*move)]) < 2 or game.board[x+(dirx*move)][1] == game.player)):
                            #not bourne off
                            temp = copy.deepcopy(game)
                            tempMoves = moves[:]
                            temp.executeMoves([[x,x+(dirx*move)]])
                            tempMoves.remove(move)
                            states.extend(get_possible_states(temp, tempMoves))
    return states
def get_input_data(game):
    data = [None] * 198
    for x in range(len(game.board)):
        data[8*x] = (1 if ('a' in game.board[x]) else 0)
        data[8*x+1] = (1 if (game.board[x].count('a') > 1) else 0)
        data[8*x+2] = (1 if (game.board[x].count('a') > 2) else 0)
        if(game.board[x].count('a') > 3):
            data[8*x+3] = game.board[x].count('a')/2
        else:
            data[8*x+3] = 0
        data[8*x+4] = (1 if ('b' in game.board[x]) else 0)
        data[8*x+5] = (1 if (game.board[x].count('b') > 1) else 0)
        data[8*x+6] = (1 if (game.board[x].count('b') > 2) else 0)
        if(game.board[x].count('b') > 3):
            data[8*x+7] = game.board[x].count('b')/2
        else:
            data[8*x+7] = 0
    data[192] = (1 if (game.player == 'a') else 0)
    data[193] = (1 if (game.player == 'b') else 0)
    data[194] = game.bar[0]/2
    data[195] = game.bar[1]/2
    data[196] = game.borne[0]
    data[197] = game.borne[1]
    return data

def get_weights(net):
    weights = []
    for layer in net.layers:
        layer_w = []
        for node in layer:
            node_w = []
            for w in node.out_con:
                node_w.append(w.weight)
            layer_w.append(node_w)
        weights.append(layer_w)
    return weights

def get_biases(net):
    biases = []
    for node in net.layers[1]:
        biases.append(node.bias)
    biases.append(net.layers[2][0].bias)
    return biases

if __name__ == '__main__':
    print("start program")
    game = Game()
    print(vars(game))
    for point in game.board:
        print(point)
    tdg = Network()

    #setting up the network
    input_layer = []
    for x in range(198):
        input_layer.append(Neuron())
    hidden_layer = []
    for x in range(50):
        hidden_layer.append(Neuron())
    output_layer = [Neuron()]

    #connecting all the nodes
    for in_node in input_layer:
        for out_node in hidden_layer:
            in_node.add_connection(out_node, 1)
    for in_node in hidden_layer:
        for out_node in output_layer:
            in_node.add_connection(out_node, 1)

    tdg.layers = [input_layer, hidden_layer, output_layer]

    #loading the weights from json file
    with open("weights.json") as json_file:
        weight_data = json.load(json_file)
        tdg.load_weights(weight_data)

    #loading the biases from json file
    with open("bias.json") as json_file:
        bias_data = json.load(json_file)
        tdg.load_biases(bias_data)

    #declare some constants
    lmbda = 0.5
    alpha = 2


    #loop through a game simulation    
    old_model = None
    game_num = 0

    while(game_num < 1000):
        #set up eligibility trace vector
        eTrace = [ [ [0]*50 ] * 198, [0]*50, [0]*51 ]
        step = 1
        old_score = 0
        score = 0
        game = Game()
        while(game.winner == None):
            #print("Move: ", step)
            game.rollDice()
            #print("Dice Roll: ",game.dice)
            states = get_possible_states(game,game.moves)
            old_board = copy.deepcopy(game)
            if(len(states) > 0):
                game = random.choice(states)
                odds = []
                for state in states:
                    #run input data through the network
                    data = get_input_data(state)
                    tdg.load_input(data)
                    for node in tdg.layers[0]:
                        node.send_output()
                    for node in tdg.layers[1]:
                        node.send_output()
                    odds.append(tdg.layers[2][0].get_output())
                    tdg.clear_inputs()
                game = (states[odds.index(max(odds))] if (game.player == "a") else states[odds.index(min(odds))])
                score = ( max(odds) if (game.player == "a") else min(odds) )
                data = get_input_data(old_board)
                tdg.load_input(data)
                for node in tdg.layers[0]:
                    node.send_output()
                for node in tdg.layers[1]:
                    node.send_output()
            else:
                game.player = ("a" if game.player == "b" else "b")
            #for point in game.board:
                #print(point)
            game.checkWinner()
            if(game.winner != None):
                score = (1 if (game.winner == "a") else 0)
            #backprop
            if(step > 1):
                old_model = copy.deepcopy(tdg)
                backprop(tdg, old_model, score, old_score, alpha, lmbda, eTrace)
            old_score = score
            step += 1
        game_num += 1
        print("finished game: ", game_num)
        if(game_num % 100 == 0):
            new_w = get_weights(tdg) 
            with open("new_weights.json","w") as weight_file:
                weight_file.write(json.dumps(new_w))
                weight_file.close()
            new_b = get_biases(tdg) 
            with open("new_bias.json","w") as bias_file:
                bias_file.write(json.dumps(new_b))
                bias_file.close()



