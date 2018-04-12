import json
from collections import defaultdict
import matplotlib.pyplot as plt

reddit_jokes = json.load(open('data/reddit_jokes.json'))

joke1 = reddit_jokes[0]
print(joke1['title'])
print(joke1['body'])

cntr = [0,0]
cntr = defaultdict(int)
for joke in reddit_jokes:
    cntr[joke['score']] += 1

print('Found', cntr[0], 'jokes with a score of zero')
print('Found', cntr[1], 'jokes with a score of one')

