#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# PROGRAMMER: Melanie Burns
# DATE CREATED: April 30, 2018
# REVISED DATE: May 20, 2018 Finished the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Main program function defined below
def main():
    # collecting start time
    start_time = time()
    
    # line arguments
    in_args = get_input_args()
    
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(image_dir=in_args.dir)
    
    # create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(images_dir=in_args.dir, 
                                 petlabel_dic=answers_dic,
                                 model=in_args.arch)
    
    # adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, dogfile=in_args.dogfile)

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)

    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results(result_dic, results_stats_dic, model=in_args.arch,    
                  print_incorrect_dogs=True, print_incorrect_breeds=True)

    # by collecting end time
    sleep(20)
    end_time = time()

    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time 
    print("\n** Total Elapsed Runtime:", pretty_print_time(tot_time))

# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def pretty_print_time(time):
  # converts seconds to hh:mm:ss format
  time = [int((time/3600)), int((time%3600) / 60), int((time%3600) % 60)]
  return ':'.join(map(str, time))

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    parser = argparse.ArgumentParser()
    
    # dir - directory argument
    parser.add_argument('--dir', type = str, default = 'my_folder',
                        help ='path to the folder my_folder')
    # arch - CNN Model architecuture 
    parser.add_argument('--arch', type = str, default = 'resnet',
                        help = 'CNN Architecture model')
    parser.add_argument('--dogfile', type = str, default = 'dognames.txt',
                        help = 'Path the the file that contains valid dognames')
    
    # Returned the parsed arguments
    return parser.parse_args() 


def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    petlabels_dic = {}
    
    # retrieves the file_names and converts to labels
    for file_name in listdir(image_dir):
        # loswers the filename and then splits on '_' 
        word_list_pet_image = file_name.lower().split('_')
        
        # creates pet name labell, joins on spaces, and cleans it
        # This splices all words EXCEPT the num sequense and the filetype
        pet_label = ' '.join(word_list_pet_image[:-1]).strip()
        
        # places filenames and labels in the dic to return
        if file_name not in petlabels_dic:
            petlabels_dic[file_name] = pet_label
        else:
            print("** Warning: Pet Image={0} already exist.".format(file_name))
    
    return petlabels_dic
      
 
