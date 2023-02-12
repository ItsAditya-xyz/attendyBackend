import requests
from time import sleep
import json

ENDPOINT = "https://purple-proud-research.solana-devnet.discover.quiknode.pro/6631431d3a5a71d8befaa3ab229efc0da4ff23b4"
GET_NFTS = "https://staging.crossmint.com/api/v1-alpha1/wallets/solana:{}/nfts"
FILECOIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGU5QjZkZTMxMzFiNzk2MTcxNjIwRTA0RUIxNjhlN2RkMjMwMzgzNzMiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NzYxNjQ3NjE5MzIsIm5hbWUiOiJoYWNrbnN1dCJ9.Ls4chdFV2RKKYL8_tGwNN5D0YdW5OV8eAFFVqMxCz0g"


def mint_nft(name: str, image_url: str, description: str, address: str):
    data_mint = {
        "jsonrpc":
        "2.0",
        "id":
        1,
        "method":
        "cm_mintNFT",
        "params": [
            "default-solana",
            "solana:" + address,
            {
                "name": name,
                "image": image_url,
                "description": description,
            },
        ],
    }

    res = requests.post(ENDPOINT, json=data_mint)

    return res.json()


def get_status(id_: str):
    data_get_mint_status = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "cm_getNFTMintStatus",
        "params": [
            "default-solana",
            id_,
        ],
    }

    res = requests.post(ENDPOINT, json=data_get_mint_status)
    status = res.json()["result"]["onChain"]["status"]
    while status in ("pending"):
        print("pending")
        sleep(1)
        res = requests.post(ENDPOINT, json=data_get_mint_status)
        status = res.json()["result"]["onChain"]["status"]
    return res.json()


def get_nfts(address: str):
    res = requests.get(GET_NFTS.format(address),
                       headers={"accept": "application/json"})
    return res.json()


def upload_filecoin_json(json_data: dict):
    ENDP = "https://api.web3.storage/upload"
    with open("./temp.json", "w") as f:
        f.write(json.dumps(json_data))
    res = requests.post(
        ENDP,
        files={
            "file": (
                "./temp.json",
                open("./temp.json", "rb"),
                "text/plain",
            )
        },
        headers={
            "Authorization": "Bearer " + FILECOIN_TOKEN,
        },
    )
    return "https://" + str(res.json()["cid"]) + ".ipfs.w3s.link"


def upload_filecoin(file_path: str):
    ENDP = "https://api.web3.storage/upload"
    res = requests.post(
        ENDP,
        files={
            "file": (
                file_path.split("/")[-1],
                open(file_path, "rb"),
                "text/plain",
            )
        },
        headers={
            "Authorization": "Bearer " + FILECOIN_TOKEN,
        },
    )
    return "https://" + str(res.json()["cid"]) + ".ipfs.w3s.link"


def get_cid(cid: str):
    ENDP = "https://api.web3.storage/user/uploads/" + cid
    res = requests.get(
        ENDP,
        headers={
            "Authorization": "Bearer " + FILECOIN_TOKEN,
        },
    )
    return res.json()


# res = mint_nft(
#     "Anime Gurl",
#     "https://pbs.twimg.com/media/FiJA7rCXwAI4dEk?format=jpg&name=medium",
#     "Animu Gurl UwU",
#     "9ir2eV4oU8me8UV8KNELeNwocTbSCu3Mbtb942QXxXMC",
# )

# res_id = res["result"]["id"]

# sleep(10)

# res = get_status(res_id)

# # hash = res["result"]["hash"]
# print(res)

# print(get_nfts("9ir2eV4oU8me8UV8KNELeNwocTbSCu3Mbtb942QXxXMC"))

# print(upload_filecoin("./res.json"))
# print(get_cid("bafkreicqdwul7tye4n52cfz2ogw73ajh2ssldlcpwnrr3okogedld3e2sq"))

