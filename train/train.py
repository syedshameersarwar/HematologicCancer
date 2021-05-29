import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectFromModel
import tensorflow as tf
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


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
        model = LogisticRegression(solver='lbfgs', max_iter=5500)
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

        print('After RFE feature selection: ', selectedFeatures.shape)
        return (selectedFeatures, y)

    def SFM(self, x, y):
      '''
      Args
      x: in the x variable we have all the input features Hb, WBC, PLT etc
      y: in the y variable we have all the output sub groups of our blood cancer

      Returns
      new_x: this x holds all the features that are selected using Select From Model(Lasso) Method
      y: nothing changes in y.
      '''

      selectedFeatures = []
      selector = SelectFromModel(estimator=LogisticRegression(penalty='l2'), threshold='median', max_features=30).fit(x, y)
      feats = selector.get_support(True)
      
      for i in range(len(feats)):
        selectedFeatures.append(x.columns[feats[i]])

      new_x = x[selectedFeatures]
      print("After SFM Featrue Selection: ", new_x.shape)

      return (new_x, y)

    def SFM_RF(self, x, y):
      '''
      Args
      x: in the x variable we have all the input features Hb, WBC, PLT etc
      y: in the y variable we have all the output sub groups of our blood cancer

      Returns
      new_x: this x holds all the features that are selected using Select From Model(Lasso) Method
      y: nothing changes in y.
      '''
      # 70 110
      selectedFeatures = []
      selector = SelectFromModel(RandomForestClassifier(n_estimators=70, random_state=17), max_features=30).fit(x, y)
      feats = selector.get_support(True)
      
      for i in range(len(feats)):
        selectedFeatures.append(x.columns[feats[i]])

      new_x = x[selectedFeatures]
      print("After SFM Random Forest Feature Selection: ", new_x.shape)

      return (new_x, y)

    def TrainLR(self, data, featureSelection='chi2'):
        #Pre-Processing
        x, y = self.prepare(data)
        
        #Feaure Selection
        if (featureSelection == 'chi2'):
          x, y = self.chi2(x, y)
          print('Feature Selected: Chi Square Method')
        elif (featureSelection == 'rfe'):
          x , y = self.RFE(x, y)
          print('Feature Selected: RFE Method')
        elif (featureSelection == 'sfm'):
          x, y = self.SFM(x, y)
          print('Feature Selected: Select From Model')
        elif (featureSelection == 'sfmrf'):
          x, y = self.SFM_RF(x, y)
          print('Feature Selected: Select From Model Random Forest')

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size= 0.1, random_state= 42)
        model = LogisticRegression(solver='lbfgs', max_iter=5500).fit(xtrain, ytrain)

        #Testing
        print(model.score(xtest, ytest))
        print(classification_report(ytest, model.predict(xtest)))

    def TrainSVM(self, data, featureSelection='chi2'):
        #Pre-Processing
        x, y = self.prepare(data)

        #Feature Selection
        if ( featureSelection == 'chi2' ):
          x, y = self.chi2(x, y)
          print('Feature Selected: Chi Square Method')
        elif ( featureSelection == 'rfe' ):
          x, y = self.RFE(x, y)
          print('Feature Selected: RFE Method')
        elif ( featureSelection == 'sfm'):
          x, y = self.SFM(x, y)
          print('Feature Selected: SFM Method')

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.1, random_state=42)
        model = SVC(kernel='poly', probability=True, C=1, gamma=0.00001, verbose=2, random_state=42, max_iter=-1, shrinking=False,
                    decision_function_shape='ovo')
        model.fit(xtrain, ytrain)

        #Testing
        print(model.score(xtest, ytest))
        print(classification_report(ytest, model.predict(xtest)))

    def TrainDT(self, data, featureSelection='chi2'):
        #Pre-Processing
        x, y = self.prepare(data)

        #Feature Selection
        if (featureSelection == 'rfe'):
          x, y = self.RFE(x, y)
          print('Feature Selected: RFE Method')
        elif (featureSelection == 'chi2'):
          x, y = self.chi2(x, y)
          print('Feature Selected: Chi Square Method')
        elif (featureSelection == 'sfm'):
          x, y = self.SFM(x, y)

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

    def TrainNB(self, data, featureSelection='chi2'):
        #Pre-Processing
        x, y = self.prepare(data)

        #Feature Selection
        if ( featureSelection == 'chi2' ):
          x, y = self.chi2(x, y)
          print('Feature Selected: Chi Square Method')
        elif ( featureSelection == 'rfe' ):
          x, y = self.RFE(x, y)
          print('Feature Selected: RFE Method')
        elif ( featureSelection == 'sfm'):
          x, y = self.SFM(x, y)
          print('Feature Selected: SFM Method')

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.1, random_state=42)
        gnb = GaussianNB()
        gnb.fit(xtrain, ytrain)

        #Testing
        print(gnb.score(xtest, ytest))
        print(classification_report(ytest, gnb.predict(xtest)))

    def TrainKNN(self, data, featureSelection='chi2'):
        #Pre-Processing
        x, y = self.prepare(data)

        #Feature Selection
        if ( featureSelection == 'chi2' ):
          x, y = self.chi2(x, y)
          print('Feature Selected: Chi Square Method')
        elif ( featureSelection == 'rfe' ):
          x, y = self.RFE(x, y)
          print('Feature Selected: RFE Method')
        elif ( featureSelection == 'sfm'):
          x, y = self.SFM(x, y)
          print('Feature Selected: SFM Method')
        elif (featureSelection == 'sfmrf'):
          x, y = self.SFM_RF(x, y)

        #Training
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.1, random_state=42)
        model = KNeighborsClassifier(n_neighbors=15, algorithm='brute', weights='distance')
        model.fit(xtrain, ytrain)

        #Testing
        print(model.score(xtest, ytest))
        print(classification_report(ytest, model.predict(xtest)))        

    def TrainANN(self, data, featureSelection='chi2'):
        #Pre-Processing
        x, y = self.prepare(data)
        
        #Feature Selection
        if (featureSelection == 'rfe'):
          x, y = self.RFE(x, y)
          print('Feature Selected: RFE Method')
        elif (featureSelection == 'chi2'):
          x, y = self.chi2(x, y)
          print('Feature Selected: Chi Square Method')
        elif (featureSelection == 'sfm'):
          x, y = self.SFM(x, y)

        x = np.asarray(x).astype('float32')
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = 0.1, random_state=42)

        #Training
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(256, input_dim=xtrain.shape[1], activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(64, activation=tf.nn.relu))
        model.add(tf.keras.layers.Dense(13, activation=tf.nn.softmax))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        model.fit(xtrain, ytrain, validation_data=(xtest, ytest), epochs=300, batch_size=48)

        #Testing
        val_loss, val_acc = model.evaluate(xtest, ytest)
        print(val_loss)
        print(val_acc)
        y_pred = model.predict(xtest, batch_size=64, verbose=1)
        y_pred_bool = np.argmax(y_pred, axis=1)
        print(classification_report(ytest, y_pred_bool))

  