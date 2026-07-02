const API = '/api/items';

const form = document.getElementById('item-form');
const formTitle = document.getElementById('form-title');
const itemIdInput = document.getElementById('item-id');
const nameInput = document.getElementById('name');
const descriptionInput = document.getElementById('description');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const refreshBtn = document.getElementById('refresh-btn');
const statusEl = document.getElementById('status');
const itemsList = document.getElementById('items-list');

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.toggle('error', isError);
}

function resetForm() {
  formTitle.textContent = 'Add Item';
  submitBtn.textContent = 'Add Item';
  itemIdInput.value = '';
  form.reset();
  cancelBtn.hidden = true;
}

function startEdit(item) {
  formTitle.textContent = 'Edit Item';
  submitBtn.textContent = 'Save Changes';
  itemIdInput.value = item._id;
  nameInput.value = item.name;
  descriptionInput.value = item.description || '';
  cancelBtn.hidden = false;
  nameInput.focus();
}

function renderItems(items) {
  itemsList.innerHTML = '';

  if (!items.length) {
    itemsList.innerHTML = '<li class="empty">No items yet. Add one above.</li>';
    return;
  }

  items.forEach((item) => {
    const li = document.createElement('li');
    li.className = 'item';
    li.innerHTML = `
      <div class="item-info">
        <h3>${escapeHtml(item.name)}</h3>
        <p>${escapeHtml(item.description || 'No description')}</p>
        <div class="item-meta">ID: ${item._id}</div>
      </div>
      <div class="item-actions">
        <button type="button" class="secondary edit-btn">Edit</button>
        <button type="button" class="danger delete-btn">Delete</button>
      </div>
    `;

    li.querySelector('.edit-btn').addEventListener('click', () => startEdit(item));
    li.querySelector('.delete-btn').addEventListener('click', () => deleteItem(item._id));
    itemsList.appendChild(li);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function loadItems() {
  setStatus('Loading...');
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error('Failed to load items');
    const items = await res.json();
    renderItems(items);
    setStatus(`${items.length} item(s)`);
  } catch (err) {
    setStatus(err.message, true);
    itemsList.innerHTML = '';
  }
}

async function saveItem(event) {
  event.preventDefault();

  const payload = {
    name: nameInput.value.trim(),
    description: descriptionInput.value.trim(),
  };

  const id = itemIdInput.value;
  const isEdit = Boolean(id);

  try {
    const res = await fetch(isEdit ? `${API}/${id}` : API, {
      method: isEdit ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Save failed');

    resetForm();
    await loadItems();
  } catch (err) {
    setStatus(err.message, true);
  }
}

async function deleteItem(id) {
  if (!confirm('Delete this item?')) return;

  try {
    const res = await fetch(`${API}/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Delete failed');
    await loadItems();
  } catch (err) {
    setStatus(err.message, true);
  }
}

form.addEventListener('submit', saveItem);
cancelBtn.addEventListener('click', resetForm);
refreshBtn.addEventListener('click', loadItems);

loadItems();
