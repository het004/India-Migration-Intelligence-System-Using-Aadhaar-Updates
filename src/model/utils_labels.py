def semantic_label(cluster_id):
    mapping = {
        0: "Metro Absorption Hubs",
        1: "Student Migration Hubs",
        2: "Economic Origin Belts",
        3: "Stable Districts"
    }
    return mapping.get(cluster_id, "Unknown")
