import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import "./index.css";
import HomePage from "./pages/HomePage";
import GamePage from "./pages/GamePage";

createRoot(document.getElementById("root")!).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/game/:gameId" element={<GamePage />} />
    </Routes>
  </BrowserRouter>,
);
