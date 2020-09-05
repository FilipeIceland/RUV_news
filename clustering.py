from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import pandas as pd
import pkl_functions
from pyvis.network import Network

def preprocessing(text):
    new_text = text.lower()
    return new_text

def determine_tfidf(text, max_df = 0.8, min_df = 0.1):
    '''
        calculate tfidf from a pd.Series returning the respective matrix and filtered terms
    '''
    #calculate tfidf matrix with text in lower case, removing stopwords, keeping values within the thresholds
    tfidf_vectorizer = TfidfVectorizer(preprocessor=preprocessing, max_df = max_df, min_df = min_df, stop_words = set(stopwords.words('english')))
    #fit text
    tfidf = tfidf_vectorizer.fit_transform(text.to_list())
    #get filtered terms
    key_terms = tfidf_vectorizer.get_feature_names()
    return tfidf, key_terms



def find_frequent_terms(key_terms, text):
    '''
        determine the number of text items in which each key term is found (sorted by descending order)
    '''
    #determine if key terms with text in lower case are found within each text item
    count_vectorizer = CountVectorizer(preprocessor=preprocessing, stop_words = set(stopwords.words('english')), vocabulary = key_terms, binary = True)
    #count documents where each term is found (for each key term)
    X = count_vectorizer.fit_transform(text.to_list()).toarray().sum(0).tolist()
    #create Data Frame
    df = pd.DataFrame({'terms': key_terms, 'count': X})
    #sort by descending order
    sorted_df = df.sort_values('count', ascending = False).reset_index(drop = True)
    return sorted_df
    
def k_means(tfidf, k = 2):
    '''
        return the output of k-means given tfidf
    '''
    return KMeans(n_clusters=k).fit(tfidf)

def create_network_kmeans(text, kmeans = [], tfidf = None, key_terms = None, freq_df = [], k_list=[2], n=20):
    '''
        create html files with network graphs, where for each cluster it is stored the most frequent terms
    '''    
    if len(kmeans) == 0:
        if tfidf is None or key_terms is None:
            #determine tfidf, key_terms
            tfidf, key_terms = determine_tfidf(text)
        
        #determine kmeans
        for k in k_list:
            kmeans.append(k_means(tfidf, k))
            
    if len(freq_df) == 0:
        #determine frequency for each key term
        freq_df = find_frequent_terms(key_terms, text)
        
    for c in range(len(k_list)):
        #number of clusters
        k = k_list[c]
        #clusters lables
        labels = pd.Series(kmeans[c].labels_.tolist())
        #start network
        G = Network(height="750px", width="100%", font_color="black")
        for i in labels.unique():
            #filter text items within the cluster
            filter_text = text.loc[labels==i].reset_index(drop = True)
            #add node with the cluster name, have the size as the number of items
            G.add_nodes(['Cluster '+ str(i)], value=[len(filter_text)])
            #determine frequency of the key within cluster only
            new_freq_df = find_frequent_terms(key_terms, filter_text)
            #for the most frequent terms within the cluster
            for j in range(n):
                #get term
                term = new_freq_df['terms'][j]
                #add node with the term with the respective frequency overall as size
                G.add_node(str(term), value=freq_df.loc[freq_df['terms']==term,]['count'].tolist()[0])
                #add edge between cluster label and term
                G.add_edge('Cluster '+ str(i), str(term))
        #create and html file with network graph            
        G.show(str(k)+"clusters.html")

#read file        
ruv_df = pkl_functions.read_pkl('RUV.pkl')
#get text
text = ruv_df['text']
#determine tfidf matrix and respective key terms
tfidf, key_terms = determine_tfidf(text)
#determine frequency of the key terms (i.e., in how many documents they occur)
freq_df = find_frequent_terms(key_terms, text)
#create network graphs running k-means, having different values of k
create_network_kmeans(text, kmeans = [], tfidf = tfidf, key_terms = key_terms, freq_df = freq_df, k_list=[2, 3, 4, 5, 10], n=30)

