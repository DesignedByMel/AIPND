from classifier import classifier


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
    true = false = 0
   
    # Classifies each pet_image
    for pet_image, pet_label in petlabel_dic.items():
        # Gets classification label using the given model
        classifier_label = classifier(images_dir+'/'+pet_image, model).lower().strip()

        # Does the pet_label and the classified match? 
        match_results = False
        found_index = classifier_label.find(pet_label) 
        
        # TODOL THis neexs to be cleaner
        # checks that it was found
        if found_index >= 0:
            # rules out false positives for a single term
            if found_index == 0 and len(pet_label) == len(classifier_label):
                match_results = True
                true += 1
            # rules out false positives for multiple terms
            elif (found_index == 0 or classifier_label[found_index-1] == " ") and ((found_index+len(pet_label) == len(classifier_label)) or ((classifier_label[found_index+len(pet_label):found_index+len(pet_label)+1]) in (' ', ','))):
                match_results = True
                true += 1
            else:
                false += 1
        
        # Crreates the results directory 
        if pet_image not in results_dic:
            results_dic[pet_image] = [pet_label, classifier_label, match_results]
        else: 
            print('** Warning: Pet Image, ' + pet_image + ' already exisits')
    
    print("False:"+false+" True:"+true)
    return results_dic