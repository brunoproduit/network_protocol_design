# network_protocol_design
Chat program for the network protocol design course


# The UI

## Setup
To start the UI, use:

`pip install pgpy`

`python3 interface.py`


The user will be prompted with the setup dialog:

First, the user will be asked to provide the location of the master key used to sign PGP keys:

`Insert path for the master_key: 'master_key_path'`


Next, the user will be asked for the path to their own key:

`Insert path for the own_node_key: 'your_key_path'`

Next the User will be asked for its neighbors:

`Add your neighbors: IP:'neighbor IP', mail:'neighbor mail'`

After these three steps the user can start using the chat by using the following commands:

```
 @mail[:file] - Message with spaces.
 @all[:file] - Message with spaces to everyone.
 help - Display help.
 quit - Exit the program
```


An example of the setup process and the `help` command can be seen here:
![UI](https://github.com/brunoproduit/network_protocol_design/blob/master/ui.PNG)

If the user has previously done the setup process, they can choose to overwrite the settings defined in the previous setup:
![overwrite](https://github.com/brunoproduit/network_protocol_design/blob/master/overwrite.PNG)
