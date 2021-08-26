
def multi_progress_bars(links: list[str]) -> None:
    number_of_tasks = len(links)
    task_dict = []
    with Progress() as progress:
        #creating tasks
        for task_url in links:
            task_dict.append(progress.add_task(f"[red]Downloading...{task_url}", total=100))

        while not progress.finished:
            for task in task_dict:
                progress.update(task, advance=1)
            
            sleep(1)