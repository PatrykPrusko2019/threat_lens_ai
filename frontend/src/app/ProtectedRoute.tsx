import { Navigate } from "react-router-dom";

import { isAuthenticated } from "./auth";
import type React from "react";

type ProtectedRouteProps = {
    children: React.ReactNode;
};

export function ProtectedRoute({ children }: ProtectedRouteProps) {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    return children;
}