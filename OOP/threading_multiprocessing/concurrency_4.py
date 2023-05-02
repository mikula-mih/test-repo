
# a `future` is an object that wraps a function call; runs in the background
# in a thread or a separate process; the `future` object has methods to
# check whether the computation has completed and to get the results;
""" Futures """
# In Python, the `concurrent.futures` module wraps either `multiprocessing` or
# `threading` depending on what kind of concurrency we need;
#
# Futures can help manage boundaries between the different threads or processes.
# Similar to the multiprocessing pool, they are useful for call and answer type
# interactions, in which processing can happen in another thread (or process) &
# then at some point in the future (they are aptly named, after all), you can
# ask it for the result. It's a wrapper around multiprocessing pools &
# thread pools, but it provides a cleaner API and encourages nicer code.
#
class ImportResult(NamedTuple):
    path: Path
    imports: Set[str]

    @property
    def focus(self) -> bool:
        return "typing" in self.imports

class ImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            self.imports.add(node.module)

def find_imports(path: Path) -> ImportResult:
    tree = ast.parse(path.read_text())
    iv = ImportVisitor()
    iv.visit(tree)
    return ImportResult(path, iv.imports)
#
# an `Abstract Syntax Tree` (AST) is the parsed source code, usually from a
# formal programming language;
def main() -> None:
    start = time.perf_counter()
    base = Path.cwd().parent
    with futures.ThreadPoolExecutor(24) as pool:
        analyzers = [
            pool.submit(find_imports, path)
            for path in all_source(base, "*.py")
        ]
        analyzed = (
            worker.result()
            for worker in futures.as_completed(analyzers)
        )
    for example in sorted(analyzed):
        print(
            f"{'->' if example.focus else '':2s} "
            f"{example.path.relative_to(base)} {example.imports}"
        )
    end = time.perf_counter()
    rate = 1000 * (end - start) / len(analyzers)
    print(f"Searched {len(analyzers)} files at {rate:.3f}ms/file")
#
