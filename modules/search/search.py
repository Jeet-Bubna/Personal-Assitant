def search(queue, y):
    while True:
        text = queue.get()
        if text == 'end':
            y.put('TERMINATED')
            break