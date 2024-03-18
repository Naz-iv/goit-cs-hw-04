import os
import multiprocessing
import time

class KeywordSearchProcess(multiprocessing.Process):
    def __init__(self, folder, keywords, result_queue):
        super().__init__()
        self.folder = folder
        self.keywords = keywords
        self.result_queue = result_queue

    def run(self):
        results = {}
        start_time = time.time_ns() // 1000

        for root, dirs, files in os.walk(self.folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        text = file.read()
                        for keyword in self.keywords:
                            count = text.count(keyword)
                            if keyword in text:
                                if keyword not in results:
                                    results[keyword] = {}
                                results[keyword][file_path] = count
                except Exception as e:
                    print(f"Error occurred during file {file_path} processing: {str(e)}")

        end_time = time.time_ns() // 1000
        self.result_queue.put((results, end_time - start_time))

def main():
    folder = r"E:\git\goit-cs-hw-04\texts"
    keywords = ["було", "життя", "себе", "часто"]
    result_queue = multiprocessing.Queue()

    processes = []
    for _ in range(2):
        process = KeywordSearchProcess(folder, keywords, result_queue)
        processes.append(process)
        process.start()

    total_results = {}
    total_time = 0

    for process in processes:
        process.join()
        results, time_taken = result_queue.get()
        total_time = max(total_time, time_taken)
        for keyword, files in results.items():
            if keyword not in total_results:
                total_results[keyword] = {}
            total_results[keyword].update(files)

        print(f"Process {process.pid} finished in {time_taken / 1000000} seconds")

    print("Search results:")
    for keyword, files in total_results.items():
        print(f"Keyword '{keyword}':")
        for file_path, count in files.items():
            print(f"- {file_path}, found {count} times")

    with open("multiprocessing_results.txt", "w", encoding="utf-8") as file:
        for keyword, files in total_results.items():
            file.write(f"Keyword '{keyword}' found in:\n")
            for file_path, count in files.items():
                file.write(f"  - {file_path}, found {count} times\n")
        file.write(f"Total execution time: {total_time / 1000000} seconds")

    print(f"Total execution time: {total_time / 1000000} seconds")


if __name__ == "__main__":
    main()
