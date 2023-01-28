=======
Facebook Group Messanger
=======



Simple python script, based on selenium,
that automate the process of sending messages to facebook group members.


Features
--------

* Sends messages to any group you are in, to all members
* Finds members name and inserts the first name in your message
* Doesnt sends message if you sent message to member 30 min before that
* Sends different messages to someone that you never engaged with before

How to Run the script
--------

To use this script you simple need to insert your email, password and group_id values as args.

To create a new session, simply insert a new number at the session_num object (so the script will take in consideration
all the changes that were made from the last run).

Edit your message at the message and first_message objects.

Run the script with Python3

``
python main.py
``

Credits
-------

Roma Sanchuk

** This is still a work in progress, more features will be added in the future.
