"""
Build a NNData class that will help us better manage our training and
testing data.
"""
from collections import deque
from enum import Enum
import numpy as np
import random
from math import floor


class DataMismatchError(Exception):
    """
    This custom exception is raised if our features and labels do not match
    in length.
    """

    def __init__(self, message):
        self.message = message


class NNData:
    class Order(Enum):
        """
        Define whether the training data is presented in the same order to NN
        each time, or in random order.
        """
        RANDOM = 0
        SEQUENTIAL = 1

    class Set(Enum):
        """
        This enum will help us identify whether we are requesting training set
        data or testing set data.
        """
        TRAIN = 0
        TEST = 1

    def __init__(self,
                 features: list = None,
                 labels: list = None,
                 train_factor: float = .9):
        """
        Class built to help us efficiently manage our training and testing
        data.
        :param features:
        :param labels:
        :param train_factor:
        """

        if features is None:
            self._features = []
        else:
            try:
                self.load_data(features=features, labels=labels)
            except (DataMismatchError, ValueError):
                self._features = None
                self._labels = None

        if labels is None:
            self._labels = []
        else:
            try:
                self.load_data(features=features, labels=labels)
            except (DataMismatchError, ValueError):
                self._features = None
                self._labels = None

        self._train_factor = self.percentage_limiter(train_factor)

        self._train_indices = []
        self._test_indices = []

        self._train_pool = deque()
        self._test_pool = deque()
        self.split_set()

    def split_set(self, new_train_factor=None):
        if self._features is None:
            self._train_indices = []
            self._test_indices = []
            return

        if new_train_factor is not None:
            self._train_factor = self.percentage_limiter(new_train_factor)

        size = len(self._features)
        available_indices = [i for i in range(0, size)]
        number_of_training_examples = floor(size * self._train_factor)
        while len(self._train_indices) < number_of_training_examples:
            r = random.randint(available_indices[0], available_indices[-1])
            if r in self._train_indices:
                continue
            else:
                self._train_indices.append(r)

        for i in available_indices:
            if i in self._train_indices:
                pass
            else:
                self._test_indices.append(i)

        self._train_indices.sort()
        self._test_indices.sort()

    @staticmethod
    def percentage_limiter(percentage: float):
        """
        Limits floats to a range between 0 and 1.
        :param percentage:
        :return:
        """
        if percentage > 1:
            return 1
        elif percentage < 0:
            return 0
        else:
            return percentage

    def load_data(self,
                  features=None,
                  labels=None):
        """
        Load features and labels into class instance.
        :param features:
        :param labels:
        :return:
        """

        if features is None:
            self._features = None
            self._labels = None
            return

        # Make sure features and labels are the same size.
        length_features = len(features)
        length_labels = len(labels)
        if length_features != length_labels:
            self._features = None
            self._labels = None
            raise DataMismatchError("Features and Labels must be of "
                                    "the same length.")

        else:
            try:
                self._features = np.array(features, dtype=float)
                self._labels = np.array(labels, dtype=float)
            except ValueError:
                self._features = None
                self._labels = None
                raise ValueError


def load_xor():
    """
    Defines an XOR feature and label set and
    creates a test object of our class with these sets.
    :return:
    """
    features = [[0, 0], [1, 0], [0, 1], [1, 1]]
    labels = [[0], [1], [1], [0]]

    test_xor_object = NNData(features=features,
                             labels=labels,
                             train_factor=1)


def unit_test():
    """
    Test constructor and methods from NNData class to make sure that they are
    up to spec.
    :return:
    """

    # Define good and bad feature/label sets
    bad_features_lengths = [[0, 0], [1, 0]]
    bad_features_values = [[0, 0], [1, "Cat"], [0, 1], [1, "Green"]]
    bad_label_value = [[0], [1], ["Cat"], [0]]
    features = [[0, 0], [1, 0], [0, 1], [1, 1]]
    labels = [[0], [1], [1], [0]]

    # Test DataMismatchError when calling load_data
    try:
        test1 = NNData()
        test1.load_data(features=bad_features_lengths, labels=labels)
        print("FAIL: NNData.load_data() did not raise DataMismatchError.")
    except DataMismatchError:
        print("SUCCESS: NNData.load_data() raises DataMismatchError when "
              "features and labels have different lengths.")

    # Test ValueError when non-float values called during method 'load_data'.
    try:
        test2 = NNData()
        test2.load_data(features=bad_features_values, labels=labels)
        print("FAIL: NNData.load_data() did not raise ValueError.")
    except ValueError:
        print("SUCCESS: NNData.load_data() raises ValueError when "
              "either features or labels include non-float values.")

    # Verify that if invalid data are passed to the constructor that labels and
    # features are set to None.
    test3 = NNData(bad_features_values, labels, .8)
    if test3._labels is None and test3._features is None:
        print("SUCCESS: invalid feature data passed to the constructor sets "
              "features and labels to None")
    else:
        print("FAIL: features or labels not set to None after invalid data "
              "passed to the constructor")

    test4 = NNData(features, bad_label_value, .8)
    if test4._labels is None and test4._features is None:
        print("SUCCESS: invalid label data passed to the constructor sets "
              "features and labels to None")
    else:
        print("FAIL: features or labels not set to None after invalid data "
              "passed to the constructor")

    # Verify that training factor is limited to range between 0 and 1
    test5 = NNData(features, labels, -5)
    if test5._train_factor == 0:
        print("SUCCESS: training factor limited to zero when negative value "
              "passed")
    else:
        print("FAIL: training factor not limited to zero when negative value "
              "passed")

    test6 = NNData(features, labels, 5)
    if test6._train_factor == 1:
        print("SUCCESS: training factor limited to one when a value greater "
              " than 1 was passed")
    else:
        print("FAIL: training factor not limited to 1 when a value greater "
              " than 1 passed")


def test():
    features = [[0, 0], [1, 0], [0, 1], [1, 1]]
    labels = [[0], [1], [1], [0]]
    x = list(range(10))
    print(features)
    y = x
    test_xor_object = NNData(features=x,
                             labels=y,
                             train_factor=.5)
    print(test_xor_object._features)

def unit_test1():
    errors = False
    try:
        # Create a valid small and large dataset to be used later
        x = list(range(10))
        y = x
        our_data_0 = NNData(x, y)
        print(our_data_0._features)
        x = list(range(100))
        y = x
        our_big_data = NNData(x, y, .5)


    except:
        print("There are errors that likely come from __init__ or a "
              "method called by __init__")
        errors = True

    # Test split_set to make sure the correct number of samples are in
    # each set, and that the indices do not overlap.
    try:
        our_data_0.split_set(.3)
        assert len(our_data_0._train_indices) == 3
        assert len(our_data_0._test_indices) == 7
        assert (list(set(our_data_0._train_indices +
                         our_data_0._test_indices))) == list(range(10))
    except:
        print("There are errors that likely come from split_set")
        errors = True  # Summary
    if errors:
        print("You have one or more errors.  Please fix them before "
              "submitting")
    else:
        print("No errors were identified by the unit test.")
        print("You should still double check that your code meets spec.")
        print("You should also check that PyCharm does not identify any "
              "PEP-8 issues.")


if __name__ == '__main__':
    test()
