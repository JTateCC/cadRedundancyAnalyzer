class STLFileHandler(CADFileHandler):
    def can_handle(self, file_path: str) -> bool:
        return Path(file_path).suffix.lower() == '.stl'