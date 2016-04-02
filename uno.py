_authors_ = 'yurii_kit_&_oleh_bogutskii'


import sys
import webbrowser
import threading
from random import choice
from time import sleep
from os import system

class Uno():

    deck = ['1_y', '2_y', '3_y', '4_y', '5_y','0_y', 'Pass_y',
            '1_y', '2_y', '3_y', '4_y', '5_y', 'pass+2_y',
            'wild', '1_r', '2_r', '3_r','4_r', '5_r', '0_r',
            'wild+4', '1_r', '2_r', '3_r','4_r', '5_r',
            'Pass_r', 'wild', 'wild+4', '1_g', '2_g', '3_g',
            '1_g', '2_g', '3_g', '4_g', '5_g', 'pass+2_r',
            '4_g', '5_g', '0_g', 'Pass_g', 'pass+2_g', 'wild', 
            'wild+4', '1_b', '2_b', '3_b', '4_b', '5_b', '0_b',
            '1_b', '2_b', '3_b', '4_b', '5_b', 'Pass_b',
            'pass+2_b', 'wild', 'wild+4'] 
            
    deck2 = []

    player_cards = []
    bot_cards = []
    count = 0
    summ1 = 0
    summ2 = 0
    double_player = False
    double_bot = False
    general_score = {'Player': 0, 'Bot': 0}

    def take_cards(self, number):
        result = []
        summ = 0
        for num in range(len(self.deck)):
            if summ < number:
                card = choice(self.deck)
                self.deck.pop(self.deck.index(card))
                result.append(card)
                summ += 1
        return result

    def base_choice(self):
        card = choice(self.deck)
        if card[0] != 'w':
            self.deck2.append(card)
            self.deck.pop(self.deck.index(card))
            return card
        else:
            return self.base_choice()  

    def action(self, count, base, card):
        color_list = ['r', 'g', 'b', 'y']
        decide = []
        
        if card[0: 4].lower() != 'pass' and card[0: 4] != 'wild' \
            and base[0] == card[0] or card[0: 4].lower() != 'pass' \
            and card[0: 4] != 'wild' and base[len(base) - 1] \
            == card[len(card) - 1]:
            count += 1
            base = self.put_few(count, card)
                
        elif card[0: 4] == 'Pass' and base[0: 4] == 'Pass' or \
            card[0: 4] == 'Pass' and base[len(base) - 1] == \
            card[len(card) - 1]:
            print '\nNext player pass'
            sleep(2)
            base = card
        
        elif card[0: 4] == 'pass' and base[0: 4] == 'pass' or card[0: 4] \
            == 'pass' and base[len(base) - 1] == card[len(card) - 1]:
            print '\nNext player takes 2 card and pass'
            sleep(2)
            if count % 2 == 0:
                for i in range(2):
                    self.new_deck()
                    add_card = choice(self.deck)
                    self.deck.pop(self.deck.index(add_card))
                    self.bot_cards.append(add_card)
            else:
                for i in range(2):
                    self.new_deck()
                    add_card = choice(self.deck)
                    self.deck.pop(self.deck.index(add_card))
                    self.player_cards.append(add_card)
            base = card
               
        elif card == 'wild':
            if count % 2 == 0:
                wild = ''
                while wild not in color_list:
                    wild = raw_input('\nNext player have to put'
                                     '( r / g / b / y ) card: ')

            else:
                for color in self.bot_cards:
                    if color[2] in ['r', 'g', 'b', 'y']:
                        decide.append(color[2])
                if decide:
                    wild = choice(decide)
                else:
                    wild = choice(['r', 'g', 'b', 'y'])
                print '\nPlayer have to put ' + wild
                sleep(2)
            base = ' ' + wild        
            count += 1
        elif card == 'wild+4':
            if count % 2 == 0:
                wild = ''
                while wild not in color_list:
                    wild = raw_input('\nNext player have to take 4 '
                            'cards and put ( r / g / b / y ) card: ')
                for i in range(4):
                    self.new_deck() 
                    card = choice(self.deck)
                    self.deck.pop(self.deck.index(card))
                    self.bot_cards.append(card)
            else:
                for color in self.bot_cards:
                    if color[2] in ['r', 'g', 'b', 'y']:
                        decide.append(color[2])
                if decide:
                    wild = choice(decide)
                else:
                    wild = choice(['r', 'g', 'b', 'y'])
                print 'Player have to put ' + wild
                sleep(2)
                for i in range(4):
                    self.new_deck()
                    card = choice(self.deck)
                    self.deck.pop(self.deck.index(card))
                    self.player_cards.append(card)
            base = ' ' + wild
            count += 1
    
        if count % 2 != 0:
            self.bot_choice(self.bot_cards, base, self.summ2, count)
        else:
            self.player_choice(self.player_cards, base, self.summ1, count)

    def put_few(self, count, card):
        if count % 2 != 0:
            return self.few_cards_player(card)
        else:
            return self.few_cards_bot(card)

    def few_cards_player(self, card):
        few_same = []
        for item in self.player_cards:
            if item.startswith(card[0]) and \
            card[0] != 'w' and (card[0]).lower != 'p':
                few_same.append(item)
    
        if few_same:
            top_card = choice(few_same)
            print '\n' + str(len(few_same) + 1) + ' cards at one time'
            sleep(2)
            for item in few_same:
                self.deck2.append(item)
                self.player_cards.pop(self.player_cards.index(item))
                print '\nTop is ' + top_card
                sleep(2)
                return top_card
        else:
            return card
        sleep(3)
    
    def few_cards_bot(self, card):
        few_same = []
        for item in self.bot_cards:
            if item.startswith(card[0]) and \
            card[0] != 'w' and (card[0]).lower != 'p':
                few_same.append(item)
    
        if few_same:
            top_card = choice(few_same)
            print '\n' + str(len(few_same) + 1) + ' cards at one time'
            sleep(2)
            for item in few_same:
                self.deck2.append(item)
                self.bot_cards.pop(self.bot_cards.index(item))
                print '\nTop is ' + top_card
                sleep(2)
                return top_card
        else:
            return card    

    def no_card(self, count, player_cards, bot_cards, \
                deck, base, summ1, summ2):
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
        system('clear')
        print '\n----- Player move -----\n'
        print 'BASE is: %s\n'% base
        print 'Your cards: %s'% player_cards
        sleep(1)

        if len(player_cards) == 1 and player_cards[0] == 'wild':
                self.extra_wild_player()

        move = []
        for card in player_cards:
            if card[0] == base[0] or base[len(base)-1] == \
            card[len(card)-1] or card[0] == 'w':
                move.append(card)
        if move == []:
            print "\nYou don't have a suitable card"
            sleep(1)
        else:
            can_choice = ''
            for cards in range(len(move)):
                can_choice += '{0}.[{1}], '.format(cards+1, move[cards])
            print 'You can choice:  %s'% can_choice
        
        if move:
            output = ''
            while output not in move:
                try:
                    output = move[(int(raw_input('\nYour choice: ')) - 1)]
                except IndexError:
                    print "Error. It's must existing value"
                except ValueError:
                    print "Error. It's must be integer"
            
            self.deck2.append(output)
            player_cards.pop(player_cards.index(output))
            
            if player_cards:
                self.action(count, base, output)
                sleep(1)
                system('clear')
            else:
                print '\nPlayer win!'
                self.final_score(self.player_cards, self.bot_cards,\
                self.general_score)
                sleep(2)
        elif not move and self.deck and not summ1:
            sleep(2)
            print '\nPlayer takes 1 card\nBASE is: %s'% base
            sleep(2)
            summ1 += 1
            self.no_card(count, player_cards, self.bot_cards, self.deck, \
                         base, summ1, self.summ2)
        elif summ1:
            print 'Player has no card to put'
            sleep(1)
            count += 1
            output = base
            self.bot_choice(self.bot_cards, base, self.summ2, count)

    def extra_wild_player(self):
        answer = raw_input('Your last card is \'wild\', so you can ' \
                'double this bot csore or -25 to your own total.' \
                ' (1 or 2 or ignore) ')
        if answer == '1':
            print '\nPlayer win!'
            print 'And olso made this bot score double!!!'
            sleep(2)
            self.deck2.append(self.player_cards[0])
            self.player_cards.pop(0)
            self.double_bot = True
            self.final_score(self.player_cards, self.bot_cards,\
            self.general_score)
            
        elif answer == '2':
            print '\nPlayer win!'
            print 'And olso made -25 to his total score!!!'
            self.deck2.append(self.player_cards[0])
            self.player_cards.pop(0)
            sleep(2)
            self.general_score['Player'] -= 25
            self.final_score(self.player_cards, self.bot_cards,\
            self.general_score)
            
    
    def extra_wild_bot(self):
        answer = choice([1, 2, 3])
        if answer == 1:
            print '\nBot win!'
            print 'And olso made this player score double!!!'
            self.deck2.append(self.bot_cards[0])
            self.bot_cards.pop(0)
            self.double_player = True
            self.final_score(self.player_cards, self.bot_cards,\
            self.general_score)
            
        elif answer == 2:
            print '\nBot win!'
            print 'And olso made -25 to his total score!!!'
            self.deck2.append(self.bot_cards[0])
            self.bot_cards.pop(0)
            self.general_score['Bot'] -= 25
            self.final_score(self.player_cards, self.bot_cards,\
            self.general_score)
            

    def bot_choice(self, bot_cards, base, summ2, count):
        system('clear')
        print '\n----- Bot move -----\n'
        print 'BASE is: %s\n'% base
        #print 'Bot cards: %s'% bot_cards 
        sleep(1)
        print 'Bot thinking...\n'

        if len(bot_cards) == 1 and bot_cards[0] == 'wild':
                self.extra_wild_bot()

        move = []
        for card in bot_cards:
            if card[0] == base[0] or base[len(base)-1] == card[len(card)-1]:
                move.append(card)
            elif card == 'wild' or card == 'wild+4' or card[0: 4] == base[0: ]:
                move.append(card)
        #print 'Bot can chose: %s\n'% move
        sleep(1.5)
        if move:
            output = choice(move)
            self.deck2.append(output)
            bot_cards.pop(bot_cards.index(output))

            print 'Bot chose: %s '% output
            sleep(2)
            if bot_cards:
                self.action(count, base, output)
            else:
                print '\nBot win!'
                self.final_score(self.player_cards, self.bot_cards,\
                self.general_score) 
        elif not move and self.deck and not summ2:
            print 'Bot has no card to put','\nBot takes 1 card\n'
            sleep(1)
            summ2 += 1
            self.no_card(count, self.player_cards, bot_cards, self.deck,\
                         base, self.summ1, summ2)
        elif summ2:
            print 'Bot has no card to put'
            sleep(1)
            count += 1
            output = base
            self.player_choice(self.player_cards, base, self.summ1, count)
        
    def final_score(self, player_cards, bot_cards, general_score):
        print '\n-----The score is-----\n'
        sum_score_player = 0
        sum_score_bot = 0

        for card in player_cards:
            if (card[0].lower() != 'p' and card[0] != 'w' and card[0] == '0'):
                sum_score_player += 10
            elif (card[0].lower() != 'p' and card[0] != 'w' and card[0] != '0'):
                sum_score_player += int(card[0])
            elif card == 'wild+4':
                sum_score_player += 20
            elif card == 'wild':
                sum_score_player += 15 
        
        if self.double_player:
            print '\n' + str(sum_score_player) + ' * 2'
            sum_score_player *= 2
            self.double_player = False

        general_score['Player'] += sum_score_player
        print 'Player ' + str(sum_score_player)
        
        for card in bot_cards:
            if card[0].lower() != 'p' and card[0] != 'w' and card[0] == '0':
                sum_score_bot += 10
            elif card[0].lower() != 'p' and card[0] != 'w' and card[0] != '0':
                sum_score_bot += int(card[0])
            elif card == 'wild+4':
                sum_score_bot += 20
            elif card == 'wild':
                sum_score_bot += 15 
        
        if self.double_bot:
            print '\n' + str(sum_score_bot) + ' * 2'
            sum_score_bot *= 2
            self.double_bot = False

        general_score['Bot'] += sum_score_bot
        print 'Bot ' + str(sum_score_bot)

        self.go_on()

    def go_on(self):
        print '\n-----Total score is:-----\n'
        sleep(2)
        for key in self.general_score:
            print key, self.general_score[key]
        sleep(1)
        if self.general_score['Player'] < 125 and self.general_score['Bot'] < 125:
            print '\nLet\'s go on!'
            self.deck.extend(self.player_cards)
            self.deck.extend(self.bot_cards)
            self.deck.extend(self.deck2)
            self.player_cards = []
            self.bot_cards = []
            self.deck2 = []
            sleep(3)
            self.start_game()
        else:
            if self.general_score['Player'] > 125:
                print 'Player\'s total score is ' + \
                str(self.general_score['Player'])
                print '\nBot wins total game!'
                sleep(100)
            else:
                print 'Bot\'s total score is ' + \
                str(self.general_score['Bot'])
                print '\nPlayer wins total game!'
                sleep(100)

    def new_deck(self):
        if not self.deck:
            self.deck = self.deck2[0:len(self.deck2) - 1]

    def start_game(self):
        system('clear')
        print '----- UNO - Card Game -----'
        print "\nDescription:\
               \nThe aim of the game is to be the first player to \
               \nscore 125 points. This is achieved (usually over \
               \nseveral rounds of play) by a player discarding \
               \nall of their cards and earning points corresponding \
               \nto the value of the remaining cards still held by \
               \nthe other players.\
               \n\nAbbreviation:\
               \nr - red, y - yellow, g - green, b - blue.\
               \n\nFor Example:\
               \n1_y it's 1 Yellow card\
               \n0_g it's 0 Green card\
               \n\n0. More details about UNO\
               \n1. Start game\
               \n9. Exit"

        varriants = [0, 1, 9]
        usr_choice = None

        while usr_choice not in varriants:
            try:     
                usr_choice = int(raw_input('\nEnter your choice: '))
            except ValueError:
                print "Error. It's must be 0, 1 or 9"
                sleep(2)
                system('clear')
        if usr_choice == 0:
            uno_web = webbrowser.open\
            ('https://en.wikipedia.org/wiki/Uno_(card_game)')
            new_start = self.start_game()
            t1 = threading.Thread(args=(uno_web))
            t2 = threading.Thread(args =(new_start))
            t1.start()
            t2.start()
            
        elif usr_choice == 1:
            self.player_cards.extend(self.take_cards(7))
            self.bot_cards.extend(self.take_cards(7))
            self.base = self.base_choice()
            self.player_choice(self.player_cards, self.base, \
            self.summ1, self.count)
        elif usr_choice == 9:
            sys.exit()


uno = Uno()
uno.start_game()
