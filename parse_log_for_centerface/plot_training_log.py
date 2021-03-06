#!/usr/bin/env python
import inspect
import os
import os.path as osp
import random
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.legend as lgd
import matplotlib.markers as mks

import parse_log


def get_log_parsing_script():
    dirname = osp.dirname(osp.abspath(inspect.getfile(
        inspect.currentframe())))

    return dirname + '/parse_log.sh'


def get_log_file_suffix():
    return '.log'


def get_chart_type_description_separator():
    return '  vs. '


def is_x_axis_field(field):
    x_axis_fields = ['Iters', 'Seconds']
    return field in x_axis_fields


def create_field_index():
    train_key = 'Train'
    test_key = 'Test'
    field_index = {train_key: {'Iters': 0, 'Seconds': 1,
                               train_key + ' learning rate': 2,
                               train_key + ' loss': 3,
                               train_key + ' loss2': 4},
                   test_key: {'Iters': 0, 'Seconds': 1,
                              test_key + ' learning rate': 2,
                              test_key + ' loss': 3,
                              test_key + ' loss2': 4,
                              test_key + ' accuracy': 5}
                   }
    fields = set()
    for data_file_type in field_index.keys():
        fields = fields.union(set(field_index[data_file_type].keys()))
#        print 'fields: ', fields
    fields = list(fields)
#    print 'fields: ', fields
    fields.sort()
#    print 'fields: ', fields
    return field_index, fields


def get_supported_chart_types():
    field_index, fields = create_field_index()
    num_fields = len(fields)
    supported_chart_types = []
    for i in xrange(num_fields):
        if not is_x_axis_field(fields[i]):
            for j in xrange(num_fields):
                if i != j and is_x_axis_field(fields[j]):
                    supported_chart_types.append('%s%s%s' % (
                        fields[i], get_chart_type_description_separator(),
                        fields[j]))
    return supported_chart_types


def get_chart_type_description(chart_type):
    supported_chart_types = get_supported_chart_types()
    chart_type_description = supported_chart_types[chart_type]
    return chart_type_description


def get_data_file_type(chart_type):
    description = get_chart_type_description(chart_type)
    data_file_type = description.split()[0]
    return data_file_type


def get_data_file(chart_type, path_to_log):
    dir_name = osp.dirname(osp.abspath(path_to_log))
    base_name = osp.basename(path_to_log)
    return osp.join(dir_name, base_name + '.' +
                    get_data_file_type(chart_type).lower() + '.txt')


def get_field_descriptions(chart_type):
    description = get_chart_type_description(chart_type).split(
        get_chart_type_description_separator())
    y_axis_field = description[0]
    x_axis_field = description[1]
    return x_axis_field, y_axis_field


def get_field_indices(x_axis_field, y_axis_field, data_file=None):
    data_file_type = get_data_file_type(chart_type)
#    print data_file_type
    fields = create_field_index()[0][data_file_type]
#    print fields
    if data_file:
        fp = open(data_file, 'r')
        line = fp.readline().strip()
        data_file_fields = line.split(',')
        print 'data_file_fields:', data_file_fields
        fp.close()

        idx = -1
        if 'loss' in y_axis_field:
            for i in range(len(data_file_fields)):
                if 'loss' in data_file_fields[i]:
                    idx = i
                    break

            if 'loss2' in y_axis_field and idx >= 0:
                idx2 = -1
                for i in range(idx2, len(data_file_fields)):
                    if 'loss' in data_file_fields[i]:
                        idx2 = i
                        break
                idx = idx2

        if 'accuracy' in y_axis_field:
            for i in range(len(data_file_fields)):
                if 'accuracy' in data_file_fields[i]:
                    idx = i
                    break
        print 'idx for %s in data_file_fields: ' % y_axis_field, idx

        if idx >= 0:
            return fields[x_axis_field], idx
        else:
            return fields[x_axis_field], fields[y_axis_field]

    else:
        return fields[x_axis_field], fields[y_axis_field]


def load_data(data_file, field_idx0, field_idx1):
    #    print data_file

    data = [[], []]
    skip = 1
    with open(data_file, 'r') as f:
        for line in f:
            if skip:  # skip the first line, which is the csv table head
                skip = 0
                continue
            line = line.strip()
            if line[0] != '#':
                if ',' in line:
                    fields = line.split(',')
                else:
                    fields = line.split()
                data[0].append(float(fields[field_idx0].strip()))
                data[1].append(float(fields[field_idx1].strip()))
    return data


def random_marker():
    markers = mks.MarkerStyle.markers
    num = len(markers.keys())
    idx = random.randint(0, num - 1)
    return markers.keys()[idx]


def get_data_label(path_to_log):
    # label = path_to_log[path_to_log.rfind('/') + 1: path_to_log.rfind(
    #     get_log_file_suffix())]
    label = osp.splitext(osp.basename(path_to_log))[0]
    return label


def get_legend_loc(chart_type):
    x_axis, y_axis = get_field_descriptions(chart_type)
    loc = 'lower right'
    if y_axis.find('accuracy') != -1:
        pass
    if y_axis.find('loss') != -1 or y_axis.find('learning rate') != -1:
        loc = 'upper right'
    return loc


