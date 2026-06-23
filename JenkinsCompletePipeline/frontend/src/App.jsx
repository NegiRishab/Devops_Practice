import { useEffect, useState } from 'react';
import { api } from './api';

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');

  const loadTasks = async () => {
    try {
      setError('');
      setTasks(await api.getTasks());
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      const task = await api.createTask({ title, description });
      setTasks((prev) => [task, ...prev]);
      setTitle('');
      setDescription('');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.deleteTask(id);
      setTasks((prev) => prev.filter((t) => t._id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Task Board</h1>
        <p>Simple task manager — starter app</p>
      </header>

      {error && <p className="error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          required
        />
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
        />
        <button type="submit">Add Task</button>
      </form>

      <ul>
        {tasks.length === 0 ? (
          <li className="empty">No tasks yet</li>
        ) : (
          tasks.map((task) => (
            <li key={task._id}>
              <div>
                <strong>{task.title}</strong>
                {task.description && <p>{task.description}</p>}
              </div>
              <button onClick={() => handleDelete(task._id)}>Delete</button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
