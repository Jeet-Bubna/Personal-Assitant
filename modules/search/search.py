def search(queue):
    while True:
        text = queue.get()
        if text == 'TERMINATE':
            print('Terminating')
            break