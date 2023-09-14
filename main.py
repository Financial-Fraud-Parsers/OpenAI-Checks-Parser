import os
import sys
import csv
import time
import json
from utils import get_files, calculate_price, calculate_google_maps_price, parse, get_coordinates, extract_file_date
from colr import Colr as C
import colorlog

# Logging
handler = colorlog.StreamHandler()
logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
handler.setFormatter(colorlog.ColoredFormatter(
    '%(red)s%(levelname)s:%(name)s:%(message)s'))

# Main


def main(inputs, out):
    with open(inputs, "r", encoding='utf-8') as f:
        files = [json.loads(line.strip()) for line in f if line.strip()]

    cost_of_operation = calculate_google_maps_price(len(files))

    print("Cost of operation:", C(
        f"${cost_of_operation}", fore="red", style="bright"))

    print("Do you want to continue?", C("(y/n)", fore="yellow"))

    if input() != "y":
        print("Exiting...")
        sys.exit(1)

    parsed = []
    for file in files:
        try:
            filename = file["filename"].split(".txt")[0]
            output = file["content"]
            address = ""
            if output["victim_street_address"]:
                address = get_coordinates(output["victim_street_address"])

            output["victim_street_address"] = address

            parsed.append({"filename": filename, "content": output})

        except Exception as e:
            logger.warning(e)
            logger.warning(f"Error parsing {file['filename']}")
            logger.info("Traceback:")
            raise e

    with open(out, "w", encoding='utf-8') as f:
        writer = csv.writer(f)

        header = ["Picture ID", "Picture Date", "Bank Name", "Bank Address", "Victim Name", "Victim Street Address", "Victim Zip Code",
                  "Victim City", "Victim State", "Victim Latitude", "Victim Longitude", "Business Name", "Business Address", "Check Date", "Check Amount"]

        writer.writerow(header)

        for item in parsed:
            address = {"latitude": "", "longitude": "",
                       "street": "", "zip": "", "city": "", "state": ""}

            if item["content"]["victim_street_address"]:
                address["latitude"] = item["content"]["victim_street_address"][0] if len(
                    item["content"]["victim_street_address"]) > 0 else ""
                address["longitude"] = item["content"]["victim_street_address"][1] if len(
                    item["content"]["victim_street_address"]) > 1 else ""
                address["street"] = item["content"]["victim_street_address"][2].get(
                    "address", "") if len(item["content"]["victim_street_address"]) > 2 else ""
                address["zip"] = item["content"]["victim_street_address"][2].get(
                    "zipcode", "") if len(item["content"]["victim_street_address"]) > 2 else ""
                address["city"] = item["content"]["victim_street_address"][2].get(
                    "city", "") if len(item["content"]["victim_street_address"]) > 2 else ""
                address["state"] = item["content"]["victim_street_address"][2].get(
                    "state", "") if len(item["content"]["victim_street_address"]) > 2 else ""

            row = [item["filename"],
                   extract_file_date(item["filename"]),
                   item["content"]["bank_name"],
                   item["content"]["bank_address"],
                   item["content"]["victim_name"],
                   address["street"],
                   address["zip"],
                   address["city"],
                   address["state"],
                   address["latitude"],
                   address["longitude"],
                   item["content"]["business_name"],
                   item["content"]["business_address"],
                   item["content"]["date"],
                   item["content"]["check_amount"]
                   ]

            writer.writerow(row)

    print(C("Done!", fore="green", style="bright"))

    # if input() == "y":
    #     parsed = []
    #     for file in files:
    #         try:
    #             filename = file["filename"].split(".txt")[0]
    #             output = file["content"]
    #             address = ""
    #             if output["victim_street_address"] is not None or output["victim_street_address"] != "":
    #                 address = get_coordinates(output["victim_street_address"])

    #             output["victim_street_address"] = address

    #             # print({"filename": filename, "content": output})
    #             # print("\n")

    #             parsed.append(
    #                 {"filename": filename, "content": output})

    #         except Exception as e:
    #             logger.warning(e)
    #             logger.warning(f"Error parsing {file['filename']}")
    #             logger.info("Traceback:")
    #             raise e

    #     f = open(out, "w")
    #     writer = csv.writer(f)

    #     header = ["Picture ID", "Picture Date", "Bank Name", "Bank Address", "Victim Name", "Victim Street Address", "Victim Zip Code",
    #               "Victim City", "Victim State", "Victim Latitude", "Victim Longitude", "Business Name", "Business Address", "Check Date", "Check Amount"]

    #     writer.writerow(header)

    #     for item in parsed:
    #         if item["content"]["victim_street_address"] is None or item["content"]["victim_street_address"] == "":
    #             address = {"latitude": "", "longitude": "",
    #                        "street": "", "zip": "", "city": "", "state": ""}
    #             row = [item["filename"], extract_file_date(item["filename"]), item["content"]["bank_name"], item["content"]["bank_address"], item["content"]["victim_name"], address["street"], address["zip"],
    #                    address["city"], address["state"], address["latitude"], address["longitude"], item["content"]["business_name"], item["content"]["business_address"], item["content"]["date"], item["content"]["check_amount"]]

    #             writer.writerow(row)
    #         else:
    #             print(item["content"]["victim_street_address"])
    #             address = {"latitude": "", "longitude": "",
    #                        "street": "", "zip": "", "city": "", "state": ""}

    #             if item["content"]["victim_street_address"]:
    #                 address["latitude"] = item["content"]["victim_street_address"][0] if len(
    #                     item["content"]["victim_street_address"]) > 0 else ""
    #                 address["longitude"] = item["content"]["victim_street_address"][1] if len(
    #                     item["content"]["victim_street_address"]) > 1 else ""
    #                 address["street"] = item["content"]["victim_street_address"][2].get(
    #                     "address", "") if len(item["content"]["victim_street_address"]) > 2 else ""
    #                 address["zip"] = item["content"]["victim_street_address"][2].get(
    #                     "zipcode", "") if len(item["content"]["victim_street_address"]) > 2 else ""
    #                 address["city"] = item["content"]["victim_street_address"][2].get(
    #                     "city", "") if len(item["content"]["victim_street_address"]) > 2 else ""
    #                 address["state"] = item["content"]["victim_street_address"][2].get(
    #                     "state", "") if len(item["content"]["victim_street_address"]) > 2 else ""

    #             # Write conditional statements that check if each value in the address dictionary exists or not, if it doesn't, then set it to an empty string

    #             row = [item["filename"], extract_file_date(item["filename"]), item["content"]["bank_name"], item["content"]["bank_address"], item["content"]["victim_name"], address["street"], address["zip"],
    #                    address["city"], address["state"], address["latitude"], address["longitude"], item["content"]["business_name"], item["content"]["business_address"], item["content"]["date"], item["content"]["check_amount"]]

    #             writer.writerow(row)

    #     f.close()

    #     print(C("Done!", fore="green", style="bright"))
    # else:
    #     print("Exiting...")
    #     sys.exit(1)


