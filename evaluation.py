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

#TODO generate folder for all the material of one experiment !
#csv, figures, latex tables
#TODO check pylatex library??

class Evaluation():
    """
    Evaluation of sequence files
    For the use of unit tests this has to be run from console!
    """

    def __init__(self, experiment) : 
        """
        Initialize evaluation
        """

        #self.sequence_path = f'/home/algo/code/alpha/gpt/agent/sequences/{experiment}'        #TODO write the path in latex
        self.sequence_path = f'/home/algo/code/alpha/gpt/agent/sequences/{experiment}'        #TODO write the path in latex
        self.sample_base_path = '/home/algo/code/alpha/alpha_dataset/codeforces'
        self.results_base_path = '/home/algo/code/alpha/gpt/agent/results'

        #generate target folder
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        self.result_path = os.path.join(self.results_base_path, formatted_datetime)
        os.mkdir(self.result_path)

    def calculate_scores(self, reference, hypothesis, pre):
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
            f"{pre}_gleu_score": float(f'{gleu:0.3f}'),
            f"{pre}_chrf_score": float(f'{chrf:0.3f}'),
            f"{pre}_nist_score": float(f'{nist:0.3f}'),
            f"{pre}_codeBleu_score": float(f'{codebleu:0.3f}'),
            f"{pre}_meteor_score": float(f'{meteor:0.3f}'),
            f"{pre}_bleu_score": float(f'{bleu:0.3f}')
        }

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

    def compute_ged(self, first, second) : 
        """
        Compute the GED (graph edit distance)
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


            return difference, jaccard_similarity
        except : 
            return -1, -1

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
                    #print(f'{in_sample} failed')
                    break

        return np.mean(results)      
        #print(results)
        # if np.mean(results) == 1:
        # #if np.mean(results) > 0 :           #BUG should be the above
        #     #print("All tests passed")
        #     return 1            #TODO return the percentage of returned tests
        # else:
        #     #print('Some tests failed')
        #     return 0

    def analyze_similarity(self, visualize = True) :
        """
        Similarity analysis
        """

        # List of metrics
        metrics = ['gleu_score', 'chrf_score', 'nist_score', 'codeBleu_score','meteor_score', 'bleu_score']

        # Calculate the average, standard deviation, maximum, and minimum of metric scores over entries
        entry_labels = ['AB', 't1B', 't2B', 't3B', 't4B']
        averages = []
        std_deviations = []
        maximums = []
        minimums = []

        for metric in metrics:
            entries_data = self.df.filter(like=metric)
            entry_averages = entries_data.mean(axis=0, numeric_only=True)
            entry_std = entries_data.std(axis=0)
            entry_max = entries_data.max(axis=0)
            entry_min = entries_data.min(axis=0)
            averages.append(entry_averages)
            std_deviations.append(entry_std)
            maximums.append(entry_max)
            minimums.append(entry_min)

        if visualize : 
            # Create line plots for each metric with lines connecting average values between timestamps
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Average Metric Scores with Std Deviation, Max, and Min', fontsize=16)

            for i, metric in enumerate(metrics):
                ax = axes[i // 3, i % 3]

                #error here
                ax.plot(entry_labels, averages[i], marker='.', linestyle='-', label='Mean', linewidth =1 )

                x = entry_labels
                y = averages[i]
                std = std_deviations[i]
                max_val = maximums[i]
                min_val = minimums[i]

                # Fill between average and standard deviation
                ax.fill_between(x, y - std, y + std, alpha=0.1, label='Std Deviation', color='blue')

                # Fill between maximum and minimum
                ax.fill_between(x, min_val, max_val, alpha=0.1, label='Max/Min', color='green')

                ax.set_title(f'Average {metric}')
                #ax.set_xlabel('Entry')
                ax.set_ylabel('Average Score')
                ax.legend(loc = 'upper left')
                ax.grid(True) 

            plt.tight_layout()
            plt.subplots_adjust(top=0.9) #just required when subtitle
            plt.savefig(os.path.join(self.result_path, 'similarity.png'))
            plt.close()

    def analyze_validity(self, visualize = True) :
        """
        Similarity analysis
        """

        entries_data = self.df.filter(like='_valid')
        entry_averages = entries_data.mean(axis=0, numeric_only=True)
        entry_std = entries_data.std(axis=0)

        if visualize : 

            # Preparing the data for plotting
            x = np.arange(1, 5)  # Transformation steps
            y = entry_averages.to_numpy()
            error = entry_std

            # Plotting the data with error bars
            plt.fill_between(x, y - error, y + error, alpha=0.2)
            plt.plot(x, y, marker='o')
            plt.title('Mean Validity of Python Files with Standard Deviation')
            plt.xlabel('Transformation')
            plt.ylabel('Mean Validity')
            plt.xticks(x)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.result_path, 'validity.png'))
            plt.close()

    def analyze_unit_tests(self, visualize = True) :
        """
        Similarity analysis
        """

        entries_data = self.df.filter(like='_unit')
        entry_averages = entries_data.mean(axis=0, numeric_only=True)
        entry_std = entries_data.std(axis=0)

        if visualize : 

            # Preparing the data for plotting
            x = np.arange(1, 5)  # Transformation steps
            y = entry_averages.to_numpy()
            error = entry_std

            # Plotting the data with error bars
            plt.fill_between(x, y - error, y + error, alpha=0.2)
            plt.plot(x, y, marker='o')
            plt.title('Mean Success of Unit tests with Standard Deviation')
            plt.xlabel('Transformation')
            plt.ylabel('Mean Pass Rate')
            plt.xticks(x)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.result_path, 'unit_tests.png'))
            plt.close()

    def analyze_modularity(self, visualize = True) :
        """
        Similarity analysis
        """

        entries_data = self.df.filter(like='_ged')
        entries_data_replaced = entries_data.replace(-1, np.nan)
        entry_averages = entries_data.mean(axis=0, numeric_only=True)
        entry_std = entries_data.std(axis=0)

        if visualize : 

            # Preparing the data for plotting
            x = np.arange(1, 6)  # Transformation steps
            y = entry_averages.to_numpy()
            error = entry_std

            # Plotting the data with error bars
            plt.fill_between(x, y - error, y + error, alpha=0.2)
            plt.plot(x, y, marker='o')
            plt.title('Mean Jaccard Score with Standard Deviation')
            plt.xlabel('Transformation')
            plt.ylabel('Mean Jaccard')
            plt.xticks(x)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.result_path, 'modularity.png'))
            plt.close()

    def analysis(self) : 
        """
        Function to compute an analysis from the dataframe self.df
        Extraction of visualization should be managed here as well
        """

        self.analyze_similarity()
        self.analyze_validity()
        self.analyze_unit_tests()
        self.analyze_modularity()

    def process_data(self, write_csv = True, unit_test = False) : 
        """
        Process sequences and writing a csv 
        #TODO later export not required. We can handle the dataframe 
        """

        output_path = self.sequence_path
        folders = os.listdir(output_path)

        self.df = pd.DataFrame()

        for folder in tqdm(folders) : 

            pathSource = os.path.join(output_path, folder, 'source.py')
            with open(pathSource, 'r') as f :         
                source = f.read() 

            pathTarget = os.path.join(output_path, folder, 'target.py')
            with open(pathTarget, 'r') as f :         
                target = f.read() 

            #TODO make flexible for number of transformations 
            path1 = os.path.join(output_path, folder, '1.py')
            with open(path1, 'r') as f :         
                seq1 = f.read() 

            path2 = os.path.join(output_path, folder, '2.py')
            with open(path2, 'r') as f :         
                seq2 = f.read() 

            path3 = os.path.join(output_path, folder, '3.py')
            with open(path3, 'r') as f :         
                seq3 = f.read() 

            path4 = os.path.join(output_path, folder, '4.py')
            with open(path4, 'r') as f :         
                seq4 = f.read() 

            #compute similarity metrics
            scores_source_target = self.calculate_scores(source, target, 'a')
            scores_t1_target = self.calculate_scores(seq1, target, 'b')
            scores_t2_target = self.calculate_scores(seq2, target, 'c')
            scores_t3_target = self.calculate_scores(seq3, target, 'd')
            scores_t4_target = self.calculate_scores(seq4, target, 'e')

            #compute validity
            t1_val = self.is_valid_python(seq1)
            t2_val = self.is_valid_python(seq2)
            t3_val = self.is_valid_python(seq3)
            t4_val = self.is_valid_python(seq4)

            #compute GED   => changed to JACCARD score
            _, ged_1 = self.compute_ged(source, seq1)
            _, ged_2 = self.compute_ged(seq1, seq2)
            _, ged_3 = self.compute_ged(seq2, seq3)
            _, ged_4 = self.compute_ged(seq3, seq4)
            _, ged_5 = self.compute_ged(seq4, target)

            #compute unit tests
            pre = folder.split('_')
            cat = f'{pre[0]}_{pre[1]}'
            sample_path = os.path.join(self.sample_base_path, cat, 'samples')

            #results = {i: [] for i in range(1, 5)}
            number_of_tests = 10
            
            if unit_test : 
                t1_unit = self.test_program(sample_path, path1, number_of_tests)
                t2_unit = self.test_program(sample_path, path2, number_of_tests)
                t3_unit = self.test_program(sample_path, path3, number_of_tests)
                t4_unit = self.test_program(sample_path, path4, number_of_tests)
            else : 
                t1_unit, t2_unit, t3_unit, t4_unit = np.random.randint(0,2), np.random.randint(0,2), np.random.randint(0,2), np.random.randint(0,2)


            #Build data entry
            data = {} 
            programs = {'t1_valid' : t1_val, 't2_valid' : t2_val, 't3_valid' : t3_val, 't4_valid' : t4_val, 't1_ged' : ged_1, 't2_ged' : ged_2, 't3_ged' : ged_3, 't4_ged' : ged_4, 't5_ged' : ged_5, 't1_unit' : t1_unit, 't2_unit' : t2_unit, 't3_unit' : t3_unit, 't4_unit' : t4_unit} #, 'A' : source, 'B': target} #, 't4' : predicted_programs[3]}
            data.update({'sequence': folder})
            data.update(scores_source_target)
            data.update(scores_t1_target)
            data.update(scores_t2_target)
            data.update(scores_t3_target)
            data.update(scores_t4_target)
            data.update(programs)

            self.df = self.df.append(data, ignore_index=True)   #TODO replace append function (deprecated)

        if write_csv : 

            self.df.to_csv(f'{self.result_path}/results.csv', index=False)
            print('written to csv')

    def merge_images(self) : 
        """
        Merge graphs
        """

        from PIL import Image

        # Load the images
        large_image = Image.open(os.path.join(self.result_path, 'similarity.png'))
        small_image1 = Image.open(os.path.join(self.result_path, 'modularity.png'))
        small_image2 = Image.open(os.path.join(self.result_path, 'validity.png'))
        small_image3 = Image.open(os.path.join(self.result_path, 'unit_tests.png'))


        # Calculate total width of the three small images
        total_small_width = small_image1.width + small_image2.width + small_image3.width

        # Check if we need to resize the large image or add padding to small images
        if large_image.width < total_small_width:
            # Resize the large image to match the total width of the small images
            large_image = large_image.resize((total_small_width, large_image.height), Image.ANTIALIAS)
        elif large_image.width > total_small_width:
            # Calculate the extra width needed and add padding to the small images
            extra_width = large_image.width - total_small_width
            padding = Image.new('RGB', (extra_width // 3, small_image1.height))
            small_image1 = Image.new('RGB', (small_image1.width + extra_width // 3, small_image1.height))
            small_image2 = Image.new('RGB', (small_image2.width + extra_width // 3, small_image2.height))
            small_image3 = Image.new('RGB', (small_image3.width + extra_width - 2 * (extra_width // 3), small_image3.height))

        # Create a new image with the appropriate size
        new_height = large_image.height + small_image1.height
        new_image = Image.new('RGB', (large_image.width, new_height))

        # Paste the large image at the top
        new_image.paste(large_image, (0, 0))

        # Paste the small images at the bottom
        current_x = 0
        for img in [small_image1, small_image2, small_image3]:
            new_image.paste(img, (current_x, large_image.height))
            current_x += img.width     

        # Save or show the new image
        new_image.save(os.path.join(self.result_path, 'merged_image.png'))
        # new_image.show()  # Uncomment to display the image


    def generate_report(self) : 
        """
        Generate full report, containing images and tables 
        """

        geometry_options = {"tmargin": "1cm", "lmargin": "2cm"}
        doc = Document(geometry_options=geometry_options)

        self.merge_images()

        with doc.create(Figure(position='h!')) as pic:
            pic.add_image(os.path.join(self.result_path, 'merged_image.png'), width='500px')

        # with doc.create(Subsection('Validity')):

        #     # entries_data = self.df.filter(like='_valid')
        #     # entry_averages = entries_data.mean(axis=0, numeric_only=True)
        #     # entry_std = entries_data.std(axis=0)
        #     # x = np.arange(1, 5)  # Transformation steps
        #     # y = entry_averages.to_numpy()

        #     with doc.create(Tabular('rc|cl')) as table:
        #         table.add_hline()
        #         table.add_row((1, 2, 3, 4))
        #         table.add_hline(1, 2)
        #         table.add_empty_row()
        #         table.add_row((4, 5, 6, 7))

        doc.generate_pdf(os.path.join(self.result_path, 'report'), clean_tex=False)
        print(f'{Fore.GREEN}{os.path.join(self.result_path, "report")}{Fore.RESET}')

if __name__ == '__main__':
    
    import sys 
    print(sys.argv)

    experiment = sys.argv[-1]
    eva = Evaluation(experiment)
    eva.process_data(write_csv = True, unit_test=True)

    eva.analysis()
    eva.generate_report()

    print(eva.df.describe())

    entry_averages = eva.df.mean(axis=0, numeric_only=True)
    entry_std = eva.df.std(axis=0)    

    #TODO allow also to enter a csv manually for the analysis function afterwards..
    #TODO make it flexible for a varying number of transformations
