# Check if the number of arguments is less than 2
#if [ $# -lt 1 ]; then
#    echo "kill all fake minion by min g -i fakeid pattern"
#    echo "Error: Not enough arguments provided."
#    echo "Usage: $0 fake-minion-id "
#    exit 1
#fi

sudo kill -9  `ps -eaf |grep 77 | grep -v grep | awk '{print $2}'`

sudo salt-key -yd Rocky*
