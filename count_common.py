


def count_urls_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            line = file.readline()
            urls = line.split()  # Split the line using spaces as the delimiter
            
            count = 1
            for url in urls:
                print(str(count) + ":" + url)
                count +=1
            num_urls = len(urls)
            return num_urls
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return 0

file_path = 'start_urls.txt'
num_urls = count_urls_in_file(file_path)
print(f"Number of URLs in the file: {num_urls}")
    
