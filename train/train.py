import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


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

