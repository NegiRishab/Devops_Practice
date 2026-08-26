import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api } from './api';

describe('api', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('getTasks fetches tasks from the API', async () => {
    const mockTasks = [{ _id: '1', title: 'Test task' }];
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockTasks),
      })
    );

    const tasks = await api.getTasks();

    expect(tasks).toEqual(mockTasks);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/tasks'),
      expect.objectContaining({ headers: expect.any(Object) })
    );
  });

  it('createTask sends POST with task body', async () => {
    const newTask = { _id: '2', title: 'New', description: 'Desc' };
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(newTask),
      })
    );

    const task = await api.createTask({ title: 'New', description: 'Desc' });

    expect(task).toEqual(newTask);
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/tasks'),
      expect.objectContaining({ method: 'POST' })
    );
  });

  it('throws when the API returns an error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        json: () => Promise.resolve({ message: 'Task not found' }),
      })
    );

    await expect(api.getTasks()).rejects.toThrow('Task not found');
  });
});
