class Poker:
    def __init__(self, cards) -> None:
        self.cards = cards
    def findOptimalHand(self):
        '''Finds the best hand that can be made with cards'''
        pass
    
    def checkStraight(self):
        '''Helper method to check if a straight can be made with cards'''
        pass

    def checkRankMatches(self):
        '''Helper method to check if pair, three of a kind, or full house can
        be made with cards'''
        pass

    def checkFlush(self):
        '''Helper method to check if flush can be made with cards'''
        pass

if __name__ == '__main__':
    hand1 = Poker(['2S', '3H', '5S', '6D', '7C', 'QS', 'KS'])
    print(hand1.findOptimalHand())