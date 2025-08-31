from linker import linker, init_threads
import queue

main_queue = queue.Queue()

def input_thread():
    while True:
        text = input("Enter command: ")
        main_queue.put(text)

def main():
    init_threads(input_thread, main_queue)
    

if __name__ == "__main__":
    main()