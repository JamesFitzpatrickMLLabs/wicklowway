import csv
import json
import requests
import argparse


def read_file(fname):
    """ read the file line by line """

    with open(fname, "r") as fid:
        return fid.readlines()


def check_trkpt(line):
    """ check if the line is a trkpt line """

    if "trkpt" in line:
        return True
    else:
        return False

    
def parse_trkpt(line):
    """ parse the lattitude and longitude """

    latitude = line.split("lat=")[1].split("\"")[1]
    longitude = line.split("lon=")[1].split("\"")[1]
    return float(latitude), float(longitude)


def read_gpx_file(fname):
    """ read the gpx file coordinates """

    lines = read_file(fname)

    coord_dict = {}
    
    for num, line in enumerate(lines):
        if check_trkpt(line):
            latitude, longitude = parse_trkpt(line)
            coord_dict[num] = {
                "latitude": latitude,
                "longitude": longitude
            }
    return coord_dict


def build_payload(coord_dict):
    """ build an open-elevation data payload """

    payload_list = list(coord_dict.values())
    payload_dict = {"locations": payload_list}
    return payload_dict


def build_post_url():
    """ build the post url """

    return "https://api.open-elevation.com/api/v1/lookup"


def build_headers():
    """ build the request headers """

    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        }


def send_request(coord_dict):
    """ send a request to open elevation api """


    payload = json.dumps((build_payload(coord_dict)))
    headers = build_headers()
    post_url = build_post_url()
    return requests.post(post_url, headers=headers, data=payload)


def parse_response(response):
    """ parse the response """

    dictionary = json.loads(response.text)
    return dictionary["results"]


def check_response(response):
    """ check the response type """

    if response.status_code == 200:
        return True
    elif response.status_code == 504:
        print("504 Gateway Timeout! Try again perhaps!")
        print("Quitting! Writing to new file aborted!")
        return False
    elif response.status_code == 502:
        print("502 Bad Gateway! Try again perhaps!")
        print("Quitting! Writing to new file aborted!")
        return False
    else:
        print("{} Error! Try again perhaps!".format(response.status_code))
        print("Quitting! Writing to new file aborted!")
        return False


def write_to_csv(filename, data):
    """ write the data to a csv """

    columns = ["latitude", "longitude", "elevation"]

    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        for line in data:
            writer.writerow(line)


def main(infile, outfile):
    """ do the things! """

    coord_dict = read_gpx_file(infile)
    print("Sending request...")
    print("Waiting for response...")
    response = send_request(coord_dict)
    if not check_response(response):
        return None
    print("Parsing response...")
    data = parse_response(response)
    print("Writing to file")
    write_to_csv(outfile, data)


# gpx_filename = "/home/james/Downloads/wicklowway/wicklowway.gpx"
# out_filename = "/home/james/Downloads/wicklowway/wicklowway.csv" 

# coord_dict = read_gpx_file(gpx_filename)
# response = send_request(coord_dict)
# data = parse_response(response)
# write_to_csv(out_filename, data)


parser = argparse.ArgumentParser(description='Parse GPX trail and spit elevations into a CSV')
parser.add_argument('-i','--infile', help='gpx filepath', required=True)
parser.add_argument('-o','--outfile', help='new csv filepath', required=True)
args = vars(parser.parse_args())

if __name__ is not "__main__":
    main(**args)
    


