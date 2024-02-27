from client import read_qr_codes, enter as car_enter, exit as car_exit, process

from dotenv import load_dotenv
import typer

app = typer.Typer()

@app.command()
def qr():
    """
    Scan QR code.
    """
    print("Car says hello")
    read_qr_codes(callback=process)

@app.command()
def park():
    """
    Scan QR code to park.
    """
    print("Car says hello")
    print("Searching for QR code...")
    read_qr_codes(callback=process)

@app.command()
def enter(contract_address: str):
    """
    Enter
    """
    print("Car says hello")
    tx = car_enter(contract_address, 0.000001)

@app.command()
def exit(contract_address: str):
    """
    Exit
    """
    print("Car says hello")
    tx = car_exit(contract_address, 0.000001)

if __name__ == "__main__":

    load_dotenv()
    app()
