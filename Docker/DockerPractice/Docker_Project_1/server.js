import "dotenv/config";
import express from "express";
import cors from "cors";
import mongoose from "mongoose";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);



const MONGO_URI = process.env.MONGO_URI || "mongodb://admin:pass@mongo:27017/todosdb?authSource=admin";
const PORT = Number(process.env.PORT) || 3000;

const CONNECT_RETRY_INITIAL_MS = Number(process.env.MONGO_RETRY_INITIAL_MS) || 1000;
const CONNECT_RETRY_MAX_MS = Number(process.env.MONGO_RETRY_MAX_MS) || 15000;

async function connectMongo(uri) {
  let delayMs = CONNECT_RETRY_INITIAL_MS;
  for (;;) {
    try {
      await mongoose.connect(uri, {
        serverSelectionTimeoutMS: 5000,
      });
      console.log("MongoDB connected");
      return;
    } catch (err) {
      console.error(
        `MongoDB not ready (${err.message}). Retrying in ${delayMs}ms…`
      );
      await new Promise((r) => setTimeout(r, delayMs));
      delayMs = Math.min(
        CONNECT_RETRY_MAX_MS,
        Math.floor(delayMs * 1.5)
      );
    }
  }
}

const todoSchema = new mongoose.Schema(
  {
    title: { type: String, required: true, trim: true, maxlength: 500 },
    completed: { type: Boolean, default: false },
  },
  { timestamps: true }
);

const Todo = mongoose.model("Todo", todoSchema);

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

app.get("/api/todos", async (_req, res) => {
  try {
    const todos = await Todo.find().sort({ createdAt: -1 }).lean();
    res.json(todos);
  } catch (err) {
    res.status(500).json({ error: "Failed to load todos" });
  }
});

app.post("/api/todos", async (req, res) => {
  try {
    const title = String(req.body?.title ?? "").trim();
    if (!title) {
      return res.status(400).json({ error: "Title is required" });
    }
    const todo = await Todo.create({ title });
    res.status(201).json(todo);
  } catch (err) {
    res.status(500).json({ error: "Failed to create todo" });
  }
});

app.patch("/api/todos/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const updates = {};
    if (typeof req.body?.title === "string") {
      const title = req.body.title.trim();
      if (!title) {
        return res.status(400).json({ error: "Title cannot be empty" });
      }
      updates.title = title;
    }
    if (typeof req.body?.completed === "boolean") {
      updates.completed = req.body.completed;
    }
    if (Object.keys(updates).length === 0) {
      return res.status(400).json({ error: "Nothing to update" });
    }
    const todo = await Todo.findByIdAndUpdate(id, updates, {
      new: true,
      runValidators: true,
    });
    if (!todo) {
      return res.status(404).json({ error: "Todo not found" });
    }
    res.json(todo);
  } catch (err) {
    if (err.name === "CastError") {
      return res.status(400).json({ error: "Invalid id" });
    }
    res.status(500).json({ error: "Failed to update todo" });
  }
});

app.delete("/api/todos/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const deleted = await Todo.findByIdAndDelete(id);
    if (!deleted) {
      return res.status(404).json({ error: "Todo not found" });
    }
    res.json({ ok: true, id });
  } catch (err) {
    if (err.name === "CastError") {
      return res.status(400).json({ error: "Invalid id" });
    }
    res.status(500).json({ error: "Failed to delete todo" });
  }
});

async function main() {
  await connectMongo(MONGO_URI);
  app.listen(PORT, () => {
    console.log(`Server http://localhost:${PORT}`);
    console.log(`MongoDB: ${MONGO_URI.replace(/\/\/.*@/, "//***@")}`);
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
