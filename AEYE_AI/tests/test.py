import server
import pytest

from server.config import load_config, build_session

import argparse
parser = argparse.ArgumentParser(description="AEYE Flask Server")
parser.add_argument('config', type=str, help="Flask config path")
args = parser.parse_args()

def main():
    cfg = load_config(args.config)
    session = build_session(cfg.SERVER)
    client = server.adapters.RequestHTTP_1_1(cfg, session)
    tensor = server.tensor.TorchTensorProvider(cfg.SERVER)
    
    dummy_data = tensor.make_payload()
    for _ in range (100):
        
        client.post(dummy_data)



if __name__ == "__main__":
    main()