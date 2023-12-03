------------------------------------------------------------------------------

File Index:

benign.txt -                    Benign url dataset for testing
calvopp.py -                    Partial preprocessor to turn URLs into values -1 to 1
preprocessor.py -               Final preprocessor to turn values -1 to 1 to 0 to 1 and make other adjustments
testing_input_ben/mal.csv -     Partially preprocessed urls from the URL grabber
testing_output.csv -            Final test file with combined benign/malicious generated urls
traffic_classifier_BINARY.py -  Machine learning model
Training Dataset.csv -          Initially downloaded training dataset
training_output_test.csv -      Testing subset of training set
training_output.csv -           Training subset of training set
URLgrabber.py -                 Program to grab fresh malicious urls as well as unwrap benign urls
main.py -                       Full implementation

To run:
    Full Program: Run main.py
    Just Model: Uncomment bottom of traffic_classifier_BINARY and run there

------------------------------------------------------------------------------

This program requires the installation of the following libraries for use:
    - csv
    - urllib
    - requests
    - whois
    - datetime
    - beautifulsoup4
    - socket
    - dns.resolver
    - googlesearch
    - numpy
    - torch
    - random
    - scikit-learn
    - time
    - datetime

------------------------------------------------------------------------------

