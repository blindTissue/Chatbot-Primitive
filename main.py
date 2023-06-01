import openai
import os
import pandas as pd


MODEL = "gpt-3.5-turbo"
MAX_TOKEN_LENGTH = 4096
# token_length = 0

real_estate_dataframe = pd.read_csv("data.csv")

# read in column description
with open("col_description.txt", "r") as f:
    col_description = f.read()

api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

# Uses two gpt3.5 models. One to convert chat to command, and another to convert command to python code.
dataframe_modifier = [
    {
        "role": "system",
        "content": "You create python code to modify the dataframe. No explaination of code is required.",
    },
    {"role": "assistant", "content": "The dataframe is called real_estate_dataframe."},
    {
        "role": "assistant",
        "content": "You should also add print statement to show modified dataframe.",
    },
    {"role": "assistant", "content": "There are 14 columns in the dataframe."},
    {
        "role": "assistant",
        "content": "The columns are: " + ", ".join(real_estate_dataframe.columns) + ".",
    },
    {"role": "assistant", "content": col_description},
]

chat_to_command = [
    {
        "role": "system",
        "content": "You paraphrase the chat into concise command for python code generation.",
    },
]


while True:
    user_in = input("User: ")
    chat_to_command.append({"role": "user", "content": user_in})

    # creates chat to command
    command_out = openai.ChatCompletion.create(model=MODEL, messages=chat_to_command)

    # appends command to dataframe_modifier
    command_message = command_out["choices"][0]["message"]["content"]
    print(command_message)
    dataframe_modifier.append({"role": "user", "content": command_message})

    # creates python code
    out_to_code = openai.ChatCompletion.create(model=MODEL, messages=dataframe_modifier)

    code_message = out_to_code["choices"][0]["message"]["content"]
    print(code_message)

    # get only message between ```python ``` for code execution
    code_message = code_message.split("```python")[1].split("```")[0]

    print(out_to_code["choices"][0]["message"]["content"])
    print(code_message)
    
    exec(code_message)
