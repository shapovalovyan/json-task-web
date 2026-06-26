import TaskForm from "./components/TaskForm";
import TaskList from "./components/TaskList";
import CompletedTaskList from "./components/CompletedTaskList";
import Footer from "./components/Footer";
import { useTask } from "./TaskProvider";

function App() {
  const { openSection, toggleSection, sortType, sortOrder, toggleSortOrder } =
    useTask();
  return (
    <dev className="app">
      <div className="task-container">
        <h1>Список задач с указанием Приоритетов</h1>
        <button
          className={`close-button ${openSection.taskList ? "open" : ""}`}
          onClick={() => toggleSection("taskList")}
        >
          +
        </button>
        {openSection.taskList && <TaskForm />}
      </div>

      <div className="task-container">
        <h2>Задачи</h2>
        <button
          className={`close-button ${openSection.tasks ? "open" : ""}`}
          onClick={() => toggleSection("tasks")}
        >
          +
        </button>
        <div className="sort-controls">
          <button
            className={`sort-button ${sortType === "date" ? "active" : ""}`}
            onClick={() => toggleSortOrder("date")}
          >
            По дате
            {sortType === "date" && (sortOrder === "asc" ? "\u2191" : "\u2193")}
          </button>
          <button
            className={`sort-button ${sortType === "priority" ? "active" : ""}`}
            onClick={() => toggleSortOrder("priority")}
          >
            По приоритету
            {sortType === "priority" &&
              (sortOrder === "asc" ? "\u2191" : "\u2193")}
          </button>
        </div>
        {openSection.tasks && <TaskList />}
      </div>

      <div className="completed-task-container">
        <h2>Выполненые задачи</h2>
        <button
          className={`close-button ${openSection.completedTasks ? "open" : ""}`}
          onClick={() => toggleSection("completedTasks")}
        >
          +
        </button>
        {openSection.completedTasks && <CompletedTaskList />}
      </div>
      <Footer />
    </dev>
  );
}

export default App;
