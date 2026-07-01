import { apiClient } from "./client";

export type CurrentUser = {
    id: number;
    email: string;
    role: string;
    is_active: boolean;
};

export async function getCurrentUser(): Promise<CurrentUser> {
    const response = await apiClient.get<CurrentUser>("/users/me");
    return response.data;
}