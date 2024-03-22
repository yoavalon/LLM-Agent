import os 
import numpy as np 
import subprocess
from openai import OpenAI
from tqdm import trange
from eval import Evaluation
from policy import Policy
from colorama import Fore, Back
import pandas as pd

"""
Code: Test gpt api ability to generate a complete transformation sequence.
Testing ToT prompt etc.

"""

output_loaction = '/home/algo/code/alpha/gpt/sequences/24'
np.random.seed(0) 

key = '**'
client = OpenAI(api_key=key)

pol = Policy()

def inference(source, target) : 

    request = f"""
    Given programs A and B, transform the first program so that it becomes syntactically more similar to the second program, while retaining its semantics. Think carefully and logically, explaining your answer. Show every intermediate program after applying each atomic transformation that maintains semantic equivalence. Don't repeat Program A or B in your answer. Please put the intermediate programs in code blocks.

    #Program A
    {source}

    #Program B
    {target}
    """

    completion = client.chat.completions.create(
    #model="gpt-3.5-turbo",
    model = "gpt-4",
    #model = "gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": request}
    ]
    )

    code = completion.choices[0].message.content

    return code

def extract_code_blocks(text):
    code_blocks = []
    in_code_block = False
    current_block = []

    for line in text.split('\n'):
        if line.strip() == '```python':
            in_code_block = True
        elif line.strip() == '```' and in_code_block:
            in_code_block = False
            code_blocks.append('\n'.join(current_block))
            current_block = []
        elif in_code_block:
            current_block.append(line)

    return code_blocks


def convert(source, target) : 
    """
    Reading from solution path and convert in temp file
    """

    #Convert from python2 to python3
    with open(source, 'r') as f :         
        solution = f.read() 

    with open(target, 'w') as f : 
        f.write(solution)

    subprocess.run(['2to3', target, '-w'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    with open(target, 'r') as f :
        ans = f.read()

    return ans 

base_path = '/home/algo/code/alpha/alpha_dataset/codeforces'   #/1_A/solutions_python'

categories = ['']


df = pd.DataFrame()

for i in trange(100) : 

  #try : 

    random_category = np.random.choice(categories)
    category_path = os.path.join(base_path, random_category)

    solutions = os.listdir(os.path.join(category_path, 'solutions_python'))
    if len(solutions) == 0 : 
        continue

    first_solution = np.random.choice(solutions)
    second_solution = np.random.choice(solutions)

    if first_solution == second_solution :      #edited
        continue

    source = os.path.join(category_path, 'solutions_python', first_solution)
    target = os.path.join(category_path, 'solutions_python', second_solution)

    source_program = convert(source, '/home/algo/code/alpha/gpt/agent/source.py')
    target_program = convert(target, '/home/algo/code/alpha/gpt/agent/target.py')

    intermediate_completions = inference(source_program, target_program)

    print(intermediate_completions)
    print('='*100)

    blocks = extract_code_blocks(intermediate_completions)

    print(len(blocks))
    if len(blocks) < 4 : 
        continue

    output_path = os.path.join(output_loaction, f'{random_category}_{first_solution.split(".")[0]}_{second_solution.split(".")[0]}')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    save_to = os.path.join(output_path, 'source.py')
    with open(save_to, 'w') as f : 
        f.write(source_program)

    save_to = os.path.join(output_path, 'target.py')
    with open(save_to, 'w') as f : 
        f.write(target_program)

    for nu, block in enumerate(blocks) : 

        save_to = os.path.join(output_path, f'{nu+1}.py')
        with open(save_to, 'w') as f : 
            f.write(block)
        
    save_to = os.path.join(output_path, f'answer.py')
    with open(save_to, 'w') as f : 
        f.write(intermediate_completions)
