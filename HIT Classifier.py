import csv

#Given the name of the task workers CSV file, and a boolean (of whether to classify all workers), 
#as inputs, this returns a list of workers who should be classified.
def read_key(key_name, all_responses):
	with open(key_name, newline='', encoding = 'utf8') as csvfile:
		submissions_list = csv.reader(csvfile)
		position = {'id':0, 'status':0}
		row_list = []
		classified_workers = []
		#Go through all the rows in the input CSV file.
		for row in submissions_list:
			row_list.append(row)
			#Find and set the positions for the worker id and assignment status columns.
			if row[0] == 'HITId':
				position['id'] = row.index('WorkerId')
				position['status'] = row.index('AssignmentStatus')
			else:
				#Add the relevant workers to the list of workers who should be classifed.
				if row[position['status']] == 'Approved' or all_responses:
					classified_workers.append(row[position['id']])
	return classified_workers

#Given the name of the all workers CSV file, and the name of the relevant qualification, as inputs, 
#this returns a list of the CSV rows, along with the positions of the worker id and classifier columns.
def read_file(file_name, qualification):
	with open(file_name, newline='', encoding = 'utf8') as csvfile:
		submissions_list = csv.reader(csvfile)
		position = {'id':0, 'classifier':0}
		row_list = []
		for row in submissions_list:
			row_list.append(row)
			if row[0] == 'Worker ID':
				position['classifier'] = row.index('UPDATE-' + qualification)
	return (row_list, position)

#Given a list of the workers to be classified, along with a list of rows of the all workers CSV file, 
#along with the positions of the worker id and classifier columns, this creates a new CSV file, called 
#"Classified workers.csv", in which the relevant workers are classified.
def write_file(classified_workers, row_list, position):
	with open('Classified workers.csv', 'w', newline='', encoding = 'utf8') as csvfile:
		classification_list = csv.writer(csvfile)
		for row in row_list:
			#Create the header row for the new CSV file.
			if row[0] == 'Worker ID':
				classification_list.writerow(row)
			else:
				#Classify the relevant workers.
				new_row = row.copy()
				if new_row[position['id']] in classified_workers:
					new_row[position['classifier']] = 100
				classification_list.writerow(new_row)

#Given the names of the task worker and all worker CSV files, along with the qualification name and a 
#boolean (whether to include all responses), creates a new CSV file in which the relevant workers are
#classified.
def auto_classify(key_name, file_name, qualification, all_responses = False):
	classified_workers = read_key(key_name, all_responses)
	(row_list, position) = read_file(file_name, qualification)
	write_file(classified_workers, row_list, position)

#An example function call. Please edit accordingly; note that all_responses is set by default to False.
#You can set all_responses to True, if you want.
auto_classify('HIT workers.csv', 'All workers.csv', 'Answered Survey')