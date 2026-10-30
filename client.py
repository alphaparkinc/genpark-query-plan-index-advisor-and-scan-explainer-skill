"""Query Plan Index Advisor & Scan Explainer.
100% Python Standard Library.
"""

class QueryPlanIndexAdvisor:
    """Analyzes query plan nodes to flag full table scans and cartesian joins, suggesting optimal composite indexes."""

    @staticmethod
    def analyze_plan(plan_nodes: list) -> dict:
        critical_issues = []
        recommendations = []
        total_estimated_cost = 0.0

        for node in plan_nodes:
            node_type = node.get("node_type", "UNKNOWN")
            table = node.get("table_name", "unknown_table")
            cost = float(node.get("cost", 0.0))
            rows = int(node.get("rows", 0))
            filter_cols = node.get("filter_columns", [])
            join_type = node.get("join_type", "")
            total_estimated_cost += cost

            if node_type in ("Seq Scan", "Full Table Scan") and rows > 1000:
                critical_issues.append({
                    "issue": "FULL_TABLE_SCAN_HIGH_VOLUME",
                    "table": table,
                    "rows_scanned": rows,
                    "cost": cost
                })
                if filter_cols:
                    col_str = ", ".join(filter_cols)
                    idx_name = f"idx_{table}_{'_'.join(filter_cols)}"
                    recommendations.append({
                        "table": table,
                        "columns": filter_cols,
                        "ddl": f"CREATE INDEX {idx_name} ON {table} ({col_str});",
                        "estimated_speedup": "85%-98%"
                    })

            if join_type in ("Cartesian Join", "Nested Loop Cross"):
                critical_issues.append({
                    "issue": "CARTESIAN_JOIN_NO_PREDICATE",
                    "table": table,
                    "cost": cost,
                    "warning": "Cross join detected; exponential row expansion risk"
                })

        return {
            "analyzed_nodes_count": len(plan_nodes),
            "total_estimated_cost": round(total_estimated_cost, 2),
            "critical_issues_detected": critical_issues,
            "index_recommendations": recommendations,
            "health_status": "OPTIMAL" if not critical_issues else "INDEX_DEFICIENCY_DETECTED"
        }
