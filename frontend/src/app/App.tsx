import { Route, Routes } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { AlertsPage } from "../pages/AlertsPage";
import { DashboardPage } from "../pages/DashboardPage";
import { EventsPage } from "../pages/EventsPage";
import { LoginPage } from "../pages/LoginPage";

export function App() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            
            <Route element={<AppLayout />}>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/alerts" element={<AlertsPage />} />
                <Route path="/events" element={<EventsPage />} />
            </Route>
        </Routes>
    );
}