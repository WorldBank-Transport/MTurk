import csv
import string

#Given a response_dict dictionary, containing keys of responses mapping to their frequency, and a total, this return 
#the majority response if it's more than one and more than half the total, along with the number of people who put
#that response. If no such response exists, this just returns ["",""]
def consensus_answer(response_dict, total):
	if len(response_dict) == 0:
		return ['','']
	for response in response_dict:
		if response_dict[response] > max(1, total/2):
			return [response, str(response_dict[response]) + ' out of ' + str(total)]
	return ['','']

#This takes in a word input, and outputs a "simpler" version, that is lowercase, and contains no spaces or punctuation.
def simplify(word):
	w = word.lower().replace(' ','')
	for c in string.punctuation:
		w = w.replace(c,'')
	return w

#Given a dictionary of answers input, this returns a list of rows (to be input into a CSV file creator), such that 
#each row either contains the relevant majority responses, or blank strings if no such response exists.
def consensus_builder(answers):
	row_list = []
	#Go through each key in answers (in this case, each specific image being tagged)
	for key in answers.keys():
		current_row = []
		current_row += list(key)
		#Go through each question (what is the shape of the roof, etc.) that was asked.
		for j in range(len(answers[key][0])):
			#Create the response_dict, and then call consensus_answer function.
			response_dict = {}
			total = 0
			#Go through each respondent
			for i in range(len(answers[key])):
				total += 1
				a = answers[key][i][j]
				response_dict[a] = response_dict.get(a,0) + 1
			current_row += consensus_answer(response_dict, total)
		row_list.append(current_row)
	return row_list

#Given the name of the relevant CSV file, along with the names of the background and answer columns, as input,
#this returns a dictionary of answers, with keys referring to the specific image being tagged, in this case. 
#These keys map to a list of responses recieved, that were not rejected.
def read_file(file_name, background_columns, answer_columns):
	with open(file_name, newline='', encoding = 'utf8') as csvfile:
		submissions_list = csv.reader(csvfile)
		status = 0
		background_position = {}
		answer_position = {}
		answers = {}
		for row in submissions_list:
			#Finding and assigning the relevant positions.
			if row[0] == 'HITId':
				status = row.index('AssignmentStatus')
				for i in range(len(background_columns)):
					background_position[i] = row.index(background_columns[i])
				for i in range(len(answer_columns)):
					answer_position[i] = row.index(answer_columns[i])
			else:
				#If the response has not been rejected, go through and collate its response into a list,
				#temp_val. Add it to the dictionary answers (or edit its value if it's already in answers).
				if row[status] != 'Rejected':
					bad_key = []
					for i in range(len(background_position)):
						bad_key.append(row[background_position[i]])
					temp_key = tuple(bad_key)
					temp_val = []
					for i in range(len(answer_position)):
						temp_val.append(row[answer_position[i]])
					answers[temp_key] = answers.get(temp_key, []) + [temp_val]
	return answers

#Given the name of the relevant  CSV file, along with a list of rows and the names of background and answer columns,
#this goes through and creates a new CSV file, containing the majority opinion responses for each image and each question,
#if available.
def write_file(file_name, row_list, background_columns, answer_columns):
	with open('Majority opinion ' + file_name, 'w', newline='', encoding = 'utf8') as csvfile:
		rows = csv.writer(csvfile)
		top_row = []
		top_row += background_columns
		for c in answer_columns:
			top_row.append(c)
			top_row.append('Frequency')
		rows.writerow(top_row)
		for row in row_list:
			rows.writerow(row)

#Given the name of the relevant  CSV file, along with the names of background and answer columns, this goes through and 
#creates a new CSV file, containing the majority opinion responses for each image and each question, if available.
def auto_majority(file_name, background_columns, answer_columns):
	answers = read_file(file_name, background_columns, answer_columns)
	row_list = consensus_builder(answers)
	write_file(file_name, row_list, background_columns, answer_columns)

#An example function call. Please edit accordingly.
auto_majority('HIT answers.csv', ['Input.File', 'Input.Name', 'Input.Url'], ['Answer.Bad image', 'Answer.Roof Material', 'Answer.Roof Shape'])