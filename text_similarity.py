'''
determine similarity between text items and create html groupping similar texts
'''

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pkl_functions
import html_functions

ruv_df = pkl_functions.read_pkl('RUV.pkl')
n = len(ruv_df)
text = ruv_df['text']
#determine tfidf
tfidf = TfidfVectorizer().fit_transform(text)
#determine similarity matrix
similarity_matrix = tfidf * tfidf.T.toarray()
#fill diagonal wiht -1
np.fill_diagonal(similarity_matrix, -1)  

#dermine max by column
max_sim = similarity_matrix.max(1)
#list columns with max above 0.6
a = np.where(max_sim > 0.6)[0].tolist()
#list with all indices to check
b = list(range(n))
#list with similar articles 
final_list = []

#loop adding all sets of similar articles, by indices of a
for i in a:
   #remove i from b
   b.pop(i)
   #check all columns with similarity above 0.6
   x = np.where(similarity_matrix[i]> 0.6)[0].tolist()
   #exlude items that were already checked (removed from b)
   z = [j for j in x if j in b]
   if len(z)>0:
       #add set i and similar text items
      final_list += [[i]+z]
    
html_body = '<h1> Articles with similar content</h1>\n<hr style="height:4px;">\n'
for l in final_list:    
    for li in l:
        title = ruv_df['title'][li]
        text = ruv_df['text'][li]
        dated = ruv_df['dated'][li]
        url = ruv_df['url'][li]
        html_body += html_functions.create_html_body(title, text, dated, url)
    html_body += '<hr style="height:4px;">\n'
html = html_functions.create_html(html_body, 'Similar articles')
with open("similar_articles.html", "w") as file:
    file.write(html)