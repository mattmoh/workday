get_workers = input("Do you want to Get Workers? (y/n): ")
if get_workers.lower() == 'y':
    import workday_get_workers
    workday_get_workers.main()

put_accounting_center_batch = input("Do you want to Initiate Accounting Center Batch? (y/n): ")
if put_accounting_center_batch.lower() == 'y':
    import workday_put_accounting_center_batch
    workday_put_accounting_center_batch.main()

clean_dir = input("Do you want to clean the output directory? (y/n): ")
if clean_dir.lower() == 'y':
    import clean_output_dir
    clean_output_dir.main()