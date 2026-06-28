import { apiClient } from "./client";
import type { CurrentUserResponse } from "../types/user";


export async function getCurrentUser(): Promise<CurrentUserResponse> {
    const response = await apiClient.get<CurrentUserResponse>("/users/me");
    return response.data;
}