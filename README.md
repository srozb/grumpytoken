# grumpytoken
CERB token generator

##DISCLAIMER
This software is intended to be educational proof of concept. You may not use it to conduct illegal activities. Be sure you are not violating local law, using it.

Feel free to fork sources.

##Requirements

Python 3.x (tested on 3.3)
PyCrypto support
PyCrypto Windows binnaries: here

##Quick start

You need your BSID value. It can be extracted from SQLITE database on your android device, as long as you have Cerb Token installed and configured. Ask google how to do it.

BSID is an encrypted representation of SID value (shared secret between you and entity you want to authenticate with). BSID might be turned into SID by decrypting it with your PIN code.

BSID is no longer needed when you obtain correct SID value, however you might want not to store SID value on a computer in unencrypted form. It's up to you if you are willing to take the risk. Alternatively you might want to store BSID and PIN simultaneously, which is equally risky.

Anyway here is how you might invoke wheel.py: * python ./wheel.py -b BSID <- will ask you for your PIN CODE every time you run it. This is most secure and recommended way to use it. * python ./wheel.py -b BSID -p PINCODE <- will compute your token immediately with no interaction with user. Might leave sensitive data in bash history and process list. * python ./wheel.py -s SID <- as above. * python ./wheel.py (with no parameters) will try to read values from you wheel.conf file.

You can create wheel.conf file by modifying sample file or run script with -s or -b and -p parameters and -w switch (python ./wheel.py -b BSID -p PINCODE -w).

-v and -q switches might be used to increase or decrease logging to console out.

Only a few parameters are implemented at the moment. Don't expect me to change it. Wheel.py is a mess and has been created only to provide stright-forward interface (wrapper) to lower-level framework routines.

You are welcome to write your own application using supplied framework. Wheel.py wrapper should not be used in the production environment. I am aware of a several bugs in it and have no time to rewrite it. Peeking into the source of this file might get you a heart attack. You've been warned. On the other hand I did my best to keep the code quality of the rest good enough to make it usable.

##Why?

Grumpy token is inspired by Wheel, Cerb token manufacturer who claims it is very secure. It uses the strongest cryptographic algorithms with tiny entropy, what makes me wonder about real security of this solution. My concerns have been reported to Wheel.

"one ought to design systems under the assumption that the enemy will immediately gain full familiarity with them" - Claude Shannon
