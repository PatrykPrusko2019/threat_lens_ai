import { apiClient } from "./client";

export type LoginPayload = {
    email: string;
    password: string;
};

export type LoginResponse = {
    access_token: string;
    token_type?: string;
};

export type RegisterPayload = {
    email: string;
    password: string;
}

export type RegisterResponse = {
    id: number;
    email: string;
    role: string;
    is_active: boolean;
};

export async function login(payload: LoginPayload): Promise<LoginResponse> {
    const response = await apiClient.post<LoginResponse>("/auth/login", payload);
    return response.data;
}

export async function register(
    payload: RegisterPayload,
): Promise<RegisterResponse> {
    const response = await apiClient.post<RegisterResponse>(
        "/auth/register",
        payload,
    );

    return response.data;
}
