import os
import pathlib
import argparse
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

if len(voices) <1:
    print('Error: no TTS voices are available')
    quit()

def parse_args():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Text-to-Speech Converter')
    parser.add_argument('--voices', dest='voices', action='store_true', help='List available TTS Voices')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('--voice', '-v', type=int, help='Voice ID to use.  Specify --voices to see a list of available voices.  If not provided the "%s" voice will be used' % voices[0].name, default=0)
    group.add_argument('--text', '-t', dest='text', help='Text to read')
    group.add_argument('--file', '-f', dest='file', help='Filename containing text to read')
    parser.add_argument('--out', '-o', dest='out', help='MP3 filename to save spoken text to')
    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Display verbose output")
    parser.add_argument('--rate', '-r', type=int, dest='rate', help="Change the voice rate")
    parser.add_argument('--volume', '-vol', type=int, dest='volume', help="Change the voice volume")

    args = parser.parse_args()
    return args

def get_outfile(file=None):
    if file is None:
        return None
    elif file.endswith('.mp3'):
        return file
    elif file is not None:
        return '%s.mp3' % file

def do_verbose(message):
    if verbose:
        print(message)

args    = parse_args()
verbose = args.verbose

if args.voices:
    print('Available Text-to-Speech voices:')
    for voice_num in range(len(voices)):
        print('\tID: %s - %s' % (voice_num, voices[voice_num].name))
    quit()

if args.rate:
    engine.setProperty('rate', args.rate)

if args.volume:
    engine.setProperty('volume', args.volume)

config = {
    "voice": voices[args.voice].id,
    "text": "",
    "out": get_outfile(args.out),
    "rate": engine.getProperty('rate'),
    "volume": engine.getProperty('volume'),
}

if args.file:
    if not os.path.isfile(args.file):
        print('File does not exist: %s' % args.file)
        quit()
    else:
        file = open(args.file)
        for line in file.readlines():
            line = line.replace("\n", "  ")
            config['text'] = config['text'] + line
        file.close()
elif args.text:
    config['text'] = args.text

do_verbose('TTS configuration=%s' % config)

engine.setProperty('voice', config['voice'])
if config['out']:
    do_verbose('Writing spoken text to %s' % config['out'])
    engine.save_to_file(config['text'], config['out'])
else:
    do_verbose('Speaking text...')
    engine.say(config['text'])
engine.runAndWait()