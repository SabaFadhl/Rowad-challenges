import random, re, time
from copy import copy as duplicate

class Crossword(object):
    def __init__(self, cols, rows, empty = ' ', maxloops = 2000, available_words=[]):
        self.cols = cols
        self.rows = rows
        self.empty = empty
        self.maxloops = maxloops
        self.available_words = available_words
        self.randomize_word_list()
        self.current_word_list = []
        self.debug = 0
        self.clear_grid()
 
    def clear_grid(self): # initialize grid and fill with empty character
        self.grid = []
        for i in range(self.rows):
            ea_row = []
            for j in range(self.cols):
                ea_row.append(self.empty)
            self.grid.append(ea_row)
 
    def randomize_word_list(self): # also resets words and sorts by length
        temp_list = []
        for word in self.available_words:
            if isinstance(word, Word):
                temp_list.append(Word(word.word, word.clue))
            else:
                temp_list.append(Word(word[0], word[1]))
        random.shuffle(temp_list) # randomize word list
        temp_list.sort(key=lambda i: len(i.word), reverse=True) # sort by length
        self.available_words = temp_list
 
    def compute_crossword(self, time_permitted = 1.00, spins=2):
        time_permitted = float(time_permitted)
 
        count = 0
        copy = Crossword(self.cols, self.rows, self.empty, self.maxloops, self.available_words)
 
        start_full = float(time.time())
        while (float(time.time()) - start_full) < time_permitted or count == 0: # only run for x seconds
            self.debug += 1
            copy.current_word_list = []
            copy.clear_grid()
            copy.randomize_word_list()
            x = 0
            while x < spins: # spins; 2 seems to be plenty
                for word in copy.available_words:
                    if word not in copy.current_word_list:
                        copy.fit_and_add(word)
                x += 1
            #print copy.solution()
            #print len(copy.current_word_list), len(self.current_word_list), self.debug
            # buffer the best crossword by comparing placed words
            if len(copy.current_word_list) > len(self.current_word_list):
                self.current_word_list = copy.current_word_list
                self.grid = copy.grid
            count += 1
        return
 
    def suggest_coord(self, word):
        count = 0
        coordlist = []
        glc = -1
        for given_letter in word.word: # cycle through letters in word
            glc += 1
            rowc = 0
            for row in self.grid: # cycle through rows
                rowc += 1
                colc = 0
                for cell in row: # cycle through  letters in rows
                    colc += 1
                    if given_letter == cell: # check match letter in word to letters in row
                        try: # suggest vertical placement 
                            if rowc - glc > 0: # make sure we're not suggesting a starting point off the grid
                                if ((rowc - glc) + word.length) <= self.rows: # make sure word doesn't go off of grid
                                    coordlist.append([colc, rowc - glc, 1, colc + (rowc - glc), 0])
                        except: pass
                        try: # suggest horizontal placement 
                            if colc - glc > 0: # make sure we're not suggesting a starting point off the grid
                                if ((colc - glc) + word.length) <= self.cols: # make sure word doesn't go off of grid
                                    coordlist.append([colc - glc, rowc, 0, rowc + (colc - glc), 0])
                        except: pass
        # example: coordlist[0] = [col, row, vertical, col + row, score]
        #print word.word
        #print coordlist
        new_coordlist = self.sort_coordlist(coordlist, word)
        #print new_coordlist
        return new_coordlist
 
    def sort_coordlist(self, coordlist, word): # give each coordinate a score, then sort
        new_coordlist = []
        for coord in coordlist:
            col, row, vertical = coord[0], coord[1], coord[2]
            coord[4] = self.check_fit_score(col, row, vertical, word) # checking scores
            if coord[4]: # 0 scores are filtered
                new_coordlist.append(coord)
        random.shuffle(new_coordlist) # randomize coord list; why not?
        new_coordlist.sort(key=lambda i: i[4], reverse=True) # put the best scores first
        return new_coordlist
 
    def fit_and_add(self, word): # doesn't really check fit except for the first word; otherwise just adds if score is good
        fit = False
        count = 0
        coordlist = self.suggest_coord(word)
 
        while not fit and count < self.maxloops:
 
            if len(self.current_word_list) == 0: # this is the first word: the seed
                # top left seed of longest word yields best results (maybe override)
                vertical, col, row = random.randrange(0, 2), 1, 1
                ''' 
                # optional center seed method, slower and less keyword placement
                if vertical:
                    col = int(round((self.cols + 1)/2, 0))
                    row = int(round((self.rows + 1)/2, 0)) - int(round((word.length + 1)/2, 0))
                else:
                    col = int(round((self.cols + 1)/2, 0)) - int(round((word.length + 1)/2, 0))
                    row = int(round((self.rows + 1)/2, 0))
                # completely random seed method
                col = random.randrange(1, self.cols + 1)
                row = random.randrange(1, self.rows + 1)
                '''
 
                if self.check_fit_score(col, row, vertical, word): 
                    fit = True
                    self.set_word(col, row, vertical, word, force=True)
            else: # a subsquent words have scores calculated
                try: 
                    col, row, vertical = coordlist[count][0], coordlist[count][1], coordlist[count][2]
                except IndexError: return # no more cordinates, stop trying to fit
 
                if coordlist[count][4]: # already filtered these out, but double check
                    fit = True 
                    self.set_word(col, row, vertical, word, force=True)
 
            count += 1
        return
 
    def check_fit_score(self, col, row, vertical, word):
        '''
        And return score (0 signifies no fit). 1 means a fit, 2+ means a cross.
 
        The more crosses the better.
        '''
        if col < 1 or row < 1:
            return 0
 
        count, score = 1, 1 # give score a standard value of 1, will override with 0 if collisions detected
        for letter in word.word:            
            try:
                active_cell = self.get_cell(col, row)
            except IndexError:
                return 0
 
            if active_cell == self.empty or active_cell == letter:
                pass
            else:
                return 0
 
            if active_cell == letter:
                score += 1
 
            if vertical:
                # check surroundings
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col+1, row): # check right cell
                        return 0
 
                    if not self.check_if_cell_clear(col-1, row): # check left cell
                        return 0
 
                if count == 1: # check top cell only on first letter
                    if not self.check_if_cell_clear(col, row-1):
                        return 0
 
                if count == len(word.word): # check bottom cell only on last letter
                    if not self.check_if_cell_clear(col, row+1): 
                        return 0
            else: # else horizontal
                # check surroundings
                if active_cell != letter: # don't check surroundings if cross point
                    if not self.check_if_cell_clear(col, row-1): # check top cell
                        return 0
 
                    if not self.check_if_cell_clear(col, row+1): # check bottom cell
                        return 0
 
                if count == 1: # check left cell only on first letter
                    if not self.check_if_cell_clear(col-1, row):
                        return 0
 
                if count == len(word.word): # check right cell only on last letter
                    if not self.check_if_cell_clear(col+1, row):
                        return 0
 
 
            if vertical: # progress to next letter and position
                row += 1
            else: # else horizontal
                col += 1
 
            count += 1
 
        return score
 
    def set_word(self, col, row, vertical, word, force=False): # also adds word to word list
        if force:
            word.col = col
            word.row = row
            word.vertical = vertical
            self.current_word_list.append(word)
 
            for letter in word.word:
                self.set_cell(col, row, letter)
                if vertical:
                    row += 1
                else:
                    col += 1
        return
 
    def set_cell(self, col, row, value):
        self.grid[row-1][col-1] = value
 
    def get_cell(self, col, row):
        return self.grid[row-1][col-1]
 
    def check_if_cell_clear(self, col, row):
        try:
            cell = self.get_cell(col, row)
            if cell == self.empty: 
                return True
        except IndexError:
            pass
        return False
 
    def solution(self): # return solution grid
        outStr = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                outStr += '%s ' % c
            outStr += '\n'
        return outStr
 
    def word_find(self): # return solution grid
        outStr = ""
        for r in range(self.rows):
            for c in self.grid[r]:
                if c == self.empty:
                    outStr += '%s ' % "-"
                else:
                    outStr += '%s ' % c
            outStr += '\n'
        return outStr
 
    def order_number_words(self): # orders words and applies numbering system to them
        self.current_word_list.sort(key=lambda i: (i.col + i.row))
        count, icount = 1, 1
        for word in self.current_word_list:
            word.number = count
            if icount < len(self.current_word_list):
                if word.col == self.current_word_list[icount].col and word.row == self.current_word_list[icount].row:
                    pass
                else:
                    count += 1
            icount += 1
 
    def display(self, order=True): # return (and order/number wordlist) the grid minus the words adding the numbers
        outStr = ""
        if order:
            self.order_number_words()
 
        copy = self
 
        for word in self.current_word_list:
            copy.set_cell(word.col, word.row, word.number)
 
        for r in range(copy.rows):
            for c in copy.grid[r]:
                outStr += '%s ' % c
            outStr += '\n'
 
        outStr = re.sub(r'[a-z]', ' ', outStr)
        return outStr
 
    def word_bank(self): 
        outStr = ''
        temp_list = duplicate(self.current_word_list)
        random.shuffle(temp_list) # randomize word list
        for word in temp_list:
            outStr += '%s\n' % word.word
        return outStr
 
    def legend(self): # must order first
        outStr = ''
        for word in self.current_word_list:
            outStr += '%d. (%d,%d) %s: %s\n' % (word.number, word.col, word.row, word.down_across(), word.clue )
        return outStr
 
