# network_protocol_design
Chat program for the network protocol design course


# The UI

## Setup
To start the UI, use:

use any linux distro as System (pgpy doesn't work on Windows)

`apt-get install python3-pip`

`pip3 install pgpy`

First time running the program to create the pgp key (creates the /keys folder that all nodes are using!)

`python3 main.py -c f@r.ee -n "Friedrich Richter"`

If the keys are already set up the program can be started with

`python3 main.py -s f@r.ee`

For the other nodes (according to neighbors.ini-s):
`python3 main.py -s m@m.ee -p 8000 -N neighbors1.ini`
`python3 main.py -s r@f.ee -p 7000 -N neighbors2.ini`


```
-c is used to create new PGPkeys
-n [name] is required with -c. The name is used to save the key pair.
-s [address] defines the source address (email) for this node.
-p [port] defines the source port for this node
```

Neighbors can be set by editing the `neighbors.ini` file.

Keys are the md5 value of the neighbor, values are corresponding IP addresses

`bcd5f9093d1136ce28850cf1b8bcd2b0=127.0.0.1:7000`

Once the chat is running, the user will be able to use the following commands:

```
 md5 mailaddress - will give you the md5 value of any address
 @mail[:file] - Message with spaces.
 @all[:file] - Message with spaces to everyone.
 help - Display help.
 quit - Exit the program
```

For example, to send a "Hello!" message to "someone@ttu.ee", use:

`@someone@ttu.ee Hello!`

An example of the setup process and the `help` command can be seen here:
![UI](https://github.com/brunoproduit/network_protocol_design/blob/master/new_ui.PNG)


## Code hierarchy
.

├── backgroundprocesses.py      -> Launches a listener thread to collect incoming messages.

├── constants.py                -> Contains the constant values.

├── crypto.py                   -> Does all the crypto stuff, is imported in main.

├── globals.py                  -> Helper file containing global variables.

├── layer3.py                   -> Layer 3 object, encapsulates l4.

├── layer4.py                   -> Layer 4 object, encapsulates l5.

├── layer5.py                   -> Layer 5 object, encapsulates raw data or file.

├── LICENSE                     -> License.

├── main.py                     -> Main entry of the program.

├── modules_install.txt         -> Can be used for pip.

├── neighbors_template.ini      -> Template for the .ini file used for neighbors.

├── packetEngine.py             -> Provides classes to split and reconstruct data upon send/receive.

├── README.md                   -> This readme.

├── routing.py                  -> Router object to be used for the routing process (bellman ford).

├── routing_table.py            -> Data storage and serialization class for the routing table.

└── utils.py                    -> Some utilities for all files.


