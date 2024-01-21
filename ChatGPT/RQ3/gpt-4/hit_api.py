import openai
import pandas as pd
import os.path
import tiktoken
from tqdm import tqdm 
import time
from openai import OpenAI
import sys

def num_tokens_from_messages(messages, model="gpt-4-1106-preview"):
  """Returns the number of tokens used by a list of messages."""
  try:
    encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")

  if model == "gpt-4-1106-preview":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              try:
                print("encoding :",encoding.encode(value))
                num_tokens += len(encoding.encode(value))
              except:
                  print("Error encoding value:", value)
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
  print(encoding)

if __name__ == "__main__":
    while True:
        try:
            try:
                preivous_df = pd.read_csv("single_prompt_output_mp.csv")
                start_index = len(preivous_df['m_prompt1'])
                output_df = preivous_df
            except:
                output_df = pd.DataFrame(columns=["m_prompt1", "m_prompt2", "m_prompt3"])
                start_index = 0

            # Set up OpenAI API credentials
            openai.api_key = ""

            client = OpenAI(api_key=openai.api_key)
            # Set up GPT-4 model and parameters
            model_engine = "gpt-4-1106-preview"
            # model="gpt-3.5-turbo"

            # Read prompts from CSV file
            df = pd.read_csv("gpt4_input_data.csv")

            #Next will be mp1,2,3
            input_list = [[x,y,z] for x,y,z in zip(df['mp1'],df['mp2'],df['mp3'])]
            p1, p2, p3 = [], [], []
            
            print(f"{start_index} is the index we're starting from")
            if(start_index == len(input_list)):
                print("We're done here")
                break
            count = 0
            for current_index,ip in enumerate(tqdm(input_list[start_index:]), start=start_index):
                # print(ip)
                print(f"Processing input at index: {current_index}")  # Print the current index
                count +=1
                extracted_messages = [] 
                # Loop through each prompt and generate text
                reference = df.at[current_index, 'message']

                for index in range(3):
                    while True:
                        try:
                            messages = [
                                {"role": "user", "content": ip[index]},
                            ]

                            tokens = num_tokens_from_messages(messages)
                            if tokens > 128000:
                                print(f"Token length {tokens} exceeded maximum length of tokens 8000")
                                extracted_messages.append("OTKL")
                                # continue
                                break # Exit the while loop and continue with the next iteration of the for loop
                                
                            response = client.chat.completions.create(
                                    messages=messages,
                                    model="gpt-4-1106-preview")
                        
                            # extracted_response = response['choices'][0]['message']['content']
                            extracted_response = response.choices[0].message.content
                            extracted_messages.append(extracted_response)
                            break  # Exit the while loop successfully after processing
                        except Exception as e:
                            print(f"An error occurred: {e}. Retrying in 70 seconds...")
                            time.sleep(70)  # Sleep for 70 seconds before retrying
                            # The while loop will cause the code to retry the try block

                datapoint_dict = {"m_prompt1": extracted_messages[0],
                                    "m_prompt2": extracted_messages[1],
                                    "m_prompt3": extracted_messages[2],
                                    "references": reference
                                 }

                new_row_df = pd.DataFrame(datapoint_dict, index=[0])  # Use index=[0] to create a DataFrame with a single row

                output_df= output_df._append(new_row_df, ignore_index=True)

                # if count%10 == 0:
                output_df.to_csv("single_prompt_output_mp.csv", index=False)


            # output_df['references'] = df['message']
            # Save the output dataframe to a new CSV file
            # output_df.to_csv("single_prompt_output_mp.csv", index=False)
        except Exception as e:
            print("going again :", e)
            print(f"Exception occurred for {start_index}", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            lineno = exc_tb.tb_lineno
            print(f"Exception occurred on line {lineno}", e)

            time.sleep(70)
