import nltk
import string
import emoji
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = text.lower()
    extra_symbols = ''.join([chr(9679), chr(8217), chr(9675), chr(10), chr(32)])
    punc = string.punctuation + extra_symbols
    text = emoji.replace_emoji(text, replace='')
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in punc and word]
    return tokens

# Generate a response
def generate_response(user_input, sent_tokens):
    user_input = user_input.lower()
    sent_tokens.append(user_input) 
    tfidf_vectorizer = TfidfVectorizer(tokenizer=preprocess, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(sent_tokens) 
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    similar_sentence_idx = cosine_similarities.argsort()[0][-2]
    flat = cosine_similarities.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        return "I'm sorry, I don't understand."
    else:
        return sent_tokens[similar_sentence_idx]


def fetch_query_response(corpus, user_input):
    print("Chatbot: Hello! I am a chatbot. Type 'bye' to exit.")
    sent_tokens = nltk.sent_tokenize(corpus)
    user_input = user_input.lower()
    if user_input == "bye":
        return "Chatbot: Goodbye!"
    else:
        response = generate_response(user_input, sent_tokens)
        print(f"Chatbot: {response}")
        sent_tokens.remove(user_input)
        return response