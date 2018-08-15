import pickle
import json

content_list = []


def write_file(content):
    try:
        with open('user.txt', 'a') as f:
            f.write('\n')
            f.write(content)
    except FileNotFoundError:
        with open('user.txt', 'w') as f:
            f.write(content)


def read_file():
    try:
        with open('user.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return 'File not found'


def write_list_pickle():
    with open('pickle.p', 'wb') as f:
        write_content = {'list':content_list}
        f.write(pickle.dumps(write_content))
        return True
    return False


def write_list_json():
    with open('json.json', 'w') as f:
        f.write(json.dumps(content_list))
        return True
    return False


def load_pickle_data():
    with open('pickle.p', 'rb') as f:
        read_content = pickle.loads(f.read())
        return read_content['list']


def load_json_data():
    with open('json.json', 'r') as f:
        read_content = json.loads(f.read())
        return read_content


while True:
    print('1. Write to file')
    print('2. Output file contents')
    print('3. Store data in list')
    print('4. Write list using pickle')
    print('5. Write list using json')
    print('6. Load pickle data')
    print('7. Load json data')
    print('0. exit')

    choice = int(input('Enter your choice: '))

    if choice == 1:
        content = input('Enter the content you want to write: ')
        write_file(content)
        continue
    elif choice == 2:
        print(read_file())
        continue
    elif choice == 3:
        line = input('Enter the content: ')
        content_list.append(line)
        continue
    elif choice == 4:
        if write_list_pickle():
            content_list = []
        else:
            print('Unable to write the list to the file')
        continue
    elif choice == 5:
        if write_list_json():
            content_list = []
        else:
            print('Unable to write the list to the file')
        continue
    elif choice == 6:
        print(load_pickle_data())
        continue
    elif choice == 7:
        print(load_json_data())
        continue
    elif choice == 0:
        break
