from datetime import datetime

from utils.metadata_manager import MetadataManager

manager = MetadataManager()

metadata = manager.read_metadata()

metadata["products"] = {
    "last_run": datetime.utcnow().isoformat()
}

manager.write_metadata(metadata)

print(manager.read_metadata())