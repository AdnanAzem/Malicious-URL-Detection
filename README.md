# Malicious-URL-Detection

## Dataset
This dataset is created to form a Balanced URLs dataset with the same number of unique Benign and Malicious URLs. The total number of URLs in the dataset is 632,508 unique URLs.

The creation of the dataset has involved 2 different datasets from Kaggle which are as follows:

<b>First Dataset: 450,176 URLs</b>, out of which 77% benign and 23% malicious URLs.
Can be found here: <a href="https://www.kaggle.com/datasets/siddharthkumar25/malicious-and-benign-urls">First Dataset</a>

<b>Second Dataset: 651,191 URLs</b>, out of which 428103 benign or safe URLs, 96457 defacement URLs, 94111 phishing URLs, and 32520 malware URLs.
Can be found here: <a href="https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset">Second Dataset</a>

To create the <b>Balanced dataset</b>, the first dataset was the main dataset, and then more malicious URLs from the second dataset were added, after that the extra Benign URLs were removed to keep the balance. Of course, unifying the columns and removing the duplicates were done to only keep the unique instances.

For more information about the collection of the URLs themselves, please refer to the mentioned datasets above.

All the URLs are in one .csv file with 3 columns:
<ul>
  <li>First column is the 'url' column which has the list of URLs.</li>
  <li>Second column is the 'label' which states the class of the URL wether 'benign' or 'malicious'.</li>
  <li>Third column is the 'result' which also represents the class of the URL but with 0 and 1 values. {0 is benign and 1 is malicious}.</li>
</ul>

<b>Our Dataset Link:</b> <a href="https://www.kaggle.com/datasets/samahsadiq/benign-and-malicious-urls">Dataset</a>

## Feature Extraction
The following features will be extracted from the URL for classification.
<ol>
<li>
    Length Features
    <ul>
        <li>Length Of Url</li>
        <li>Length of Hostname</li>
        <li>Length Of Path</li>
        <li>Length Of First Directory</li>
    </ul>
</li>
   <br> 
<li>
    Count Features
    <ul>
        <li>Count Of '-'</li>
        <li>Count Of '@'</li>
        <li>Count Of '?'</li>
        <li>Count Of '%'</li>
        <li>Count Of '.'</li>
        <li>Count Of '='</li>
        <li>Count Of 'http'</li>
        <li>Count Of 'www'</li>
        <li>Count Of Digits</li>
        <li>Count Of Letters</li>
        <li>Count Of Number Of Directories</li>
    </ul>
</li>
    <br>
<li>
    Binary Features
    <ul>
        <li>Use of IP or not</li>
        <li>Use of Shortening URL or not</li>
    </ul>
</li>
</ol>
