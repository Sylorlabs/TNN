#!/bin/sh
# unmap_a.sh -- frozen inverse output mapping, Variant A (PREREG 4.2).
# stdin -> stdout.
export PATH="$HOME/safebin"
sed -e 's/5001/21/g; s/5002/22/g; s/5003/61/g; s/5004/62/g; s/5005/63/g; s/5006/71/g; s/5007/81/g; s/5008/82/g; s/5009/83/g; s/5010/84/g' \
    -e 's/5011/101/g; s/5012/102/g; s/5013/103/g; s/5014/111/g; s/5015/112/g; s/5016/201/g; s/5017/202/g; s/5018/203/g; s/5019/211/g' \
    -e 's/QB/P6-ABL-X/g; s/QC/P6-ABL-Y/g; s/QD/P6-PIPE/g; s/QA/P6/g'
