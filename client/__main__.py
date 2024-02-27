from client import read_qr_codes

def main():
    print("Car says hello")

    read_qr_codes(callback=print)

if __name__ == "__main__":
    main()
