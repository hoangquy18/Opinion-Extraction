# Opinion Extraction from user reviews in e-commerce
Crawl data on laptops on e-commerce websites to get user reviews and build a model to extract user opinions.
## Overview
* Use Beautifulsoup and Selenium libraries to crawl user reviews. 

* Use Text Normalization and Tone Standardization for data preprocessing. 

* Experiments with different embeddings: word, character, and contextual embedding.  

## Dataset
|         | Train           | Dev  | Test |
| ------------- |:-------------:| :-------------: | :-------------: | 
| Number of comments      | 1066 | 356 | 355 | 
| Number of Aspect       | 1871 | 623 | 619 | 
| Average number of aspect per sentence | 1.75 | 1.75 | 1.74|
| Average length per sentence | 88.18 | 86.16 | 90.55 |
| Average span length | 38.22 | 37.23 | 37.75 |

## Experiments
|  Embedding type       | Pretrained model |Precision           | Recall  | F1-score |
| ------------- |:-------------:|:-------------:| :-------------: | :-------------: | 
| Word      | - |53.08 | 55.55 | 52.74 |
| Word + Character| -       | 52.48 | 55.00 | 52.33 |
| Word + Character + Contextual | XLM-RoBERTa| 55.75 | 58.12 | 55.48 |
| Word + Character + Contextual | PhoBERT| 62.65 | 63.68 | 61.80 |

