from heapq import heapify, heappop, heappush

class Result:
    def __init__(self, handName, handCards) -> None:
        self.handName = handName
        self.handCards = handCards

    def __repr__(self) -> str:
        return f"Best Hand: {self.handName} Cards: {self.handCards}\n -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --"

class Poker:
    def __init__(self, cards) -> None:
        self.rankMapper={'J': 11, 'Q':12, 'K':13, 'A':14}
        self.cards = cards
        self.suits = {'D': [], 'S': [], 'C': [], 'H': []}
        self.ranks = {2: [], 3: [], 4:[], 5: [], 6:[], 7: [], 8: [], 9:[], 10: [], 11: [], 12: [], 13:[], 14:[]}
        

    def findOptimalHand(self):
        '''Finds the best hand that can be made with cards'''
        self.populateRanksAndSuits()

        # find pairs, trios, and full houses
        bestPairRank, bestTrioRank = self.checkRankMatches()

        if bestPairRank > 0 and bestTrioRank > 0:
            return Result(handName='Full House', handCards=self.ranks[bestPairRank] + self.ranks[bestTrioRank])
        
        flushSuit, flush = self.checkFlush()
        if flushSuit:
            return Result(handName='Flush', handCards=flush)
        
        straightExists, selectedCards, highestRank  = self.checkStraight()
        if straightExists:
            return Result(handName='Straight', handCards=selectedCards)
        
        if bestTrioRank > 0:
            if len(self.ranks[bestTrioRank]) >= 4:
                return Result(handName="Four of a Kind", handCards=self.ranks[bestTrioRank])
            else:
                return Result(handName="Three of a Kind", handCards=self.ranks[bestTrioRank])
        
        if bestPairRank > 0:
            return Result(handName="Pair", handCards=self.ranks[bestPairRank])
        
        else:
            return Result(handName="High Card", handCards=self.highestCardHand(highestRank))
    
    def highestCardHand(self, highestRank):
        '''Given the highestRank it gets the high card and then fills the rest of the hand
        with other cards'''
        hand = set()
        hand.add(self.ranks[highestRank][0])
        i = 0
        while len(self.cards) > i and len(hand) < 5:
            hand.add(self.cards[i])
            i+=1

        return list(hand)

    def checkStraight(self):
        '''Helper method to check if a straight can be made with cards'''
        # store this card in the scenario where High Card is the best hand
        highestRank = -1
        
        streak = None
        selectedCards = []
        for rank in range(14, 1, -1):
            if streak:
                # stop once streak is at len 5
                if len(streak) == 5:
                    break
                
                # if current rank is in hand
                if self.ranks[rank]:

                    # is it the next in the streak?
                    if rank == streak[-1]-1:
                        streak.append(rank)
                        selectedCards.append(self.ranks[rank][0])
                    else:
                        streak = [rank]
                        selectedCards = [self.ranks[rank][0]]
                else:
                    streak = None
                    selectedCards = []

            # for first time building streak
            else:
                if self.ranks[rank]:
                    streak = [rank]
                    selectedCards.append(self.ranks[rank][0])

            # update highestRank
            if self.ranks[rank]:
                highestRank = max(highestRank, rank)
        

        return len(selectedCards) == 5, selectedCards, highestRank


    def checkRankMatches(self):
        '''Helper method to check if pair, three of a kind, or full house can
        be made with cards'''
        bestPairRank  = -1
        bestTrioRank = -1
        for r in self.ranks:
            length = len(self.ranks[r]) 
            if length > 2:
                bestTrioRank = max(bestTrioRank, r)
            elif length == 2:
                bestPairRank = max(bestPairRank, r)
        return bestPairRank, bestTrioRank

    def checkFlush(self):
        '''Helper method to check if flush can be made with cards'''

        # the suits that have 5+ cards
        flushSuits = []
        for s in self.suits:
            if len(self.suits[s]) >= 5:
                flushSuits.append(s)
        
        # break the tie if there are multiple flushes
        highestCard = -1
        flushSuit = None
        for suit in flushSuits:
            for s in self.suits[suit]:
                if s.isalpha():
                    s = self.rankMapper[s[:-1]]
                else:
                    s = int(s[:-1])
                if highestCard < s:
                    highestCard = s
                    flushSuit = suit
        
        if not flushSuit:
            return None, None

        # get the 5 highest cards, use maxHeap
        heap = []
        heapify(heap)
        for card in self.suits[flushSuit]:
            rank = card[:-1]
            if rank.isalpha():
                rank = self.rankMapper[rank]
            else:
                rank = int(rank)
            heappush(heap, [rank*-1, card])
        
        flush = []
        for i in range(5):
            flush.append(heappop(heap)[1])

        return flushSuit, flush

    def populateRanksAndSuits(self):
        # loop to populate the ranks and suits
        for c in self.cards:
            rank = c[:-1]
            suit = c[-1]
            
            # make sure rank is a number
            if rank.isalpha():
                rank = self.rankMapper[rank]
            rank = int(rank)

            # add ranks to map
            if self.ranks[rank]:
                self.ranks[rank].append(c)
            else:
                self.ranks[rank] = [c]

            # add suits to map
            if self.suits[suit]:
               
                self.suits[suit].append(c)
            else:
                self.suits[suit] = [c]

if __name__ == '__main__':
    straight = Poker(['2S', '3H', '4D', '5S', '6D', '7C', 'QS', 'KS'])
    print("straight:",straight.findOptimalHand())
    

    full_house = Poker(['2S', '2H', '2D', '3S', '3D', '5C', '7H'])
    print("full_house:",full_house.findOptimalHand())

    flush = Poker(['2H', '4H', '6H', '8H', '9H', 'JS', 'KD'])
    print("flush:",flush.findOptimalHand())

    trio = Poker(['3D', '3S', '3H', '5C', '7S', '9D', 'KH'])
    print("trio:",trio.findOptimalHand())

    pair = Poker(['5H', '5C', '7D', '9S', 'JH', 'KD', '2S'])
    print("pair:",pair.findOptimalHand())

    straight2 = Poker(['4C', '5D', '6H', '7S', '8C', 'QH', 'AD'])
    print("straight2:",straight2.findOptimalHand())

    long_flush = Poker(['2H', '4H', '5H', '6H', '7H', '9H', 'JH', 'KH', '3D', '9S'])
    print("long_flush:",long_flush.findOptimalHand())

    high_card = Poker(['4C', '9D', '2H', '5S', '8C', 'QH', 'AD'])
    print("high_card:",high_card.findOptimalHand())



