import TaskItem from "./TaskItem";
import { useTask } from "../TaskProvider";

export default function TaskList() {
  const { activeTasks, currentTime } = useTask();

  return (
    <ul className="task-list">
      {activeTasks.map((task) => (
        <TaskItem
          isOverDueFlag={new Date(task.deadLine) < currentTime}
          task={task}
          key={task.id}
        />
      ))}
    </ul>
  );
}
