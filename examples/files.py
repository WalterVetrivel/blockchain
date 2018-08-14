f = open('demo.txt', mode='w')  # w mode opens in write mode. Always overwrites content if file exists.
f.write('Praise the Lord')
f.close()  # needed to save changes to the file and to prevent memory leaks

f = open('demo.txt', mode='a')  # a mode to append content to file
f.write('. Jesus Christ is Lord.')
f.close()

f = open('demo.txt', mode='a')
f.write('\nChrist died for our sins and rose again.')  # \n to add new line
f.close()

f = open('demo.txt', mode='r')  # r mode to read
file_content = f.read()  # read entire content of file
print(file_content)
f.close()

f = open('demo.txt', mode='r')
file_lines = f.readlines()  # read multiline content and store in list
for index, line in enumerate(file_lines):
    print('Line ' + str(index + 1) + ': ' + line)
f.close()

with open('demo.txt', mode='r') as f:  # automatically closes the file
    line = f.readline()  # read one line at a time
    while line:
        print(line)
        line = f.readline()
