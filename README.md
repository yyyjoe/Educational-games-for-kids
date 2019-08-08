# Educational Math Games for Kids

## Introduction
The preferred way of counting and basic arithmetic of young child between the ages of 3-6 is with their fingers. It is a primitive but proven way for young children to establish their fundamentals in math. There is a very limited selection of tools that facilitate learning by way of finger counting, and none of them are online.

Our solution is to use finger recognition to create a web application that will query and guide a young user in using their fingers to solve basic arithmetic problems. Our application is designed to have several modes that interact with the user to create a unique and streamlined learning experience. For example, the application asks the user what 2+3 is, and the user is expected to use a combination of fingers from both of their hands to come up with a correct answer.

## Models
For finger recognition model, we use [**CNN-HowManyFingers**](https://github.com/jaredvasquez/CNN-HowManyFingers) (mt_video_feed.py) to predict the number of fingers. When kids correctly answer the question, we add a feedback on the user interface using [**Creating GIFs with OpenCV**](https://github.com/vaibhavshukla182/Creating-GIFs-with-OpenCV) (feed_back.py).

Key Requirements: Python 3+, Keras 2+, TensorFlow 1+, OpenCV 2+.


# Demo
![](https://media.giphy.com/media/f3GURJolX4cbtUzf1G/giphy.gif)

# How to run
Clone the repository
```bash
git clone https://github.com/yyyjoe/Educational-games-for-kids.git
```

Install required packages:
```bash
pip install -r requirements.txt
```

Download finger and face detection models:
```python
python download.py
```

Run the server:
```python
python server.py
```

Open web browser and head to [**http://localhost:5000/**](http://localhost:5000/) to see your local app running.





