import caffe
import numpy as np
import os.path as osp
import sys

#bp_file = 'age_gender_mean.binaryproto'
bp_file = r'C:\zyf\github\caffe\data\ilsvrc12\imagenet_mean.binaryproto'

# reload saved bp_file
blob = caffe.proto.caffe_pb2.BlobProto()
data = open( bp_file, 'rb' ).read()
blob.ParseFromString(data)
arr = caffe.io.blobproto_to_array(blob)
print('npy.shape reloaded bp_file: {}'.format(arr.shape))
mean_img_reloaded = np.array(arr)

print('mean_img_reloaded.shape:\n{}'.format(mean_img_reloaded.shape))
#print('mean_img_reloaded:\n{}'.format(mean_img_reloaded))