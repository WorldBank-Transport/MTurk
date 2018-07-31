import csv
import string

#This takes in a phrase input, and seperates it into lowercase words, dividing on punctuation and spaces.
def seperate(phrase):
	w = phrase.lower()
	for p in string.punctuation:
		w = w.replace(p, ' ')
	return w.split(' ')

#Given a word_dict (a dictionary with keys that refer to specific questions. Those keys map to dictionaries 
#that contain keys of words that map to their frequencies), the list of demographic question columns, and a 
#minimum word length as inputs, this outputs dictionary word_stats, which is essentially the same as word_dict,
#except with small words for non-demographic questions excluded, and the words sorted in lists. 
def compiler(word_dict, demographic_columns, min_word_length):
	word_stats = {}
	for key in word_dict:
		temp_list = []
		for minorkey in word_dict[key]:
			#If the word is long enough, or if it is a response to a demographic question, add it 
			#and its frequency to temp_list
			if len(minorkey) >= min_word_length or key in demographic_columns:
				temp_list.append([minorkey, word_dict[key][minorkey]])
		temp_list.sort(key=lambda x: x[1], reverse = True)
		word_stats[key] = temp_list
	return word_stats

#Given the name of the relevant CSV file, along with a list of the names of the answer and demographic 
#columns, and a boolean (whether to include all responses), this outputs word_dict, which is a dictionary
#with column names as keys; those keys map to dictionaries, with words as keys that map to their frequencies.
def read_file(file_name, answer_columns, demographic_columns, all_responses):
	with open(file_name, newline='', encoding = 'utf8') as csvfile:
		submissions_list = csv.reader(csvfile)
		columns = answer_columns + demographic_columns
		position = []
		word_dict = {}
		status = 0
		for row in submissions_list:
			#Find and assign the position of relevant columns
			if row[0] == 'HITId':
				status = row.index('AssignmentStatus')
				for i in range(len(columns)):
					position.append(row.index(columns[i]))
					word_dict[columns[i]] = {}
			else:
				#If the work was approved, or if all_responses is True, go through and add
				#the relevant words to word_dict
				if row[status] == 'Approved' or all_responses:
					for i in range(len(columns)):
						if columns[i] in answer_columns:
							word_list = seperate(row[position[i]])
						else:
							word_list = [row[position[i]]]
						for word in word_list:
							word_dict[columns[i]][word] = word_dict[columns[i]].get(word, 0) + 1
	return word_dict

#Given the name of the relevant CSV file, a list of all the column names, and the word_stats dictionary,
#this creates multiple CSV files, containing words and their frequences for each desired column.
def write_file(file_name, columns, word_stats):
	for column in columns:
		with open(column + ' statistics for ' + file_name, 'w', newline='', encoding = 'utf8') as csvfile:
			rows = csv.writer(csvfile)
			rows.writerow([column, 'Frequency'])
			for row in word_stats[column]:
				rows.writerow(row)

#Given the name of the relevant CSV file, a list of all the column names, a boolean (whether to include all responses),
#and a minimum word length, this creates multiple CSV files, containing words and their frequences for each desired column.
def auto_stats(file_name, answer_columns, demographic_columns, all_responses = False, min_word_length = 4):
	word_dict = read_file(file_name, answer_columns, demographic_columns, all_responses)
	word_stats = compiler(word_dict, demographic_columns, min_word_length)
	columns = answer_columns + demographic_columns
	write_file(file_name, columns, word_stats)

#An example function call. Please edit accordingly; note that all_responses is set by default to False, and 
#min_word_length is set by default to 4. You can change these values, if you want.
auto_stats('HIT responses.csv', ['Answer.New', 'Answer.Old decline', 'Answer.Old steady'], ['Answer.Nationality'])