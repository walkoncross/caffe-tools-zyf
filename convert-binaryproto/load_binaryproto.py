#!/usr/bin/env python
import numpy as np
import os.path as osp
#import caffe.proto
from caffe.proto import caffe_pb2
from caffe.io import blobproto_to_array


def load_binaryproto(bp_file):
    blob_proto = caffe_pb2.BlobProto()
    data = open(bp_file, 'rb').read()
    blob_proto.ParseFromString(data)
    arr = blobproto_to_array(blob_proto)
#    print type(arr)
    return arr


if __name__ == '__main__':
    #bp_file = 'age_gender_mean.binaryproto'
    bp_file = r'C:\zyf\github\caffe\data\ilsvrc12\imagenet_mean.binaryproto'

    arr = load_binaryproto(bp_file)
    print('loaded array shape: {}'.format(arr.shape))
#    mean_img_reloaded = np.array(arr)
#
#    print('mean_img_reloaded.shape:\n{}'.format(mean_img_reloaded.shape))
#    # print('mean_img_reloaded:\n{}'.format(mean_img_reloaded))
