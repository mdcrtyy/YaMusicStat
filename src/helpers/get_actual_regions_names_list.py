import json


def get_regions_names(path='../data/input/info_about_regions.json'):
    """
    Функция, возвращающая название Российских регионов, для дальнейшей их сверки с данными артиста
    :param path:
    :return:
    """
    regions_names = []
    with open(path, 'r') as f:
        info_about_regions = json.load(f)
        for region_id, region_data in info_about_regions.items():
            region_name = region_data.get('name', '')
            regions_names.append(region_name)
    return regions_names

