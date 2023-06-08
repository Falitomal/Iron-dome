#!/bin/bash
set -e
if [ ! -d "/usr/src/iron/data" ]; then
    mkdir /usr/src/iron/data
fi
sh -c "echo > /usr/src/iron/data/tst lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum"

sleep 10
python3 irondome.py /usr/src/iron/data/

sleep 3
mv /usr/src/iron/data/tst /usr/src/iron/data/test.txt
sleep 1
sh -c " echo >> ha '  
                                                                                                                                                                                                                                                                                                                                                                                                                        '"
service ssh start
tail -f /dev/null