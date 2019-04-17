def split_sentence(stri):
	""" Rule 1) split sentence with '.' . Output as list"""
	sentences = stri.split('.')
	return sentences

def split_words(sentence):
	""" Output as list"""
	sentence = sentence.strip()
	words = sentence.split(' ')
	return words

def detect_keyword(word):
	return word.isupper()

def check_keyword_type():
	"""Detect <> <<>> and return keyword type"""
	pass

string = """IF you are not BULKING, THEN follow ORDER 1)INCREASE PROTEIN, 2)INCREASE FAT, 3)INCREASE CARBOHYDRATE.
	IF you are <FAT>, THEN first CUT your existing body fat WITH save your existing muscle mass. by calory deplet, then if you are lean go to calory surplus."""
sentences = split_sentence(string)[:-1]

for sentence in sentences:
	words = split_words(sentence)
	keywords = [word for word in words if detect_keyword(word)]
	print(keywords)