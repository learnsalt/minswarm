while true
do
sudo salt '*' test.ping --out=txt
    sleep 1
done
