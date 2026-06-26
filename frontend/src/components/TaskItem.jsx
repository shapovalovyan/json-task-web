export default function TaskItem({
  task,
  deleteTask,
  completeTask,
  isOverDueFlag,
}) {
  const { title, priority, deadLine, id, completed } = task;

  return (
    <li
      className={`task-item ${priority.toLowerCase()} ${
        isOverDueFlag ? "overdue" : ""
      }`}
    >
      <div className="task-info">
        <div>
          {title} <strong>{priority}</strong>
        </div>
        <div className="task-deadline">
          Дата: {new Date(deadLine).toLocaleString()}
        </div>
      </div>
      <div className="task-buttons">
        {!completed && (
          <button className="complete-button" onClick={() => completeTask(id)}>
            Выполнить
          </button>
        )}

        <button className="delete-button" onClick={() => deleteTask(id)}>
          Удалить
        </button>
      </div>
    </li>
  );
}
