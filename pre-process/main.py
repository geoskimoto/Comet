#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import joern_cpg 
import json 
import os
import shutil
import pandas as pd
    
junk_data_list = []
junk_counter = 0
cpg = joern_cpg.Cpg()

file = "val.json"

json_file = json.load(open(file))

# DataFrame
delta = []
message = []

for index in range(len(json_file)):

    try:

        for i,c in enumerate(json_file[index]['classes']):
            
            os.makedirs("old",exist_ok=True)
            os.makedirs("new",exist_ok=True)        

            with open("old/"+c['class_name'].split("/")[0]+"dot"+str(i)+".java","w") as f:
                f.write(c['prev_code'])
            
            f.close()
            
            with open("new/"+c['class_name'].split("/")[0]+"dot"+str(i)+".java","w") as f:
                f.write(c['new_code'])
                            
            f.close()
        
        sliced_graph = cpg.get_dot("old", "new")

        # Appending to the list 
        string1, string2, string3 = " "," "," "
        for x in sliced_graph.get_nodes():
            if x.get_attributes().get("TYPE") == "ADD":
                string1+=x.get_attributes().get("CODE")
            elif x.get_attributes().get("TYPE") == "DEL":
                string2+=x.get_attributes().get("CODE")
            elif x.get_attributes().get("TYPE") == "COMMON":
                string3+=x.get_attributes().get("CODE")

        delta.append(string1+"[SEP]"+string2+"[SEP]"+string3)
        message.append(json_file[index]['commit_message'])
                                      
        # Cleaning the directory space 
        shutil.rmtree("old")
        shutil.rmtree("new")
        os.remove("prev_file.dot")
        os.remove("new_file.dot")
        print("Files completed : ", index)
        
    except:
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