import sys
import os.path as osp

import numpy as np

import caffe.io
from caffe.proto import caffe_pb2

def npy_to_binaryproto(npy_file, bp_file):

    mean_img = np.load(npy_file)
    print('mean_img.shape:\n{}'.format(mean_img.shape))
    print('mean_img:\n{}'.format(mean_img))

    if mean_img.ndim == 3:
        ms_bf = mean_img.shape
        mean_img = mean_img[np.newaxis, :]
        print('convert mean_img.shape from {} to {}'.format(ms_bf, mean_img.shape))
    elif mean_img.ndim == 2:
        ms_bf = mean_img.shape
        mean_img = mean_img[np.newaxis, np.newaxis, :]
        print('convert mean_img.shape from {} to {}'.format(ms_bf, mean_img.shape))

    # mean_img is your numpy array with the average data
    blob = caffe.io.array_to_blobproto(mean_img)
    with open(bp_file, 'wb') as f:
        f.write(blob.SerializeToString())

    # reload saved bp_file
    blob = caffe_pb2.BlobProto()
    data = open(bp_file, 'rb').read()
    blob.ParseFromString(data)
    arr = caffe.io.blobproto_to_array(blob)
    print('npy.shape reloaded bp_file: {}'.format(arr.shape))
    mean_img_reloaded = np.array(arr)

    print('mean_img_reloaded.shape:\n{}'.format(mean_img_reloaded.shape))
    print('mean_img_reloaded:\n{}'.format(mean_img_reloaded))

    print('sum(mean_img_reloaded - mean_img) = {}'.format(np.sum(mean_img_reloaded - mean_img)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python convert_npy_to_binaryproto.py proto.mean out.npy"
        sys.exit()

    #npy_file = 'center_face_mean_127.5_3x112x96.npy'
    npy_file = 'center_face_mean_127.5_1x3.npy'
    #npy_file = 'ilsvrc_2012_mean.npy'
    basename = osp.basename(npy_file)
    bp_file = osp.splitext(basename)[0] + '.binaryproto'

    npy_to_binaryproto(npy_file, bp_file)
