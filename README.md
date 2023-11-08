===================================================================
<p>
    To log in you can use:<br>
<br>
        username: Leraar (Uppercase and lowercase are accapted)<br>
        password: leraar (Needs to be lowercase)<br>
<br>
    Or to log in as admin you can use:<br>
<br>
        username: Admin (Uppercase and lowercase are accepted)<br>
        password: admin (Needs to be lowercase)
</p>

===================================================================

<h1>Stationzuil Application<h1>
    
<h2>Introduction<h2>
<p>
The Stationzuil application is a Python GUI program built using the Tkinter library. It allows users to log in and post messages related to different train stations. There is also an administrative panel for moderators to review and manage the posted messages. This README file provides an overview of the code structure and functionality.
</p>
<h3>Code Structure</h3>
<p>
Import Statements
The code begins with import statements that bring in necessary libraries and modules, including Tkinter for the GUI, psycopg2 for database connectivity, and datetime for working with dates and times.
</p>
<h3>Window Initialization</h3>
<p>
The Tkinter application is initialized with a window configuration of size 1280x720 and given the title "Stationzuil."
Variables
Various global variables are defined, such as optionMenuText, database connection details, and placeholder functions.
</p>
<h3>Base Functions</h3>
<p>
PlaceholderEvent class and some base functions are defined. These functions handle data manipulation, making widgets visible or invisible, and switching between different frames or screens.
</p>
<h3>Data Manipulation</h3>
<p>
The data_manipulation function connects to a PostgreSQL database, executes SQL queries, and retrieves or modifies data based on the operation parameter. It handles operations like fetching station records, user records, inserting messages, and retrieving approved messages.
</p>
<h3>Widget Implementation</h3>
<p>
The code defines the structure and layout of the GUI. It includes login screens, the main user interface, and the admin interface. Key elements include labels, entry fields, buttons, and message display areas.
</p>
<3>Functionality</h3>
<p>
The code contains functions for user login, sending messages, checking message contents, and displaying messages. There are separate functions for reading and writing messages to CSV files. The admin panel allows moderators to review and delete messages.
</p>
<h3>Window Loop</h3>
<p>
The application enters the main event loop with root.mainloop(), allowing user interactions and GUI updates.
</p>
<h3>How to Use</h3>
<p>
Run the code, and the initial login screen will appear.
Enter valid login credentials (username and password) to access the main interface.
In the main interface, you can select a station, enter a name, and type a message before clicking "Enter" to send a message.
The admin panel allows moderators to review messages, delete them, and send pending messages to the database.
</p>
<h3>Dependencies</h3>
<p>
Tkinter: The code uses the Tkinter library for building the graphical user interface.
psycopg2: This library is required to connect to a PostgreSQL database.
Python 3: The code is written in Python 3.11.6 (64-bit).
</p>
<h3>Database</h3>
<p>
The code is designed to connect to a PostgreSQL database to store and manage messages and user data. Ensure that the database is set up and that the database connection details in the code match your configuration. The database configuration is in the database template file.
</p>
<h4>Note</h4>
<p>
This code structure assumes that you have a PostgreSQL database set up and running. Make sure to update the database connection details and schema according to your setup.
</p>
<h4>Author</h4>
<p>
[MrJackRegen]
</p>
<h4>Contact</h4>
<p>
For questions or support, please contact [fake.email@gmail.com] (Do not contact me!).
</p>
<h3>Acknowledgments</h3>
<p>
Big thank you to the creators of the tkinter library and psycopg2 library.
</p>