# General info
This toolkit is a powerful library/API written in Java that can classify apps' releases to bad, good or neutral based on users' reviews.
# How to use it ?
In this version, is not possible to extract the training/input data. Hence, we provide an example of an app's data (in "train_data_exp.csv"). To launch the tool, please refer to this file in order to pick a release number, which is indeed the input for this toolkit.
We run the tool, we recommend to launch it with Java10. Once, the release number is entered, the toolkit displays the classification (bad, good or neutral) of the release in the command line console.
3. To get more details, the user can have a look at the explanation (a PDF file).
# Example of usage
To predict the class of the release number "249000053":
```
java -jar AppTracker.jar 249000053
```
