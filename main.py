import random
import re

with open('wordsGuess.txt') as f:
    words = [line.rstrip() for line in f]

answer = random.choice(words)

with open('words.txt') as wordF:
    words5 = [line.rstrip() for line in wordF]


def check_guess(guess, answer):
    j = 0
    boxes = {}
    guesses = {}
    wrongLetters = []
    wrongSpots = []
    rightSpots = []
    for i in range(5):
        boxes[i] = '⬛'
        guesses[i] = '_'
    for x in guess:
        if x == answer[j]:
            boxes[j] = '🟩'
            guesses[j] = x
            rightSpots.append(x)
        elif x in answer:
            if x not in wrongSpots + rightSpots:
                wrongSpots.append(x)
                boxes[j] = '🟨'
                guesses[j] = x
        else:
            if x not in wrongLetters:
                wrongLetters.append(x)
        j += 1
    print(' '.join(boxes.values()))
    print('', '  '.join(guesses.values()))
    return boxes, guesses, wrongLetters


def solve(answer, boxes, guesses, wrongLetters, firstGuess):
    validWords = words5
    tries = 0
    guessedWords = []
    wrongLetters = []
    patternW = []
    while True:
        if firstGuess and tries == 0:
            guess = "soare"  # set starting guess
        else:
            guess = random.choice(validWords)
        tries += 1
        print("Guess:", guess)
        #print("Answer:", answer)
        boxes, guesses, wrong = check_guess(guess, answer)
        wrongLetters.extend(wrong)
        boxItr = ''.join(boxes.values())
        if guess == answer and tries <= 6:
            print("~~ WOO 🎉 ~~")
            print("Took the bot", tries, "tries")
            break
        elif guess == answer and tries > 6:
            print("~~ FAIL ❌ ~~")
            print("Took the bot", tries, "tries")
            break
        guessedWords.append(guess)
        rightSpots = [x.start() for x in re.finditer('🟩', boxItr)]
        wrongSpots = [x.start() for x in re.finditer('🟨', boxItr)]
        rightLettersRSpots = [guesses[x] for x in rightSpots]
        rightLettersWSpots = [guesses[x] for x in wrongSpots]

        # print("RIGHT SPOTS:", rightSpots)
        # print("WRONG SPOTS:", wrongSpots)
        # print("RIGHT LETTERS RIGHT SPOTS:", rightLettersRSpots)
        # print("RIGHT LETTER WRONG SPOTS", rightLettersWSpots)

        patternR = []
        countR = len(rightSpots)

        for y in range(countR):
            patternR.append((rightLettersRSpots[y], rightSpots[y]))
        #print("pattern r:", patternR)

        countW = len(wrongSpots)

        for z in range(countW):
            patternW.append((rightLettersWSpots[z], wrongSpots[z]))
        # print("pattern w:", patternW)

        def matches(word, pattern):
            # if len(pattern) > len(word):
            # return False
            return all(word[position] == x for (x, position) in pattern)

        def matchesW(word, pattern):
            # if len(pattern) > len(word):
            # return False
            return all(x in word and word[position] != x for (x, position) in pattern)

        #print("wrong letters:", wrongLetters)

        def all_matches(patternR, patternW, words5):
            a = []
            for word in words5:
                if matches(word, patternR) and (all(letter not in word for letter in wrongLetters)) and matchesW(word, patternW) and (word not in guessedWords):
                    a.append(word)
            return a
        validWords = all_matches(patternR, patternW, words5)
        # print(validWords)


solve(answer, None, None, None, 0)
#check_guess("filth", "tight")


# To implement:
# if guess has all but one right letter and not on 6th guess (e.g. answer is light, guess is right, possible answer are light, night, might, sight..., use a diff word that uses as many letters
# as possible to better figure out answer (need word with l,n,m,s, can try means, males, etc.)
