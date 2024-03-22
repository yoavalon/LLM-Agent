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

output_loaction = '/home/algo/code/alpha/gpt/sequences/31'
np.random.seed(0) 

key = '**'
client = OpenAI(api_key=key)

pol = Policy()

def inference(source, target) : 

    request = f"""
    Given programs A and B, transform program A so that it becomes syntactically as similar as possible to program B while retaining its semantics. Imagine three different experts are answering this question. All experts will write down an intermediate program after applying one atomic transformation of their thinking to program A that maintains semantic equivalence and brings it syntactically closer to B. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. Please put the intermediate programs in code blocks. The final program should be the last program.

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

categories = ['144_A', '189_A', '266_B', '557_B', '596_B', '598_A']

#TODO for more accurate results we have to limit the programs
# categories = ['177_D2', '441_B', '316_A1', '567_B', '479_B', '178_A3', '218_B', '501_B', '518_C', '349_A', '579_B', '178_A1', '492_C', '614_B', '373_B', '178_A2', '583_B', '331_C1', '690_F1']

#Shorter programs list 
# categories = ['460_A', '112_A', '337_A', '141_A', '190_A', '236_A', '552_A', '509_A', '71_A', '182_B', '688_B', '598_A', '620_A', '110_B', '262_A', '355_A', '581_A', '168_A', '263_B', '104_A', '677_A', '630_R', '520_A', '479_A', '189_A', '199_A', '61_A', '466_A', '136_A', '478_B', '237_A', '49_A', '664_A', '131_A', '472_B', '519_B', '272_A', '278_A', '263_A', '617_A', '432_A', '546_A', '630_B', '59_A', '431_A', '139_A', '630_C', '478_A', '579_A', '99_A', '554_B', '9_A', '439_A', '202_A', '195_A', '58_A', '268_B', '669_A', '271_A', '148_A', '463_B', '41_A', '96_A', '255_B', '50_A', '81_A', '158_A', '327_B', '118_A', '347_A', '443_A', '625_B', '276_A', '266_A', '92_A', '488_A', '265_A', '171_A', '554_A', '339_A', '34_B', '630_J', '459_B', '146_A', '231_A', '513_A', '144_A', '12_A', '205_A', '385_A', '46_A', '401_A', '266_B', '630_A', '282_A', '439_B', '552_B', '630_L', '469_A', '313_A', '493_D', '129_A', '448_A', '75_A', '426_A', '4_A', '334_A', '224_A', '486_A', '208_A', '38_A', '110_A', '519_C', '160_A', '285_C', '350_A', '151_A', '118_B', '560_A', '672_A', '472_A', '332_A', '318_A', '584_A', '690_A1', '409_H', '122_A', '510_A', '84_A', '246_B', '465_A', '467_A', '1_A', '285_A', '158_B', '242_A', '246_A', '37_A', '194_A', '596_B', '610_A', '124_A', '233_A', '281_A', '270_B', '630_H', '500_A', '557_B', '133_A', '221_A', '228_A', '678_A', '137_B', '82_A']

df = pd.DataFrame()

#was 100
for i in trange(200) : 

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
    # if len(blocks) < 4 : 
    #     continue

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
