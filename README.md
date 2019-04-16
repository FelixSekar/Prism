A flask web app to plausibly colorize grayscale face portraits using deep learning.

Steps for execution: 

Note: Make sure you have Python 2.7 or 3.5 installed on your computer
Follow the below steps to run the app.
1)	Clone this repository

		git clone https://github.com/FelixSekar/Prism.git
2)	Create a folder called "models" inside the repository.
3)	Download the model file named “group.h5” from [here](https://drive.google.com/open?id=1XorKfx_YLTuFnve8FdujqV-bgtL6AQzS) and place it inside the newly created “models” folder.
4)	Install all the required python packages using the following command :

		pip install -r requirements.txt
5)	After successful installation of all the necessary packages run the “app.py” file using the below command:

		python app.py
6)	Wait for a while as the app loads required packages and model used for prediction. When you get the message “Model loaded. Start serving…” open your web browser and type “localhost:5001” in the address bar. The app is ready to use. 
 

Credits : 

https://github.com/mtobeiyf/keras-flask-deploy-webapp

https://github.com/emilwallner/Coloring-greyscale-images
