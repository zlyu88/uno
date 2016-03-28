from random import choice

deck = ['1_y', '2_y', '3_y', '4_y', '5_y', '6_y', '7_y', '8_y', '9_y', 'Pass_y', 'pass+2_y', 'wild', 'wild+4', '1_r', '2_r', '3_r', '4_r', '5_r', '6_r', '7_r', '8_r', '9_r', 'Pass_r', 'pass+2_r', 'wild', 'wild+4', '1_g', '2_g', '3_g', '4_g', '5_g', '6_g', '7_g', '8_g', '9_g', 'Pass_g', 'pass+2_g', 'wild', 'wild+4', '1_b', '2_b', '3_b', '4_b', '5_b', '6_b', '7_b', '8_b', '9_b', 'Pass_b', 'pass+2_b', 'wild', 'wild+4']
player_cards = []
bot_cards = []
count = 0
summ1 = 0
summ2 = 0 

def take_cards(number):
	result = []
	summ = 0
	for i in range(len(deck)):
		if summ < number:
			card = choice(deck)
			deck.pop(deck.index(card))
			result.append(card)
			summ += 1
	return result


def base():
	card = choice(deck)
	if card[0] != 'w':
		deck.pop(deck.index(card))
		return card
	else:
		return base()
	

player_cards.extend(take_cards(4))
bot_cards.extend(take_cards(4))
base = base()	

def action(count, base, card):
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
				card = choice(deck)
				deck.pop(deck.index(card))
				bot_cards.append(card)
		else:
			for i in range(2):
				card = choice(deck)
				deck.pop(deck.index(card))
				player_cards.append(card)
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
			print len(deck)
			for i in range(4):
				card = choice(deck)
				deck.pop(deck.index(card))
				bot_cards.append(card)
			print len(deck)
		else:
			wild = choice(['r', 'g', 'b', 'y'])
			print 'Player have to put ' + wild
			for i in range(4):
				card = choice(deck)
				deck.pop(deck.index(card))
				player_cards.append(card)
		base = ' ' + wild
		count += 1
	
	print 'Now the base is ' + base
	if count % 2 != 0:
		bot_choice(bot_cards, base, summ2, count)
	else:
		player_choice(player_cards, base, summ1, count)

print '- - - - - Base is ' + base + ' - - - - -'


def no_card(count, player_cards, bot_cards, deck, base, summ1, summ2):
	if count % 2 != 0:
		card = choice(deck)
		deck.pop(deck.index(card))
		bot_cards.append(card)
		print base
		bot_choice(bot_cards, base, summ2, count)
	elif count % 2 == 0:
		card = choice(deck)
		deck.pop(deck.index(card))
		player_cards.append(card)
		print base
		player_choice(player_cards, base, summ1, count)


def player_choice(player_cards, base, summ1, count):
	print '-----Player move'
	print 'BASE - ' + base
	print player_cards

	move = []
	for card in player_cards:
		if card[0] == base[0] or base[len(base)-1] == card[len(card)-1] or card[0] == 'w':
			move.append(card)
	print move
	if move:
		output = player_cards[int(raw_input('Player put ' )) - 1]
		player_cards.pop(player_cards.index(output))
		if player_cards:
			action(count, base, output)
		else:
			print 'Player win!'
	elif not move and deck and not summ1:
		print 'Player takes 1 card' + ' BASE is ' + base
		summ1 += 1
		no_card(count, player_cards, bot_cards, deck, base, summ1, summ2)
	elif summ1:
		print 'Player has no card to put'
		print count + 'before'
		count += 1
		print count + 'after'
		output = base
		bot_choice(bot_cards, base, summ2, count)

def bot_choice(bot_cards, base, summ2, count):
	print '-----Bot move'
	print 'BASE - ' + base
	print bot_cards
	move = []
	for card in bot_cards:
		if card[0] == base[0] or base[len(base)-1] == card[len(card)-1]:
			move.append(card)
		elif card == 'wild' or card == 'wild+4' or card[0:4] == base[0:4]:
			move.append(card)
	print move
	if move:
		output = choice(move)
		bot_cards.pop(bot_cards.index(output))
		print '---bot put ' + output
		if bot_cards:
			action(count, base, output)
		else:
			print 'Bot win!'
	elif not move and deck and not summ2:
		print 'Bot takes 1 card'
		summ2 += 1
		no_card(count, player_cards, bot_cards, deck, base, summ1, summ2)
	elif summ2:
		print 'Bot has no card to put'
		print count + 'before'
		count += 1
		print count + 'after'
		output = base
		player_choice(player_cards, base, summ1, count)


player_choice(player_cards, base, summ1, count)

