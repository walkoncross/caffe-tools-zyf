#!/usr/bin/env sh
LOGFILE=$1

/disk2/zhaoyafei/parse_train_log/plot_training_log_for_sphereface.py 10 train_loss_vs_iters.png $LOGFILE --force-parse
/disk2/zhaoyafei/parse_train_log/plot_training_log_for_sphereface.py 8 train_lr_vs_iters.png $LOGFILE
/disk2/zhaoyafei/parse_train_log/plot_training_log_for_sphereface.py 6 train_lambda_vs_iters.png $LOGFILE
/disk2/zhaoyafei/parse_train_log/plot_training_log_for_sphereface.py 2 test_loss_vs_iters.png $LOGFILE
/disk2/zhaoyafei/parse_train_log/plot_training_log_for_sphereface.py 0 test_acc_vs_iters.png $LOGFILE
/disk2/zhaoyafei/parse_train_log/plot_training_log_for_sphereface.py 4 test_acc_top5_vs_iters.png $LOGFILE
