##################################
# Goal: Create a GUI application with Python, PyQt and tensorflow (inception_v3) with these goals:
# 	Primary
# 	1. Allow loading of image file/s
# 	2. Run inference on image
# 	3. Output human-readable classification of objects in image
# 	Secondary
# 	1. Retrain model using image file/s
#   2. Load/Save model to/from file
##################################


import os
import sys
import re
import tensorflow as tf
import numpy as np

from PyQt5 import QtGui, QtCore, QtWidgets, uic

import mainwindow

model_dir = "C:\git\ClassifyThis\imagenet"
# uiFile = "mainwindow.ui"

# ui_mw, baseClass = uic.loadUiType(uiFile)

# Main app
# Initialize with QMainWindow since that was the base widget used in the UI
# This class inherits from QtWidgets.QMainWindow and mainwindow.Ui_MainWindow
class ClassifyThisApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    currentFile = []
    image_data = []
    def __init__(self, parent=None):
        super(ClassifyThisApp, self).__init__(parent)
        self.setupUi(self)  # This function sets up the UI - defined in pyuic5'd file

        self.loadFileButton.clicked.connect(self.loadFileFromBrowser)
        self.classifyButton.clicked.connect(self.classify)

    def loadFile(self,name):
        """ Load the image file
        :return: none
        """

        print("Loading file: " + name)
        if not tf.gfile.Exists(name):
            tf.logging.fatal('File does not exist %s', name)
        self.image_data = tf.gfile.FastGFile(name, 'rb').read()

        image = QtGui.QImage(name)
        image_pixmap = QtGui.QPixmap.fromImage(image)
        size = self.imageGraphicsView.size()
        image_pixmap = image_pixmap.scaledToHeight(self.imageGraphicsView.height())
        scene = QtWidgets.QGraphicsScene(self.imageGraphicsView)
        scene.addPixmap(image_pixmap)

        self.imageGraphicsView.setScene(scene)
        self.imageGraphicsView.repaint()
        self.imageGraphicsView.show()
        print("File " + name + " loaded")


    def loadFileFromBrowser(self):
        """ Shows file browser and returns the filepath

        :return: none
        """
        fd = QtWidgets.QFileDialog()
        fd.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # fd.setFilter("Image files (.jpg)")
        if fd.exec_():
            filenames = fd.selectedFiles()
            self.filePathLineEdit.setText(filenames[0])
            self.loadFile(filenames[0])
            self.currentFile = filenames[0]
        

    def createGraph(self):
        """ Loads the saved inception_v3 CNN"""
        print("Creating graph")
        with tf.gfile.FastGFile(os.path.join(model_dir, 'classify_image_graph_def.pb'),'rb') as f:
            graph_def = tf.GraphDef()   # Empty graph definition
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def,name='')
        print("Loaded graph from classify_image_graph_def.pb")

    def classify(self):
        """ Run inference on loaded image using tensorflow


        :return: Classification output from CNN
        """

        self.createGraph()

        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('softmax:0') # Normalized prediction across 1000 labels
            pred = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': self.image_data})
            pred = np.squeeze(pred)
        print(pred)

        # Create lookup node
        node_lookup = NodeLookup()

        top_k = pred.argmax()
        hr = node_lookup.id_to_string(top_k)
        score = pred[top_k]

        answer = "This is a {0} and I'm {1}% sure".format(hr, round(pred[top_k]*100,2))
        self.answerLabel.setText(answer)



class NodeLookup(object):
    """Converts int node ID's to human readable labels for classification"""

    def __init__(self,
                 label_lookup_path = None,
                 uid_lookup_path = None):
        if not label_lookup_path:
            label_lookup_path = os.path.join(model_dir,'imagenet_2012_challenge_label_map_proto.pbtxt')
        if not uid_lookup_path:
            uid_lookup_path = os.path.join(model_dir, 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path,uid_lookup_path)

    def load(self,label_lookup_path,uid_lookup_path):
        """Loads a human readable English name for each softmax node

        Args:
            label_lookup_path: string uid to int node ID
            uid_lookup_path: string uid to human-readable string
        Returns:
            dict from node_ID to human-readable string
        """

        # Check if files exist
        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Load mapping from string UID to h-r string
        # Read in proto as ascii
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
        uid_to_hr = {}
        p = re.compile(r'[n\d]*[ \S,]*') # <-- what is this doing?
        for line in proto_as_ascii_lines:
            parsed_items = p.findall(line)
            uid = parsed_items[0]
            hrs = parsed_items[2]
            uid_to_hr[uid] = hrs

        # Loads mapping from string UID to int node ID
        node_id_to_uid = {}
        proto_as_ascii_lines = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii_lines:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_hr:
                tf.logging.fatal('Failed to locate %s', val)
            name = uid_to_hr[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self,node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]

# main function has standard stuff
if __name__ == "__main__":
    # Define app
    app = QtWidgets.QApplication(sys.argv)
    form = ClassifyThisApp()
    form.show()
    app.exec_()
