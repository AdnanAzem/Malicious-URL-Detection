from urllib.parse import urlparse
import re
import streamlit as st
from PIL import Image
import joblib

rf_clf = joblib.load('../models/RandomForest.pkl')

def predict_url(url):
    url_features = extract_features(url)
    rf_prediction = rf_clf.predict(url_features)
    prediction = rf_prediction
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

    return

def load_images(file_name):
    img = Image.open(file_name)
    return st.image(img, width=150)

def main():
    image = Image.open('./pictures/cyber-security.jpeg')
    image2 = Image.open('./pictures/ariel-logo.jpeg')

    col1, mid, col2 = st.columns([1, 1, 100])
    with col1:
        st.image(image, width=150)
    with mid:
        st.image(image2, width=150)

    st.title("Malicious URL Detection")
  #   """Phishing URL Detection App
  #   With Streamlit
  #
  # """

    html_temp = """
  <div style="background-color:blue;padding:10px">
  <h2 style="color:grey;text-align:center;">Streamlit App </h2>
  </div>

  """
    # st.markdown(html_temp, unsafe_allow_html=True)
    url = st.text_input("Enter website address or URL")

    if st.button("Predict"):
        result = predict_url(url)

        if result >= 0.6:
            prediction = 'phishing website'
            img = 'bad.png'
            st.warning('The video: {}  is a malicious video'.format(prediction))
        else:
            prediction = 'benign website'
            img = 'good.png'
            st.success('The URL was classified as a {}'.format(prediction))


        load_images(img)

    st.subheader("About")
    st.info("Adnan Azem & Jode Shibli Final Project")
    st.info("Link to the project:  "+ "")


if __name__ == '__main__':
    main()