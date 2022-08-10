import random

with open('wordsGuess.txt') as f:
    words = [line.rstrip() for line in f]

answer = random.choice(words)

with open('words.txt') as wordF:
    words5 = [line.rstrip() for line in wordF]


boxes = {}
guesses = {}
wrongLetters = []
wrongSpots = []
def check_guess(guess, answer):
    j = 0
    for i in range(5):
        boxes[i] = '⬛'
        guesses[i] = '_'
    for x in guess:
        if x == answer[j]:
            boxes[j] = '🟩'
            guesses[j] = x
        elif x in answer and answer.count(x) >= guess.count(x):
            boxes[j] = '🟨'
            guesses[j] = '_'
            if x not in wrongSpots:
                wrongSpots.append(x)
        else:
            if x not in wrongLetters:
                wrongLetters.append(x)
        j += 1
    print(' '.join(boxes.values()))
    print('', '  '.join(guesses.values()))
def solve(answer):
    validWords = words5
    tries = 0
    while True:
        guess = random.choice(validWords)
        tries += 1
        print("Guess:", guess)
        print("Answer:", answer)
        rightLetters = []
        rightSpots = []
        wrongSpots = []
        check_guess(guess,answer)
        guessItr = ''.join(guesses.values())
        #print("GUESS ITR:", guessItr)
        #print(sorted(''.join(wrongLetters)))
        if guess == answer:
            print("WOO")
            print("Took the bot", tries, "tries")
            break
        for x in guessItr:
            if x != '_':
                rightLetters.append(x)
                rightSpots.append(guessItr.find(x))

        pattern = []
        count=len(rightSpots)

        for y in range(count):
            pattern.append((rightLetters[y], rightSpots[y]))

        def matches(word, pattern):
            if len(pattern) > len(word):
                return False
            return all(word[position] == x for (x, position) in pattern)

        def all_matches(pattern, words5):
            a = []
            for word in words5:
                if matches(word, pattern) and (letter not in word for letter in wrongLetters):
                    a.append(word)
            return a
        validWords = all_matches(pattern, words5)
        #print(validWords)

solve(answer)
