def transposer(string: str, delim: str='\n'):
    '''
    @param string: The string to be transposed
    @param delim: The character that separates each set

    Assumes that each set is of equal length
    '''
    words = string.split(delim)
    words = [word for word in words if len(word) > 1]
    transposed = ''
    for i in range(len(words[0])):
        for elm in words:
            transposed = ''.join([transposed, elm[i]])
        transposed = ''.join([transposed, '\n'])
    return transposed

if __name__ == '__main__':
    s = 'column1\ncolumn2\ncolumn3\ncolumn4'
    t = transposer(s)
    print(t)
