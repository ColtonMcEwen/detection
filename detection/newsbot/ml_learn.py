# Create a vector of zeros equal to the size of the DictEntry table, then set
# the specific row to 1 if the word related to that ID by DictEntry appears in the article.
# Then create a matrix of vectors transposed so each row represents the truth vector for 1
# article. Then the Y vectors will be the scores of those same articles.

# Once trained, test it on a new input and see what it comes up with.

import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

import pickle
import os, sys, re, time

proj_path = "/Users/colton/detection/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "detection.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.gis.views import feed
from newsbot.models import *
from newsbot.util import *

print("Setting up..")
cDict = loadCanonDict()
qs_Examples = ArticleExample.objects.filter(quality_class__lt = 5)

print("Processing examples")
(Y_vector, examplesMatrix) = processExamples(qs_Examples, cDict)

print("\nExamplesMatrix Results: ")
print(examplesMatrix.shape)
print("Y values results:")
print(Y_vector.shape)

print("Max/min of Y: ")
ymax = max(Y_vector)
ymin = min(Y_vector)
print(str(ymax)+ "/" + str(ymin))

X_train, X_test, y_train, y_test = train_test_split(examplesMatrix, Y_vector, test_size=0.2)
print("Training...")

# Commented code for several models:
model = MLPClassifier(hidden_layer_sizes=(128,64,32,16,8), max_iter=2500)
# model = SVC(gamma='scale', probability = True)
# model = KNeighborsClassifier()
# model = LinearDiscriminantAnalysis()
# model = GaussianNB()
# model = DecisionTreeClassifier()
# model = LogisticRegression()

model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Test to see if the model(s) is seeing and producing reasonable values
print("Max/min of predictions: ")
ymax = max(predictions)
ymin = min(predictions)
print(str(ymax)+ "/" + str(ymin))

print("Max/Min of Y_test")
ymax = max(y_test)
ymin = min(y_test)
print(str(ymax)+ "/" + str(ymin))

print("Max/Min of Y_train")
ymax = max(y_train)
ymin = min(y_train)
print(str(ymax)+ "/" + str(ymin))

print("Statistical tests...")
print("***************")
print("Accuracy score: " + str(accuracy_score(predictions, y_test)))
print("Confusion Matrix: ")
print(confusion_matrix(predictions, y_test))
print("Classification report: ")
print(classification_report(predictions, y_test))
print("***************")
print("Regression based: ")
rSq = r2_score(y_test, predictions)
expVariance = explained_variance_score(y_test, predictions)
maxErr = max_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
print("R^2: " + str(rSq))
print("Explained variance: " + str(expVariance))
print("Max Error: " + str(maxErr))
print("Mean absolute Error: " + str(mae))

exit(0)







