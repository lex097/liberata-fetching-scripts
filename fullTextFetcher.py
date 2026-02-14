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

def getMetaData(db: Client, id: [str]):
    training_data = {"training_data" : []}
    for i in id:       
        response = db.table('manuscripts').select('title, abstract, topics').eq('id', i).single().execute()
        training_data["training_data"].append(response.data)
    folder = "data"
    filename = os.path.join(folder, "training_data.json")
    os.makedirs(folder, exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(training_data, f, indent = 2)
    return training_data

def getIDs(db: Client) -> [str]:

    IDs = db.table('manuscripts').select('id').limit(10).execute()
    rows = IDs.data
    IDs = [row['id'] for row in rows]
    return IDs

def main():
    db = initialize_supabase_client()
    IDs = getIDs(db)
    print(getMetaData(db, IDs)) #takes in ID -> returns metadata




if __name__ == '__main__':
    main()