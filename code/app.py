from urllib.parse import urlparse
import re
import streamlit as st
from PIL import Image
import joblib
import numpy as np
import pandas as pd
import collections
from sklearn.ensemble import RandomForestClassifier

import math
from collections import Counter
import joblib
import tldextract
from publicsuffixlist import PublicSuffixList
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder


psl = PublicSuffixList()

dga_clf = joblib.load('../models/DGA_Lightgbm.pkl')
rf_clf = joblib.load('../models/RandomForest.pkl')
alexa_vc = joblib.load('../models/alexa_vc.pkl')
dict_cv = joblib.load('../models/dict_cv.pkl')
def predict_url(url):

    url_features = extract_features(url)
    dga_features = extract_DGA_features(url)
    rf_prediction = rf_clf.predict([url_features])
    dga_prediction = dga_clf.predict([dga_features])
    prediction = rf_prediction*0.5 + dga_prediction*0.5
    return prediction

def redirection(url):
    pos = url.rfind('//')
    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0

def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1  # phishing
    else:
        return 0

############ Length Features ############
def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0


def hostname_length(url):
    return len(urlparse(url).netloc)


def path_length(url):
    return len(urlparse(url).path)


def url_length(url):
    return len(str(url))

############ End of Length Features ############

############ Count Features ############

def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')


# Gets all count features
def get_counts(url):
    count_features = []

    i = url.count('@')
    count_features.append(i)

    i = url.count('?')
    count_features.append(i)

    i = url.count('%')
    count_features.append(i)

    i = url.count('.')
    count_features.append(i)

    i = url.count('=')
    count_features.append(i)

    i = url.count('http')
    count_features.append(i)

    i = url.count('https')
    count_features.append(i)

    i = url.count('www')
    count_features.append(i)

    return count_features

############ End of Count Features ############

############ Binary Features ############

