from client import read_qr_codes, enter as car_enter

from dotenv import load_dotenv
import typer

app = typer.Typer()

@app.command()
def qr():
    """
    Scan QR code.
    """
    print("Car says hello")
    read_qr_codes(callback=print)

@app.command()
def enter(contract_address: str):
    """
    Enter
    """
    print("Car says hello")
    tx = car_enter(contract_address, 0.11)


if __name__ == "__main__":

    load_dotenv()
    app()
