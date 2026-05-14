argus -F argus.conf -i s1-eth8 -w flows-binary.argus
cat flows-binary.argus | ra -r - -n -F ra.conf -Z b > flows-binary.binetflow