# Use of IP or not in domain
def having_ip_address(url):
    match = re.search(
        # IPv4 in hexadecimal
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        # print match.group()
        return -1
    else:
        # print 'No matching pattern found'
        return 1


def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return -1
    else:
        return 1
############ End of Binary Features ############

def extract_features(url):
    url_features = []

    i = hostname_length(url)
    url_features.append(i)

    i = path_length(url)
    url_features.append(i)

    i = fd_length(url)
    url_features.append(i)

    i = get_counts(url)
    url_features = url_features + i

    i = digit_count(url)
    url_features.append(i)

    i = letter_count(url)
    url_features.append(i)

    i = no_of_dir(url)
    url_features.append(i)

    i = redirection(url)
    url_features.append(i)

    i = having_ip_address(url)
    url_features.append(i)

    i = prefixSuffix(url)
    url_features.append(i)

    return url_features

def load_images(file_name):
    img = Image.open(file_name)
    return st.image(img, width=150)

############ DGA Features ############
def entropy(domain_name):
    """ Function which computes the entropy of a given domain name based on it's chars """
    elements, length = Counter(domain_name), len(domain_name)

    return -sum(element / length * math.log(element / length, 2) for element in elements.values())


def get_domain_name(domain):
    """ Function which extracts domain name from subdomain name """
    res = tldextract.extract(domain)
    return res.domain if len(res.domain) > len(res.subdomain) or entropy(res.domain) > entropy(res.subdomain) else res.subdomain

def load_words():
    words_df = pd.read_csv("../data/DGA/words.txt", names=["word"],
                             encoding="utf-8", header=None, dtype={"word": np.str_}, sep='\t')
    return words_df

words = load_words()


def load_topLevelDomain():
    """ Load Valid Top Level Domains data """
    topLevelDomain = []
    with open('../data/DGA/tlds-alpha-by-domain.txt', 'r') as content:
        for line in content:
            topLevelDomain.append((line.strip('\n')))
    return topLevelDomain


topLevelDomain = load_topLevelDomain()


def ignoreVPS(domain):
    # Return the rest of domain after ignoring the Valid Public Suffixes:
    validPublicSuffix = '.' + psl.publicsuffix(domain)
    if len(validPublicSuffix) < len(domain):
        # If it has VPS
        subString = domain[0: domain.index(validPublicSuffix)]
    elif len(validPublicSuffix) == len(domain):
        return 0
    else:
        # If not
        subString = domain

    return subString


def domain_length(domain):
    # Generate Domain Name Length (DNL)
    return len(domain)


def subdomains_number(domain):
    # Generate Number of Subdomains (NoS)
    subdomain = ignoreVPS(domain)
    return subdomain.count('.') + 1


def subdomain_length_mean(domain):
    # Generate Subdomain Length Mean (SLM)
    subdomain = ignoreVPS(domain)
    result = (len(subdomain) - subdomain.count('.')) / (subdomain.count('.') + 1)
    return result


def has_www_prefix(domain):
    # Generate Has www Prefix (HwP)
    if domain.split('.')[0] == 'www':
        return 1
    else:
        return 0


def has_hvltd(domain):
    # Generate Has a Valid Top Level Domain (HVTLD)
    if domain.split('.')[len(domain.split('.')) - 1].upper() in topLevelDomain:
        return 1
    else:
        return 0


def contains_single_character_subdomain(domain):
    # Generate Contains Single-Character Subdomain (CSCS)
    domain = ignoreVPS(domain)
    str_split = domain.split('.')
    minLength = len(str_split[0])
    for i in range(0, len(str_split) - 1):
        minLength = len(str_split[i]) if len(str_split[i]) < minLength else minLength
    if minLength == 1:
        return 1
    else:
        return 0


def contains_TLD_subdomain(domain):
    # Generate Contains TLD as Subdomain (CTS)
    subdomain = ignoreVPS(domain)
    str_split = subdomain.split('.')
    for i in range(0, len(str_split) - 1):
        if str_split[i].upper() in topLevelDomain:
            return 1
    return 0


def underscore_ratio(domain):
    # Generate Underscore Ratio (UR) on dataset
    subString = ignoreVPS(domain)
    result = subString.count('_') / (len(subString) - subString.count('.'))
    return result


def contains_IP_address(domain):
    # Generate Contains IP Address (CIPA) on datasetx
    splitSet = domain.split('.')
    for element in splitSet:
        if (re.match("\d+", element)) is None:
            return 0
    return 1


def contains_digit(domain):
    """
     Contains Digits
    """
    subdomain = ignoreVPS(domain)
    for item in subdomain:
        if item.isdigit():
            return 1
    return 0


def vowel_ratio(domain):
    """
    calculate Vowel Ratio
    """
    VOWELS = set('aeiou')
    v_counter = 0
    a_counter = 0
    subdomain = ignoreVPS(domain)
    for item in subdomain:
        if item.isalpha():
            a_counter += 1
            if item in VOWELS:
                v_counter += 1
    if a_counter > 1:
        ratio = v_counter / a_counter
        return ratio


def digit_ratio(domain):
    """
    calculate digit ratio
    """
    d_counter = 0
    counter = 0
    subdomain = ignoreVPS(domain)
    for item in subdomain:
        if item.isalpha() or item.isdigit():
            counter += 1
            if item.isdigit():
                d_counter += 1
    if counter > 1:
        ratio = d_counter / counter
        return ratio


def prc_rrc(domain):
    """
    calculate the Ratio of Repeated Characters in a subdomain
    """
    subdomain = ignoreVPS(domain)
    #   subdomain =''.join(re.findall('[a-zA-Z]+', subdomain))
    subdomain = re.sub("[.]", "", subdomain)
    char_num = 0
    repeated_char_num = 0
    d = collections.defaultdict(int)
    for c in list(subdomain):
        d[c] += 1
    for item in d:
        char_num += 1
        if d[item] > 1:
            repeated_char_num += 1
    ratio = repeated_char_num / char_num
    return ratio


def prc_rcc(domain):
    """
    calculate the Ratio of Consecutive Consonants
    """
    VOWELS = set('aeiou')
    counter = 0
    cons_counter = 0
    subdomain = ignoreVPS(domain)
    #   subdomain =''.join(re.findall('[a-zA-Z]+', subdomain))
    i = 0
    for item in subdomain:
        if item.isalpha() and item not in VOWELS:
            counter += 1
        else:
            if counter > 1:
                cons_counter += counter
            counter = 0
        i += 1
    if i == len(subdomain) and counter > 1:
        cons_counter += counter
    ratio = cons_counter / len(subdomain)
    return ratio


def prc_rcd(domain):
    """
    calculate the ratio of consecutive digits
    """
    counter = 0
    digit_counter = 0
    subdomain = ignoreVPS(domain)
    #   subdomain =''.join(re.findall('[a-zA-Z]+', subdomain))
    i = 0
    for item in subdomain:
        if item.isdigit():
            counter += 1
        else:
            if counter > 1:
                digit_counter += counter
            counter = 0
        i += 1
    if i == len(subdomain) and counter > 1:
        digit_counter += counter
    ratio = digit_counter / len(subdomain)
    return ratio


def prc_entropy(domain):
    """
    calculate the entropy of subdomain
    :param domain_str: subdomain
    :return: the value of entropy
    """
    subdomain = ignoreVPS(domain)
    # get probability of chars in string
    prob = [float(subdomain.count(c)) / len(subdomain) for c in dict.fromkeys(list(subdomain))]

    # calculate the entropy
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy


def extract_DGA_features(url):
    dga_features = []

    i = domain_length(url)
    dga_features.append(i)

    i = subdomains_number(url)
    dga_features.append(i)

    i = subdomain_length_mean(url)
    dga_features.append(i)

    i = has_www_prefix(url)
    dga_features.append(i)

    i = has_hvltd(url)
    dga_features.append(i)

    i = contains_single_character_subdomain(url)
    dga_features.append(i)

    i = contains_TLD_subdomain(url)
    dga_features.append(i)

    i = underscore_ratio(url)
    dga_features.append(i)

    i = contains_IP_address(url)
    dga_features.append(i)

    i = contains_digit(url)
    dga_features.append(i)

    i = vowel_ratio(url)
    dga_features.append(i)

    i = digit_ratio(url)
    dga_features.append(i)

    i = prc_rrc(url)
    dga_features.append(i)

    i = prc_rcc(url)
    dga_features.append(i)

    i = prc_rcd(url)
    dga_features.append(i)

    i = prc_entropy(url)
    dga_features.append(i)

    domain_name = get_domain_name(url)
    # dga_features.append(domain_name)

    ngrams_features = alexa_vc.transform([url])
    alexa_counts = np.log10(np.asarray(ngrams_features.sum(axis=0)).flatten())
    alexa = alexa_counts * alexa_vc.transform([domain_name]).T
    dga_features.append(alexa[0])

    wordgram_feature = dict_cv.transform([url])
    dict_counts = np.log(np.asarray(wordgram_feature.sum(axis=0)).flatten())
    wordgram = dict_counts * dict_cv.transform([domain_name]).T
    dga_features.append(wordgram[0])

    return dga_features

def main():
    image = Image.open('./pictures/cyber-security.jpeg')
    image2 = Image.open('./pictures/ariel-logo.jpeg')

    col1, mid, col2 = st.columns([1, 1, 100])
    with col1:
        st.image(image, width=150)
    with mid:
        st.image(image2, width=150)

    st.header(":skull: Malicious URL Detection :skull:",divider='rainbow')

    html_temp = """
  <div style="background-color:blue;padding:10px">
  <h2 style="color:grey;text-align:center;">Streamlit App </h2>
  </div>

  """
    url = st.text_input("Enter website address or URL")

    if st.button("Predict"):
        result = predict_url(url)
        print(result)

        if result > 0.5:
            prediction = 'phishing website'
            img = 'bad.png'
            st.warning('The URL: {}  is a malicious URL'.format(prediction))
        else:
            prediction = 'benign website'
            img = 'good.png'
            st.success('The URL was classified as a {}'.format(prediction))

        load_images(img)

    st.subheader("About")

    # Create a container
    with st.container():
        # Customize the background color, padding, and some styling
        st.markdown("""
            <style>
            .beautiful-container {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding-left: 20px;
                padding-bottom: 10px
                padding-top: 10px
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .beautiful-title {
                color: #333;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }
            </style>
            <div class="beautiful-container">
                <b class="beautiful-title">Created by:</b>
                <ul>
                <li> Adnan Azem </li>
                <li> Jode Shibli </li>
                </ul>

            </div>
            """, unsafe_allow_html=True)


    st.link_button("Go to Project", "https://github.com/AdnanAzem/Malicious-URL-Detection.git")
    link = '''
    <a href = "https://github.com/AdnanAzem/Malicious-URL-Detection.git">click here</a>
    '''

if __name__ == '__main__':
    main()