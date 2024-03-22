import numpy as np 
from nltk.translate.gleu_score import sentence_gleu
from nltk.translate.chrf_score import sentence_chrf
from nltk.translate.nist_score import sentence_nist
from nltk.translate.meteor_score import single_meteor_score
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
import os 
import pandas as pd
from codebleu import calc_codebleu
import ast
import networkx as nx
import subprocess
from tqdm import trange, tqdm
import datetime
import matplotlib.pyplot as plt
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic
from colorama import Fore, Back
from collections import Counter
import re 

class Evaluation():
    """
    Evaluation of sequence files
    For the use of unit tests this has to be run from console!
    """

    def __init__(self) : 
        """
        Initialize evaluation
        """

        self.sample_base_path = '/home/algo/code/alpha/alpha_dataset/codeforces'
        self.results_base_path = '/home/algo/code/alpha/gpt/agent/results'

        self.temp_path = '/home/algo/code/alpha/gpt/agent/temp.py'

        #generate target folder
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        self.result_path = os.path.join(self.results_base_path, formatted_datetime)
        os.mkdir(self.result_path)

    def calculate_similarity(self, reference, hypothesis):
        """
        Compute similarity metrics
        """

        reference_tokens = word_tokenize(reference)
        hypothesis_tokens = word_tokenize(hypothesis)

        gleu = sentence_gleu([reference], hypothesis)
        chrf = sentence_chrf(reference, hypothesis)
        nist = sentence_nist([reference], hypothesis)
        meteor = single_meteor_score(reference_tokens, hypothesis_tokens)
        bleu = sentence_bleu([reference_tokens], hypothesis_tokens, weights=(0.5, 0.5), smoothing_function=SmoothingFunction().method1)

        codeBleu = calc_codebleu([reference], [hypothesis], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
        codebleu = codeBleu['codebleu']

        return {
            f"gleu_score": float(f'{gleu:0.3f}'),
            f"chrf_score": float(f'{chrf:0.3f}'),
            f"nist_score": float(f'{nist:0.3f}'),
            f"codeBleu_score": float(f'{codebleu:0.3f}'),
            f"meteor_score": float(f'{meteor:0.3f}'),
            f"bleu_score": float(f'{bleu:0.3f}')
        }, np.round(codebleu,3)

    def is_valid_python(self, source):
        try:
            # with open(file_path, 'r') as file:      #TODO multiple opening is not necessary
            #     source = file.read()
            ast.parse(source)
            return 1
        except SyntaxError:
            return 0

    def ast_to_networkx_tree(self, node):
        """
        Convert an AST node to a NetworkX graph representation.
        """
        graph = nx.DiGraph()
        def add_nodes_edges(node, parent=None):
            if parent is not None:
                graph.add_edge(parent, id(node))
            graph.add_node(id(node), label=str(type(node).__name__))
            for child in ast.iter_child_nodes(node):
                add_nodes_edges(child, parent=id(node))
        add_nodes_edges(node)

        return graph

    def compute_modularity(self, first, second) : 
        """
        Compute the Jaccard score
        """
        try  :
            # Parse the code into ASTs
            ast1 = ast.parse(first)
            ast2 = ast.parse(second)

            # Convert ASTs to graphs
            graph1 = self.ast_to_networkx_tree(ast1)
            graph2 = self.ast_to_networkx_tree(ast2)

            #GED = nx.graph_edit_distance(graph1, graph2)

            num_nodes_G1 = graph1.number_of_nodes()
            num_nodes_G2 = graph2.number_of_nodes()

            # Compute the difference
            difference = abs(num_nodes_G1 - num_nodes_G2)

            node_labels_list1 = [data['label'] for _, data in graph1.nodes(data=True)]
            node_labels_list2 = [data['label'] for _, data in graph2.nodes(data=True)]

            #compute the jaccard score
            edges_set1 = set(node_labels_list1)
            edges_set2 = set(node_labels_list2 )

            # Calculate the intersection and union of edge sets
            intersection = edges_set1.intersection(edges_set2)
            union = edges_set1.union(edges_set2)

            # Calculate the Jaccard similarity coefficient
            jaccard_similarity = len(intersection) / len(union)


            #return difference, jaccard_similarity
            return np.round(jaccard_similarity,3)
        except : 
            return -1

    def load_sample(self, base_path, in_name, out_name):
        """
        Read a single sample for unit test.
        """

        sample_input_path = os.path.join(base_path, in_name)
        sample_output_path = os.path.join(base_path, out_name)

        with open(sample_input_path, 'r') as f:
            sample_input = f.read().replace('...', '\n')

        with open(sample_output_path, 'r') as f:
            sample_output = f.read()

        return sample_input, sample_output

    def replace_last_newline(self, s, replacement=''):
        # Find the last occurrence of \n
        last_newline_index = s.rfind('\n')

        # Check if \n is found
        if last_newline_index != -1:
            # Slice and concatenate
            return s[:last_newline_index] + replacement + s[last_newline_index+1:]
        else:
            # If no \n found, return the original string
            return s

    def compare_outputs(self, expected, actual):

        expected = expected.replace(" ", "")
        actual = actual.replace(" ", "")

        expected = self.replace_last_newline(expected)
        actual = self.replace_last_newline(actual)

        # print(f'{Back.CYAN}{expected}{Back.RESET}')
        # print(f'{Back.MAGENTA}{actual}{Back.RESET}')

        # Step 1: Check if the outputs are identical as strings
        if str(expected) == str(actual):
            return True
        
        # if str(expected).replace(" ", "") == str(actual).replace(" ", ""):
        #     return True

        # Step 2: Try to compare as integers
        try:
            if int(expected) == int(actual):
                return True
        except ValueError:
            pass  # Move on to the next check if conversion to integer fails

        # Step 3: Try to compare as floats
        try:
            if float(expected) == float(actual):
                return True
        except ValueError:
            pass  # Move on to the next check if conversion to float fails

        try:

            filtered_str1 = re.sub(r'[^a-zA-Z0-9]', '', expected)
            filtered_str2 = re.sub(r'[^a-zA-Z0-9]', '', actual)
            if Counter(filtered_str1) == Counter(filtered_str2) :
                return True
        except : 
            pass 

        # If all checks fail, the outputs are not identical
        return False


    def unit_test(self, program_path, sample_input, sample_output, timeout_seconds=5):
        """
        Unit test program for sample pair with a timeout.
        
        :param program_path: Path to the program to be tested
        :param sample_input: The input to be passed to the program
        :param sample_output: The expected output of the program
        :param timeout_seconds: Maximum time in seconds to allow for execution
        :return: True if output matches, False otherwise
        """

        try:
            p = subprocess.run(['python3', program_path], input=sample_input, 
                            capture_output=True, text=True, timeout=timeout_seconds)

            # print('_'*50)
            # print(program_path)
            # print('Expected: ', sample_output)
            # print('Received: ', p.stdout)
            #input()

            #check validity
            computed_output = p.stdout.strip()

            result = self.compare_outputs(sample_output, computed_output)

            # if not result: 
            #     print('_'*50)
            #     print(program_path)
            #     print(f'{Back.CYAN}{sample_output}{Back.RESET}')
            #     print(f'{Back.MAGENTA}{computed_output}{Back.RESET}')

            # if not result : 
            #     print(f'{Fore.RED}invalid{Fore.RESET}')
            
            return result

        except subprocess.TimeoutExpired:
            print(f"Program exceeded time limit of {timeout_seconds} seconds.")
            return False
        except subprocess.CalledProcessError as e:
            print("Subprocess error:", e)
            return False

    def test_program(self, sample_path, program_path, limit = 5) : #base_path, program_path):
        """
        Load all samples and unit test.
        """
        #sample_dir = os.path.join(base_path, 'samples')
        samples = os.listdir(sample_path)

        results = []
        for i in range(min(len(samples)//2, limit)):
            in_sample = f'{i+1}_input.txt'
            out_sample = f'{i+1}_output.txt'

            if in_sample in samples and out_sample in samples:
                sample_input, sample_output = self.load_sample(sample_path, in_sample, out_sample)
                result = self.unit_test(program_path, sample_input, sample_output)
                results.append(result)

                if not result:
                    break
                
        #print(results)
        
        return np.mean(results)

        # if np.mean(results) == 1:
        #     return 1         
        # else:
        #     return 0


    def live_check(self, folder, source_program, last, first, second, num_of_tests) : 
        """
        Check all metrics live

        Inputs: 
            folder - required for unit tests 
            first - previous program 
            second - current program (LLM's answer)

        In terms of workflow: source and target checks have to be done before..
        Here we just compare with out asking where from. 
        Visualization also not here???      
        """

        #the idea is to write the csv live ..
        #Not sure it should be the same 

        valid = self.is_valid_python(second)        #TODO shall we just check the new/second one??? yes..

        sim_dic, sim_source = self.calculate_similarity(source_program, first)       
        sim_dic, sim_last = self.calculate_similarity(last, first)
        sim_dic, sim_target = self.calculate_similarity(first, second)    #So first can be changed to previous
        
        mod_last = self.compute_modularity(last, first)
        mod_target = self.compute_modularity(first, second)
        
        #obtain the folder for unit test samples
        pre = folder.split('_')
        cat = f'{pre[0]}_{pre[1]}'
        sample_path = os.path.join(self.sample_base_path, cat, 'samples')

        #temp file for unit tests
        temp_path = self.temp_path
        with open(temp_path, 'w') as f : 
            f.write(second)
        passed_unit_tests = self.test_program(sample_path, temp_path, limit = num_of_tests)

        return [valid, passed_unit_tests, sim_source, sim_last, sim_target, mod_last, mod_target]

if __name__ == '__main__':
    
    eva = Evaluation()
