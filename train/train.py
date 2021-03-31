import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE


class Train():

    def prepare(self, data):
        '''
        Args
        data: pandas dataframe already opened using pd.read_csv

        Returns
        x: in the x variable we have all the input features Hb, WBC, PLT etc
        y: in the y variable we have all the output sub groups of our blood cancer
        '''
        nan_values = float("NaN")

        print('Before cleaning the NaN: ', data.shape)

        data.replace("#NULL!", nan_values, inplace=True)
        data.dropna(subset = ['NE_SFL'], inplace=True)
        dropped_cols = ['Sub_groups1', 'Sub_groups2']
        data.drop(dropped_cols, axis='columns', inplace=True)

        print('After cleaning the NaN: ', data.shape)

        x = data[data.columns[1:]]
        y = data[data.columns[0]]

        return (x,y)

    def chi2(self, x ,y):
        '''
        Args
        x: in the x variable we have all the input features Hb, WBC, PLT etc
        y: in the y variable we have all the output sub groups of our blood cancer

        Returns
        new_x: this x holds all the features that are selected using chiSquare Method
        y: nothing changes in y
        '''
        test = SelectKBest(score_func=chi2, k='all')
        fit = test.fit(x, y)

        np.set_printoptions(precision=3)
        features = fit.transform(x)
        features[0][25] = float(features[0][25])

        zipFeatures = zip(features[0], x.columns)
        sortedFeatures = sorted(tuple(zipFeatures))

        chi2_features = []
        for i in range(len(sortedFeatures)):
            if (i >= 17):
                chi2_features.append(sortedFeatures[i][1])
        
        new_x = x[chi2_features]
        print('After ChiSquare feature selection: ', new_x.shape)

        return (new_x, y)

    def RFE(self, x, y):
        '''
        Args
        x: in the x variable we have all the input features Hb, WBC, PLT etc
        y: in the y variable we have all the output sub groups of our blood cancer

        Returns
        selectedFeatures: this x holds all the features that are selected using RFE Method
        y: nothing changes in y.
        '''
        model = LogisticRegression(solver='lbfgs')
        rfe = RFE(model, 30)
        fit = rfe.fit(x, y)

        rfeFeatures = fit.ranking_
        rfe_x = zip(rfeFeatures, x.columns)
        rfe_x = sorted(tuple(rfe_x))

        selectedFeatures = []
        for i in range(len(rfe_x)):
            if ( rfe_x[i][0] == 1 ):
                selectedFeatures.append(rfe_x[i][1])
        selectedFeatures = x[selectedFeatures]

        return (selectedFeatures, y)

    def TrainLR(self, data):
        #Pre-Processing
        x, y = self.prepare(data)
        x, y = self.chi2(x, y)

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size= 0.1, random_state= 42)
        model = LogisticRegression(solver='lbfgs', max_iter=2000).fit(xtrain, ytrain)

        #Testing
        print(model.score(xtest, ytest))
        print(classification_report(ytest, model.predict(xtest)))

    def TrainSVM(self, data):
        #Pre-Processing
        x, y = self.prepare(data)
        x, y = self.RFE(x, y)

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=3)
        model = SVC(kernel='poly', probability=True, C=15, verbose=2, random_state=42)
        model.fit(xtrain, ytrain)

        #Testing
        print(model.score(xtest, ytest))
        print(classification_report(ytest, model.predict(xtest)))

    def TrainDC(self, data):
        #Pre-Processing
        x, y = self.prepare(data)
        x, y = self.RFE(x, y)

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=3)
        model = DecisionTreeClassifier(random_state=5)
        classifier = model.fit(xtrain, ytrain)
        
        print("Trying post pruning with complexity pruning to remove overfitting")

        path = classifier.cost_complexity_pruning_path(xtrain, ytrain)

        ccp_alphas, impurities = path.ccp_alphas, path.impurities

        classifiers = []
        for ccp_alpha in ccp_alphas:
            classifier = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
            classifier.fit(xtrain, ytrain)
            classifiers.append(classifier)

        #Testing
        classifiers = classifiers[:-1]
        ccp_alphas = ccp_alphas[:-1]

        train_scores = [clf.score(xtrain, ytrain) for clf in classifiers]
        test_scores = [clf.score(xtest, ytest) for clf in classifiers]
        max_test_accuracy_classifier = classifiers[test_scores.index(max(test_scores))]
        max_test_score = max_test_accuracy_classifier.score(xtest, ytest)
        print("Model Test Score after pruning: ", max_test_score)

