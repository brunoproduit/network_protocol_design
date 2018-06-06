# network_protocol_design
Chat program for the network protocol design course


# The UI

## Setup
To start the UI, use:

use any linux distro as System (pgpy doesn't work on Windows)

`apt-get install python3-pip`

`pip3 install pgpy`

`python3 main.py`


The user will be prompted with the setup dialog:

First, the user will be asked to provide the location of the master key used to sign PGP keys:

`Insert path for the master_key: 'master_key_path'`


Next, the user will be asked for the path to their own key:

`Insert path for the own_node_key: 'your_key_path'`

In order to set neighbors edit the file neighbors.ini
Keys are the md5 value of the neighbor, values are corresponding IP addresses

67c91edbbb46ce9f7bca0b68feece836=127.0.0.1

```
 md5 mailaddress - will give you the md5 value of an address
 @mail[:file] - Message with spaces.
 @all[:file] - Message with spaces to everyone.
 help - Display help.
 quit - Exit the program
```


An example of the setup process and the `help` command can be seen here:
![UI](https://github.com/brunoproduit/network_protocol_design/blob/master/ui.PNG)

If the user has previously done the setup process, they can choose to overwrite the settings defined in the previous setup:
![overwrite](https://github.com/brunoproduit/network_protocol_design/blob/master/overwrite.PNG)
