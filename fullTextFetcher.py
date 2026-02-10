import os
import json
from tokenize import String
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, List, Optional, Tuple, Any, Union


def initialize_supabase_client(
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None,
    force_reinit: Optional[bool] = False,
    use_dotenv: Optional[bool] = True,
) -> Client:
    """
    Initialize and return a Supabase client.

    Parameters
    ----------
    supabase_url, supabase_key : Optional[str]
        Overrides for env vars.
    force_reinit : bool
        If True, recreate the client even if one exists.
    use_dotenv : bool
        If True, call load_dotenv() to populate environment variables.

    Returns
    -------
    supabase.Client
    """

    # return client if one exists already
    global supabase
    if not force_reinit and 'supabase' in globals() and supabase is not None:
        return supabase

    if use_dotenv:
        load_dotenv()

    url = supabase_url or os.getenv('SUPABASE_URL')
    key = supabase_key or os.getenv('SUPABASE_KEY')
    if not url or not key:
        raise RuntimeError("Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY or pass overrides")

    try:
        supabase = create_client(url, key)
        return supabase
    except Exception:
        supabase = None
        raise

def getMetaData(db: Client, id):
    response = db.table('manuscripts').select('title, abstract').eq('id', id).single().execute()
    folder = "data"
    filename = os.path.join(folder, "output.json")
    os.makedirs(folder, exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(response.data, f, indent = 2)
    return response.data

def main():
    db = initialize_supabase_client()
    print(getMetaData(db, '000a71e9-7d71-4353-847d-3600ebdf8b18')) #takes in ID -> returns metadata




if __name__ == '__main__':
    main()