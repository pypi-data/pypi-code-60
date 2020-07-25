import os
import sys

import psutil

from monk.pytorch_prototype import prototype
from monk.compare_prototype import compare
from monk.pip_unit_tests.pytorch.common import print_start
from monk.pip_unit_tests.pytorch.common import print_status


def test_optimizer_momentum_rmsprop(system_dict):
    forward = True;

    test = "test_optimizer_momentum_rmsprop";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward):
        try:
            gtf = prototype(verbose=0);
            gtf.Prototype("sample-project-1", "sample-experiment-1");
            gtf.Default(dataset_path="../../system_check_tests/datasets/dataset_cats_dogs_train", 
                model_name="resnet18", freeze_base_network=True, num_epochs=2);
            gtf.optimizer_momentum_rmsprop(0.01, weight_decay=0.0001, decay_rate=0.9);
            gtf.Train();
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
