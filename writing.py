with open('test.txt','r+') as file:
    f = file.write('hello how are you today')
    with open('test.txt','r') as line:
        d = line.read()
        print(d)  