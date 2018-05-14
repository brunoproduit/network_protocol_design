# network_protocol_design
Chat program for the network protocol design course


# The UI

## Setup
To start the UI, use:
`python3 interface.py`

The user will be prompted with the setup dialog:

First, the user will be asked to provide the location of the master key used to sign PGP keys:
`Insert path for the master_key: 'master_key_path'`

Next, the user will be asked for the path to their own key:
`Insert path for the own_node_key: 'your_key_path'`

After these two steps the user can start using the chat by using the following commands:
```
# Commands ------------------------------------------------------------------------
ADD_NEIGHBOR_COMMAND = "+"
REMOVE_NEIGHBOR_COMMAND = "-"
BROADCAST_MAIL = "@all"
DETAIL_SEPERATOR = ":"
SEND_FILE_COMMAND = "file"
SEND_MESSAGE_COMMAND = "message"
QUIT_COMMAND = "quit"
HELP_COMMAND = "help"
HELP_TEXT = "The follwoing commands are valid:\n @mail[:file] Message with spaces.\n @all[:file] Message with spaces to everyone.\n help Display help. \n quit Exit the program"
UNKNOWN_COMMAND = "unknown"
INVALID_COMMAND = "invalid"
```

An example of the setup process and the `help` command can be seen here:
![UI setup](network_protocol_design/ui.PNG)

If the user has previously done the setup process, they can choose to overwrite the settings defined in the previous setup:
![settings_overwrite](network_protocol_design/overwrite.PNG)

