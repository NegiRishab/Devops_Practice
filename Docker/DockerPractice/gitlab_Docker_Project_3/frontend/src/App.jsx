import { useEffect, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080/api";

const emptyForm = {
  name: "",
  email: "",
  employed: true,
  timing: "",
  role: "",
  department: ""
};

function App() {
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchEmployees = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_BASE}/employees`);
      if (!response.ok) throw new Error("Failed to fetch employees");
      const data = await response.json();
      setEmployees(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    const url = editingId ? `${API_BASE}/employees/${editingId}` : `${API_BASE}/employees`;
    const method = editingId ? "PUT" : "POST";

    try {
      const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });
      if (!response.ok) {
        throw new Error(`Failed to ${editingId ? "update" : "create"} employee`);
      }
      resetForm();
      fetchEmployees();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (employee) => {
    setForm({
      name: employee.name,
      email: employee.email,
      employed: employee.employed,
      timing: employee.timing || "",
      role: employee.role || "",
      department: employee.department || ""
    });
    setEditingId(employee.id);
  };

  const handleDelete = async (id) => {
    setError("");
    try {
      const response = await fetch(`${API_BASE}/employees/${id}`, {
        method: "DELETE"
      });
      if (!response.ok) throw new Error("Failed to delete employee");
      fetchEmployees();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h1>Company Employees</h1>
      <p className="subtitle">Manage employee details, roles, timing, and employment status.</p>

      {error && <p className="error">{error}</p>}

      <form className="employee-form" onSubmit={handleSubmit}>
        <input name="name" value={form.name} onChange={handleChange} placeholder="Name" required />
        <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="Email" required />
        <input name="role" value={form.role} onChange={handleChange} placeholder="Role" required />
        <input name="department" value={form.department} onChange={handleChange} placeholder="Department" required />
        <input name="timing" value={form.timing} onChange={handleChange} placeholder="Timing (e.g. 09:00-17:00)" required />
        <label className="checkbox">
          <input name="employed" type="checkbox" checked={form.employed} onChange={handleChange} />
          Employed
        </label>
        <div className="actions">
          <button type="submit">{editingId ? "Update Employee" : "Add Employee"}</button>
          {editingId && (
            <button type="button" className="secondary" onClick={resetForm}>
              Cancel
            </button>
          )}
        </div>
      </form>

      <h2>Employee List</h2>
      {loading ? (
        <p>Loading employees...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Department</th>
              <th>Timing</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((employee) => (
              <tr key={employee.id}>
                <td>{employee.name}</td>
                <td>{employee.email}</td>
                <td>{employee.role}</td>
                <td>{employee.department}</td>
                <td>{employee.timing}</td>
                <td>{employee.employed ? "Employed" : "Not Employed"}</td>
                <td className="row-actions">
                  <button type="button" onClick={() => handleEdit(employee)}>
                    Edit
                  </button>
                  <button type="button" className="danger" onClick={() => handleDelete(employee.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
