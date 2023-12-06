# MADE BY. 
# INSUNG HWANG  
# 1TE22533R   
# 九州大学 工学部 航空宇宙工学科
# 2023/12/06

import streamlit as st
from datetime import datetime

def main():
    if 'tasks' not in st.session_state:
        st.session_state['tasks'] = []

    st.title("TASK")

    display_task()
    if st.sidebar.button("Remove All"):
        clear_task()

    tab1, tab2, tab3, tab4 = st.tabs(["HOME", "SHOW", "ADD", "EDIT & DELETE"])
    with tab1:
        home()
    with tab2:
        show()
    with tab3:
        add_task()
    with tab4:
        edit_task()


def display_task():
    st.sidebar.title("Task List")
    for task_name, task_date, task_thing in st.session_state.tasks:
        st.sidebar.write('・ ' , task_name)


def home():
    st.header("Welcome!")
    st.write('\n')
    st.write("MADE BY.")
    st.write("INSUNG HWANG  1TE22533R")
    st.write("工学部    航空宇宙工学科")
    st.write("hwang.insung.762@s.kyushu-u.ac.jp")


def show():
    selected_taskname = st.selectbox("Choose Task To Show", [task_name for task_name, _, _ in st.session_state.tasks], key="select_box_in_show")

    if selected_taskname:
        selected_task = next(task for task in st.session_state.tasks if task[0] == selected_taskname)
        selected_date = selected_task[1]
        selected_taskthing = selected_task[2]

        st.markdown(f"**Task Name:** {selected_taskname}")
        st.markdown(f"**Deadline:** {selected_date}")
        st.markdown(f"**Task Detail:** {selected_taskthing}")


def add_task():
    st.header("Add Task")

    task_name = st.text_input("Input Task name")
    task_date = str(st.date_input("Deadline"))
    task_thing = st.text_area("Input Task")

    if(st.button("SAVE", key="save_button_in_addtask")):
        if task_name and task_date and task_thing:
            new_task_name = task_name
            id = 1
            while any(existing_task[0] == new_task_name for existing_task in st.session_state.tasks):
                new_task_name = f"{task_name} ({id})"
                id += 1
            st.session_state.tasks.append((new_task_name, str(task_date), task_thing))
            st.experimental_rerun()


def edit_task():
    selected_taskname = st.selectbox("Choose Task To Edit", [task_name for task_name, _, _ in st.session_state.tasks])

    if selected_taskname:
        selected_task = next(task for task in st.session_state.tasks if task[0] == selected_taskname)
        selected_date = selected_task[1]
        selected_taskthing = selected_task[2]
        edited_taskname = st.text_input("Edit Task name", value=selected_taskname)
        edited_date = st.date_input("Edit Deadline", value=datetime.strptime(selected_date.strip(), "%Y-%m-%d"))
        edited_taskthing = st.text_area("Edit Task", value=selected_taskthing)

        if st.button("SAVE"):
            st.session_state.tasks.remove(selected_task)
            st.session_state.tasks.append((edited_taskname, str(edited_date), edited_taskthing))
            st.experimental_rerun()

        elif st.button("DELETE"):
            st.session_state.tasks.remove(selected_task)
            st.experimental_rerun()

def clear_task():
    st.session_state.tasks = []
    st.experimental_rerun()

if __name__ == "__main__":
    main()


# 最初は、.txtファイルを用いて値を入れたり出したりしようとした。
# だが、他のパソコンで駆動できるか疑問（指定した.txtファイルがパソコンにあるか、無かったら作る、.txtから値を入れたり出したり）
# どんなパソコンでも駆動できるように、st.session_stateを用いてこのアプリに直接値をセーブすることにした。
# → コードが簡潔になった。

# この前、HTMLについて少し勉強したことがあって、「ADD」と「EDIT＆DELETE」を違うページのように作りたかった。
# APIで探すとtabということがあって、それを使った。
# そして、タスクのリストはいつでも見られるようにsidebarにおく。

# また、各演算過程は関数に定義し、より理解しやすくした。

# 一番難しいかったことは、SHOWやEDITにある、タスクを選択するところだった。
# 
# 初めは、selected_task = next(task for task in st.session_state.tasks if task[0] == selected_taskname) でSelectしたタスクの名前でタスクの内容と期限を探すようにした。
# しかし、同じ名前のタスクが既にあると指定したいタスクが指定できない場合が生じた。
# それで、ADDするとき、idという識別子（数字）をタスクの名前の前につけてセーブした。
# たが、DELETEとしても数字が残ってしまって、醜いと思って他の方法を模索。
# EX) 1. A
#     2. B    → DELETE 
#     3. C

#     1. A
#     3. C

# 普通のパソコンのように、もう同じ名前のタスクがあった場合のみ、その名前の後ろに（数字）をつけることにする。
# EX) 1. A
#     2. B
#     3. A (1)

# selected_task = next(task for task in st.session_state.tasks if task[0] == selected_taskname)
# selectboxから選択されたタスクの名前を用いて、st.session_state.tasksの中で、0番つまり初めの値（名前）が一致しているlistを探してselected_taskに入れる。
# そのselected_taskから、タスクの期限と内容の値も取り出せる。
# SHOWでは、選択したタスクを示すだけで、EDITでは、元の値を消して、新たな値を元のタスクに入れるだけである。
