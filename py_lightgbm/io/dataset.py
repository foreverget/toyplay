# -*- coding: utf-8 -*-


"""
@version: 1.0
@author: clark
@file: dataset.py
@time: 2017/7/8 10:59
@change_time:
1.2017/7/8 10:59 init dataset, add BinMapper
"""
from py_lightgbm.io.bin import BinMapper
from py_lightgbm.tree.feature_histogram import FeatureHistogram
from collections import Counter

import numpy as np


MIN_DATA_IN_BIN = 10


class MetaData(object):
    """
    store some meta data used for trainning data
    """
    def __init__(self):
        self._labels = []
        self._init_scores = []
        return


class Dataset(object):
    """
    The main class of dataset
    """
    def __init__(self, X, y, feature_name):
        self._train_X = X
        self._feature_names = feature_name
        self._num_data = self._train_X.shape[0]
        self._num_features = self._train_X.shape[1]

        self._labels = None
        self._label2real = {}
        self._real2label = {}
        self.create_label(y)

        self._init_score = None

        self._bin_mappers = None
        return

    @property
    def num_data(self):
        return self._num_data

    @property
    def num_features(self):
        return self._num_features

    @property
    def labels(self):
        return self._labels

    @property
    def init_score(self):
        return self._init_score

    def create_label(self, y):
        labels = np.zeros(y.shape)
        self._init_score = np.zeros(y.shape)

        raw_labels = Counter(labels).keys()
        self._label2real = {
            1: raw_labels[0],
            -1: raw_labels[1],
        }

        self._real2label = {
            raw_labels[0]: 1,
            raw_labels[1]: -1,
        }

        for i in xrange(y.shape[0]):
            labels[i] = self._real2label[y[i]]

        mean_y = np.mean(labels)

        self._init_score[:] = 1.0 / 2 * np.log((1 + mean_y) / (1 - mean_y))

        self._labels = labels
        return

    def construct_histograms(self, is_feature_used, data_indices, leaf_idx, gradients, hessians):
        ordered_gradients = gradients[data_indices]
        ordered_hessians = hessians[data_indices]

        feature_histograms = []
        # 为每一个feature建立一个Bin数据,Bin数据用于之后的划分
        for feature_index in xrange(self._num_features):
            feature_histogram = FeatureHistogram(feature_index, self._bin_mappers[feature_index])
            feature_histogram.init(self._train_X, data_indices, ordered_gradients, ordered_hessians)
            feature_histograms.append(feature_histogram)

        return feature_histograms

    def fix_histogram(self, feature_idx, sum_gradients, sum_hessian, num_data, histogram_data):

        return

    def split(self, feature, threshold, default_bin_for_zero, data_indices, num_data, lte_indices, gt_indices):

        return

    def construct(self, bin_mappers):
        self._bin_mappers = bin_mappers
        return

    def create_bin_mapper(self, max_bin):
        bin_mappers = []
        for i in xrange(self._num_features):
            bin_mapper = BinMapper()
            values = self._train_X[:, i]
            bin_mapper.find_bin(values, max_bin, min_data_in_bin=MIN_DATA_IN_BIN)
            bin_mappers.append(bin_mapper)
        return bin_mappers


if __name__ == '__main__':
    pass
