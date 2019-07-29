import multiprocessing
from multi_processing_tasks.Task import Task

class MPTasks:
    def __init__(self, tasks_list, percentage_of_processors_to_use):
        self.percentage_of_processors_to_use = percentage_of_processors_to_use
        self.tasks_list = tasks_list
        self.num_of_processors_to_use = int(multiprocessing.cpu_count() * percentage_of_processors_to_use)
        if self.num_of_processors_to_use == 0:
            self.num_of_processors_to_use = 1
        self.lock = multiprocessing.RLock()
        self.ready_tasks = []
        self.processes_list = None

    def prepare_tasks_for_processes(self):
        processes_tasks_indexes_range = self.get_tasks_indexes_for_each_process()
        self.processes_list = [
            multiprocessing.Process(target=self.process_tasks_executor, args=(self.tasks_list[start_idx:end_idx],)) for
            start_idx, end_idx in processes_tasks_indexes_range]
        return self.processes_list

    def retrieve_tasks_results(self):
        if not self.processes_list:
            self.prepare_tasks_for_processes()
        [process.start() for process in self.processes_list]
        [process.join() for process in self.processes_list]
        return self.processes_list

    def get_tasks_indexes_for_each_process(self):
        processes_tasks_indexes_range = []
        tasks_length = len(self.tasks_list)
        num_of_tasks_for_each_process = tasks_length // self.num_of_processors_to_use
        counter = 0
        for i in range(1, self.num_of_processors_to_use + 1):
            processes_tasks_indexes_range.append([counter, num_of_tasks_for_each_process * i])
            counter = num_of_tasks_for_each_process * i
        processes_tasks_indexes_range[-1][1] += tasks_length % num_of_tasks_for_each_process
        return processes_tasks_indexes_range


    def process_tasks_executor(self,tasks_list):
        ready_tasks = []
        for task in tasks_list:
            task_res = task()
            self.lock.acquire()
            ready_tasks.append(task_res)
            self.lock.release()
        return ready_tasks


def super_pow(x, y):
    return x ** y ** 2

if __name__ == "__main__":
    import random


    tasks_list = [Task(super_pow,i,i+1) for i in range(255)]
    print(tasks_list)
    mptasks = MPTasks(tasks_list,0.5)
    print(mptasks.retrieve_tasks_results())