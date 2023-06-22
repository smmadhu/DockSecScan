import requests

def docker_hub_namespace(name):
    data_dump = []
    # API endpoint to list images of a user namespace
    url = f'https://hub.docker.com/v2/repositories/{name}/?page_size=100'

    # Send GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()

        # Iterate over the images and print their names
        for image in json_data["results"]:
            data_dump.append(f'{image["namespace"]}/{image["name"]}')
    else:
        print(f"Error: {response.status_code}")
    return data_dump


def docker_hub_search(name):
    data_dump = []
    # API endpoint to search images with string
    url = f'https://hub.docker.com/v2/search/repositories/?query={name}&page_size=100'

    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()

        # Iterate over the images and print their names
        for image in json_data["results"]:
            data_dump.append(f'{image["repo_name"]}')
    else:
        print(f"Error: {response.status_code}")
    return data_dump

output1 = docker_hub_namespace("user_namespace_here")
output2 = docker_hub_search("search_string_here")

combined_list = output1 + output2
unique_values = list(set(combined_list))


image_list = []
for images in unique_values:
    url_tag = f'https://hub.docker.com/v2/repositories/{images}/tags/?page_size=25&page=1'
    response = requests.get(url_tag)
    if response.status_code == 200:
        json_data = response.json()
        if json_data["count"] > 0:
            image_list.append(f'{images}:{json_data["results"][0]["name"]}')

print(len(image_list))

# print(image_list)

write_file = open('out.txt', 'w')
for data in image_list:
    write_file.write(data + '\n')

write_file.close()
