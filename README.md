# trashsegregator
This repository contains code for classifying various types of trash into different categories using CNN with the dataset containing very less images.

The idea for this project is based on [this](http://cs229.stanford.edu/proj2016/poster/ThungYang-ClassificationOfTrashForRecyclabilityStatus-poster.pdf) paper.

[Here's](https://github.com/garythung/trashnet) the link to the original repository. You can download the original dataset from there.

[Here's](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html) the tutorial which was followed to write this code.
Requirements for this code:
1)Tensorflow
2)Keras
3)OpenCv
4)Numpy

Around 400 images for each class were used for training and 100 images for each class were used for validation. The validation accuracy achieved was roughly 85%-90%. 

In order to reduce time for training, CUDA was used. The GPU used was Nvidia GTX 1050 Ti.
