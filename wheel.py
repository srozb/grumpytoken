#!/usr/bin/env python3
#
# THIS LOOKS LIKE SHIT AND THAT'S A FEATURE.
# AS A HIGH-LEVEL INTERFACE TO GRUMPY TOKEN FRAMEWORK, IT IS AN EXAMPLE OF USE.

import argparse
import configparser
from Specific.Wheel import Token
from Specific.Wheel import BSIDcoder
from Helper import Clock, Grum
from binascii import b2a_hex
from sys import platform, exit

desctxt = "Grumpy token v.0.9b (C) 2014: poc@rozbicki.eu"
epitxt = """Default action is to generate token value based on given BSID and
PIN pair, or unencrypted SID value. Notice that sensitive data might be seen in
bash history or process list when provided in command line. If no parameters
given, values stored in config file or sqlite db file will be parsed. If no PIN
provided, you will be asked to input it interactively. For more info read the
manual.

BETA NOTICE: ONLY A FEW OPTIONS ARE IMPLEMENTED FOR NOW."""

parser = argparse.ArgumentParser(epilog=epitxt, description=desctxt)

parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="count")
parser.add_argument("-q", "--quiet", help="be quiet, output only token value",
                    action="store_true")
parser.add_argument("-b", "--bsid",
                    help="pin-encrypted SID value for Wheel token (hexform)")
parser.add_argument("-p", "--pin", help="""PIN code to decrypt given BSID.
Potentially INSECURE. Will ask you to provide PIN interactively if not
explicitly given.""")
parser.add_argument("-s", "--sid", help="""wheel SID value
(unencrypted hex form). Potentially INSECURE.""")
parser.add_argument("-c", "--config", help="""path to config file.
./wheel.conf is default.""")
parser.add_argument("-w", "--write", help="save configuration to ./wheel.conf",
                    action="store_true")
parser.add_argument("-r", "--read", help="read BSID from sqlite db file.")
parser.add_argument("-n", "--next", help="generate N next values for future.",
                    type=int)
parser.add_argument("-l", "--loop", help="don't quit, generate endless.",
                    action="store_true")
parser.add_argument("-d", "--decrypt", help="decrypt BSID with PIN.",
                    action="store_true")
parser.add_argument("-e", "--encrypt", help="encrypt SID with PIN.",
                    action="store_true")
parser.add_argument("-g", "--gui", help="Use GUI instead of stdout",
                    action="store_true")
args = parser.parse_args()

VERBOSE = 0


def log(buf, threshold=0):
    if (VERBOSE >= threshold):
        print(buf)


def haxorview(buf):
    return ' '.join(a + b for a, b in zip(buf[::2], buf[1::2]))


def print_token(sidhex):
    log("SID:\t\t{}".format(haxorview(str(sidhex)[2:])), 1)
    T = Token.Token(sidhex)
    C = Clock.Clock()
    epoch = C.GetEpoch()
    value = T.Generate(epoch)
    log("Binary token:\t{}".format(haxorview(str(T.GetTokenValue())[2:])), 1)
    log("", 1)
    log("Generated at:\t{} (Unix time:{}, Wheel Time:{})".format(
        C.EpochToStr(epoch), epoch, T.GetPointInTime()), 1)
    if (VERBOSE == -1):
        print(value)
    else:
        log("")
        log("Token:\t\t{}".format(value))
    if (not args.write):
        exit(0)


def ask_pin():
    pin = input("Enter PIN: ")
    return pin


def decode_bsid(bsid, pin):
    Decoder = BSIDcoder.BSIDcoder()
    Decoder.Decode(bsid, pin)
    log("", 1)
    log("PINHASH:\t{}".format(haxorview(str(Decoder.GetPINHASH())[2:])), 1)
    sidhex = Decoder.GetSIDHex()
    return sidhex

config = configparser.ConfigParser()
config['Global'] = {}

if (args.verbose):
    VERBOSE += args.verbose
    log("verbosity set to: {}".format(VERBOSE))
if (args.quiet):
    VERBOSE = -1
else:
    if (platform != 'win32'):
        print(Grum.banner)

if (args.sid):
    sidhex = args.sid
    print_token(sidhex)
    config['Global']['sid'] = args.sid
elif (args.bsid):
    config['Global']['bsid'] = args.bsid
    pin = ""
    if (not args.pin):
        pin = ask_pin()
    else:
        pin = args.pin
        config['Global']['pin'] = args.pin
    sidhex = decode_bsid(args.bsid, pin)
    print_token(sidhex)

if (args.write):
    with open('wheel.conf', 'w') as configfile:
        config.write(configfile)
    log("Config file written to ./wheel.conf, farewell!")
    exit(0)
else:
    config = ""  # clear config vars that were populated in case of write.
    if (args.config):
        if (args.config[-5:] == ".conf"):
            try:
                config.read(args.config)
                log("Reading config: {}".format(args.config))
            except:
                ""
        else:
            try:
                config.read(args.config + '/wheel.conf')
                log("Reading config: {}".format(args.config + '/wheel.conf'))
            except:
                ""
    else:
        try:
            config = configparser.ConfigParser()
            config.read('wheel.conf')
            log('Reading config: ./wheel.conf')
        except:
            ""
if ('Global' in config):
    if ('sid' in config['Global']):
        log("SID value taken from config file (INSECURE)")
        print_token(config['Global']['sid'])
    elif ('bsid' in config['Global']):
        pin = ""
        if (not 'pin' in config['Global']):
            pin = ask_pin()
        else:
            pin = config['Global']['pin']
            log("PIN taken from config file (INSECURE)")
        bsid = config['Global']['bsid']
        log("BSID value taken from config file", 1)
        sidhex = decode_bsid(bsid, pin)
        print_token(sidhex)
