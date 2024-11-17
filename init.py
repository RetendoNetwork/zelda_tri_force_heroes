import os
import logging
from dotenv import load_dotenv
import grpc
from grpc import metadata
from google.protobuf import empty_pb2

# Configure the logger
logger = logging.getLogger('Retendo')
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def init():
    load_dotenv()

    postgres_uri = os.getenv("PN_TFH_POSTGRES_URI")
    kerberos_password = os.getenv("PN_TFH_KERBEROS_PASSWORD")
    authentication_server_port = os.getenv("PN_TFH_AUTHENTICATION_SERVER_PORT")
    secure_server_host = os.getenv("PN_TFH_SECURE_SERVER_HOST")
    secure_server_port = os.getenv("PN_TFH_SECURE_SERVER_PORT")
    account_grpc_host = os.getenv("PN_TFH_ACCOUNT_GRPC_HOST")
    account_grpc_port = os.getenv("PN_TFH_ACCOUNT_GRPC_PORT")
    account_grpc_api_key = os.getenv("PN_TFH_ACCOUNT_GRPC_API_KEY")

    if not postgres_uri:
        logger.error("PN_TFH_POSTGRES_URI environment variable not set")
        os._exit(0)

    if not kerberos_password:
        logger.warning(f"PN_TFH_KERBEROS_PASSWORD environment variable not set. Using default password: {globals.KerberosPassword}")
    else:
        globals.KerberosPassword = kerberos_password

    if not authentication_server_port:
        logger.error("PN_TFH_AUTHENTICATION_SERVER_PORT environment variable not set")
        os._exit(0)

    try:
        port = int(authentication_server_port)
        if port < 0 or port > 65535:
            raise ValueError
    except ValueError:
        logger.error(f"PN_TFH_AUTHENTICATION_SERVER_PORT is not a valid port. Expected 0-65535, got {authentication_server_port}")
        os._exit(0)

    if not secure_server_host:
        logger.error("PN_TFH_SECURE_SERVER_HOST environment variable not set")
        os._exit(0)

    if not secure_server_port:
        logger.error("PN_TFH_SECURE_SERVER_PORT environment variable not set")
        os._exit(0)

    try:
        port = int(secure_server_port)
        if port < 0 or port > 65535:
            raise ValueError
    except ValueError:
        logger.error(f"PN_TFH_SECURE_SERVER_PORT is not a valid port. Expected 0-65535, got {secure_server_port}")
        os._exit(0)

    if not account_grpc_host:
        logger.error("PN_TFH_ACCOUNT_GRPC_HOST environment variable not set")
        os._exit(0)

    if not account_grpc_port:
        logger.error("PN_TFH_ACCOUNT_GRPC_PORT environment variable not set")
        os._exit(0)

    try:
        port = int(account_grpc_port)
        if port < 0 or port > 65535:
            raise ValueError
    except ValueError:
        logger.error(f"PN_TFH_ACCOUNT_GRPC_PORT is not a valid port. Expected 0-65535, got {account_grpc_port}")
        os._exit(0)

    if not account_grpc_api_key:
        logger.warning("Insecure gRPC server detected. PN_TFH_ACCOUNT_GRPC_API_KEY environment variable not set")

    globals.GRPCAccountClientConnection = grpc.insecure_channel(f"{account_grpc_host}:{account_grpc_port}")
    globals.GRPCAccountClient = pb.AccountStub(globals.GRPCAccountClientConnection)
    globals.GRPCAccountCommonMetadata = metadata.Metadata(
        ("X-API-Key", account_grpc_api_key),
    )

    database.connect_postgres()

# Initialize
init()
