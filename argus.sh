argus -F argus.conf -i s1-eth8 -w flows-binary
cat flows-binary | ra -r - -n -F ra.conf -Z b > flows-binary.txt
