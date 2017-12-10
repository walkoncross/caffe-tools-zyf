#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import caffe
import numpy as np

import sys
import argparse


def parse_argv(argvs):
    parser = argparse.ArgumentParser()

    # Required arguments: input and output files.
    parser.add_argument(
        "input_file",
        help="Input binaryproto filename."
    )

    parser.add_argument(
        "output_file",
        help="Output npy filename."
    )

    args = parser.parse_args(argvs)

    return args


def binaryproto_to_npy(bp_file, npy_file=None):
    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(bp_file, 'rb').read()
    blob.ParseFromString(data)

    array = np.array(caffe.io.blobproto_to_array(blob))
    print 'loaded mean array shape: ', array.shape
    print 'per-channel mean: ', mean_array.mean(2).mean(2)

    mean_npy = array[0]
    if npy_file is not None:
        np.save(npy_file, mean_npy)

    return array


if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = parse_argv(sys.argv)
        bp_file = args.input_file
        npy_file = args.output_file
    else:
#        bp_file = r'C:\zyf\dnn_models\resnet-msra\ResNet_mean.binaryproto'
        bp_file = r'C:\zyf\github\caffe\data\ilsvrc12\imagenet_mean.binaryproto'
        npy_file = None

    mean_array = binaryproto_to_npy(bp_file, npy_file)
