###############################################################################################
###############################################################################################
###############################################################################################
How to obtain elevations for gpx tracks using the python script to query the open elevation api
###############################################################################################
###############################################################################################
###############################################################################################
The script can be used through the command line (or using the main function within it). It com-
es with a requirements.txt for required packages. Python version needs to be 3.5+.

There are two arguments that need to be specified, the input gpx file (containing the track se-
gment) and a the path to an output csv file which will contain the latitudes and longitudes in 
the same order they are specified in the gpx, along with the queried elevations. The former is 
the "infile" and the latter is the "outfile". A correctly-formed command will look like:


python3 wicklowway.py --infile <path to gpx> --outfile <path to csv>


Sometimes the api will be overwhelmed with requests and it may timeout. It can be attempted a 
few times and usually this is enough to get it to work. It usually takes between 15-45 seconds 
for a request to be processed. There is no limit on the size of the gpx file at the time of 
writing. 
