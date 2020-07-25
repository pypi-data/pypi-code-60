import os
import sys

import psutil

from monk.pytorch_prototype import prototype
from monk.compare_prototype import compare
from monk.pip_functionality_tests.pytorch.common import print_start
from monk.pip_functionality_tests.pytorch.common import print_status



def test_analyse(system_dict):
    forward = True;

    test = "analyse_object_creation";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward):
        try:
            ptf = prototype(verbose=0);
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");


    test = "analyse_Prototype()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            ptf.Prototype("sample-project-1", "sample-experiment-1");
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");


    test = "analyse_Default()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            ptf.Default(dataset_path="../datasets/dataset_cats_dogs_train", 
                model_name="resnet18", freeze_base_network=True, num_epochs=2);
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");


    test = "analyse_Analyse_Learning_Rates()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            analysis_name = "analyse_learning_rates"
            lrs = [0.1, 0.05];
            epochs=2
            percent_data=40
            analysis = ptf.Analyse_Learning_Rates(analysis_name, lrs, percent_data, num_epochs=epochs, state="keep_none");
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");


    test = "analyse_Analyse_Input_Sizes()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            analysis_name = "analyse_input_sizes";
            input_sizes = [128, 256];
            epochs=2;
            percent_data=40;
            analysis = ptf.Analyse_Input_Sizes(analysis_name, input_sizes, percent_data, num_epochs=epochs, state="keep_none");
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");



    test = "analyse_Analyse_Batch_Sizes()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            analysis_name = "analyse_batch_sizes";
            batch_sizes = [2, 3];
            epochs = 2;
            percent_data = 40;
            analysis = ptf.Analyse_Batch_Sizes(analysis_name, batch_sizes, percent_data, num_epochs=epochs, state="keep_none");
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");




    test = "analyse_Analyse_Models()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            analysis_name = "analyse_models";
            models = [["resnet18", True, True], ["resnet34", False, True]]; 
            percent_data=40;
            analysis = ptf.Analyse_Models(analysis_name, models, percent_data, num_epochs=epochs, state="keep_none");
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");



    test = "analyse_Analyse_Optimizers()";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward): 
        try:
            analysis_name = "analyse_optimizers";
            optimizers = ["sgd", "adam"];
            epochs = 2;
            percent_data = 40;
            analysis = ptf.Analyse_Optimizers(analysis_name, optimizers, percent_data, num_epochs=epochs, state="keep_none");
            system_dict["successful_tests"] += 1;
            print_status("Pass");
        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");







    

    return system_dict