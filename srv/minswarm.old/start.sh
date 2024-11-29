sudo systemctl start  salt-master && sleep 5
sudo systemctl start  salt-minion

sleep 2 && ps -eaf |grep salt |grep -v grep


