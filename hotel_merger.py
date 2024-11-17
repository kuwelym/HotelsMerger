import argparse
from hotels_service import fetch_hotels

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("hotel_ids", type = str, help = "Comma-separated list of Hotel IDs or 'none'")
    parser.add_argument("destination_ids", type = str, help = "Comma-separated list of Destination IDs or 'none'")

    # Parse the arguments
    args = parser.parse_args()

    hotel_ids = [] if args.hotel_ids.lower() == "none" else args.hotel_ids.split(",")
    destination_ids = [] if args.destination_ids.lower() == "none" else [int(i) for i in args.destination_ids.split(",")]

    result = fetch_hotels(hotel_ids, destination_ids)
    print(result)

if __name__ == "__main__":
    main()