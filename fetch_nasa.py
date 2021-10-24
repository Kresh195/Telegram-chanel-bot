import os
import requests
from urllib.parse import urlparse


def fetch_file_format(link_nasa_image):
    path_from_link = urlparse(link_nasa_image).path
    file_format = os.path.splitext(path_from_link)[1]
    file_name = os.path.split(path_from_link)[1].split('.')[0]
    return file_format, file_name


def fetch_nasa_images(link_nasa_image):
    file_format, file_name = fetch_file_format(link_nasa_image)
    response = requests.get(link_nasa_image)
    response.raise_for_status()
    with open('NASA_images/{}{}'.format(file_name, file_format), 'wb') as file:
        file.write(response.content)


def fetch_epic_images(epic_images_info, nasa_token):
    for epic_image_info in epic_images_info:
        date = epic_image_info['date'].split(' ')[0].split('-')
        epic_image_link = 'https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png' \
                          '?api_key={}'.format(date[0], date[1], date[2],
                                               epic_image_info['image'], nasa_token)
        response = requests.get(epic_image_link)
        response.raise_for_status()
        with open('Epic_images/{}.png'.format(epic_image_info['image']), 'wb') as file:
            file.write(response.content)


def main():
    nasa_token = os.getenv('NASA_TOKEN')
    response_links_nasa = requests.get(
        'https://api.nasa.gov/planetary/apod?count=30&api_key={}'.format(nasa_token))
    response_links_nasa.raise_for_status()
    response_links_epic = requests.get(
        'https://api.nasa.gov/EPIC/api/natural?api_key={}'.format(nasa_token))
    response_links_epic.raise_for_status()
    links_nasa = response_links_nasa.json()
    epic_images_info = response_links_epic.json()[:5]
    for link_nasa in links_nasa:
        link_nasa_image = link_nasa['hdurl']

        fetch_nasa_images(link_nasa_image)
    fetch_epic_images(epic_images_info, nasa_token)


if __name__ == '__main__':
    main()
