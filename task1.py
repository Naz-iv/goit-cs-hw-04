import os
import threading
import time


class KeywordSearch(threading.Thread):
    def __init__(self, folder, keywords, result_dict):
        threading.Thread.__init__(self)
        self.folder = folder
        self.keywords = keywords
        self.result_dict = result_dict
        self.start_time = 0

    def run(self):
        self.start_time = time.time_ns() // 1000
        for root, dirs, files in os.walk(self.folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding='utf-8') as file:
                        text = file.read()
                        for keyword in self.keywords:
                            count = text.count(keyword)
                            if count > 0:
                                if keyword not in self.result_dict:
                                    self.result_dict[keyword] = {}
                                self.result_dict[keyword][file_path] = count
                except Exception as e:
                    print(f"Error occurred during file {file_path} processing: {str(e)}")
        end_time = time.time_ns() // 1000

        print(f"Thread {self.ident} finished in {(end_time - self.start_time) / 1000000} seconds")


def main():
    folder = r"E:\git\goit-cs-hw-04\texts"
    keywords = ["було", "життя", "себе", "часто"]

    result_dict = {}

    threads = []
    for _ in range(2):
        thread = KeywordSearch(folder, keywords, result_dict)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Search results:")
    for keyword, files in result_dict.items():
        print(f"Keyword '{keyword}' found in:")

        for file_path, count in files.items():
            print(f"  - {file_path}, found {count} times")

    with open("multithreading_results.txt", "w", encoding="utf-8") as file:
        for keyword, files in result_dict.items():
            file.write(f"Keyword '{keyword}' found in:\n")
            for file_path, count in files.items():
                file.write(f"  - {file_path}, found {count} times\n")


if __name__ == "__main__":
    main()
