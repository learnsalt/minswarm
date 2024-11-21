for i in {1..1000}
do
time sudo salt \* test.ping --out=txt
time sudo salt \* grains.item saltversion id --out=txt
done
