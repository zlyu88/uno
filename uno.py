from random import choice
from time import sleep

class Uno():
    deck = ['1_y', '2_y', '3_y', '4_y', '5_y', '6_y', '7_y', '8_y', '9_y', 'Pass_y', 'pass+2_y', 'wild', 'wild+4', '1_r', '2_r', '3_r', '4_r', '5_r', '6_r', '7_r', '8_r', '9_r', 'Pass_r', 'pass+2_r', 'wild', 'wild+4', '1_g', '2_g', '3_g', '4_g', '5_g', '6_g', '7_g', '8_g', '9_g', 'Pass_g', 'pass+2_g', 'wild', 'wild+4', '1_b', '2_b', '3_b', '4_b', '5_b', '6_b', '7_b', '8_b', '9_b', 'Pass_b', 'pass+2_b', 'wild', 'wild+4']
    player_cards = []
    bot_cards = []
    count = 0
    summ1 = 0
    summ2 = 0 

    def take_cards(self, number):
        result = []
        summ = 0
        for i in range(len(self.deck)):
            if summ < number:
                card = choice(self.deck)
                self.deck.pop(self.deck.index(card))
                result.append(card)
                summ += 1
        return result


    def base(self):
        card = choice(self.deck)
        if card[0] != 'w':
            self.deck.pop(self.deck.index(card))
            return card
        else:
            return self.base()	

    def action(self, count, base, card):
        if card[0:4].lower() != 'pass' and card[0:4] != 'wild' and base[0] == card[0] or card[0:4].lower() != 'pass' and card[0:4] != 'wild' and base[len(base) - 1] == card[len(card) - 1]:
            count += 1
            base = card
				
        elif card[0:4] == 'Pass' and base[0:4] == 'Pass' or card[0:4] == 'Pass' and base[len(base) - 1] == card[len(card) - 1]:
            print 'Next player pass'
            base = card
		
        elif card[0:4] == 'pass' and base[0:4] == 'pass' or card[0:4] == 'pass' and base[len(base) - 1] == card[len(card) - 1]:
            print 'Next player takes 2 card and pass'
            if count % 2 == 0:
                for i in range(2):
                    add_card = choice(self.deck)
                    self.deck.pop(self.deck.index(add_card))
                    self.bot_cards.append(add_card)
            else:
                for i in range(2):
                    add_card = choice(self.deck)
                    self.deck.pop(self.deck.index(add_card))
                    self.player_cards.append(add_card)
            base = card

				
        elif card == 'wild':
            if count % 2 == 0:
                wild = raw_input('Next player have to put (r/g/b/y) card ')
			
            else:
                wild = choice(['r', 'g', 'b', 'y'])
                print 'Player have to put ' + wild
            base = ' ' + wild
					
            count += 1
        elif card == 'wild+4':
            if count % 2 == 0:
                wild = raw_input('Next player have to take 4 cards and put (r/g/b/y) card ')
                print len(self.deck)
                for i in range(4):
                    card = choice(self.deck)
                    self.deck.pop(self.deck.index(card))
                    self.bot_cards.append(card)
                print len(self.deck)
            else:
                wild = choice(['r', 'g', 'b', 'y'])
                print 'Player have to put ' + wild
                for i in range(4):
                    card = choice(self.deck)
                    self.deck.pop(self.deck.index(card))
                    self.player_cards.append(card)
            base = ' ' + wild
            count += 1
	
        print 'Now the base is ' + base
        if count % 2 != 0:
            self.bot_choice(self.bot_cards, base, self.summ2, count)
        else:
            self.player_choice(self.player_cards, base, self.summ1, count)


    def no_card(self, count, player_cards, bot_cards, deck, base, summ1, summ2):
        if count % 2 != 0:
            card = choice(deck)
            deck.pop(deck.index(card))
            bot_cards.append(card)
            self.bot_choice(bot_cards, base, summ2, count)
        elif count % 2 == 0:
            card = choice(deck)
            deck.pop(deck.index(card))
            player_cards.append(card)
            self.player_choice(player_cards, base, summ1, count)


    def player_choice(self, player_cards, base, summ1, count):
        print '\n----- Player move -----\n'
        print 'BASE is: %s\n'% base
        print 'Your cards: %s'% player_cards

        move = []
        for card in player_cards:
            if card[0] == base[0] or base[len(base)-1] == card[len(card)-1] or card[0] == 'w':
                move.append(card)
        print 'You can use: %s'% move
        if move:
            output = move[int(raw_input('Your choice:  ' )) - 1]
            player_cards.pop(player_cards.index(output))
            if player_cards:
                self.action(count, base, output)
            else:
                print 'Player win!'
        elif not move and self.deck and not summ1:
            sleep(2)
            print 'Player takes 1 card\nBASE is: %s'% base
            summ1 += 1
            self.no_card(count, player_cards, self.bot_cards, self.deck, base, summ1, self.summ2)
        elif summ1:
            print 'Player has no card to put'
            print str(count) + ' before'
            count += 1
            print str(count) + ' after'
            output = base
            self.bot_choice(self.bot_cards, base, self.summ2, count)

    def bot_choice(self, bot_cards, base, summ2, count):
        print '\n-----Bot move-----\n'
        print 'BASE is: %s\n'% base
        print 'Bot cards: %s'% bot_cards
        sleep(2)
        move = []
        for card in bot_cards:
            if card[0] == base[0] or base[len(base)-1] == card[len(card)-1]:
                move.append(card)
            elif card == 'wild' or card == 'wild+4' or card[0:4] == base[0:4]:
                move.append(card)
        print 'Bot can chose: %s'% move
        sleep(2)
        if move:
            output = choice(move)
            bot_cards.pop(bot_cards.index(output))
            print 'Bot chose: %s '% output
            sleep(1)
            if bot_cards:
                self.action(count, base, output)
            else:
                print 'Bot win!'
        elif not move and self.deck and not summ2:
            print 'Bot takes 1 card'
            summ2 += 1
            self.no_card(count, self.player_cards, bot_cards, self.deck, base, self.summ1, summ2)
        elif summ2:
            print 'Bot has no card to put'
            print str(count) + ' before'
            count += 1
            print str(count) + ' after'
            output = base
            self.player_choice(self.player_cards, base, self.summ1, count)
            
    def start_game(self):   
        self.player_cards.extend(self.take_cards(4))
        self.bot_cards.extend(self.take_cards(4))
        self.base = self.base()
        self.player_choice(self.player_cards, self.base, self.summ1, self.count)

uno = Uno()
uno.start_game()


