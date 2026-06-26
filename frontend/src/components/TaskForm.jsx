import { useTask } from "../TaskProvider";

export default function TaskForm() {
  const { addTask } = useTask();
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("Low");
  const [deadLine, setDeadLine] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (title.trim() && deadLine) {
      addTask({ title, priority, deadLine });
      setTitle("");
      setPriority("Low");
      setDeadLine("");
    }
  }
  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        placeholder="название задачи"
        required
        onChange={(e) => setTitle(e.target.value)}
      />
      <select value={priority} onChange={(e) => setPriority(e.target.value)}>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>
      <input
        type="datetime-local"
        required
        value={deadLine}
        onChange={(e) => setDeadLine(e.target.value)}
      />
      <button type="submit">Добавить задачу</button>
    </form>
  );
}
