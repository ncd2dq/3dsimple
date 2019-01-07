from main import create_env

def test_performance(env):
    import numpy as np
    #print string vs print array
    chars = ''.join(env)
    chars = bytes(chars, 'utf-8')
    a_chars = env
    np_chars = np.array(env)

    str_total = 0
    a_total = 0
    np_total = 0

    trials = 1000

    for i in range(trials):
        print('\rFull String------', end='')
        before = time.time()
        #os.system('cls')
        #print(chars, end='\r')
        sys.stdout.buffer.write(chars)
        after = time.time()
        str_total += after - before

        '''
        print('\rBoring Array------', end='')
        before = time.time()
        #os.system('cls')
        print(a_chars, end='')
        after = time.time()
        a_total += after - before

        print('\rNumpy Array------')
        before = time.time()
        #os.system('cls')
        print(np_chars, end='')
        after = time.time()
        np_total += after - before
        '''

    str_total /= trials
    a_total /= trials
    np_total /= trials

    print(str_total)
    print(a_total)
    print(np_total)

    #Best performance was python array, string/numpy are relatively close
    #os.system('cls') reduces run time to 0.02 (50fps) for all versions

if __name__ == '__main__':
    env = create_env()
    test_performance(env)
