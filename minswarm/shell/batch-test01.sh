#
for i in {1..$1}
do
sudo salt \* test.ping --out=txt
sudo salt \* grains.item saltversion id --out=txt
done
