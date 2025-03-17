#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import joern_cpg 
import json 
import os
import shutil
import pandas as pd
import getpass
    
junk_data_list = []
junk_counter = 0
print('initializing joern_cpg in main.py')
cpg = joern_cpg.Cpg()

print('initialization of joern_cpg.Cpg() in main.py ran to completion.')
file = "val.json"

print('loading json')
json_file = json.load(open(file))
print('json_file (val.json) uploaded in main.py.')

def ensure_permissions(folder):
    if os.path.exists(folder):
        # Change ownership to the current user
        os.system(f"sudo chown -R {getpass.getuser()}:{getpass.getuser()} {folder}")
        # Ensure write permissions
        os.chmod(folder, 0o777)
        print('Permissions changed to 777.')

# DataFrame
delta = []
message = []
print(f'length of json: {len(json_file)}')
for index in range(len(json_file)):
    print(f'index: {index}')
    try:
        for i,c in enumerate(json_file[index]['classes']):
            print('Ensuring proper permissions...')
            ensure_permissions("old")
            ensure_permissions("new")

            print('making directory old')
            os.makedirs("old",exist_ok=True)
            print('making directory new')
            os.makedirs("new",exist_ok=True)        
            print('opening and writing to old/')
            with open("old/"+c['class_name'].split("/")[0]+"dot"+str(i)+".java","w") as f:
                f.write(c['prev_code'])
            
            f.close()
            
            print('old/ closed. Opening and writing to new/'  )

            with open("new/"+c['class_name'].split("/")[0]+"dot"+str(i)+".java","w") as f:
                f.write(c['new_code'])
                            
            f.close()
            print('new/ closed')
        print('running sliced_graph in main.py')
        try:
            sliced_graph = cpg.get_dot("old", "new")
            print(f'sliced_graph ran to completion for {index}')
        except Exception as e:
            print(e)
            print('broke at running sliced_graph in main.py')
            break
        # print('sliced_graph ran to completion.')
        # Appending to the list 
        string1, string2, string3 = " "," "," "
        for x in sliced_graph.get_nodes():
            print('starting loop through sliced_graph')
            if x.get_attributes().get("TYPE") == "ADD":
                string1+=x.get_attributes().get("CODE")
            elif x.get_attributes().get("TYPE") == "DEL":
                string2+=x.get_attributes().get("CODE")
            elif x.get_attributes().get("TYPE") == "COMMON":
                string3+=x.get_attributes().get("CODE")

        delta.append(string1+"[SEP]"+string2+"[SEP]"+string3)
        message.append(json_file[index]['commit_message'])
                                      
        # Cleaning the directory space 
        print('removing directory old')
        shutil.rmtree("old")
        print('removing directory new')
        shutil.rmtree("new")
        print('removing file prev_file.dot')
        os.remove("prev_file.dot")
        print('removing file new_file.dot')
        os.remove("new_file.dot")
        print("Files completed : ", index)
        
    except:
        print('Something failed in for loop - check sliced_graph')
        junk_data_list.append(json_file[index])

        try:
            shutil.rmtree("old")
            shutil.rmtree("new")
            os.remove("prev_file.dot")
            os.remove("new_file.dot")
        except:
            pass

    

    df = pd.DataFrame()
    df["delta"] = delta
    df["message"] = message


    df.to_csv("data.csv", index=False)    