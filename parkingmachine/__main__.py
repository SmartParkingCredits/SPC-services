from dotenv import load_dotenv
import typer
from parkingmachine import run_service

app = typer.Typer()

def deploy_contract():
    """
    Function to handle the deployment logic.
    You can add your deployment code here.
    """
    print("Deploying the smart contract...")
    # Add your deployment code here
    # For example, compile the contract, connect to Ethereum, and deploy
    print("Smart contract deployed successfully!")


@app.command()
def deploy():
    """
    Deploy command.
    """
    deploy_contract()

@app.command()
def service(contract_address: str):
    """
    Service command.
    """
    run_service(contract_address)

if __name__ == "__main__":

    load_dotenv()
    app()