# def main(directory, out):
#     files = get_files(directory)
#     files_with_outputs = []

#     for file in files:
#         with open(os.path.join(directory, file), "r") as f:
#             files_with_outputs.append(
#                 {"filename": file, "content": "".join(f.read().split("\n")[:-1])})

#     cost_of_operation = 0

#     for file in files_with_outputs:
#         cost_of_operation += calculate_price(
#             file["content"]) + calculate_google_maps_price(1)

#     print("Cost of operation:", C(
#         f"${cost_of_operation}", fore="red", style="bright"))

#     print("Do you want to continue?", C("(y/n)", fore="yellow"))

#     if input() == "y":
#         parsed = []
#         unparseable = []
#         for file in files_with_outputs:
#             try:
#                 # Sleep function to avoid getting ratelimited
#                 time.sleep(0.025)

#                 filename = file["filename"].split(".txt")[0]
#                 output = parse(file["content"])
#                 # print('\n' + output + '\n')
#                 address = get_coordinates(output["victim_street_address"])

#                 output["victim_street_address"] = address

#                 parsed.append(
#                     {"filename": filename, "content": output})
#             except Exception as e:
#                 logger.warning(e)
#                 logger.warning(f"Error parsing {file['filename']}")
#                 logger.info("Traceback:")
#                 unparseable.append(file["filename"])
#                 # raise e

#         f = open(out, "w")
#         writer = csv.writer(f)

#         header = ["Picture ID", "Picture Date", "Bank Name", "Bank Address", "Victim Name", "Victim Street Address", "Victim Zip Code",
#                   "Victim City", "Victim State", "Victim Latitude", "Victim Longitude", "Business Name", "Business Address", "Check Date", "Check Amount"]

#         writer.writerow(header)

#         for item in parsed:
#             address = {"latitude": "", "longitude": "",
#                        "street": "", "zip": "", "city": "", "state": ""}
#             if item["content"]["victim_street_address"] is not None:
#                 address = {"latitude": item["content"]["victim_street_address"][0], "longitude": item["content"]["victim_street_address"][1], "street": item["content"]["victim_street_address"]
#                            [2]["address"], "zip": item["content"]["victim_street_address"][2]["zipcode"], "city": item["content"]["victim_street_address"][2]["city"], "state": item["content"]["victim_street_address"][2]["state"]}

#             row = [item["filename"], extract_file_date(item["filename"]), item["content"]["bank_name"], item["content"]["bank_address"], item["content"]["victim_name"], address["street"], address["zip"],
#                    address["city"], address["state"], address["latitude"], address["longitude"], item["content"]["business_name"], item["content"]["business_address"], item["content"]["date"], item["content"]["check_amount"]]

#             writer.writerow(row)

#         f.close()

#         print(C("Done!", fore="green", style="bright"))
#         print(C("Unparseable files:", fore="yellow", style="bright", end=" "))
#         print(C(", ".join(unparseable), fore="red", style="bright"))
#     else:
#         print("Exiting...")
#         sys.exit(1)


if __name__ == "__main__":
    main(inputs=sys.argv[1], out=sys.argv[2])
