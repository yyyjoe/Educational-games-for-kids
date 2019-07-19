
from flask import Flask, render_template, Response, session, redirect,url_for, request, json
from mt_video_feed import VideoFeed
import time
from keras.models import load_model
import tensorflow as tf
from questions import Generator
from feed_back import positive_feedback
app = Flask(__name__)

model = load_model('assets/mobilenet.h5')
model._make_predict_function()
graph = tf.get_default_graph()
ans = -1
score = 0
vs = VideoFeed(model)

converter = {}
converter["NONE"] = 0
converter["ONE"] = 1
converter["TWO"] = 2
converter["THREE"] = 3
converter["FOUR"] = 4
converter["FIVE"] = 5
global counter
counter = 0
global CORRECT
CORRECT = 0


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/video_feed')
def video_feed():
	global graph
	global p1, p2
	
	def generate(camera):
		global CORRECT
		global ans
		global counter
		while True:
			img,frame = camera.get_frame()

			p1, p2 = camera.get_prediction()
			if p1 != "" and p2 != "":
				op1 = converter[p1]
				op2 = converter[p2] 
				user_ans = op1 + op2
			else:
				user_ans = -2

			if user_ans == ans:
				counter+=1
				CORRECT = 1

			if (CORRECT and counter>15):
				pf = positive_feedback()
				step = pf.detect_eyes(img)
				for(i,y) in enumerate(step):
					pf_frame = pf.gif_generator(i,y,img)
					yield (b'--frame\r\n'
							b'Content-Type: image/jpeg\r\n\r\n' + pf_frame + b'\r\n\r\n')
				time.sleep(3)
				CORRECT = 0
				counter = 0
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

	with graph.as_default():
		return app.response_class(generate(vs),
								  mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/game_selector')
def game_selector():
	return render_template('game_selector.html')

@app.route('/finger_game')
def finger_game():
	return render_template('finger_game.html')

@app.route('/finger_add', methods=['GET', 'POST'])
def finger_add():
	global ans
	num1, num2, a = Generator().questions_generator(1)
	ans =a
	return render_template('finger_operation.html', num1 = num1, num2 = num2, mode = 1 )

@app.route('/finger_sub', methods=['GET', 'POST'])
def finger_sub():
	global ans
	num1, num2, a = Generator().questions_generator(2)
	ans =a
	return render_template('finger_operation.html', num1 = num1, num2 = num2, mode = 2 )

@app.route('/finger_mul', methods=['GET', 'POST'])
def finger_mul():
	global ans
	num1, num2, a = Generator().questions_generator(3)
	ans =a
	return render_template('finger_operation.html', num1 = num1, num2 = num2, mode = 3 )

@app.route('/finger_div', methods=['GET', 'POST'])
def finger_div():
	global ans
	num1, num2, a = Generator().questions_generator(4)
	ans =a
	return render_template('finger_operation.html', num1 = num1,num2 = num2,mode = 4 )

@app.route('/check')
def check():
	global ans 
	global score
	global converter
	p1, p2 = vs.get_prediction()
	if p1 != "" and p2 != "":
		op1 = converter[p1]
		op2 = converter[p2] 
		user_ans = op1 + op2
	else:
		user_ans = -2

	if user_ans == ans:
		global CORRECT
		CORRECT = 1

	return render_template('finger_score.html', score = score)




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
