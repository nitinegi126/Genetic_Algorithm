# SPDS PROJECT
# Genetic Algorithm for multiprocessor scheduling
# ANAMIKA BASRAL 2020CSM1004
# AKSHAY KUMAR DIXIT 2020CSM1003

import random

population_size = 150  # population size
Max_Iterations = 1500  # maximum number of iterations
Cross_Prob = 1.0
Mut_Prob = 0.05
Max_FT = 0
MAX_H_1 = 0
best_Sched = []
task_cnt, edges_cnt, proc_cnt = map(int, input().split())
min_value = 9999999999
task_h = []
task_h_1 = []
set_succ = []
set_pre = []

i = 0
while i < task_cnt:
    task_h_1.append(-1)  # set task_h_1 of all task as -1 in start
    task_h.append(-1)  # set task_h of all task as -1 in start
    set_succ.append([])  # create set_succ[[]]
    set_pre.append([])  # create set_pre[[]]
    i = i + 1

time = list(map(int, input().split()))
task_DAG = []

for i in range(task_cnt):
    task_DAG.append([])
    for j in range(task_cnt):
        task_DAG[i].append(0)


def main():
    i = 0
    while i < edges_cnt:
        first, second = map(int, input().split())
        task_DAG[first][second] = 1
        i = i + 1
    for i in range(task_cnt):
        for j in range(task_cnt):
            if task_DAG[i][j] == 1:
                set_succ[i].append(j)
                set_pre[j].append(i)
    # print(graph)
    i = 0
    while i < task_cnt:
        cal_task_H(i)
        i += 1
    # print(task_h)
    cal_taskH_1()  # calculate improved height
    # print(task_h_1)
    calc_makespan()   # calculate the makespan length


def cal_min_max_ft(FT_list, j, MIN_FT):
    global Max_FT
    Max_FT = max(Max_FT, FT_list[j])
    MIN_FT = min(MIN_FT, FT_list[j])
    return Max_FT, MIN_FT


def calc_makespan():
    global Max_Iterations, Max_FT
    global Cross_Prob, best_Sched
    min_val = 99999999
    sched_pop = []  # 2d list of schedules random population
    i = 0
    while i < population_size:    # Generating initial population
        print("Iteration: " + str(i))
        initial_pop = Initialization_Sched()
        sched_pop.append(initial_pop)
        print(initial_pop)
        i += 1
    MIN_FT = 0
    bs = min_val   # best FT uptil now
    best_schedule = []   # will hold the best schedule
    it_cnt = 0
    while it_cnt < Max_Iterations:  # Running loop for no of iterations
        FT_list = []  # holds the  FT of schedules
        MIN_FT = min_val   # current min FT
        l = len(sched_pop)   # length of the schedules
        j = 0
        while j < l:
            FT_list.append(cal_SchedFT(sched_pop[j]))   # calculate FT of each population and add to FT_list
            Max_FT, MIN_FT = cal_min_max_ft(FT_list, j, MIN_FT)  # calculate Max_FT and min_FT uptil now
            j = j + 1

        bs = min(bs, MIN_FT)  # min_FT value stored in bs variable
        sum_FS = 0  # for sum of all fitness score
        j = 0
        fitness_score = []
        min_index_FS = -1
        min_FS = min_val
        while j < population_size:   # for all the schedules

            fitness_score.append(Max_FT - FT_list[j])  # calculate the FT score of each population
            sum_FS = sum_FS + fitness_score[j]  # find the sum of all FT score
            if fitness_score[j] < min_FS :
                min_FS = fitness_score[j]
                min_index_FS = j  # Note the schedule index of the best schedule
            j += 1

        if len(best_schedule):
            sched_pop[min_index_FS] = list(best_schedule)  # replace schedule with with min FS with the best schedule

        new_sched_pop, best_Sched = Reproduction(sched_pop, fitness_score, sum_FS)  # perform reproduction
        new_sched_temp = []
        j = 0
        len_schedpop = len(sched_pop)
        while j < len_schedpop:
            newschedule1, newschedule2 = crossover(new_sched_pop[j], new_sched_pop[j + 1], Cross_Prob)
            new_sched_temp.extend((newschedule1, newschedule2))
            j = j + 2

        sched_pop = []
        for s in new_sched_temp:
            newsch = list(mutation(s, Mut_Prob))
            sched_pop.append(newsch)
        if best_schedule == [] or cal_SchedFT(best_Sched) < cal_SchedFT(best_schedule):
            best_schedule = best_Sched

        it_cnt += 1

    print("Processor Wise Task Schedule")
    temp_sched = cal_SchedFT(best_schedule)
    for a in best_schedule:
        print(a)
    print("Finishing time of schedule = " + str(temp_sched) + "\n")


