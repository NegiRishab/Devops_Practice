const { test, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const app = require('../src/app');

let mongoServer;

before(async () => {
  mongoServer = await MongoMemoryServer.create();
  await mongoose.connect(mongoServer.getUri());
});

after(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

beforeEach(async () => {
  await mongoose.connection.dropDatabase();
});

test('GET /api/health returns ok', async () => {
  const res = await request(app).get('/api/health');

  assert.equal(res.status, 200);
  assert.equal(res.body.status, 'ok');
  assert.equal(res.body.message, 'Task Board API is running');
});

test('GET /api/tasks returns empty array initially', async () => {
  const res = await request(app).get('/api/tasks');

  assert.equal(res.status, 200);
  assert.deepEqual(res.body, []);
});

test('POST /api/tasks creates a task', async () => {
  const res = await request(app)
    .post('/api/tasks')
    .send({ title: 'Write tests', description: 'Add CI tests' });

  assert.equal(res.status, 201);
  assert.equal(res.body.title, 'Write tests');
  assert.equal(res.body.description, 'Add CI tests');
  assert.ok(res.body._id);
});

test('POST /api/tasks rejects missing title', async () => {
  const res = await request(app).post('/api/tasks').send({ description: 'No title' });

  assert.equal(res.status, 400);
  assert.match(res.body.message, /Title is required/);
});

test('GET /api/tasks/:id returns task by id', async () => {
  const created = await request(app)
    .post('/api/tasks')
    .send({ title: 'Fetch me' });

  const res = await request(app).get(`/api/tasks/${created.body._id}`);

  assert.equal(res.status, 200);
  assert.equal(res.body.title, 'Fetch me');
});

test('GET /api/tasks/:id returns 404 for unknown id', async () => {
  const fakeId = new mongoose.Types.ObjectId();
  const res = await request(app).get(`/api/tasks/${fakeId}`);

  assert.equal(res.status, 404);
  assert.equal(res.body.message, 'Task not found');
});

test('DELETE /api/tasks/:id removes task', async () => {
  const created = await request(app)
    .post('/api/tasks')
    .send({ title: 'Delete me' });

  const deleted = await request(app).delete(`/api/tasks/${created.body._id}`);

  assert.equal(deleted.status, 200);
  assert.equal(deleted.body.message, 'Task deleted');

  const list = await request(app).get('/api/tasks');
  assert.equal(list.body.length, 0);
});
