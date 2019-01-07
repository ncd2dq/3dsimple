def transposer(string: str, delim: str='\n'):
    '''
    @param string: The string to be transposed
    @param delim: The character that separates each set

    Takes a screen represented by a string of characters, each column of
    the screen separated by @param delim and transposes it. Each separated set must be the
    same length.
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
