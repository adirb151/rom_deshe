# Meshi Project - Maintenance Guide
## Meshi-Side
### Prerequisites
- For you to be able to make changes in the backend of the server, which is located on a remote server (*meshi-srv1.cs.bgu.ac.il*) in the BGU network, you must be connected to the BGU-VPN.
  Follow [this guide](https://in.bgu.ac.il/computing/DocLib/Pages/vpn-service/%d7%97%d7%99%d7%91%d7%95%d7%a8%20VPN%20%d7%91%d7%9e%d7%a2%d7%a8%d7%9b%d7%aa%20%d7%94%d7%a4%d7%a2%d7%9c%d7%94%20windows10%20-%d7%99%d7%95%d7%a0%d7%99%202022.pdf) to obtain a security token from the university and to install the required application to connect to the VPN.
- Since the server is remote, to view and edit it, we must connect to it via SSH. Therefore, We recommend you download [MobaXterm](https://mobaxterm.mobatek.net/download.html) in order to get a simple and comfortable representation of the remote working area (which consists of a file system and a cmd interface).
> Note: to connect to the remote meshi server, you'll need a user in the BGU network. To obtain one, contact the administration here: *cs.help@post.bgu.ac.il*.
### Connecting to the Django Working Area
- Connect to the BGU-VPN.
- Inside MobaXterm (or a terminal of your choice), start a new session with the remote host *meshi-srv1.cs.bgu.ac.il*.
- Log-in as your BGU user.
- To navigate to the project directory, run `cd /home/cluster/orelhaz/bin/rom_deshe`.

### Running the Django Server
- From within the *rom_deshe* folder, you first need to activate the virtual environment that contains the required libraries and extensions that make the server run.
  To do so, run `source ./myenv/bin/activate.csh`.
- Once inside the running environment, you may run the Django server with the following commands:
  ```
  cd ./djangonautic
  python3 manage.py runserver
  ```
  If the action was succesfull, you will see a message stating that the server is listening on a connection.
- Now you may enter http://meshi-srv1.cs.bgu.ac.il:7070 in a browser of your choice to view the website.
> Note: in order to view the website from a browser, the computer *MUST* be connected to the BGU-VPN.
### Change the Query Model
From within the [models.py](djangonautic/queries/models.py) file, you may add/delete/edit fields and functions from the Query class.

After you've made your changes, you'll need to migrate them to the DjangoDB. To do so, you must type the following commands into the cmd from the *rom_deshe* folder:
```
cd ./djangonautic/
python3 manage.py makemigrations
python3 manage.py migrate
```
> Note: some changes might affect the [db_utils.py](db_utils.py) file, further information about this file is shown bellow.
### Modifying the Website
In order to modify the website (such as add a new button, edit a page etc.), do so in the relevant html files.

- Files pertaining to the about page, home page and the base layout of the site are located [here](djangonautic/templates).
- Files pertating to the query pages (list and details pages) are located [here](djangonautic/queries/templates/queries).
- Files pertaining to the styling of the website (CSS & Images) are located [here](djangonautic/assets).

### Modifying the _db_utils.py_ File
The [db_utils.py](db_utils.py) file is a python script that is run to makes changes to the DjangoDB.
This file is responsible for receiving real-time information regarding the queries and updating the relevent changes in the DjangoDB.

In this file you will find functionality regarding database connection and disconnection, additions/updates to the database and retrieving info from the database.

> Note: since this file works with sensitive data regarding the queries, so changes you make to the [models.py](djangonautic/queries/models.py) file might affect its functionality. It is advised to make use of the file's documentation and make sure it is changed accordingly.
