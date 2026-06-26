import TaskItem from "./TaskItem";

export default function TaskList({
  activeTasks,
  deleteTask,
  completeTask,
  currentTime,
}) {
  return (
    <ul className="task-list">
      {activeTasks.map((task) => (
        <TaskItem
          isOverDueFlag={new Date(task.deadLine) < currentTime}
          deleteTask={deleteTask}
          completeTask={completeTask}
          task={task}
          key={task.id}
        />
      ))}
    </ul>
  );
}
