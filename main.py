from linker import linker
import logging
import sys
# === Logger Configuration ===
logger = logging.getLogger("main")

def init_logger():

    logger.setLevel(logging.DEBUG)        # info, INFO, WARNING, ERROR, CRITICAL

    # --- Formatter (how logs look) ---
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # --- Console Handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)   # logs of this level and above go to console
    console_handler.setFormatter(formatter)

    # --- File Handler ---
    file_handler = logging.FileHandler(r"logs\logfile.log", mode="a")
    file_handler.setLevel(logging.INFO)     # logs of this level and above go to file
    file_handler.setFormatter(formatter)


    # --- Attach Handlers ---
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    

def main():
    
    init_logger()
    linker()
    logger.info('Main ended ---')
    

if __name__ == "__main__":
    main()