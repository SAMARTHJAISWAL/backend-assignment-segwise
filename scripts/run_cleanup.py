from app.services.scheduler import cleanup_archived_events, cleanup_old_logs

if __name__ == "__main__":
    print("Running cleanup_archived_events...")
    cleanup_archived_events()
    print("Archived events cleanup completed.")

    print("Running cleanup_old_logs...")
    cleanup_old_logs()
    print("Old logs cleanup completed.")