def mutation(sched, mut_prob):
    new_sched = list(sched)
    ran_num = random.uniform(0, 1)
    if ran_num > mut_prob:  # regularizing with mutation probability
        return new_sched

    ran_num = random.randint(0, task_cnt - 1)
    pnt_i = 0
    pnt_j = 0
    i = 0
    while i < proc_cnt:
        j = 0
        while j < len(new_sched[i]):
            if new_sched[i][j] == ran_num:
                pnt_i = i
                pnt_j = j
                break
            j += 1
        i += 1

    flag = 0
    i = 0
    while i < proc_cnt:
        j = 0
        while j < len(new_sched[i]):
            x = task_h_1[new_sched[i][j]]
            y = task_h_1[ran_num]
            if x == y and new_sched[i][j] != ran_num:
                flag = 1
                new_sched[i][j], new_sched[pnt_i][pnt_j] = new_sched[pnt_i][pnt_j], new_sched[i][j]
                break
            j += 1
        if flag == 1:
            break
        i += 1

    return new_sched


def perform_crossover(sched_1, sched_1j, sched_2j, sched_2, new_sched_1, new_sched_2, i):
    if sched_2j != len(sched_2[i]):
        new_sched_1[i] = sched_1[i][:sched_1j] + sched_2[i][sched_2j:]

    else:
        new_sched_1[i] = sched_1[i][:sched_1j]

    if sched_1j != len(sched_1[i]):
        new_sched_2[i] = sched_2[i][:sched_2j] + sched_1[i][sched_1j:]

    else:
        new_sched_2[i] = sched_2[i][:sched_2j]
    return new_sched_1[i], new_sched_2[i]


def crossover(sched_1, sched_2, cross_prob):
    global proc_cnt, task_h_1
    c = random.uniform(0, 1)
    if c > cross_prob:  # regularising with crossover probability
        return sched_1, sched_2

    new_sched_1 = []
    new_sched_2 = []
    for i in range(proc_cnt):   # initialize two new sched 1 and 2
        new_sched_1.append([])
        new_sched_2.append([])

    ran_h = random.randint(0, MAX_H_1)  # find the cross over sites
    i = 0
    while i < proc_cnt:
        sched_1j = len(sched_1[i])
        j = 0
        while j < len(sched_1[i]):
            if task_h_1[sched_1[i][j]] > ran_h:   # check the height condition
                sched_1j = j
                break
            j += 1

        sched_2j = len(sched_2[i])
        j = 0
        while j < len(sched_2[i]):
            if task_h_1[sched_2[i][j]] > ran_h:   # check the height condition
                sched_2j = j
                break
            j += 1
        new_sched_1[i], new_sched_2[i] = perform_crossover(sched_1, sched_1j, sched_2j, sched_2, new_sched_1,
                                                           new_sched_2, i)
        i += 1

    return new_sched_1, new_sched_2


def Reproduction(sched_pop, fitness_score, sum_FS):  # give slots to schedules as per their FT
    new_sched_pop = [] # create a new schedule 2D list
    i = 1
    while i < len(sched_pop):
        r = random.randint(1, sum_FS)
        temp = 0
        j = 0
        while j < population_size:  # for all populations
            temp += fitness_score[j]
            if r <= temp:
                new_sched_pop.append(sched_pop[j])
                break
            j += 1
        i += 1
    max_index_FS = -1
    temp_FS = 0
    j = 0
    while j < population_size:       # find the best schedule of previous population add to the current new sched
        if fitness_score[j] > temp_FS:
            temp_FS = fitness_score[j]
            max_index_FS = j
        j += 1

    new_sched_pop.append(sched_pop[max_index_FS])
    return new_sched_pop, sched_pop[max_index_FS]


