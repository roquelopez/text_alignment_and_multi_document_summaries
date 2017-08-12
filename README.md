# Automatic alignment of texts and their multi document summaries

In this system, we implemented the following four approaches to align texts and their multi-document summaries:
- Superficial Approach
- Deep Approach
- Hybrid Approach
- Jing and McKeown (1999) method

For more information about these methods, see our paper: http://link.springer.com/chapter/10.1007%2F978-3-319-09761-9_25

We used news texts, CST relations and the summaries of the CSTNews corpus for the experiments.

In the "src folder", you can find the code and, in the "resource folder", the resources that were used.


## Execution:
To run this program, it is necessary to have installed Python 3.2 or higher and the library BeautifulSoup 4.0.

The general way to run this program is the following:
```
 $ python main.py option
 
```

Where option could be:
- "superficial", to run the superficial approach. By default, it is selected the Word Overlap method (you can change it in the line 30 of the main.py file).
- "deep", to run the deep approach.
- "hybrid", to run the hybrid approach.
- "jing", to run the Jing and McKeown method.

## Example:
```
 $ python main.py "jing"

```
## Notes:
If you want to change the paths of the input data, in the main.py file change these options:

- folder_corpus = "YOUR PATH"
- folder_manual_alignments = "YOUR PATH"
- folder_cst_relations = "YOUR PATH"
- file_matrix_features = "YOUR PATH"
