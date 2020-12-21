import os
import math
import pandas as pd
punctuations = '''!()-[]{};:'"\,\n<>./?@#$%^&*_~'''

files=os.listdir('./actors')
document_index={}
for i in range(len(files)):
    document_index[str(i+1)]=files[i].replace(".json","")
  

count = 1
Documents_dict = {}
vocab_dict = {}   
for fil in files:     
    f=pd.read_json('./actors/'+str(fil))
    text = f['text'][0]
    text = text.replace('\n', ' ')
    final_text = ""
    for char in text:
    	if char not in punctuations:
    		final_text = final_text + char
    list_text = final_text.split(" ")
    for word in list_text:
    	if word in vocab_dict.keys():
    		vocab_dict[word] = vocab_dict[word] + 1
    	else:
    		vocab_dict[word] = 1
    Length_text = len(list_text)
    uniq_set = set(list_text)
    uniq_text = (list(uniq_set))
    # print("Document - ", count, ":")
    # print(final_text, "\n")
    TF_dict = {}
    # print("TERMS", "->", "TERM FREQ", "->", "NORM TERM FREQ  (term freq/ doc size) ", "\n")
    norm_doc = 0
    for words in uniq_text:
    	# print(words, " -> ", list_text.count(words), " -> ", list_text.count(words), "/",Length_text)
    	list_temp = [list_text.count(words), list_text.count(words)/Length_text]
    	TF_dict[words] = list_temp
    	norm_doc = norm_doc + TF_dict[words][1]*TF_dict[words][1]
    norm_docc = math.sqrt(norm_doc)
    TF_dict["norm_doc"+str(count)] = norm_docc
    # print("\n|| d"+str(count)+" || = ", norm_docc)
    Documents_dict["doc"+str(count)] = TF_dict
    # print("\n")
    # f.close()
    count = count + 1
freq_vocab = []
uniq_vocab = []
for word in vocab_dict.keys():
	if vocab_dict[word] > 10:
		freq_vocab.append(word)
	elif vocab_dict[word] == 1:
		uniq_vocab.append(word)
# print("High frequency words :")
# print(freq_vocab, "\n")
# print("Rare words:")
# print(uniq_vocab, "\n")
count = count - 1


print("Enter your query: ")
query = input()
query = query.split(" ")
query_set = set(query)
query_list = (list(query_set))
i=0
Query_doc_freq = {}
Total_doc_freq = 0
while i<len(query_list):
	doc_freq = 0
	j=1
	while j<=count:
		if query_list[i] in Documents_dict["doc"+str(j)].keys():
			doc_freq = doc_freq + 1
		j=j+1
	Total_doc_freq = Total_doc_freq + doc_freq
	Query_doc_freq[query_list[i]] = doc_freq
	i = i+1
if Total_doc_freq == 0:
	print("--------Query not found--------")
else:
	# print("\n\nTERMS", "->", "DOC FREQ", "->", "NORM DOC FREQ  (doc freq/total doc freq)\n")
	norm_q = 0
	for Keyss in Query_doc_freq:
		print(Keyss, "->", Query_doc_freq[Keyss], "->", Query_doc_freq[Keyss]/Total_doc_freq)
		Query_doc_freq[Keyss] = Query_doc_freq[Keyss]/Total_doc_freq
		norm_q = norm_q + Query_doc_freq[Keyss]*Query_doc_freq[Keyss]
	norm_qq = math.sqrt(norm_q)
	print("\n|| q || = ", norm_qq, "\n")
	Similarity_scores = {}
	i=1
	while i<= count:
		sim_temp = 0
		j=0
		while j<len(query_list):
			if query_list[j] in Documents_dict["doc"+str(i)].keys():
				sim_temp = sim_temp + Documents_dict["doc"+str(i)][query_list[j]][1]*Query_doc_freq[query_list[j]]
			j=j+1
		denominator = norm_qq*Documents_dict["doc"+str(i)]["norm_doc"+str(i)]
		Similarity_scores["doc"+str(i)] = sim_temp/denominator
		i=i+1
	# print(vocab_dict)
	print("Similarity scores:")
	print(Similarity_scores)
	print("\nRanking based on similarity scores: ")
	# print (sorted(Similarity_scores.items(), reverse=True, key = lambda x : x[1]))
	print("\n")
i=1
for a in sorted(Similarity_scores.items(), reverse=True, key = lambda x : x[1]):
    
    if a[1]!=0:
        print(document_index[a[0].replace("doc","")]+".json is the Document"+"Ranked at "+str(i)+" With "+" Similarity Score :"+str(a[1]))
    i=i+1
        # print("\n")
    