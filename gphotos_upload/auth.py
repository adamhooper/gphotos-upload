import appdirs
import os
import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow

from gphotos_upload.service import Service

def login(flags, logger):
    """Returns a Service that wraps API requests.

    Throws on failure.

    "flags" is an ArgumentParser's returned args.
    """
    flow = load_flow()

    flow.run_local_server()

    #dump_flow(flow)

    session = flow.authorized_session()
    session.headers['GData-Version'] = '3'

    return Service(session, logger)

def _get_flow_path():
    """Returns, e.g., ~/.config/gphotos-upload/auth-flow.p"""
    config_dir = appdirs.user_config_dir('gphotos-upload', 'adamhooper.com')
    os.makedirs(config_dir, exist_ok=True)
    path = os.path.join(config_dir, 'auth-flow.p')
    return path

def load_flow():
    """Returns a valid google-auth Flow.

    Logic:
    * Try to load from cached "auth-flow.p" file in, e.g., ~/.config/gphotos-upload/
    * Fall back to a default one
    """
    path = _get_flow_path()

    try:
        with open(path, 'rb') as f:
            flow = pickle.load(f)
            # TODO verify that "flow" is, in fact, a valid Flow
            return flow
    except FileNotFoundError:
        scope = 'https://picasaweb.google.com/data/'
        client_secrets = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

        return InstalledAppFlow.from_client_secrets_file(client_secrets, scopes=[scope])

def dump_flow(flow):
    """Saves flow, for the next call to load_flow().
    """
    path = _get_flow_path()
    with open(path, 'wb') as f:
        pickle.dump(flow, f)
