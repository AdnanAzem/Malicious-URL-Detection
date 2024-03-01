# Malicious-URL-Detection

## Dataset
### In this project we use 2 datasets:
<ul>
  <li>
    <b>First Dataset:</b>
  </li>

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

<b>Our First Dataset Link:</b> <a href="https://www.kaggle.com/datasets/samahsadiq/benign-and-malicious-urls">Dataset1</a>
<li>
  <b>Second Dataset:</b>  
</li>
This dataset has been collected from Alexa website ranking a blacklist of previous DGA domain names both sources are avaiblable within the provenance section.

Files 4 files two DGA files, one alexa ranking dataset and an english words dataset.
<ol>
  <li>
    <b>dga_project_dga_domain_list_clean.txt:</b> This file contains the name of the DGA (irrelevant IMO for just building a classifier), domain (most importanta information) name and a timestamp
    What is important to keep as information are the domain names, the rest can be dropped as we will do some feature engineering to create relevant columns.
  </li>
  <li>
    <b>dga_project_top-1m.csv:</b> This file contains legitimate domain names from Alexa, domain name are ranked by their popularity
  </li>
  <li>
    <b>top-1m.csv:</b> This is similar to the previous file dga_project_top_1m.csv but a bit longer
  </li>
  <li>
    <b>words.txt:</b> This is a ditionary of english words collected from <a href= "https://github.com/dwyl/english-words">github</a>. This file will be used to compare ngrams from domain names.
  </li>
</ol>

<b>Our Second Dataset Link:</b> <a href="https://www.kaggle.com/datasets/slashtea/domain-generation-algorithm?select=dga_project_dga_domain_list_clean.txt">Dataset2</a>

</ul>

## Feature Extraction
The following features will be extracted from the URL of the first dataset for classification.
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

The following features will be extracted from the DGA of the secon dataset for classification.
<br> 
<ol>
  <li>
    Structural Features
    <ul>
      <li>Domain Name Length</li>
      <li>Number of Subdomains</li>
      <li>Subdomain Length Mean</li>
      <li> Has www Prefix</li>
      <li>Has www Prefix</li>
      <li>Has valid TLD</li>
      <li>Contains Single-Character Subdomain</li>
      <li>Contains TLD as Subdomain</li>
      <li>Underscore Ratio</li>
      <li>Contains IP Address</li>
    </ul>
  </li>
  <br> 
  <li>
    Linguistic Features
    <ul>
      <li>Contains Digits</li>
      <li>Vowel Ratio</li>
      <li>Digit Ratio</li>
      <li>Ratio of Repeated Characters</li>
      <li>Ratio of Consecutive Consonants</li>
      <li> Ratio of Consecutive Digits</li>
    </ul>
  </li>
  <br> 
  <li>
    Statistical Features
    <ul>
      <li>Entropy</li>
      <li>words gram</li>
      <li>alexia gram</li>
    </ul>
  </li>
</ol>














