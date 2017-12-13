#!/bin/bash
# Usage parse_log.sh caffe.log
# It creates the following two text files, each containing a table:
#     caffe.log.test (columns: '#Iters Seconds TestAccuracy TestLoss')
#     caffe.log.train (columns: '#Iters Seconds TrainingLoss LearningRate')


# get the dirname of the script
#DIR="$( cd "$(dirname "$0")" ; pwd -P )"
DIR="/disk2/zhaoyafei/caffe-bvlc-for-mxnet-container/tools/extra"

if [ "$#" -lt 1 ]
then
echo "Usage parse_log.sh /path/to/your.log"
exit
fi

LOG=`basename $1`

sed -n '/Iteration .* Testing net/,/Iteration *. softmax_loss/p' $1 > aux.txt
sed -i '/Waiting for data/d' aux.txt
sed -i '/prefetch queue empty/d' aux.txt
sed -i '/Iteration .* loss/d' aux.txt
sed -i '/Iteration .* lr/d' aux.txt
sed -i '/Train net/d' aux.txt
sed -i '/MultiStep Status:/d' aux.txt
grep 'Iteration ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
grep 'Test net output #0' aux.txt | awk '{print $11}' > aux1.txt
grep 'Test net output #2' aux.txt | awk '{print $11}' > aux2.txt
grep 'Test net output #1' aux.txt | awk '{print $11}' > aux5.txt
grep 'Test net output #3' aux.txt | awk '{print $11}' > aux6.txt

# Extracting elapsed seconds
# For extraction of time since this line contains the start time
grep '] Solving ' $1 > aux3.txt
grep 'Testing net' $1 >> aux3.txt
$DIR/extract_seconds.py aux3.txt aux4.txt

# Generating
echo '#Iters Seconds TestAccuracy TestLoss lambda Top5Acc'> $LOG.test
paste aux0.txt aux4.txt aux1.txt aux2.txt aux5.txt aux6.txt | column -t >> $LOG.test
rm aux.txt aux0.txt aux1.txt aux2.txt aux3.txt aux4.txt aux5.txt aux6.txt

# For extraction of time since this line contains the start time
grep '] Solving ' $1 > aux.txt
grep ', loss = ' $1 >> aux.txt
grep 'Iteration ' aux.txt | sed  's/.*Iteration \([[:digit:]]*\).*/\1/g' > aux0.txt
grep ', loss = ' $1 | awk -F = '{print $2}' > aux1.txt
grep ', lr = ' $1 | awk '{print $9}' > aux2.txt
# grep ': lambda = ' $1 | awk -F = '{print $2}' > aux5.txt
# grep ': softmax_loss = ' $1 | awk -F = '{print $2}' | awk '{print $1}'> aux6.txt
grep 'Train net output #0' $1 | awk -F = '{print $2}' > aux5.txt
grep 'Train net output #1' $1 | awk -F = '{print $2}' | awk '{print $1}'> aux6.txt

# Extracting elapsed seconds
$DIR/extract_seconds.py aux.txt aux3.txt

# Generating
echo '#Iters Seconds TrainingLoss LearningRate lambda softmax_loss'> $LOG.train
paste aux0.txt aux3.txt aux1.txt aux2.txt aux5.txt aux6.txt | column -t >> $LOG.train
rm aux.txt aux0.txt aux1.txt aux2.txt  aux3.txt aux5.txt aux6.txt