class Word(object):
    def __init__(self, word=None, clue=None):
        self.word = re.sub(r'\s', '', word.lower())
        self.clue = clue
        self.length = len(self.word)
        # the below are set when placed on board
        self.row = None
        self.col = None
        self.vertical = None
        self.number = None
 
    def down_across(self): # return down or across
        if self.vertical: 
            return 'down'
        else: 
            return 'across'
 
    def __repr__(self):
        return self.word
 
### end class, start execution
 
#start_full = float(time.time())
 
words_list = [
    {"word": "Yemen"  , "question": "Country?"},
    {"word": "yes"    , "question": "Anser?"},
    {"word":"July", "question":"The seventh month of the year"},
    {"word":"Python", "question":"A programming language"},
    {"word":"ِAlgeria", "question":"The biggest country in Africa"},
    {"word":"Happy", "question":"Opposite of sad"},
    {"word":"Manila", "question":"The capital of the Philippines"},
    {"word":"Tigris", "question":"ِA river in Iraq"},
    {"word":"Joe Biden", "question":"The president of America "},
    {"word":"Abdel Halim Hafez", "question":"An Egyptian singer"},
    {"word":" censorious", "question":"The synonym of critical"},
    {"word":"S400", "question":"Air missile system"},
    {"word": "orang", "question": "what is orang color?"},
    {"word": "red", "question": "what is appale color?"},
    {"word": "yallow", "question": "what is banana color?"},
    {"word": "rose", "question": "what is Strawberry color?"},
    {"word": "green", "question": "what is watermelon color?"},
    {"word": "black", "question": "what is Grape color?"},
    {"word": "blue", "question": "what is Cranberries color?"},
    {"word": "white", "question": "what is fig color?"},
    {"word": "browen", "question": "what is Kiwi color?"},
    {"word": "darkgreen", "question": "what is avocado color?"},
    {"word": "songs", "question": "which You listen everyday?"},
    {"word": "nliy", "question": "Her most important work is a movie and men.?"},
    {"word": "Om Klthom", "question": "The Lady of Arabic Singing?"},
    {"word": "pm", "question": "night time?"},
    {"word": "gta", "question": " still car  game?"},
    {"word": "china", "question": "From Southeast Asian countries?"},
    {"word": "go", "question": "form somewhere?"},
    {"word": "Sun", "question": "the biggest start in our galaxy?"},
    {"word": "okay", "question": "when everything is fain?"},
    {"word": "spong pop", "question": "Who lives in the sea and people are loved it ?"},
    {"word": "left", "question": "Which way is anti-clockwise, left or righ?"},
    {"word": "lgloo", "question": " What do you call a house made of ice?"},
    {"word": "nile", "question": " Which is the longest river on the earth?"},
    {"word": "Japan", "question": "Which country is called the land of rising sun?"},
    {"word": "mars", "question": " Which planet is known as the Red Planet?"},
    {"word": "skin", "question": " Which is the most sensitive organ in our body?"},
    {"word": "India", "question": " The largest 'Democracy' in the world?"},
    {"word": "water", "question": "What makes up (approx.) 80% of our brain's volume?"},
    {"word": "Ghana", "question": " Which African nation is famous for chocolate?"},
    {"word": "red", "question": "What is the top color in a rainbow?"},
    {"word": "lago", "question": " What is the name of the main antagonist in the Shakespeare play Othello "},
    {"word": "four", "question": "How many human players are there on each side in a polo match ?"},
    {"word": "feb", "question": " Which month of the year has the least number of days"},
    {"word": "sty", "question": " Where does a pig live?"},
    {"word": "nose", "question": " We smell with our?"},
    {"word": "tibet", "question": " Which place is known as the roof of the world?"},
    {"word": "tin", "question": " What element is denoted by the chemical symbol Sn in the periodic table?"},
    {"word": "krone", "question": " What is the currency of Denmark?"},
    {"word": "knee", "question": " In which part of your body would you find the cruciate ligament?"},
    {"word": "east", "question": " In which direction does the sun rise ?"},
    {"word":"Sky", "question":"something is starting with s \'b\'"},
    {"word":"Sedney", "question":"A capital city of Australia"},
    {"word":"Popup", "question":"Alert message"},
    {"word":"FTP", "question":"standard for File Transfer Protocol"},
    {"word":"Taxes", "question":"The position of Dallas"},
    {"word":"Islam", "question":"What your religion"},
    {"word":"Team", "question":"meaning of co-workers"},
    {"word":"Koyoto", "question":"The name of Japan anime city \'C\'"},
    {"word":"Vaccine", "question":"Synonym of medicine"},
    {"word":"Dark", "question":"The opposite of \'light\'"},
    {"word": "songs", "question": "which You listen everyday?"},
    {"word": "lion", "question": "who is the king of the jungle?"},
    {"word": "Om Klthom", "question": "The Lady of Arabic Singing?"},
    {"word": "Oval", "question": "Shape of Egg is?"},
    {"word": "Pluto", "question": " It is one of the planets of the solar system?"},
    {"word": "china", "question": "From Southeast Asian countries?"},
    {"word": "purple", "question": "it is mean I trust You?"},
    {"word": "Sun", "question": "the biggest start in our galaxy?"},
    {"word": "Roma", "question": "one of Italia country?"},
    {"word": "sponge pop", "question": "Who lives in the sea and people are loved it ?"},
    {"word":"Tokyo", "question":"Asia's largest city"},
    {"word":"Australia", "question":"The largest island in the world"},
    {"word":"Washington", "question":"What is the capital of America"},
    {"word":"Nile", "question":"The longest river in the world"},
    {"word":"Whale", "question":"The heaviest animal on earth"},
    {"word":"Jupiter", "question":"The largest planet in the solar system"},
    {"word":"Algorithm", "question":"Founder of Algebra"},
    {"word":"Asia", "question":"Largest continents"},
    {"word":"Ostrich", "question":"The fastest bird in the world"},
    {"word":"London", "question":"The city is located the famous Big Ben Watch"},
    {"word":"Friday", "question":"the last day from week?" },
    {"word":"seven", "question":"number of days in week"},
    {"word":"france", "question":"where is effil tower"},
    {"word":"sanaa", "question":"the capital of yemen"},
    {"word":"Cairo", "question":"the capital of Egypt"},
    {"word":"iraq", "question":"Baghdad is a capital of"},
    {"word":"cars", "question":"a taxi is a type of?"},
    {"word":"Egypt", "question":" where is The Nile River'"},
    {"word":"Yemen", "question":"where is Socotra Island"},
    {"word":"Amina", "question":" mother of our massenger"},
    {"word":"Bahrain", "question":"A gulf country that starts with \'b\'"},
    {"word":"Brazil", "question":"A country that hosted World Cup in 2014"},
    {"word":"Cheap", "question":"Opposite of expensive"},
    {"word":"Ready", "question":"A word describing a state"},
    {"word":"Nivada", "question":"The state where Las Vegas is located"},
    {"word":"House", "question":"Where you live"},
    {"word":"Bus", "question":"A form of public transportation"},
    {"word":"Canada", "question":"A country in South America that starts with the letter \'C\'"},
    {"word":"Need", "question":"A word similar to require"},
    {"word":"Die", "question":"The opposite of \'live\'"},
    {"word": "CPU", "question": "Brain of computer is?"},
    {"word": "Camel", "question": "Which animal has hump on its back?"},
    {"word": "Jasmine", "question": "flower is white in colour?"},
    {"word": "Oval", "question": "Shape of Egg is?"},
    {"word": "Winter", "question": " In which season we wear warm clothes?"},
    {"word": "Seven", "question": "colors are there in a rainbow?"},
    {"word": "Red", "question": "primary color?"},
    {"word": "Sun", "question": "principal source of energy for earth?"},
    {"word": "Africa", "question": "continent is known as 'Dark' continent?"},
    {"word": "Asia", "question": "the largest continent in the world?"},
    {"word": "after", "question": "Behind in place or order"},
    {"word": "draft", "question": "A current of air in an enclosed area."},
    {"word": "call", "question": "To say in a loud voice"},
    {"word": "little", "question": "Small in size"},
    {"word": "option", "question": "The act of choosing"},
    {"word": "signal", "question": "A message communicated by such means."},
    {"word": "writer", "question": "a person engaged in writing books"},
    {"word": "follow", "question": "To come or go after"},
    {"word": "camera", "question": " a hand-held photographic device"},
    {"word": "detail", "question": "An individual part or item"},
    {"word": "action", "question": "process of being active"},
    {"word": "beauty", "question": "One that is beautiful, especially a beautiful woman."},
    {"word": "center", "question": "A point or place that is equally distant from the sides "},
    {"word": "detect", "question": "To learn something hidden and"},
    {"word": "orange", "question": "Of the color orange."},
    {"word": "finish", "question": "to stop"},
    {"word": "online", "question": "Connected to a central computer or to a computer network"},
    {"word": "player", "question": "A gambler."},
    {"word": "later", "question": "afterwards"},
    {"word": "dog", "question": " A male animal of the family Canidae"},
    {"word":"Sanaa", "question":"The capital of the state of Yemen is?"},
    {"word":"Baghdad", "question":"capital of Iraq"},
    {"word":"ِWashington", "question":"the capital of america"},
    {"word":"Athena", "question":"the capital of Greece"},
    {"word":"Cairo", "question":"The capital of Egypt"},
    {"word":"Damascus", "question":"ِthe capital of Syria"},
    {"word":"Paris", "question":"the capital of France "},
    {"word":"Ottawa", "question":"Canada's capital"},
    {"word":"Beirut", "question":"the capital of Lebanon"},
    {"word":"S400", "question":"The capital of Tunisia is:"}

 ]
new_list=list()
for i in words_list:
    row=list()
    row.append(i['word'])
    row.append(i['question'])
    new_list.append(row)
    
# print (new_list)
    
a = Crossword(10, 10, '-', 5000, new_list)
a.compute_crossword(2)
# print (a.word_bank())
print (a.solution())
# print (a.word_find())
a.display()
print (a.legend())
# print (len(a.current_word_list), 'out of', len(word_list))
# print (a.debug)
# #end_full = float(time.time())
#print end_full - start_full