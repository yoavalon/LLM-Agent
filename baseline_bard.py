import os 
import numpy as np 
import subprocess
from openai import OpenAI
from tqdm import trange
from eval import Evaluation
from policy import Policy
from colorama import Fore, Back
import pandas as pd
from bardapi import Bard
import re 

print('in proto bard')

"""
Purpose of this code: 
1. Make LLM requests
2. Perform checks on the answer, or better: the top 5 answers (Validity, Unit tests, similarity, clone, jaccard on ast)
2.5 Document values
3. Agent gives a decision on the best answer

Purpose: 
Comparison between with and without agent. So build the ability to put things on/off inside this code.
Write evaluations in live to pd
"""

output_loaction = '/home/algo/code/alpha/gpt/agent/sequences/9'
np.random.seed(0) 

cookie = '__Secure-1PSID'
token = '***'
bard = Bard(token=token)

pol = Policy()

def extract_code_snippets(text):
  """Extracts code snippets enclosed with `python ... ` symbols from a string.

  Args:
    text: The string containing the code snippets.

  Returns:
    A list of code snippets, each represented as a string.
  """

  code_blocks = re.findall(r"`python\n(.*?)\n`", text, flags=re.DOTALL)
  return code_blocks

def inference(first, second, number_completions) : 

    request = f'Given programs {first} and {second}, transform the first program so that it becomes syntactically more similar to the second program, while retaining its semantics. Apply only one atomic transformations. Provide only the source code without your comments. Please provide 4 options.'
    response = bard.get_answer(request)#['code']
    code_snippets = extract_code_snippets(response['content'])

    return code_snippets 


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
categories = os.listdir(base_path)

df = pd.DataFrame()


for i in trange(20) : 

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

    output_path = os.path.join(output_loaction, f'{random_category}_{first_solution.split(".")[0]}_{second_solution.split(".")[0]}')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    save_to = os.path.join(output_path, 'source.py')
    with open(save_to, 'w') as f : 
        f.write(source_program)

    save_to = os.path.join(output_path, 'target.py')
    with open(save_to, 'w') as f : 
        f.write(target_program)

    #start here, but break before
    last = source_program
    evaluation = Evaluation()

    limit_unit_tests = 10
    number_of_completions = 4

    #valid, passed_unit_tests, code_bleu_score, mod_score  
    last_features = evaluation.live_check(random_category, source_program, last, last, target_program, limit_unit_tests)
    print('valid, passed_unit_tests, sim_source, sim_last, sim_target, mod_last, mod_target')
    print(last_features)
    print("="*50)
    #Mod score can be -1 in case it doesn't pass

    invalid = False

    #Compute n transformation steps
    for it in range(1,5) : 

        intermediate_completions = inference(last, target_program, number_of_completions)

        #iterate over first n answers and compute the scores/features
        features = []
        for infer in range(number_of_completions) : 
            intermediate = intermediate_completions.choices[infer].message.content

            feats = evaluation.live_check(random_category, source_program, last, intermediate, target_program, limit_unit_tests)
            #print(feats)
            features.append(feats)

        decision = pol.decide(features, last_features, agent_on = True)

        for infer2 in range(number_of_completions) : 
            if infer2 == decision : 
                print(f'{Fore.GREEN}{features[infer2]}{Fore.RESET}')
            else : 
                print(f'{Fore.BLUE}{features[infer2]}{Fore.RESET}')
        
        print(f'{Back.GREEN}{features[decision][4]}{Back.RESET}')

        #Apply decision and reinitialize last element and last features
        intermediate = intermediate_completions.choices[decision].message.content

        last_features = features[decision]
        last = intermediate 

        save_to = os.path.join(output_path, f'{it}.py')
        with open(save_to, 'w') as f : 
            f.write(intermediate)

        print("="*50)

#   except Exception as E:
#       print(f'error {E}') 
      

    # intermediate = inference(source_program, target_program)
    # save_to = os.path.join(output_path, '5.py')
    # with open(save_to, 'w') as f : 
    #     f.write(intermediate)