def classify_images(images_dir, petlabel_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    results_dic = {} 
   
    # Classifies each pet_image
    for pet_image, pet_label in petlabel_dic.items():
        # Gets classification label using the given model
        classifier_label = classifier(images_dir+'/'+pet_image, model).lower().strip()

        # Does the pet_label and the classified match? 
        match_results = 0
        found_index = classifier_label.find(pet_label) 
        
        # TODO this needs to be cleaner
        # checks that it was found
        if found_index >= 0:
            # rules out false positives for a single term
            if found_index == 0 and len(pet_label) == len(classifier_label):
                match_results = 1
            # rules out false positives for multiple terms
            elif (found_index == 0 or classifier_label[found_index-1] == " ") and ((found_index+len(pet_label) == len(classifier_label)) or ((classifier_label[found_index+len(pet_label):found_index+len(pet_label)+1]) in (' ', ','))):
                match_results = 1
        
        # Crreates the results directory 
        if pet_image not in results_dic:
            results_dic[pet_image] = [pet_label, classifier_label, match_results]
        else: 
            print('** Warning: Pet Image, ' + pet_image + ' already exisits')
    
    return results_dic


def adjust_results4_isadog(results_dic, dogfile):
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    
    # Reads in valid dog names
    dog_names_set = set()
    with open(dogfile) as dogfile_lines:
        for line in dogfile_lines:
            dog_names = line.split(',')
            for dog_name in dog_names:
                dog_name = dog_name.strip()
                dog_names_set.add(dog_name)
    
    # Test is a dog
    for key, results in results_dic.items():
        image_is_a_dog = 0
        classifier_is_a_dog = 0
        
        # Pet Image label 'is a' dog
        if results[0] in dog_names_set:
           image_is_a_dog = 1
            
        # Classifier label 'is a' dog
        for class_label_name in results[1].split(','):
            if class_label_name.strip() in dog_names_set:
                classifier_is_a_dog = 1
                break
        
        # extends the results list
        results_dic[key].extend((image_is_a_dog, classifier_is_a_dog))


def calculates_results_stats(results_dic):
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    # Initialize the results stats dictionary 
    count_keys = ['n_images', 'n_dog_images', 'n_correct_dogs', 'n_correct_breed', 
                  'n_correct_non_dogs', 'n_not_dog_images', 'n_label_matches']
    pct_keys = ['pct_correct_dogs', 'pct_correct_non_dogs', 'pct_correct_breed',
                'pct_label_matches']
    results_stats = {key:0 for key in count_keys + pct_keys} 
    
    # Calculate the counts
    results_stats['n_images'] = len(results_dic) 
    for result_list in results_dic.values():
        # Correct dogs and non-dog matches
        if result_list[3] == 1 and result_list[4] == 1:
            results_stats['n_correct_dogs'] += 1
        elif result_list[3] == 0 and result_list[4] == 0:
            results_stats['n_correct_non_dogs'] += 1
            
        # Is a dog
        if result_list[3] == 1:
            results_stats['n_dog_images'] += 1
        else:
            results_stats['n_not_dog_images'] += 1 
    
        # Correct breed matches (pet label is a dog and labels match)
        if result_list[3] == 1 and result_list[2] == 1:
            results_stats['n_correct_breed'] += 1
        
        # Labels match
        if result_list[2] == 1:
            results_stats['n_label_matches'] += 1
            
    # Calculate the percentages
    # Calculate pct of correct dogs and breeds
    if results_stats['n_dog_images'] > 0:
        results_stats['pct_correct_dogs'] = 100 * (results_stats['n_correct_dogs']/
                                                   results_stats['n_dog_images'])
        results_stats['pct_correct_breed'] = 100 * (results_stats['n_correct_breed']/
                                                   results_stats['n_dog_images'])
    else: 
        results_stats['pct_correct_dogs'] = 0      
        results_stats['pct_correct_breed'] = 0
    
    # Calculate percentaget of coreectly classified non-dog
    if results_stats['n_not_dog_images'] > 0:
        results_stats['pct_correct_non_dogs'] = 100 *       (results_stats['n_correct_non_dogs']/results_stats['n_not_dog_images'])
    else: 
        results_stats['pct_correct_non_dogs'] = 0      
        
     # Calculate percentage of label matches
    if results_stats['n_images'] > 0:
        results_stats['pct_label_matches'] = 100 *             (results_stats['n_label_matches']/results_stats['n_images'])
    else: 
        results_stats['pct_label_matches'] = 0  
      
    # completed stats
    return results_stats
        
def print_results(results_dic, results_stats, model, 
                  print_incorrect_dogs=False, print_incorrect_breeds=False):
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    # Taken from the lab solution as their formatting was really nice
    print("\n\n**** Results Summary for CCN Model Arch.. {0} ***".format(model.upper()))
    print("%20s: %3d" % ('N Images', results_stats['n_images']))
    print("%20s: %3d" % ('N Dog Images', results_stats['n_dog_images']))
    print("%20s: %3d" % ('N Not-Dog Images', results_stats['n_not_dog_images']))
    
    for key in results_stats:
        if 'pct_' in key:
            print("%20s: %5.1f" % (key, results_stats[key]))
    
    
    # IF print_incorrect_dogs == True AND there were images incorrectly 
    # classified as dogs or vice versa - print out these cases
    if (print_incorrect_dogs and 
        ( (results_stats['n_correct_dogs'] + results_stats['n_correct_non_dogs'])
          != results_stats['n_images'] ) 
       ):
        print("\nINCORRECT Dog/NOT Dog Assignments:")

        # process through results dict, printing incorrectly classified dogs
        for key in results_dic:

            # Pet Image Label is a Dog - Classified as NOT-A-DOG -OR- 
            # Pet Image Label is NOT-a-Dog - Classified as a-DOG
            if sum(results_dic[key][3:]) == 1:
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                          results_dic[key][1]))

    # IF print_incorrect_breed == True AND there were dogs whose breeds 
    # were incorrectly classified - print out these cases                    
    if (print_incorrect_breeds and 
        (results_stats['n_correct_dogs'] != results_stats['n_correct_breed']) 
       ):
        print("\nINCORRECT Dog Breed Assignment:")

        # process through results dict, printing incorrectly classified breeds
        for key in results_dic:

            # Pet Image Label is-a-Dog, classified as-a-dog but is WRONG breed
            if ( sum(results_dic[key][3:]) == 2 and
                results_dic[key][2] == 0 ):
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0], results_dic[key][1]))
       
         
# Call to main function to run the program
if __name__ == "__main__":
    main()
