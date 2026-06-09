import os
import logging
from typing import Optional, List
from supabase import create_client, Client
from ..config import Config

logger = logging.getLogger(__name__)

class SupabaseManager:
    _client: Optional[Client] = None
    _bucket_name: str = "arva-data"

    @classmethod
    def get_client(cls) -> Optional[Client]:
        if cls._client is None:
            url = Config.SUPABASE_URL or os.environ.get("SUPABASE_URL")
            key = Config.SUPABASE_SERVICE_KEY or os.environ.get("SUPABASE_SERVICE_KEY")
            
            if not url or not key:
                logger.warning("Supabase URL or Key not configured. Supabase sync is disabled.")
                return None
            
            try:
                cls._client = create_client(url, key)
                logger.info("Supabase client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                return None
                
        return cls._client

    @classmethod
    def upload_file(cls, local_path: str, remote_path: str) -> bool:
        """Upload a file to Supabase Storage, overwriting if exists."""
        client = cls.get_client()
        if not client or not os.path.exists(local_path):
            return False
            
        try:
            with open(local_path, 'rb') as f:
                # Use upsert to overwrite existing files
                client.storage.from_(cls._bucket_name).upload(
                    path=remote_path,
                    file=f,
                    file_options={"upsert": "true"}
                )
            logger.debug(f"Uploaded {local_path} to Supabase: {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Error uploading {local_path} to Supabase: {e}")
            return False

    @classmethod
    def download_file(cls, remote_path: str, local_path: str) -> bool:
        """Download a file from Supabase Storage if it doesn't exist locally."""
        if os.path.exists(local_path):
            return True # Already exists
            
        client = cls.get_client()
        if not client:
            return False
            
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            res = client.storage.from_(cls._bucket_name).download(remote_path)
            with open(local_path, 'wb') as f:
                f.write(res)
            logger.debug(f"Downloaded {remote_path} from Supabase to {local_path}")
            return True
        except Exception as e:
            # File might not exist remotely yet, not necessarily an error
            logger.debug(f"Could not download {remote_path} from Supabase: {e}")
            return False

    @classmethod
    def list_directory(cls, remote_dir: str) -> List[str]:
        """List all files in a Supabase Storage directory."""
        client = cls.get_client()
        if not client:
            return []
            
        try:
            res = client.storage.from_(cls._bucket_name).list(remote_dir)
            if res:
                return [item['name'] for item in res if item['name'] != '.emptyFolderPlaceholder']
            return []
        except Exception as e:
            logger.error(f"Error listing directory {remote_dir} in Supabase: {e}")
            return []
