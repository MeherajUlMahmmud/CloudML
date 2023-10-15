import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomePage from "./pages/homePage/HomePage";
import AppLayout from "./components/AppLayout";
import LogoutPage from "./pages/auth/LogoutPage";
import LoginPage from "./pages/auth/LoginPage";
import AuthLayout from "./components/AuthLayout";
import ProjectDetailsPage from "./pages/projectDetailsPage/ProjectDetailsPage";
import DatasetDetailsPage from "./pages/datasetDetailsPage/DatasetDetailsPage";
import ModelDetailsPage from "./pages/modelDetailsPage/ModelDetailsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/project/:id" element={<ProjectDetailsPage />} />
          <Route path="/project/:id/dataset/:id" element={<DatasetDetailsPage />} />
          <Route path="/project/:id/dataset/:id/trained-model/:id" element={<ModelDetailsPage />} />
        </Route>
        <Route path="/auth" element={<AuthLayout />} >
          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/logout" element={<LogoutPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}


export default App;
