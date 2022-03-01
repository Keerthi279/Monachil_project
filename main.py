import csv
import requests
import pprint

# rain data from .
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.html
# used dataset:
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):.25:(42.0)%5D%5B(-123.0):.25:(-113.0)%5D

def get_rain_data():
	csv_file = open("C:/Users/keert/PycharmProjects/Monachil_project/chirps20GlobalPentadP05_997f_a76a_61c6.csv")
	csv_reader = csv.reader(csv_file, delimiter=",")
	line_count = 0
	rain_data = list()
	for row in csv_reader:
		line_count += 1
		if line_count <= 2:
			# print(f'Column names are {", ".join(row)}')
			continue
		elif line_count >= 10e10:
			break
		rain_data.append(row)
	csv_file.close()
	return rain_data

def get_city_lat_long(city=None):
	response = requests.get("https://nominatim.openstreetmap.org/search.php?city=" + city + "&format=jsonv2&namedetails=0&addressdetails=0&limit=1")
	return (response.json()[0]["lat"],response.json()[0]["lon"])



def main(dist_thresh = 0.05, rain_thresh = 8.0):
	val = str(input("Enter city name:[San Jose]") or "San Jose")
	dates = list()
	try:
		c_lat, c_lon = get_city_lat_long(val)
		rain_data = get_rain_data()
		for row in rain_data:
			t, lat, lon, rain = row
			t = t[:10]
			lat_diff = abs(float(lat) - float(c_lat))
			lon_diff = abs(float(lon) - float(c_lon))
			if rain != "NaN":
				if float(rain) >= rain_thresh:
					if lat_diff < dist_thresh:
						if lon_diff < dist_thresh:
							dates.append((t, rain))

		for item in dates:
			print(item)
		print("number of rainy 5-days: " + str(len(dates)))
	except:
		print('City name not found...')


# dates=sorted(list(set(dates)))

if __name__=='__main__':
	main()

