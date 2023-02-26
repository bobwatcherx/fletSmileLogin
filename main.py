from flet import *
import json
import cv2


# AND LOAD YOU HAARDARSCADE FILE
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

cap = None


def main(page:Page):
	global cap

	nametxt = TextField(label="username")
	passwordtxt = TextField(label="password")
	page.vertical_alignment = "center"



	# CREATE DIALOG FOR YOU NATURAL FACE
	dialog = AlertDialog(
		modal=True,
		title=Text("Warning !!!!",size=30,weight="bold"),
		content=Container(
			padding=10,
			bgcolor="red",
			content=Column([
				Icon(name="face",size=100,color="white"),
				Text("You Can't login because you dont SMILE",
					size=30,weight="bold",color="white"
					)
				],alignment="center")

			)

		)

	# AND NOW CREATE CAMERA FOR DETECT SMILE OR NATURAL
	# FOR YOU FACE 
	# IF NATURAL SHOW ALERT

	def detect_expression(gray_frame,color_frame):
		faces = face_cascade.detectMultiScale(gray_frame,1.3,5)
		
		for(x,y,w,h) in faces: 
			# CREATE RECTANGLE IN YOU FACES
			cv2.rectangle(color_frame,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray_frame[y:y+h,x:x+w]
			roi_color = color_frame[y:y+h,x:x+w]

			# AND DETECT SMILE IN YOU FACE
			smiles = smile_cascade.detectMultiScale(roi_gray,1.8,20)

			# AND IF YOU SMILING THEN PRINT
			if len(smiles) > 0:
				# AND ADD TEXT SMILE IN CAMERA
				cv2.putText(color_frame,"You SMile",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)						
				print("YOu smile !!!")
				dialog.open = False
				page.update()

			else:
				# IF DETECT YOU FACE IS NETRAL
				cv2.putText(color_frame,"Neutral",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)						
				print("YOu netral not smile !!!!")
				page.dialog = dialog
				dialog.open = True
				page.update()
		return color_frame



	def registernow(e):
		data = {}
		data[nametxt.value] = passwordtxt.value

		# AND WRITE USERNAME AND PASSWORD YOU TO FILE JSON
		with open("users.json","w") as file:
			json.dump(data,file)
			print("YOu Account created")

			# AND SHOW SNACJ BAR YOU SUCCESS LOGIN
			page.snack_bar = SnackBar(
				Text("YOu Account created",size=30),
				bgcolor="green"
				)
			page.snack_bar.open = True
			page.update()

			# AND CLEAR INPUT TEXT
			nametxt.value = ""
			passwordtxt.value = ""
			page.update()



	def loginnow(e):
		
		# OPEN FILE json AND FIND USERNAME AND PASSWORD
		# IF FOUND THEN SHOW SUCCESS MESSAGE
		with open("users.json","r") as file:
			data = json.load(file)
		if nametxt.value in data and data[nametxt.value] == passwordtxt.value:
			print("YOu success login")
			# AND SHOW SNACJ BAR YOU SUCCESS LOGIN
			page.snack_bar = SnackBar(
				Text("YOu Login sucecss",size=30),
				bgcolor="blue"
				)
			page.snack_bar.open = True
			page.update()		
		else:
			print("You Failed login wrong username ")
			# AND SHOW SNACJ BAR YOU SUCCESS LOGIN
			page.snack_bar = SnackBar(
				Text("YOu Login FAILED",size=30),
				bgcolor="red"
				)
			page.snack_bar.open = True
			page.update()
			nametxt.value = ""
			passwordtxt.value = ""
			page.update()


	def showregister(e):
		# IF YOU IN REGISTER MODE 
		# THEN CAMERA WILL CLOSE 
		cap.release()
		cv2.destroyAllWindows()
		registercon.visible = True
		logincon.visible = False
		page.update()


	def showlogin(e):
		# AND IF YOU IN LOGIN MODE 
		# THEN OPEN CAMERA AUTOMATYCALY
		# THEN DETECT YOU FACE 
		# IF NOT SMILE 
		# OPEN DIALOG YOU NOT SMILE
		# AND YOU CANT LOGIN
		registercon.visible = False
		logincon.visible = True
		page.update()

		# THEN OPEN CAMERA
		global cap
		cap = cv2.VideoCapture(0)

		# LOOP CAMERA AND IF YOU CLICK Q THEN CLOSE
		while True:
			ret,frame = cap.read()

			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

			# AND SHOW WINDOW WEBCAM
			cv2.imshow("WINDOW YOU FACE",detect_expression(gray,frame))

			# IF CLICK Q THEN CLOSE WINDOW WEBCAM
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break
		cap.release()
		cv2.destroyAllWindows()	




	# CREATE REGISTER CONTAINER
	registercon = Container(
		bgcolor="yellow200",
		padding=10,
		content=Column([
			Text("Register Account",size=30,weight="bold"),
			nametxt,
			passwordtxt,
			ElevatedButton("Register",
				bgcolor="white",color="black",
				on_click=registernow
				),
			Row([
				TextButton("I Have Account",
					on_click=showlogin
					)

				],alignment="center")


			])
		)

	# CREATE LOGIN CONTAINER
	logincon = Container(
		bgcolor="blue200",
		padding=10,
		content=Column([
			Text("Login Account",size=30,weight="bold"),
			nametxt,
			passwordtxt,
			ElevatedButton("Register",
				bgcolor="white",color="black",
				on_click=loginnow
				),
			Row([
				TextButton("I dont have account",
					on_click=showregister
					)

				],alignment="center")


			])
		)


	# BY DEFAULT HIDE LOGINCON
	logincon.visible = False

	page.add(
		registercon,
		logincon 

		)


flet.app(target=main)
