def import_modules():
    from modules import music
    from modules import search
    from modules import timer

    return "Modules imported"

def main():
    import_modules()

    # Get user input, for now its text

    input = input("Enter command: ")

    


if __name__ == "__main__":
    main()