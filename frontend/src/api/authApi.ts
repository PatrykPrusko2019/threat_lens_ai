import { apiClient } from "./client";

export type LoginPayload = {
    email: string;
    password: string;
};

export type LoginResponse = {
    access_token: string;
    token_type?: string;
};

export async function login(payload: LoginPayload): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>("/auth/login", payload);
    return response.data;
}