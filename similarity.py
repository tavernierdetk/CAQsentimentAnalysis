
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import warnings
import pickle

def sortBySimilarity(df, column):
    df = df.sort_values(by=column, ascending=False)
    df = df[:1000]
    return df

def runDocSim(attributes, df, commentColumnName):
    #to ignore deprecation warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    #Please use xlsx file format to read the data
    reviews_df=df

    #checking for nulls if present any
    print("Number of rows with null values:")
    print(reviews_df.isnull().sum().sum())
    reviews_df=reviews_df.dropna()

    #reading the attributes file
    #check into the "attributes.txt" file for the proper format
    #each attribute has to be listed in a new line.
    # attributes=list(line.strip() for line in open('attributes.txt'))
    attributes=" ".join(attributes)

    #merging attibutes to the review
    #Restaurant_review is the name of the column with review text.
    tempDataFrame=pd.DataFrame({commentColumnName:[attributes]})
    tempDataFrame=tempDataFrame.transpose()
    description_list1=reviews_df[commentColumnName]
    frames = [tempDataFrame, description_list1]
    result = pd.concat(frames)
    result.columns = ['review']
    result = result.reset_index()

    #building bag of words using frequency
    vec_words = CountVectorizer(decode_error='ignore')
    total_features_words = vec_words.fit_transform(result['review'])
    #print("The size of the vocabulary space:")
    #print(total_features_words.shape)

    #Calculating pairwise cosine similarity
    subset_sparse = sparse.csr_matrix(total_features_words)
    total_features_review=subset_sparse
    total_features_attr=subset_sparse[0,]
    similarity=1-pairwise_distances(total_features_attr,total_features_review, metric='cosine')

    #Assigning the similarity score to dataframe
    #similarity=np.array(similarities[0]).reshape(-1,).tolist()
    similarity=pd.DataFrame(similarity)
    similarity=similarity.transpose()
    colName = "similarity_" + attributes
    similarity.columns = [colName]
    similarity=similarity.drop(similarity.index[[0]])
    reviews_df=reviews_df.assign(colName=similarity.values)
    reviews_df = reviews_df.rename(columns={'colName': colName})
    print(reviews_df)


    reviews_df.to_excel('excelFiles/textExcel.xlsx',index=False)

    return reviews_df

if __name__ == "__main__":
    print("Running DocSim")

    attributes = ["famille",'education','travail','argent']
    with open('pickleFiles/dfFromJson.pkl', 'rb') as file:
        df = pickle.load(file)

    for attribute in attributes:
        df = runDocSim([attribute],df, "message")

    with open('pickleFiles/outputWithSimilarity.pkl', 'wb') as file:
        pickle.dump(df, file)