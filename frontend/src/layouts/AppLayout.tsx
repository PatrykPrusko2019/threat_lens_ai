import { Outlet } from "react-router-dom";

import { Sidebar } from "../components/layout/Sidebar";
import { Topbar } from "../components/layout/Topbar";

export function AppLayout() {
    return (
        <div className="min-h-screen bg-slate-950 text-slate-100">
            <div className="flex min-h-screen">
                <Sidebar />

                <main className="flex-1">
                    <Topbar />
                    <div className="p-6">
                        <Outlet />
                    </div>
                </main>
            </div>
        </div>
    );
}