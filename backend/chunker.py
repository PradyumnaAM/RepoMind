import ast

def chunk_python_document(document: dict) -> list[dict]:
    path = document["path"]
    content = document["content"]
    chunks = []
    assignment_nodes = []
    assignment_contents = []
    line = content.splitlines()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"Skipping invalid Python file: {path}")
        return []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for method in node.body:
                if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    start_line = method.lineno

                    if method.decorator_list:
                        start_line = min(
                            decorator.lineno for decorator in method.decorator_list
                        )
                    split = line[start_line-1 : method.end_lineno]
                    code = "\n".join(split)
                    result =  {
                        "path": path,
                        "type": "method",
                        "class_name": node.name,
                        "name": method.name,
                        "start_line": start_line,
                        "end_line": method.end_lineno,
                        "content" : code,
                    }
                    chunks.append(result)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start_line = node.lineno

            if node.decorator_list:
                start_line = min(
                    decorator.lineno for decorator in node.decorator_list
                )
            split2 = line[start_line-1 : node.end_lineno]
            code2 = "\n".join(split2)
            result = {
                "path" : path,
                "type": "function",
                "name": node.name,
                "start_line": start_line,
                "end_line": node.end_lineno,
                "content" : code2,
            }
            chunks.append(result)
        if isinstance(node, ast.Assign):
            assignment_nodes.append(node)

    if assignment_nodes:
        start_line = assignment_nodes[0].lineno
        end_line = assignment_nodes[-1].end_lineno
        source_ranges = []
        
        for assignment in assignment_nodes:
            source = line[assignment.lineno - 1 : assignment.end_lineno]
            code = "\n".join(source)
            assignment_contents.append(code)
            

            source_range = {
                "start_line": assignment.lineno,
                "end_line": assignment.end_lineno
            }   

            source_ranges.append(source_range)        

        assign = "\n".join(assignment_contents)
        

        result = {
            "path": path,
            "type": "configuration",
            "name": "module_config",
            "start_line": start_line,
            "end_line" : end_line,
            "content" : assign,
            "source_ranges": source_ranges
        }
        
        chunks.append(result)

            

    return chunks