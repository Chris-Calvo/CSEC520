import random
import calvopp
import preprocessor
import URLgrabber
import traffic_classifier_BINARY

def select_random_items(original_list, num_items):
    # Ensure the number of items requested is not greater than the length of the original list
    if num_items > len(original_list):
        raise ValueError("Number of items requested is greater than the length of the original list.")

    # Use random.sample to select x random items from the original list
    random_items = random.sample(original_list, num_items)
    return random_items

def main():
    print("Grabbing Testing URL Lists...")

    # Generate URL List
    # url_list = URLgrabber.grabLongPhishingURLs()
    mal_url_list = URLgrabber.grabLivePhishingURLs()
    ben_url_list = URLgrabber.readBenignURLs("benign.txt")

    print("Mixing with benign URLs in 5:1 ratio for test dataset...")

    trimmed_ben_url_list = select_random_items(ben_url_list,len(mal_url_list)*5)

    # Convert URLS to CSV Values
    for url in mal_url_list:
        calvopp.append_to_csv("testing_input_mal.csv",calvopp.process_url(url))
    for url in trimmed_ben_url_list:
        calvopp.append_to_csv("testing_input_ben.csv",calvopp.process_url(url))

    # Preprocess
    preprocessor.convert_csv_testing("testing_input_mal.csv","testing_input_ben.csv","testing_output.csv")

    preprocessor.convert_csv_training("Training Dataset.csv","training_output.csv","training_output_test")

    #Train and test model on different testing sets
    traffic_classifier_BINARY.train_traffic_classifier("training_output.csv","training_output_test.csv")
    traffic_classifier_BINARY.train_traffic_classifier("training_output.csv","testing_output.csv")

if __name__=="__main__":
    main()