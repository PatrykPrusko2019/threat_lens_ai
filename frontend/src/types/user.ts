export type CurrentUserResponse = {
    id: number;
    email: string;
    role: string;
    is_activate?: boolean;
    full_name?: string | null;
};