def plot_chart(chart_type, path_to_png, path_to_log_list, force_parse=True):
    for path_to_log in path_to_log_list:
        #        if sys.platform=='win32':
        #            print '--->parsing log by pars_log.py'
        #            output_dir = osp.dirname(osp.abspath(path_to_log))
        #            parse_log.main(['%s' % path_to_log, '--output_dir', output_dir])
        #        else:
        #            parsing_script = get_log_parsing_script()
        #            parsing_cmd = '%s %s' % (parsing_script, path_to_log)
        #            print '--->parsing script is: ', parsing_script
        #            print '--->parsing cmd is: ', parsing_cmd
        #            os.system(parsing_cmd)
        data_file = get_data_file(chart_type, path_to_log)
        if not force_parse and osp.exists(data_file):
            print '===> Parsing result data file already exists: ', data_file
            print 'Will use this data file. Please use --force-parse option if you want reparse the log files'
        else:
            print '===> Parsing log file: ', path_to_log
            output_dir = osp.dirname(osp.abspath(path_to_log))
            parse_log.main(
                ['%s' % path_to_log, '--output_dir', output_dir])

        x_axis_field, y_axis_field = get_field_descriptions(chart_type)
#        print 'x_axis_field, y_axis_field: ', x_axis_field, y_axis_field
        x, y = get_field_indices(x_axis_field, y_axis_field, data_file)
        data = load_data(data_file, x, y)
        # TODO: more systematic color cycle for lines
#        color = [random.random(), random.random(), random.random()]
        color = 'red'
        color = [1.0, 0.0, 0.0]  # red
#        color = [0.0, 1.0, 0.0] # green
#        color = [0.0, 0.0, 1.0] # blue
        label = get_data_label(path_to_log)
        linewidth = 0.75
        # If there too many datapoints, do not use marker.
        use_marker = False
#        use_marker = True
        if not use_marker:
            plt.plot(data[0], data[1], label=label, color=color,
                     linewidth=linewidth)
        else:
            # marker = random_marker()
            marker = 'x'
            plt.plot(data[0], data[1], label=label, color=color,
                     marker=marker, linewidth=linewidth)
    legend_loc = get_legend_loc(chart_type)
    plt.legend(loc=legend_loc, ncol=1)  # ajust ncol to fit the space
    plt.title(get_chart_type_description(chart_type))
    plt.xlabel(x_axis_field)
    plt.ylabel(y_axis_field)
    plt.savefig(path_to_png)
    # plt.show()


def print_help():
    print """This script mainly serves as the basis of your customizations.
Customization is a must.
You can copy, paste, edit them in whatever way you want.
Be warned that the fields in the training log may change in the future.
You had better check the data files and change the mapping from field name to
 field index in create_field_index before designing your own plots.
Usage:
    ./plot_training_log.py chart_type[0-%s] /where/to/save.png /path/to/first.log ... --force-parse
Notes:
    1. Supporting multiple logs.
    2. Append 'force-parse' at the end of options to force parsing log files.
       Otherwise only use the parse results from last parsing.
    """ % (len(get_supported_chart_types()) - 1)
#     2. Log file name must end with the lower-cased "%s".
# Supported chart types:""" % (len(get_supported_chart_types()) - 1,
#                              get_log_file_suffix())
    supported_chart_types = get_supported_chart_types()
    num = len(supported_chart_types)
    for i in xrange(num):
        print '    %d: %s' % (i, supported_chart_types[i])
    print '\n==================\n'
#    sys.exit()


def is_valid_chart_type(chart_type):
    return chart_type >= 0 and chart_type < len(get_supported_chart_types())


if __name__ == '__main__':
    print_help()
    if len(sys.argv) < 4:
        #        print_help()
        pass
    else:
        chart_type = int(sys.argv[1])
        print 'chart_type: ', chart_type
        if not is_valid_chart_type(chart_type):
            print '%s is not a valid chart type.' % chart_type
            print_help()
        path_to_png = sys.argv[2]
        print 'path_to_png:', path_to_png
        if not path_to_png.endswith('.png'):
            print 'Path must ends with png' % path_to_png
            sys.exit()

        # path_to_logs = sys.argv[3:]
        force_parse = False
        path_to_logs = []
        for i in range(3, len(sys.argv)):
            if 'force-parse' in sys.argv[i]:
                force_parse = True
            else:
                path_to_logs.append(sys.argv[i])

        for path_to_log in path_to_logs:
            if not osp.exists(path_to_log):
                print 'Path does not exist: %s' % path_to_log
                sys.exit()
            # if not path_to_log.endswith(get_log_file_suffix()):
            #     print 'Log file must end in %s.' % get_log_file_suffix()
            #     # print_help()
            #     new_log = osp.splitext(path_to_log)[0] + '.log'
            #     print 'Copy %s into %s' % (path_to_log, new_log)
            #     shutil.copy(path_to_log, new_log)

        # plot_chart accpets multiple path_to_logs
        plot_chart(chart_type, path_to_png, path_to_logs, force_parse)
