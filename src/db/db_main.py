from db_insert import insert_genres_data, insert_regions_data, all_insert
import os
import glob


def main():
    directory = '../../data/output'
    pattern = '*.json'

    try:
        files = glob.glob(os.path.join(directory, pattern))
        for file in files:
            all_insert(file)
            print(f'----{file}------')
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
