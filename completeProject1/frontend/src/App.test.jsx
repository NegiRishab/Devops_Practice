import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';

vi.mock('./api', () => ({
  api: {
    getTasks: vi.fn().mockResolvedValue([
      { _id: '1', title: 'Sample task', description: 'Demo' },
    ]),
    createTask: vi.fn(),
    deleteTask: vi.fn(),
  },
}));

describe('App', () => {
  it('renders the Task Board heading', async () => {
    render(<App />);
    expect(await screen.findByText('Task Board')).toBeInTheDocument();
  });

  it('renders tasks from the API', async () => {
    render(<App />);
    expect(await screen.findByText('Sample task')).toBeInTheDocument();
  });

  it('shows empty state when there are no tasks', async () => {
    const { api } = await import('./api');
    api.getTasks.mockResolvedValueOnce([]);

    render(<App />);
    expect(await screen.findByText('No tasks yet')).toBeInTheDocument();
  });
});
