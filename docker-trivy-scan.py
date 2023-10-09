import subprocess
import requests
import logging
import time

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Read image names from file
with open("image_data", "r") as file:
    image_list = [line.strip() for line in file.readlines()]


# Iterate over each image
def scan_image():
    for image in image_list:
        image = 'xx/xxxx:1.0.2'
        try:
            logging.info("________________________________________")
            logging.info(f"pulling image {image}")
            time.sleep(10)
            subprocess.check_output(["docker", "pull", image])
            logging.info(f"started scanning image for {image}")
            # Run the command and capture the output
            output = subprocess.check_output(['trivy', 'image', '--scanners', 'secret', image, '--timeout', '10m']).decode('utf-8')

            # Count the number of lines in the output
            line_count = len(output.splitlines())
            time.sleep(5)
            # Check if the line count is greater than 3
            if line_count > 3:
                # If more than 3 lines, trigger the API call
                api_url = "https://api.telegram.org/botxxxxx:xxxxxxxx/sendMessage"
                chat_id = "-xxxxxx"
                message = f"Found secrets on image {image}:\n{output[:4000]}"
                payload = {
                    "chat_id": chat_id,
                    "text": message
                }
                response = requests.post(api_url, data=payload)
                if response.ok:
                    logging.info(f"API call triggered successfully for {image}")
                else:
                    logging.error(f"Failed to trigger API call for {image}")
                with open("output_file.txt", "a") as file:
                    file.write(f"data for {image}\n {output}\n")
            else:
                # If 3 lines or fewer, save the data to a file
                with open("output_file.txt", "a") as file:
                    file.write(f"myimage, {output}\n")
                logging.info(f"No secrets found for image")
                logging.info(f"scan data saved to output_file.txt for {image}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error running trivy command for {image}: {e}")

def final_post():
    api_url = "https://api.telegram.org/botxxxxx:xxxxxxxx/sendMessage"
    chat_id = "-xxxxxx"
    payload = {
        "chat_id": chat_id,
        "text": "scan commpleted"
    }
    response = requests.post(api_url, data=payload)
    if response.ok:
        logging.info(f"final call triggered successfully")
    else:
        logging.error(f"Failed to trigger API call for")

scan_image()
final_post()
