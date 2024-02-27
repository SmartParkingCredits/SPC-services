from dotenv import load_dotenv
import typer
from parkingmachine import run_service, deploy_contract

app = typer.Typer()


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
