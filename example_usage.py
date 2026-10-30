"""Example usage for Query Plan Index Advisor & Scan Explainer."""
from client import QueryPlanIndexAdvisor

if __name__ == "__main__":
    nodes = [
        {"node_type": "Seq Scan", "table_name": "orders", "rows": 85000, "cost": 3400.0, "filter_columns": ["customer_id", "status"]},
        {"node_type": "Index Scan", "table_name": "users", "rows": 1, "cost": 4.5}
    ]
    report = QueryPlanIndexAdvisor.analyze_plan(nodes)
    print("Plan Health:", report["health_status"])
    print("Recommendations:", report["index_recommendations"])
