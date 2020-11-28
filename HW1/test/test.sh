num="e2237170"
totalTests=20
rm -r your_out
mkdir your_out
for ((i=1;i<=totalTests;i++));
do
	python3 ../${num}_hw1.py < test${i}_inp.txt > your_out/test${i}_out.txt
done
success=0
for ((i=1;i<=totalTests;i++));
do 
	DIFF=$(diff common_out/test${i}_out.txt your_out/test${i}_out.txt) 
	if [ "$DIFF" ] 
	then
		echo "Error in test ${i}"
	else 
		((success=success+1))
	fi
done
echo "Passed Tests: $success/$totalTests"
