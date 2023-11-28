# prisoners dilemma:
# |  |  C  |  D  |
# |C | 1/1 | 3/0 |
# |D | 3/0 | 2/2 |

from random import randint
import matplotlib.pyplot as plt

class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.p1_score = 0 
        self.p2_score = 0
        self.scoring_matrix = {
            'CC': [1, 1], 
            'CD': [3, 0], 
            'DC': [0, 3], 
            'DD': [2, 2]
            }

    def play_round(self):
        p1_move = self.p1.play()
        p2_move = self.p2.play()
        self.p1.update_strat(p2_move)
        self.p2.update_strat(p1_move)
        score = self.scoring_matrix[p1_move + p2_move]
        self.p1_score += score[0]
        self.p2_score += score[1]

    def award_scores(self):
        self.p1.total_years += self.p1_score
        self.p2.total_years += self.p2_score

class Player:
    def __init__(self, Strategy, idx):
        self.total_years = 0
        self.strategy = Strategy()
        self.idx = idx
    def play(self):
        return self.strategy.play()
    def reset_strat(self):
        self.strategy.reset_state()
    def update_strat(self, opponent_move):
        self.strategy.update_state(opponent_move)
    def name(self):
        return(self.strategy.name() + "_" + str(self.idx))

class TitForTat():
    def __init__(self):
        self.reset_state()
    def reset_state(self):
        self.state = 'C'
    def play(self):
        return self.state
    def update_state(self, opponent_move):
        self.state = opponent_move
    def name(self):
        return 'T'

class Hawk():
    def __init__(self):
        self.reset_state()
    def reset_state(self):
        self.state = 'D'
    def play(self):
        return self.state
    def update_state(self, opponent_move):
        pass
    def name(self):
        return 'H'

class Random():
    def __init__(self, ratio=0.7):
        self.ratio = ratio
        self.reset_state()
    def reset_state(self):
        if(randint(0, 1)<self.ratio):
            self.state = 'C'
        else:
            self.state = 'D'
    def play(self):
        return self.state
    def update_state(self, opponent_move):
        self.reset_state()
    def name(self):
        return 'R'
    
class Grudge():
    def __init__(self):
        self.reset_state()
    def reset_state(self):
        self.state = 'C'
    def play(self):
        return self.state
    def update_state(self, opponent_move):
        if(opponent_move == 'D'):
            self.state = 'D'
    def name(self): 
        return 'G'

class Dove():   
    def __init__(self):
        self.reset_state()
    def reset_state(self):
        self.state = 'C'
    def play(self):
        return self.state
    def update_state(self, opponent_move):
        pass
    def name(self):
        return 'D'
    
class Tournament():
    def __init__(self, classes, distribution):
        self.iteration = 0
        self.classes = classes
        self.distribution = distribution
        self.players = []
        for i in range(len(classes)):
            for j in range(distribution[i]):
                self.players.append(Player(classes[i], idx=j))
        self.names = [player.name() for player in self.players]
        self.colour_dict = {
            classes[0]: 'red',
            classes[1]: 'blue',
            classes[2]: 'green',
            classes[3]: 'black',
            classes[4]: 'purple'
        }
        self.colours = [self.colour_dict[player.strategy.__class__] for player in self.players]

    def plot_scores(self):
        x = self.names
        y = [player.total_years for player in self.players]
        L = sorted(zip(x, y, self.colours), key=lambda x: x[1], reverse=True)
        x, y, new_colours = zip(*L)
        plt.bar(x, y, color=new_colours)
        plt.savefig('scores_' + str(self.iteration) + '.png')

    def run_all_v_all(self, rounds=100):
        self.iteration+=1
        for i in range(len(self.players)):
            for j in range(i+1, len(self.players)):
                game = Game(self.players[i], self.players[j])
                for k in range(100):
                    game.play_round()
                game.award_scores()

def main():
    tournament = Tournament([TitForTat, Hawk, Random, Grudge, Dove], [1, 1, 1, 1, 1])
    tournament.run_all_v_all()
    tournament.plot_scores()

if __name__ == '__main__':
    main()