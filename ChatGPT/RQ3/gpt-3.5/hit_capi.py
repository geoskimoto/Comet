import openai
import pandas as pd
import os.path
import tiktoken
from tqdm import tqdm 
import time

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


while True:
    try:
        try:
            preivous_df = pd.read_csv("multi_message_output.csv")
            start_index = len(preivous_df['m_prompt1'])
            output_df = preivous_df
        except:
            output_df = pd.DataFrame(columns=["m_prompt1", "m_prompt2", "m_prompt3"])
            start_index = 0


        # Set up OpenAI API credentials
        openai.api_key = "YOUR API KEY"

        # Set up GPT-3.5 Turbo model and parameters
        model_engine = "gpt-3.5-turbo-16k"

        # Read prompts from CSV file
        df = pd.read_csv("chat_api_data.csv")

        #Next will be mp1,2,3
        input_list = [[x,y,z] for x,y,z in zip(df['mp1'],df['mp2'],df['mp3'])]
        p1, p2, p3 = [], [], []
        print(start_index)
        count = 0
        for ip in tqdm(input_list[start_index:]):
            count +=1
            extracted_messages = [] 
            # Loop through each prompt and generate text

            for index in range(3):
                messages = [
                    {"role": "user", "content": ip[index]},
                ]
                
                # Count the number of tokens in the prompt
                num_tokens = num_tokens_from_messages(messages)
                if num_tokens > 16383:
                    extracted_messages.append("Null Values due to token limit")
                    continue
                
                response = openai.ChatCompletion.create(
                    model=model_engine,
                    messages=messages
                )

                extracted_response = response.choices[0]["message"]['content']

                extracted_messages.append(extracted_response)

            datapoint_dict = {"m_prompt1": extracted_messages[0],
                              "m_prompt2": extracted_messages[1],
                              "m_prompt3": extracted_messages[2]
                              }

            new_row_df = pd.DataFrame(datapoint_dict, index=[0])  # Use index=[0] to create a DataFrame with a single row

            output_df= output_df._append(new_row_df, ignore_index=True)

            if count%10 == 0:
                output_df.to_csv("multi_message_output.csv", index=False)


        output_df['references'] = df['message']
        # Save the output dataframe to a new CSV file
        output_df.to_csv("multi_message_output.csv", index=False)
    except:
        print("going again")

    time.sleep(5)
