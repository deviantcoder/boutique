def renumber_todo_list(input_file):
    with open(input_file, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        current_number = 1
        for line in lines:
            index = line.find('.')
            if index != -1:
                number = line[:index]
                if number.isdigit():
                    new_line = str(current_number) + line[index:]
                    current_number += 1
                    f.write(new_line)
                else:
                    f.write(line)
            else:
                f.write(line)
        f.truncate()

renumber_todo_list('D:/django/boutique/todo.txt')