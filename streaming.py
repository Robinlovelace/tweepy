from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import configparser # for reading the configuration file
import os
import sys
import json # For converting string into json object
import argparse # For parsing command-line arguments
import time # For adding a timestamp to files
import gzip # For compressing files
import traceback # For printing the traceback when errors occur

# add your details
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

# Global variables
credentials_file = "./credentials.ini" # Assume in local directory
TWEETS_PER_FILE = 1000000 # Number of tweets to store before creating a new file

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

class FileWriterListener(StreamListener):
    """
    A listener handles tweets are the received from the stream, writing them to a file
    """

    def __init__(self):
        self.json_filename = ""  # Name of the file that tweets are being written to
        self.csv_filename = ""   # (will be tXX where XX is the timestamp in seconds)
        self.counter = 0 # Count the number of tweets

    def on_data(self, raw_data):

        # See if a new file needs to be created for these tweets
        if self.counter % TWEETS_PER_FILE == 0:

            old_filename = self.json_filename

            tm = str(int(time.time() * 1000) ) # Append timestamp to files
            self.json_filename = "data/t"+tm+".json"
            self.csv_filename = "data/t"+tm+".csv"

            print "Writing to files:", self.json_filename, self.csv_filename

            # Compress the old filename (only to json, not csv) (and not when the script starts)
            if self.counter > 0:
                print "Compressing json file and creating new one (counter={c})".format(c=self.counter)
                # ('with' is just a fancy way of openning and closing files)
                #with open( old_filename, 'rb'), gzip.open(old_filename+".gz", 'wb') as ( old_file, zipfile) :
                #    zipfile.writelines(oldfile)
                oldfile = open( old_filename, 'rb')
                zipfile = gzip.open(old_filename+".gz", 'wb')
                zipfile.writelines(oldfile)
                oldfile.close()
                zipfile.close()
                os.remove(old_filename)




        # Call the parent (StreamReader) function which does some error checking, returning False if
        # this isn't a tweet.
        # if super(StreamListener, self).on_data(raw_data) == False:
        #    print "This doesn't look like a tweet"
        #    return False

        # 1 - use json library to create a python dictionary object from the raw data (a 
        # json-formatter string). This can be then be interrogated to find info. about the tweet.
        try:
            data = json.loads(raw_data)
        except ValueError as e:
            print "****\nCaught a ValueError:",str(e),".\nThe raw_data is:**\n\t",raw_data,"**"
            print "The trackback is:"
            print traceback.format_exc()
            print "****"


        # 2 - get the id (e.g. data['id'] )

        try:
            tweetid = str(data['id'])
            print "read tweet",tweetid
            # 3 - write to a file (with filename of tweet id)
            f = open(self.json_filename,'a')
            try:
                f.write(raw_data) # 
            finally:
                f.close()

            # 4 - TODO extract ueful info and write to a csv file

            # P.S. this is a nicer way to write to files using 'with' syntax:
            #with open('data/'+tweetid,'w') as f:
            #    f.write(str(data))

        except KeyError as e:
            print "Caught error receiving tweet: ", str(e) # Show what the error was
            print "Looks like we have received something that isn't a tweet. Will write it to a different file." 

            # Call the file 'error<time>.json'
            f = open("error"+str(int(time.time() * 1000) )+".json",'w')
            try:
                f.write(raw_data) # 
            finally:
                f.close()

        self.counter += 1

        return True

    def on_error(self, status):
        print "ERROR: ", str(status)



def check_locations(locs):
    """Checks that the locations input from the command line look OK. Exit if not."""
    # argparse will have turned the arguments into a 4-item list
    if locs[0] > locs[2]:
        print "Error with locations ({locs}), min x ({minx}) is greater than max x ({maxx})".format( \
                locs=locs, minx=locs[0], maxx=locs[2])
        sys.exit(1)
    if locs[1] > locs[3]:
        print "Error with locations ({locs}), min y ({miny}) is greater than max y ({maxy})".format( \
                locs=locs, miny=locs[1], maxy=locs[3])
        sys.exit(1)


if __name__ == '__main__':

    # Parse command-line options
    parser = argparse.ArgumentParser()
#    (description='Usage %prog -l <locations> [-c <credentials_file]')
    parser.add_argument('-l', nargs=4, dest='locs', type=float, required=True, \
            help='specify min/max coordinates of bounding box (minx miny maxx maxy)')
    parser.add_argument('-c', nargs=1, dest='cred', type=str, required=False, \
            help='specify location of credentials file', default=credentials_file)
    args = parser.parse_args()

    if not os.path.isfile(args.cred):
        print "Error",args.cred,"doesn't look like a file. See the README for details."
        sys.exit(1)
    credentials_file = args.cred

    locations = args.locs
    check_locations(locations)

    # Read the twitter authentication stuff from the configuration file (see README for details).
    try:
        config = configparser.ConfigParser()
        config.read(credentials_file)

        consumer_key=str(config['CREDENTIALS']['consumer_key'])
        consumer_secret=str(config['CREDENTIALS']['consumer_secret'])
        access_token=str(config['CREDENTIALS']['access_token'])
        access_token_secret=str(config['CREDENTIALS']['access_token_secret'])

    except:
        print "Error reading credentials from", credentials_file

    print "Starting listener on locations:",locations

    #l = StdOutListener()
    l = FileWriterListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    try: 
        stream = Stream(auth, l)
        stream.filter(locations=locations)
    finally:
        stream.disconnect()
