import random

value = random.random() # between 0 and 1, not inclusive
value = random.uniform(1, 10)

integer = random.randint(1, 6) # inclusive 1 to 6

greetings ['Hello', 'Hi', 'Hey', 'Howdy', 'Hola']
choice = random.choice(greetings)

colors = ['Red', 'Black', 'Green']
multiple_choice = random.choices(colors, k=10) # will give 10 random choices
weighted_choice = random.choices(colors, weights=[18, 18, 2], k=10)

deck = list(range(1, 53))

random.shuffle(deck)
print(deck)
hand = random.sample(deck, k=5)
print(hand)
