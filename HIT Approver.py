import csv
import string

#This takes in a word input, and outputs a list of "close" words. #More specifically, this list contains the original word, 
#all variants of this word that are missing a letter, all variants of this word that have an extra letter, and all variants 
#of this word that have two swapped letters. This is to safeguard against minor misspellings, for free response questions. 
def close_words(word):
	new_words = [word]
	for i in range(len(word)):
		new_words += [word[0:i] + word[i+1:len(word)]]
		for p in string.ascii_lowercase:
			new_words += [word[0:i] + p + word[i+1:len(word)]]
		if i >= 1:
			new_words += [word[0:i-1] + word[i] + word[i-1] + word[i+1:len(word)]]
	return new_words

#This takes in a word input, and outputs a "simpler" version, that is lowercase, and contains no spaces or punctuation.
def simplify(word):
	w = word.lower().replace(' ','')
	for c in string.punctuation:
		w = w.replace(c,'')
	return w

#Given the CSV file name, the official answers, and the answer column name as inputs, returns a list of correct workers, 
#a list of all the rows in the CSV file, and the positions of the worker id, "Reading check", Approve, and Reject columns.
def read_file(file_name, answers, answer_column):
	with open(file_name, newline='', encoding = 'utf8') as csvfile:
		submissions_list = csv.reader(csvfile)
		position = {'id':0, 'check':0, 'approve':0, 'reject':0}
		row_list = []
		correct_workers = []
		#Go through all the rows in the input CSV file.
		for row in submissions_list:
			#Find and set the positions for the worker id, "Reading check", Approve, and Reject columns.
			if row[0] == 'HITId':
				position['id'] = row.index('WorkerId')
				position['check'] = row.index(answer_column)
				position['approve'] = row.index('Approve')
				position['reject'] = row.index('Reject')
			else:
				not_done = True
				#If an official answer is contained within (a close variant of) the worker's answer, 
				#add him/her to the correct_workers list.
				for entry in close_words(simplify(row[position['check']])):
					for answer in answers:
						if answer in entry and not_done:
							correct_workers.append(row[position['id']])
							not_done = False
			while len(row) <= position['reject']:
				row.append('')
			row_list.append(row)
	return (correct_workers, row_list, position)

#Given the CSV file name, the list of correct workers, the list of rows, the positions of relevant columns, 
#and a boolean(whether to reject "incorrect" workers too) as inputs, creates a new CSV file, which can then 
#be uploaded to MTurk to automatically approve (or reject) workers.
def write_file(file_name, correct_workers, row_list, position, also_reject):
	with open('New ' + file_name, 'w', newline='', encoding = 'utf8') as csvfile:
		approval_list = csv.writer(csvfile)
		for row in row_list:
			#Creates the header row for the CSV file.
			if row[0] == 'HITId':
				approval_list.writerow(row)
			else:
				new_row = row.copy()
				#Approves workers who were correct.
				if new_row[position['id']] in correct_workers:
					new_row[position['approve']] = 'x'
				#If also_reject is set to True, rejects workers who were incorrect.
				elif also_reject:
					new_row[position['reject']] = 'Incorrect Answer to first question.'
				approval_list.writerow(new_row)

#Given the CSV file name, the official answers, the answer column name, and a boolean (whether to reject "incorrect" workers too) 
#as inputs, creates a new CSV file, which can then be uploaded to MTurk to automatically approve (or reject) workers.
def auto_approve(file_name, answers, answer_column, also_reject = False):
	(correct_workers, row_list, position) = read_file(file_name, answers, answer_column)
	write_file(file_name, correct_workers, row_list, position, also_reject)

#An example function call. Please edit accordingly; note that all the official answers should be lowercase, and contain no 
#spaces or punctuation. Also, unless the reading check question is incredibly important, typically also_reject should be
#left as False (for surveys at least, people who give otherwise valid responses might answer the "Reading check" incorrectly).
auto_approve('HIT responses.csv', ['automationinnovation', 'innovationautomation', 'automationandinnovation', 'innovationandautomation'], 'Answer.Reading check')
