#**Behavioral Cloning** 

##Writeup Template

###You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[TryLenet]: ./Try_Lenet.png 
[Lenet20]: ./Lenet_E20_LR001_B50_NoAug.png 
[Lenet20Aug]: ./Lenet_E20_LR001_B50.png 
[LenetAdam]: ./Lenet_Adam.png 

[Nvidia]: ./Nvidia_E50_D35.png 
[NvidiaFinal]: ./Nvidia_Final.png 
[TheCorner]: ./The_Corner.png
[Model]:./model.png

## Rubric Points
###Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
###Files Submitted & Code Quality

####1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup.md  summarizing the results
* video.mp4 

####2. Submission includes functional code
####3. Submission code is usable and readable
The code is in model.py which contains preprocessing data,constructing model,train

###Model Architecture and Training Strategy

####1. Appropriate training data

I use following approach to get appropriate training data:
1. use track 1 to gather data,keep the car in the middle
2. extract 10 frame every second
3. add mirror image for every raw image
4. use left and right  camera image to teach the car to switch to middle

####2. Generate data
Because image size is large 160x320,my computer can not load all data ,so I used generator on train ,validation set,
####3. Final Model Architecture
The all weighted layer are:

|Layer|Des|
|---|---|
|Conv| filter=24,kernel=5x5,stride=1x1|
|Conv| filter=36,kernel=5x5,stride=1x1|
|Conv| filter=48,kernel=5x5,stride=1x1|
|Conv| filter=64,kernel=3x3,stride=1x1|
|Conv| filter=64,kernel=3x3,stride=1x1|
|Full Connect| unit = 400|
|Full Connect| unit = 50|
|Full Connect| unit = 10|
|Full Connect| unit = 1|

Here is a visualization of the architecture 
![][Model]

####4. Solution Design Approach

It is a computer vision problem,though is regression,but i gusses the Lenet is useful. So i build a Lenet model,and do a quick test, optimizer=sgd,learning rate = 0.001batch=50,epoch=5.I got this result:
![][Try Lenet]
Now i know the model is approprite,so i try  20 epochs and got this
![][Lenet20]
Then i add mirror image ,left right camera image to prevent overfit
![][Lenet20Aug]
But the final error is also high.so i try adam optimizerthe result looks better than sgd optimizer,but the overfit appears again. the train error is 0.4,but validation error is about 1.0
![][LenetAdam]
In order to prevent overfit ,i decide to complex my model ,and add dropout layer.I accept Nvidia model,dropout = 0.35 on full connecting layer.And i got this.The result is improved little.
![][Nvidia]
I tried this model on the simulator,but the car run out of road at a corner,I try to tune the learning rate,dropout,kenel of conv layer,but it did not work.
![][TheCorner]
Finally,i think should train the car through the corner agian,so i just collect some data abount the car through corner.And eventually ,after training only 10 epoch,my car can finish track 1,even the car speed is 30km/h.The final error is this:
![][NvidiaFinal]

####5. Attempts to reduce overfitting in the model
1. data is splited into train,validation and test set
1. Every Full connected layer is followed a dropout layer to reduce overfit,final keep_prob = 0.65
2. add a rotated image for every center image


####6. Model parameter tuning
* Switch SGD to Adam optimizer
* select keep_prob = 0.65
* compare learning rate of 0.001,0.0005,0.0001,finaly select 0.0005

###Conclusion
For me,The difficult part is finish the corner, i use collec more data to overcome it. It shows the importance of train data,they can decide the model's performance directly.
Maybe if i collect right data,the  Lenet Model can also achieve the goal.

