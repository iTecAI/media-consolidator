import importlib
from fsspec import AbstractFileSystem
from models import BaseModel

class DownloadTarget:
    def __init__(
        self,
        displayName: str,
        module: str,
        obj: str,
        root: str,
        args: list = [],
        kwargs: dict = {},
    ):
        self.displayName = displayName
        self.module = importlib.import_module(module)
        self.object: AbstractFileSystem = getattr(self.module, obj)(*args, **kwargs)
        self.root = root

    def mkpath(self, path: str | list | dict):
        if type(path) == str:
            return self.root.rstrip("/") + "/" + path.lstrip("/")
        if type(path) == list:
            return [self.root.rstrip("/") + "/" + p.lstrip("/") for p in path]
        if type(path) == dict:
            return {
                k: self.root.rstrip("/") + "/" + p.lstrip("/") for k, p in path.items()
            }

    def cat(self, path, recursive=False, on_error="raise", **kwargs):
        return self.object.cat(
            self.mkpath(path), recursive=recursive, on_error=on_error, **kwargs
        )

    def cat_file(self, path, start=None, end=None, **kwargs):
        return self.object.cat_file(self.mkpath(path), start=start, end=end, **kwargs)

    def checksum(self, path):
        return self.object.checksum(self.mkpath(path))

    def clear_instance_cache(self):
        self.object.clear_instance_cache()

    def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
        self.object.copy(
            self.mkpath(path1),
            self.mkpath(path2),
            recursive=recursive,
            on_error=on_error,
            **kwargs
        )

    def cp(self, path1, path2, recursive=False, on_error=None, **kwargs):
        self.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)

    def created(self, path):
        return self.object.created(self.mkpath(path))

    def current(self):
        return self.object.current()

    def delete(self, path, recursive=False, maxdepth=None):
        self.object.delete(self.mkpath(path), recursive=recursive, maxdepth=maxdepth)

    def du(self, path, total=True, maxdepth=None, **kwargs):
        return self.object.delete(
            self.mkpath(path), total=total, maxdepth=maxdepth, **kwargs
        )

    def disk_usage(self, path, total=True, maxdepth=None, **kwargs):
        return self.du(path, total=total, maxdepth=maxdepth, **kwargs)

    def download(self, rpath, lpath, recursive=False, **kwargs):
        self.object.download(self.mkpath(rpath), lpath, recursive=recursive, **kwargs)

    def end_transaction(self):
        self.object.end_transaction()

    def exists(self, path, **kwargs):
        return self.object.exists(self.mkpath(path), **kwargs)

    def expand_path(self, path, recursive=False, maxdepth=None):
        return self.object.expand_path(
            self.mkpath(path), recursive=recursive, maxdepth=maxdepth
        )

    def find(self, path, maxdepth=None, withdirs=False, detail=False, **kwargs):
        return self.object.find(
            self.mkpath(path),
            maxdepth=maxdepth,
            withdirs=withdirs,
            detail=detail,
            **kwargs
        )

    def get(self, rpath, lpath, recursive=False, **kwargs):
        self.object.get(self.mkpath(rpath), lpath, recursive=recursive, **kwargs)

    def get_file(self, rpath, lpath, outfile=None, **kwargs):
        self.object.get_file(self.mkpath(rpath), lpath, outfile=outfile, **kwargs)

    def glob(self, path, **kwargs):
        return self.object.glob(self.mkpath(path), **kwargs)

    def head(self, path, size=1024):
        return self.object.head(self.mkpath(path), size=size)

    def info(self, path, **kwargs):
        return self.object.info(self.mkpath(path), **kwargs)

    def isdir(self, path):
        return self.object.isdir(self.mkpath(path))

    def isfile(self, path):
        return self.object.isfile(self.mkpath(path))

    def lexists(self, path, **kwargs):
        return self.object.lexists(self.mkpath(path), **kwargs)

    def ls(self, path, detail=True, **kwargs):
        return self.object.ls(self.mkpath(path), detail=detail, **kwargs)

    def listdir(self, path, detail=True, **kwargs):
        return self.ls(path, detail=detail, **kwargs)

    def mkdir(self, path, create_parents=True, **kwargs):
        self.object.mkdir(self.mkpath(path), create_parents=create_parents, **kwargs)

    def makedir(self, path, create_parents=True, **kwargs):
        self.object.mkdir(self.mkpath(path), create_parents=create_parents, **kwargs)

    def makedirs(self, path, exist_ok=False):
        self.object.makedirs(self.mkpath(path), exist_ok=exist_ok)

    def mkdirs(self, path, exist_ok=False):
        self.object.makedirs(self.mkpath(path), exist_ok=exist_ok)

    def modified(self, path):
        return self.object.modified(self.mkpath(path))

    def move(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
        self.object.move(
            self.mkpath(path1),
            self.mkpath(path2),
            recursive=recursive,
            maxdepth=maxdepth,
            **kwargs
        )

    def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
        self.object.mv(
            self.mkpath(path1),
            self.mkpath(path2),
            recursive=recursive,
            maxdepth=maxdepth,
            **kwargs
        )

    def open(
        self,
        path,
        mode="rb",
        block_size=None,
        cache_options=None,
        compression=None,
        **kwargs
    ):
        return self.object.open(
            self.mkpath(path),
            mode=mode,
            block_size=block_size,
            cache_options=cache_options,
            compression=compression,
            **kwargs
        )

    def pipe(self, path, value=None, **kwargs):
        self.object.pipe(self.mkpath(path), value=value, **kwargs)

    def pipe_file(self, path, value, **kwargs):
        self.object.pipe_file(self.mkpath(path), value, **kwargs)

    def put(self, lpath, rpath, recursive=False, **kwargs):
        self.object.put(lpath, self.mkpath(rpath), recursive=recursive, **kwargs)

    def put_file(self, lpath, rpath, **kwargs):
        self.object.put_file(lpath, self.mkpath(rpath), **kwargs)

    def rename(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
        self.object.move(
            self.mkpath(path1),
            self.mkpath(path2),
            recursive=recursive,
            maxdepth=maxdepth,
            **kwargs
        )

    def rm(self, path, recursive=False, maxdepth=None):
        self.object.delete(self.mkpath(path), recursive=recursive, maxdepth=maxdepth)

    def rm_file(self, path):
        self.object.rm_file(self.mkpath(path))

    def rmdir(self, path):
        self.object.rmdir(self.mkpath(path))

    def size(self, path):
        return self.object.size(self.mkpath(path))

    def sizes(self, paths):
        return self.object.sizes(self.mkpath(paths))

    def stat(self, path, **kwargs):
        return self.object.info(self.mkpath(path), **kwargs)

    def tail(self, path, size=1024):
        return self.object.tail(self.mkpath(path), size=size)

    def touch(self, path, truncate=True, **kwargs):
        self.object.touch(self.mkpath(path), truncate=truncate, **kwargs)

    def ukey(self, path):
        return self.object.ukey(self.mkpath(path))

    def upload(self, lpath, rpath, recursive=False, **kwargs):
        self.object.put(lpath, self.mkpath(rpath), recursive=recursive, **kwargs)

    def walk(self, path, maxdepth=None, **kwargs):
        return self.object.walk(self.mkpath(path), maxdepth=maxdepth, **kwargs)


class DownloadManager:
    def __init__(self, simultaneous_downloads: int, targets: dict) -> None:
        self.simultaneous_downloads = simultaneous_downloads
        self.targets = {
            name: DownloadTarget(
                args["displayName"],
                args["module"],
                args["object"],
                args["root"],
                args=args["args"],
                kwargs=args["kwargs"],
            )
            for name, args in targets.items()
        }
        self.queue = []
        self.in_progress = []
    
    def __getitem__(self, key: str):
        return self.targets[key]
    
    def add_download(self, target: str, fn, *args, **kwargs):
        self.queue.append({
            "function": fn,
            "target": target,
            "args": args,
            "kwargs": kwargs
        })
    
    def progress_queue(self):
        for item in self.in_progress:
            pass

        while len(self.in_progress) < self.simultaneous_downloads:
            queued_item = self.queue.pop(0)
            queued_item["kwargs"]["target"] = queued_item["target"]
            
    

    

