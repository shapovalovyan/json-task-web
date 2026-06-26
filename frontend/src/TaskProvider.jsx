import { useEffect, createContext, useState, useContext } from "react";

export const TaskContext = createContext();

export default function TaskProvider({ children }) {
  const [tasks, setTasks] = useState([]);
  const [sortType, setSortType] = useState("date");
  const [sortOrder, setSortOrder] = useState("asc");
  const [currentTime, setCurrentTime] = useState(new Date());
  const [openSection, setOpenSection] = useState({
    taskList: false,
    tasks: true,
    completedTasks: true,
  });

  useEffect(() => {
    fetch("/api/todos")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Ошибка загрузки");
        }
        return res.json();
      })
      .then((data) => {
        setTasks(data);
      })
      .catch(console.error);
  }, []);

  function toggleSection(section) {
    setOpenSection((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  }

  function addTask(task) {
    fetch("/api/todos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: task.title,
        priority: task.priority,
        deadLine: task.deadLine,
        completed: false,
      }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка создания");
        return res.json();
      })
      .then((updatedTodos) => {
        setTasks(updatedTodos);
      })
      .catch(console.error);
  }

  function deleteTask(id) {
    fetch(`/api/todos/${id}`, { method: "DELETE" })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка удаления");
        return res.json();
      })
      .then((updatedTodos) => setTasks(updatedTodos))
      .catch(console.error);
  }

  function completeTask(id) {
    fetch(`/api/todos/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: true }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка обновления");
        return res.json();
      })
      .then((updatedTodos) => setTasks(updatedTodos))
      .catch(console.error);
  }

  function sortTask(tasks) {
    return tasks.slice().sort((a, b) => {
      if (sortType === "priority") {
        const priorityOrder = { High: 1, Medium: 2, Low: 3 };
        return sortOrder == "asc"
          ? priorityOrder[a.priority] - priorityOrder[b.priority]
          : priorityOrder[b.priority] - priorityOrder[a.priority];
      } else {
        return sortOrder === "asc"
          ? new Date(a.deadLine) - new Date(b.deadLine)
          : new Date(b.deadLine) - new Date(a.deadLine);
      }
    });
  }

  function toggleSortOrder(type) {
    if (sortType === type) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortType(type);
      setSortOrder("asc");
    }
  }

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);

    return () => clearInterval(timer);
  }, []);

  const activeTasks = sortTask(tasks.filter((task) => !task.completed));
  const completedTasks = sortTask(tasks.filter((task) => task.completed));
  return (
    <TaskContext.Provider
      value={{
        sortType,
        sortOrder,
        openSection,
        currentTime,
        toggleSection,
        addTask,
        deleteTask,
        completeTask,
        sortTask,
        toggleSortOrder,
        activeTasks,
        completedTasks,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
}

export function useTask() {
  const context = useContext(TaskContext);
  return context;
}
