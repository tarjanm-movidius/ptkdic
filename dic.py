#!/usr/bin/python3 -OO

import sys
import re
import gzip
import pickle
from timeit import default_timer as timer
import unichar


class TrieNode(object):
	"""
	Trie node holding letter and optional word article
	"""
	def __init__(self, char: str):
		self.char = char
		self.children = []
		self.article = {}


nodecnt = 1
def add_w(root, word: str, trans):
	"""
	Adding a word in the trie structure
	"""
	node = root
	for char in unichar.nouc(word):
		found_in_child = False
		# Search for the character in the children of the present node
		for child in node.children:
			if child.char == char:
				# Point the node to the child that contains this char
				node = child
				found_in_child = True
				break
		# Character not found in children, adding a new child
		if not found_in_child:
			global nodecnt
			new_node = TrieNode(char)
			nodecnt += 1
			node.children.append(new_node)
			# Point to new child
			node = new_node
	# Insert word into node
	word = unichar.uc(word)
	newword = 1
	if word in node.article:
		# Join translations, eliminate duplicates, sort
		trans = list(dict.fromkeys(node.article[word] + trans))
		trans.sort()
		newword = 0
	node.article[word] = trans
	return newword


def find_prefix(root, prefix: str):
	"""
	Search for word starting with prefix and return its dictionary article
	"""
	node = root
	# If the root node has no children, then return nothing
	if not root.children:
		return []
	for char in prefix:
		char_not_found = True
		# Search through all the children of the present node
		for child in node.children:
			if child.char == char:
				# We found the char in the child, moving on to next letter
				char_not_found = False
				node = child
				break
		if char_not_found and node.children:
			# Return nothing if there are other characters
			# in branch but not what we were searching for
			return []
	# We found the prefix or the end of the branch. Return all words in branch
	return listWords(node)

eliminated = 0
def optimise(node, parentbusy):
	"""
	Eliminate branch elements that only point to a single child and don't hold words
	The first in the single branch will get the word from the end, rest deleted
	Recursive algorithm
	  end leaf (no children):
		returns word article
	  'busy' node (holds more children or a word):
		won't change, iterates through children flagging 'parent busy'
		return nothing
	  first 'non-busy' node with parent 'busy'
		calls child (chain) not flagging 'parent busy'
		if it returns an article, store it and delete child (chain)
		return nothing
	  'non-busy' node with parent 'non-busy'
		calls child (chain) not flagging 'parent busy'
		returns child's article (coming from the end leaf)
	Note that a first 'non-busy' node that has other 'busy' nodes down its child
	chain won't update as nothing will be returned to it
	"""
	global eliminated
	if len(node.children) == 0:
		# end leaf
		return node.article
	if len(node.children) == 1 and node.article == {}:
		# non-busy node
		article = optimise(node.children[0], 0)
		if parentbusy and article != {}:
			# first non-busy node down its chain, update & eliminate
			node.article = article
			node.children = []
			eliminated += 1
			return {}
		else:
			# not first non-busy or nothing returned, return what we got
			return article
	else:
		# busy node
		for child in node.children:
			optimise(child, 1)
		return {}


def listWords(node):
	retval = []
	for w in node.article:
		# Build list of dictionaries of words in article
		retval.append({w: node.article[w]})
	for child in node.children:
		# Append children's words to list
		for w in listWords(child):
			retval.append(w)
	return retval

def wcount(node):
	"""
	Count words in trie. Recursive, returns sum of own + children's word count
	"""
	cnt = len(node.article)
	for child in node.children:
		cnt += wcount(child)
	return cnt


def readDic(filename):
	dic = {}
	try:
		with gzip.open(filename, "rb") as fp:
			dic = pickle.load(fp)
			print("# Read", filename, ',', len(dic), "words")
	except IOError:
		print("Error: can\'t find file '"+filename+"' or read data")
	return dic


def saveDic(filename, dic):
	with gzip.open(filename, "wb") as fp:
		pickle.dump(dic, fp)
#	print("dic =", len(dic))


def importDB(root, filename):
	wordcnt = 0
	global nodecnt
	try:
		with open(filename, "rb") as fp:
			for w in fp:
				while len(w) <= 1:
					w = fp.readline()
				tr = []
				t = fp.readline()
				while len(t) > 1:
					tr.append(unichar.uc(t))
					t = fp.readline()
				wordcnt += add_w(root, w, tr)
			print("# Read \'"+filename+"\',", wordcnt, "words,", nodecnt, "nodes")
	except IOError:
		print("Error: can\'t find file \'"+filename+"\' or read data")
	return wordcnt


def readDB(filename):
	root = TrieNode('*')
	try:
		with gzip.open(filename, "rb") as fp:
			root = pickle.load(fp)
#			if __debug__:
#				print("# Read \'"+filename+"\',", wcount(root), "words")
	except IOError:
		print("Error: can\'t find file \'"+filename+"\' or read data")
	return root


def saveDB(root, filename):
	with gzip.open(filename, "wb") as fp:
		pickle.dump(root, fp)
	if __debug__:
		print("# Saved", wcount(root), "words to \'"+filename+"\'")


def main():

#	print(str(unicodedata.normalize('NFKD', sys.argv[1]).encode('ascii','ignore')))
#	print(unichar.udec(sys.argv[1]).lower())
#	sys.exit()

	if len(sys.argv) < 3 or not sys.argv[1] in ["am", "ma", "nm", "mn", "ed", "de"]:
		print("Error: parameter wrong or missing! Usage:", sys.argv[0], "<lang> <word_prefix>")
		print("Where lang is: (am|ma|nm|mn|ed|de), angol/magyar/német English/Deutsch")
		sys.exit(1)
	if sys.argv[2] == "--import":
		importText = 1
	else:
		importText = 0
	if importText:
		root = TrieNode('*')
		print("Importing DB")
		if __debug__:
			start = timer()
		importDB(root, "wl"+sys.argv[1]+".txt")
		if __debug__:
			print("# Elapsed time", timer() - start)
			print("Optimising trie of", wcount(root))
			start = timer()
		optimise(root, 1)
		if __debug__:
			global eliminated
			print("# Elapsed time", timer() - start)
			print("# Eliminated", eliminated, "nodes, word count", wcount(root))
	else:
		if __debug__:
			print("Loading DB")
			start = timer()
		root = readDB("wl"+sys.argv[1]+"_trie.pgz")
		if __debug__:
			print("# Elapsed time", timer() - start)

	if __debug__:
		start = timer()
	for w in find_prefix(root, unichar.udec(sys.argv[2]).lower()):
		for item in w:
			print(item)
			for t in w[item]:
				print("  ", t)
	if __debug__:
		print("# find_prefix() took", timer() - start)

	if importText:
		if __debug__:
			print("Saving DB")
			start = timer()
		saveDB(root, "wl"+sys.argv[1]+"_trie.pgz")
		if __debug__:
			print("# Elapsed time", timer() - start)

if __name__ == '__main__':
	main()
