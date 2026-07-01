import { Route, Routes } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { AlertsPage } from "../pages/AlertsPage";
import { DashboardPage } from "../pages/DashboardPage";
import { EventsPage } from "../pages/EventsPage";
import { LoginPage } from "../pages/LoginPage";
import { ProtectedRoute } from "./ProtectedRoute";
import { AiDetectionPage } from "../pages/AiDetectionPage";
import { RegisterPage } from "../pages/RegisterPage";

export function App() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            

            <Route 
                element={
                    <ProtectedRoute>
                        <AppLayout />
                    </ProtectedRoute>
                }
            >
                <Route path="/" element={<DashboardPage />} />
                <Route path="/alerts" element={<AlertsPage />} />
                <Route path="/events" element={<EventsPage />} />
                <Route path="/ai-detection" element={<AiDetectionPage />} />
            </Route>
        </Routes>
    );
}