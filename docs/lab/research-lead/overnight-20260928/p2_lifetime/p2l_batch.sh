export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/p2_lifetime/
./p2l_treat_bin > p2l_treat_run2.txt 2>&1; echo "EXIT=$?" >> p2l_treat_run2.txt
./p2l_treat_bin > p2l_treat_run3.txt 2>&1; echo "EXIT=$?" >> p2l_treat_run3.txt
./p2l_abl_bin > p2l_abl_run1.txt 2>&1; echo "EXIT=$?" >> p2l_abl_run1.txt
./p2l_abl_bin > p2l_abl_run2.txt 2>&1; echo "EXIT=$?" >> p2l_abl_run2.txt
./p2l_abl_bin > p2l_abl_run3.txt 2>&1; echo "EXIT=$?" >> p2l_abl_run3.txt
./p2l_ctrl_bin > p2l_ctrl_run1.txt 2>&1; echo "EXIT=$?" >> p2l_ctrl_run1.txt
./p2l_ctrl_bin > p2l_ctrl_run2.txt 2>&1; echo "EXIT=$?" >> p2l_ctrl_run2.txt
./p2l_ctrl_bin > p2l_ctrl_run3.txt 2>&1; echo "EXIT=$?" >> p2l_ctrl_run3.txt
echo "P2L-BATCH-DONE"
