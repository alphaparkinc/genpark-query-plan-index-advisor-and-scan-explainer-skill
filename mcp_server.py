"""MCP server for Query Plan Index Advisor & Scan Explainer."""
import sys
import json
from client import QueryPlanIndexAdvisor

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "analyze_plan",
                    "description": "Analyze execution plan nodes for scans and Cartesian joins to advise indexes",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "plan_nodes": {"type": "array"}
                        },
                        "required": ["plan_nodes"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "analyze_plan":
            out = QueryPlanIndexAdvisor.analyze_plan(args.get("plan_nodes", []))
            return {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
    return {"error": "Unsupported method or tool"}

if __name__ == "__main__":
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
