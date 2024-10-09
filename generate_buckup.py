

import json

backup_file = 'events.json'
backup_path = 'D:\w\TG_OSO\\backup\\'
with open(backup_path+backup_file, 'r', encoding='utf-8') as file:
    file = file.read()
    with open(backup_path+f'{backup_file.split(".")[0]}_new', 'w', encoding='utf-8') as new_file:
        for line in json.loads(file):
            # print(json.dumps(line))
            new_file.write(str((line)).replace("'", '"').replace(", ", ',').replace(": ", ':')+'\n')  # .replace('$oid', 'oid')
            print(line)
    # file = file[1:-1]
    # print(file)
    # print(json.dumps(file))
# with open(backup_path+f'{backup_file}_new', 'w', encoding='utf-8') as file:
#     file.write(json.dumps(ff))
