__author__ = 'Michael'

import os
import numpy as np
import scipy as sp

train_folder = 'C:/Users/Michael/Projects/Kaggle EEG/train'

class EegDataSeries():
    '''
    Class represents a single "series" of data in the EEG training data, including both the raw data and the
    events data. For example, includes subj12_series8_events.csv and subj12_series8_data.csv
    '''

    # placeholders
    inputs = None # eventually a should be a numpy array
    outputs = None # eventually a numpy array
    prediction = None # eventually a nupmy array
    subject = None # integer
    series = None # integer
    def __init__(self,subj,srs):
        '''
        Should read in the events and data files to numpy arrays and work with them from there
        :param file:
        :return:
        '''
        self.subject = subj
        self.series = srs
        self.events_file = os.path.join(train_folder,'subj'+subj + '_series'+srs +'_events.csv')
        self.data_file = os.path.join(train_folder,'subj'+subj + '_series'+srs +'_data.csv')

        # ... read those guys to numpy arrays ...

    def predict(self):
        # iterate over each frame and provide the prediction, and store it to self.prediction
        # self.prediction should have the same structure as self.outputs

        pass

    def calculate_confusion_matrix(self):
        # iterate over the frames of the data and compare predicted values to actual, creating a confusion matrix.
        pass

def import_training_data():
    all_series = []
    subject = [1,2,3,4] #etc...
    series = [1,2,3] # etc...

    # psuedocode:
    for i in series:
        for j in subject:
            foo = None
            # create new EegDataSeries object (called e.g. 'foo') for each one
            all_series.append(foo)
    pass

def main():
    import_training_data()
    # do other stuff here, like train a model, etc...