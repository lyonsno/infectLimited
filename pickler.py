import pickle

extension = '.pkl'

def save_as(data, filename):
	enforce_extension(filename) 
	with open(filename, 'wb') as output:
		pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)

def load_file(filename):
	enforce_extension(filename)
	with open(filename, 'rb') as input:
		return pickle.load(input)

def enforce_extension(filename):
	if is_valid_filename(filename):
		return filename
	else:
		return filename + extension

def is_valid_filename(filename):
	if not filename.endswith(extension):
		return False
	return True

