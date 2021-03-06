# Assignment 1 - Collocation tool
 
Link to GitHub of this assignment: https://github.com/sarah-hvid/Lang_assignment1

## Assignment description
The purpose of this assignment is to perform collocational analysis using string processing and NLP tools. The ```.py``` created should take a user-defined search term , window-size and text file. Based on the input the mutual information score should be calculated for each context word. The results should be saved to a CSV file.\
The full assignment description is available in the ```assignment1.md``` file.

## Methods
Initially, the user must specify whether to work with a single file or a directory. The methods applied are the same for each file inputted in either way, only the output may differ for the two inputs.\
The input must be a text file containing english text. The text is read in and then preprocessed to remove puncts and lowercase all words. This ensures that puncts cannot be collocates and that capitalized words aren't seen as different from uncapitalized words. ```Spacy``` is then used to tokenize the text. From here, the metrics needed to calculate the mutual information (MI) score are gathered by looping through the corpus. The MI score is calculated according to the [english-corpora](https://www.english-corpora.org/mutualInformation.asp) formula (Davies, n.d.). The user must specify the keyword to find collocates for, and may also specify the window of words to either side of the keyword. The default window size is 5 _(**note** if the keyword is unfortunately located in the very beginning or end of the doc, it will cause an error as window words aren't available. You must choose a different word for the file.)_. The words of the corpus and the collocates are then counted which creates a dictionary. The final metrics are gathered by looping through the dictionaries. The MI score is then calculated for each collocate. If the user specified a single file, a dataframe is created containing the filename, keyword, metrics and MI score. The CSV will be saved in the ```output``` folder and named according to the keyword input and the file name. If the user specified a directory, the user may also specify whether they want to create several CSV outputs per text file input, or a gathered CSV containing all results per text file. The default value is separate CSV files. 

## Usage
In order to run the script, certain modules need to be installed. These are available in the ```requirements.txt``` file. The folder structure must be the same as in this GitHub repository (ideally, clone the repository).
```bash
git clone https://github.com/sarah-hvid/Lang_assignment1.git
cd Lang_assignment1
pip install -r requirements.txt
```
The data used in this assignment is the ```100_english_novels```. The data is available in the shared ```CDS-LANG``` folder. The data may also be downloaded from the Computational stylistics [GitHub repository](https://github.com/computationalstylistics/100_english_novels). The files must be placed in the ```data``` folder in order to replicate the results of this assignment.\
The current working directory when running the script must be the one that contains the ```data```, ```output``` and ```src``` folder.\
\
How to run the script from the command line: 

__The collocation analysis script__\
Specified file and keyword (search term):
```bash
python src/collocation.py -f data/Woolf_Years_1937.txt -st love
```
Specified directory, keyword and window:
```bash
python src/collocation.py -f data -st hate -wi 5
```
Specified directory, keyword, window and output type:
```bash
python src/collocation.py -f data -st love -wi 5 -o gathered
```

Examples of the outputs of the script can be found in the ```output``` folder. 

## Results
The results of the script are as expected. The CSV files are created as they should. As this script does not attempt to analyse any particular data but rather functions on any _'random'_ data, there are no results to discuss per se. However, it could be noted that this script does not take low frequencies (1-3 tokens) of collocate words into account. The MI score for these collocates are therefore weird and should maybe be filtered out if the scores should be used for further analysis. Another point here might be the presence of stopwords as collocates. These are rarely informative as context words and could also be removed after the analysis.\
\
The output CSV for a single file:\
\
[**CSV file**](/output/MI_Barclay_Ladies_1917_red.csv)

| file_name	| key_word	| window	| collocate_term |	collocate_frequency	| text_frequency	| MI_score |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Barclay_Ladies_1917	| red	 | 5	 | bloomed	| 2	| 1	| 9.893733236193917 |
| Barclay_Ladies_1917	| red	 | 5	 | drooped	| 1	| 1	| 8.893733236193917 |
| Barclay_Ladies_1917	| red	 | 5	 | floated |	1 |	1	| 8.893733236193917 |
| ...  | ...  | ...  | ... | ...  | ...  | ... |

The output CSV for multiple files when gathered:\
\
[**CSV file**](/output/MI_all_jealous.csv)

| file_name	| key_word	| window	| collocate_term |	collocate_frequency	| text_frequency	| MI_score |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Bennet_Helen_1910 |	jealous |	5	 | lilian	| 1	| 31	| 4.633715117394616 |
| Bennet_Helen_1910 |	jealous |	5	 | 	should  |	1 |	54 |	3.833023925618023 |
| Bennet_Helen_1910 |	jealous |	5	 | imagine	| 1	| 15	| 5.681020832172973 |
| ...  | ...  | ...  | ... | ...  | ...  | ... |
| Woolf_Years_1937 |	jealous |	5 |	face |	1 |	127 |	4.104402703672052 |
| Woolf_Years_1937 |	jealous |	5 |	he |	7 |	2869 |	2.414110059733157 |
| Woolf_Years_1937 |	jealous |	5 |	was |	5 |	2729 |	2.000858806057439 |
| ...  | ...  | ...  | ... | ...  | ...  | ... |

## References

Computational Stylistics Group. (Aug, 2017). 100 English Novels (1.4) [Computer software]. Retrieved May 24, 2022, from https://github.com/computationalstylistics/100_english_novels 

Davies, M. (n.d.). Mutual information. English Corpora. Retrieved May 24, 2022, from https://www.english-corpora.org/mutualInformation.asp

