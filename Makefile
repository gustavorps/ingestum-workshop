clean:
	rm -rf .data/
jq-content:
	cat ${path} | jq -r '.content'