def cal_SchedFT(Schedule):
    st_pnt = []  # start time of task
    fn_pnt = []  # finishing time of task
    proc_comp = []  # processor task list completed or not
    indi_task = []  # individual task list
    previous = []   # previous task
    i = 0

    while i < task_cnt:
        st_pnt.append(-1)   # initialize start time of task as -1
        fn_pnt.append(-1)   # initialize start time of task as -1
        proc_comp.append(0) # processor done for the task
        previous.append(-1)  # previous of the task
        i += 1

    for proc_string in Schedule:  # for each individual processor wise task list
        l = len(proc_string)
        j = 0
        while j < l:
            indi_task.append(proc_string[j])    # add all task in the indi_task list from the schedule
            j = j + 1
    i = 0
    while i < proc_cnt:  # for all processors
        l = len(Schedule[i])  # task list length of the processor
        j = 1
        while j < l:
            previous[Schedule[i][j]] = Schedule[i][j - 1]  # add previous of all task as per Graph
            j = j + 1
        i += 1

    while len(indi_task) > 0:  # for task in task list
        k = indi_task[-1]      # last task number

        l = len(set_pre[k])    # length predecessor of last task
        flag = 0
        if not proc_comp[k]:    # if last task proc is not completed
            if previous[k] == -1:  # if its previous task is not there
                if not l:       # if pred list is empty
                    proc_comp[k] = 1 # mark computed
                    st_pnt[k] = 0  # start time =0
                    fn_pnt[k] = time[k] # FT = computation time of task k
                    indi_task.pop() # remove task from the task list
                    continue

            for m in set_pre[k]:  # for all the pred of the task
                if not proc_comp[m]: # if they are not computed add to the indi task list
                    indi_task.append(m)
                    flag = 1

            if previous[k] > -1:  # if previous exist
                if previous[k] not in set_pre[k]:  # and it is not in pred list
                    if proc_comp[previous[k]] == 0:  # and if its  previous not computed flag =1
                        flag = 1
                        indi_task.append(previous[k]) # add in individual list

            if not flag: # if flag not changed we found the task with no pred and no previous comp left
                for pred in set_pre[k]:
                    st_pnt[k] = max(st_pnt[k], fn_pnt[pred])
                if previous[k] > -1:
                    if previous[k] not in set_pre[k]:
                        st_pnt[k] = max(st_pnt[k], fn_pnt[previous[k]])

                proc_comp[k] = 1
                indi_task.pop()  # remove that task from the list
                fn_pnt[k] = st_pnt[k] + time[k]


        else:
            indi_task.pop()

    return max(fn_pnt)


def cal_min_maxH(i):
    height_max = -1
    height_min = min_value
    for task in set_pre[i]:  # calcuate height_max
        if task_h[task] > height_max:
            height_max = task_h[task]

    for task in set_succ[i]:
        if (task_h[task] < height_min): # calcuate height_min
            height_min = task_h[task]
    return height_max, height_min


def cal_taskH_1():
    global MAX_H_1, task_h_1
    MAX_H_1 = 0
    i = 0
    while i < task_cnt:   # calculate task_h_1 for all task
        height_max, height_min = cal_min_maxH(i)
        if height_max == -1 or height_min == 9999999999:
            task_h_1[i] = task_h[i]
        else:
            task_h_1[i] = random.randint(height_max + 1, height_min - 1)
        MAX_H_1 = max(MAX_H_1, task_h_1[i])
        i = i + 1


def add_TaskstoProc(iter_h, listG, setGTemp, task_S, proc_num, ran_cnt, i):  # Adding ran_cnt task from listG to the proc list task_S
    z = 0
    for task_iter in listG[iter_h]:  # adding task to the processor list
        z += 1
        task_S[proc_num[i]].append(task_iter)
        setGTemp.remove(task_iter)

        if z >= ran_cnt:
            break

    listG[iter_h] = set(setGTemp)
    return listG, task_S, setGTemp


def Initialization_Sched():  # Create Random Schedules as part of Initialization
    global task_h_1, proc_cnt, MAX_H_1
    listG = []  # will hold the set of task according to height
    i = 0
    while i < (MAX_H_1 + 1):   # create listG a list of set
        listG.append(set())
        i += 1
    i = 0
    while i < task_cnt:  # Adding task in listG according to the heights
        listG[task_h_1[i]].add(i)
        i += 1
    task_S = []
    for i in range(proc_cnt):  # Initialize task Schedule list for all processors
        task_S.append([])
    proc_num = []
    for i in range(proc_cnt):  # Processor list
        proc_num.append(i)

    # print(proc_num[-1])
    i = 0
    while i < proc_cnt - 1:  # for the first proc_cnt-1 processors
        iter_h = 0
        while iter_h < MAX_H_1 + 1:
            if len(listG[iter_h]):
                ran_cnt = random.randint(0, len(listG[iter_h]))
                setGTemp = set(listG[iter_h])
                listG, task_S, setGTemp = add_TaskstoProc(iter_h, listG, setGTemp, task_S, proc_num, ran_cnt, i)
            iter_h += 1
        i += 1

    # Last processor add remaining elements to schedule list
    iter_h = 0
    while iter_h < MAX_H_1 + 1:
        l = len(listG[iter_h])
        if l:
            setGTemp = set(listG[iter_h])
            for task_iter in listG[iter_h]:
                task_S[proc_num[-1]].append(task_iter)
                setGTemp.remove(task_iter)

            listG[iter_h] = setGTemp
        iter_h += 1

    return task_S


def cal_nonrootH(t):  # Find the max height of predecessor
    global task_h
    height_max = -1
    for a in set_pre[t]:  # for all predecessor of task t find the max height
        t = cal_task_H(a)
        if t > height_max:
            height_max = t
    return height_max


def cal_task_H(t):
    global task_h
    if task_h[t] > -1:  # if height already found , anchor condition
        return task_h[t]

    if len(set_pre[t]):
        task_h[t] = cal_nonrootH(t) + 1  # for non root code , Find the max height of predecessor and add 1
    else:
        # if no pred means root set height as zero
        task_h[t] = 0

    return task_h[t]


main()
