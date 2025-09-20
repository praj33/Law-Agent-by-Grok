from expanded_legal_sections import create_expanded_legal_database

db = create_expanded_legal_database()
stats = db.get_stats()
print(f"IPC Sections: {stats['total_ipc_sections']}")