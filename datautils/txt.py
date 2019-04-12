
def extract(file_content):
    '''
    Read the contents of a text file

    Takes an open text file
    Returns a list of dicts of {header: content}
    '''
    return file_content.splitlines()

