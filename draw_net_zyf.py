#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 04:40:05 2016

@author: zhaoy
"""

"""
Draw a graph of the net architecture.
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from google.protobuf import text_format

import caffe
import caffe.draw
from caffe.proto import caffe_pb2


def parse_args(argv):
    """Parse input arguments
    """

    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('input_net_proto_file',
                        help='Input network prototxt file')
    parser.add_argument('output_image_file',
                        help='Output image file')
    parser.add_argument('--rankdir',
                        help=('One of TB (top-bottom, i.e., vertical), '
                              'RL (right-left, i.e., horizontal), or another '
                              'valid dot option; see '
                              'http://www.graphviz.org/doc/info/'
                              'attrs.html#k:rankdir'),
                        default='LR')

    args = parser.parse_args(argv)
    return args


def main(argv):
    args = parse_args(argv)
    print 'args after parse_args:\n\t'
    print args
    print '\n'
    net = caffe_pb2.NetParameter()
    text_format.Merge(open(args.input_net_proto_file).read(), net)
    print('Drawing net to %s' % args.output_image_file)
    caffe.draw.draw_net_to_file(net, args.output_image_file, args.rankdir)


if __name__ == '__main__':
    import sys

    rankdirs = ['LR', 'BT']

    #input_net_proto_file = 'C:/zyf/github/face_models/age_gender_net/deploy_age.prototxt'
    #input_net_proto_file = 'vgg_face/VGG_FACE_deploy.prototxt'
    #input_net_proto_file = './age_gender_net/deploy_age_v1.prototxt'
    #input_net_proto_file = './age_gender_net/deploy_gender_v1.prototxt'
    #input_net_proto_file = 'C:/zyf/github/face_models/face_landmarks/vanilla_deploy_v1.prototxt'
    #input_net_proto_file = 'C:/zyf/github/fcn.berkeleyvision.org/voc-fcn-alexnet/train.prototxt'
    #input_net_proto_file = 'C:/zyf/github/fcn.berkeleyvision.org/voc-fcn32s/train.prototxt'
    #input_net_proto_file = 'C:/zyf/github/caffe-windows/models/bvlc_alexnet/deploy.prototxt'
    #input_net_proto_file = 'C:/zyf/github/caffe-windows/models/bvlc_googlenet/deploy.prototxt'
    #input_net_proto_file = 'C:/zyf/github/caffe-windows/models/bvlc_reference_caffenet/deploy.prototxt'
    #input_net_proto_file = 'C:/zyf/github/caffe-windows/models/bvlc_reference_rcnn_ilsvrc13/deploy.prototxt'
    #input_net_proto_file = 'C:/zyf/github/caffe-windows/models/finetune_flickr_style/deploy.prototxt'
    #input_net_proto_file =  'C:/zyf/py-faster-rcnn-master-0808/py-faster-rcnn-master/models/pascal_voc/ZF/fast_rcnn/test.prototxt'
    #input_net_proto_file =  r'C:\zyf\github\caffe-windows\Build\x64\Release\pycaffe\examples\net_surgery\bvlc_caffenet_full_conv.prototxt'
    #input_net_proto_file =  r'C:\zyf\github\caffe-windows\Build\x64\Release\pycaffe\examples\mnist\lenet.prototxt'
#    input_net_proto_file =  r'C:\zyf\github\py-faster-rcnn\models\pascal_voc\ZF\faster_rcnn_alt_opt\stage1_rpn_train-draw.pt'
    #input_net_proto_file =  r'C:\zyf\github\py-faster-rcnn\models\pascal_voc\ZF\faster_rcnn_end2end\train-draw.prototxt'
#    input_net_proto_file = r'C:\zyf\dnn_models\face_models\norm_face\Center_Face_99.2\face_train_test.prototxt'
    input_net_proto_file = r'C:\zyf\dnn_models\face_models\centerloss\center_face_deploy.prototxt'

    if len(sys.argv) > 1:
        input_net_proto_file = sys.argv[1]

    for rankdir in rankdirs:
        output_image_file = input_net_proto_file + '_drawNet' + rankdir + '.png'

        argv = [input_net_proto_file, output_image_file, '--rankdir='+rankdir]

        print '============='
        print 'rankdir:\n\t', rankdir
        print 'input file:\n\t', input_net_proto_file
        print 'output image:\n\t', output_image_file
        print 'argv:\n\t', argv
        print '============='

        main(argv)