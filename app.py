import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract_abi = []

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Simple Dashboard with Web3 Integration"),
                className="text-center mt-4 mb-4",
            )
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Transfering Tokens"),
                        dbc.Input(id="transfer-to", placeholder="Address to transfer to",
                                  type="text", className="mb-2"),
                        dbc.Input(id="transfer-amount", placeholder="Amount to transfer",
                                  type="number", className="mb-2"),
                        dbc.Button("Transfer", id="transfer-button",
                                   color="primary", className="mb-2"),
                        html.Div(id="transfer-output"),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.H3("Checking Balance"),
                        dbc.Button("Check Balance", id="balance-button",
                                   color="primary", className="mb-2"),
                        html.Div(id="balance-output"),
                    ],
                    width=4,
                )
            ]
        )
    ],
    fluid=True,
    className="bg-dark text-white"
)

def transfer_tokens(n_clicks, to_address, amount):
    if n_clicks is None:
        return ""
    
    if not Web3.isAddress(to_address):
        return "Invalid address"
    
    try:
        tx_hash = contract.functions.transfer(to_address, int(amount)).transact({'from': w3.eth.accounts[0]})
        w3.eth.waitForTransactionReceipt(tx_hash)
        return "Transfer of {amount} tokens to {to_address} successful"
    except Exception as e:
        return f"Erro: {str(e)}"
    
@app.callback(
    Output("transfer-output", "children"),
    Input("transfer-button", "n_clicks"),
    State("transfer-to", "value"),
    State("transfer-amount", "value")
)

def verify_collateral(n_clicks):
    if n_clicks is None:
        return ""
    
    try:
        is_collateral_sufficient = contract.functions.verifyCollateral().call()
        if is_collateral_sufficient:
            return "Collateral is sufficient"
        else:
            return "Collateral is insufficient"
    except Exception as e:
        return f"Erro: {str(e)}"
    
if __name__ == "__main__":
    app.run_server(debug=True)

