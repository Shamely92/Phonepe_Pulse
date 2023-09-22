# Phonepe_Pulse
Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly

Importing the Libraries:

Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

Data extraction:

Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.

    from git.repo.base import Repo
    Repo.clone_from("GitHub Clone URL","Path to get the cloded files")

In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages. And finally converted the dataframe into CSV file and storing in the local drive.

path1 = "Path of the JSON files"
agg_trans_list = os.listdir(path1)

Database insertion:

To insert the datadrame into SQL first I've created a new database and tables using "mysql-connector-python" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

Dashboard creation:

To create insightful dashboard I've used Plotly libraries in Python to create an interactive and visually appealing dashboard by using streamlit and applying the radio button the options on the dashboard show output in the visualization the main components of the dashboard are: a. top ten transaction b. top ten user c. stae wise transaction data d. state wise user data e. india transaction data f. india user data the india map show the state wise total transaction of phonepe and the map comes with zoom option and display the state transaction the main function use to create the map and overall transaction details the total transaction data is use for the see the total transaction count and total transaction amount in state wise.

Data retrieval:

Finally if needed Using the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.
