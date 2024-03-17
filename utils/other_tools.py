def read_addresses(path: str = 'data/btc.txt'):
    with open(path) as file:
        return file.read().splitlines()
